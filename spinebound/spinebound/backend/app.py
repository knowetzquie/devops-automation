"""
Spinebound API — a single-file FastAPI backend.

Stores shelves and books in a local SQLite database (spinebound.db,
created automatically on first run) and proxies Open Library's free
search API so the frontend never has to call a third party directly.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "spinebound.db"
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
DEFAULT_SHELVES = ["Currently Reading", "To Be Read", "Finished"]

app = FastAPI(title="Spinebound API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- models -----------------------------------------------------------

class ShelfCreate(BaseModel):
    label: str


class BookCreate(BaseModel):
    shelfId: str
    key: Optional[str] = None
    title: str
    author: Optional[str] = "Unknown author"
    year: Optional[int] = None
    coverId: Optional[int] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None


# --- database -----------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shelves (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                position INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                shelf_id TEXT NOT NULL REFERENCES shelves(id) ON DELETE CASCADE,
                key TEXT,
                title TEXT NOT NULL,
                author TEXT,
                year INTEGER,
                cover_id INTEGER,
                isbn TEXT,
                pages INTEGER,
                position INTEGER NOT NULL
            )
            """
        )
        conn.commit()

        shelf_count = conn.execute("SELECT COUNT(*) FROM shelves").fetchone()[0]
        if shelf_count == 0:
            for i, label in enumerate(DEFAULT_SHELVES):
                conn.execute(
                    "INSERT INTO shelves (id, label, position) VALUES (?, ?, ?)",
                    (str(uuid4()), label, i),
                )
            conn.commit()
    finally:
        conn.close()


def book_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "shelfId": row["shelf_id"],
        "key": row["key"],
        "title": row["title"],
        "author": row["author"],
        "year": row["year"],
        "coverId": row["cover_id"],
        "isbn": row["isbn"],
        "pages": row["pages"],
        "position": row["position"],
    }


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# --- health -----------------------------------------------------------

@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


# --- shelves -----------------------------------------------------------

@app.get("/api/shelves")
def list_shelves():
    conn = get_connection()
    try:
        shelf_rows = conn.execute("SELECT * FROM shelves ORDER BY position ASC").fetchall()
        result = []
        for shelf in shelf_rows:
            book_rows = conn.execute(
                "SELECT * FROM books WHERE shelf_id = ? ORDER BY position ASC",
                (shelf["id"],),
            ).fetchall()
            result.append(
                {
                    "id": shelf["id"],
                    "label": shelf["label"],
                    "position": shelf["position"],
                    "books": [book_row_to_dict(b) for b in book_rows],
                }
            )
        return result
    finally:
        conn.close()


@app.post("/api/shelves", status_code=201)
def create_shelf(payload: ShelfCreate):
    label = payload.label.strip()
    if not label:
        raise HTTPException(status_code=400, detail="label is required")

    conn = get_connection()
    try:
        position = conn.execute("SELECT COUNT(*) FROM shelves").fetchone()[0]
        shelf_id = str(uuid4())
        conn.execute(
            "INSERT INTO shelves (id, label, position) VALUES (?, ?, ?)",
            (shelf_id, label, position),
        )
        conn.commit()
        return {"id": shelf_id, "label": label, "position": position, "books": []}
    finally:
        conn.close()


@app.delete("/api/shelves/{shelf_id}", status_code=204)
def delete_shelf(shelf_id: str):
    conn = get_connection()
    try:
        existing = conn.execute("SELECT id FROM shelves WHERE id = ?", (shelf_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="shelf not found")
        conn.execute("DELETE FROM books WHERE shelf_id = ?", (shelf_id,))
        conn.execute("DELETE FROM shelves WHERE id = ?", (shelf_id,))
        conn.commit()
    finally:
        conn.close()


# --- books -----------------------------------------------------------

@app.post("/api/books", status_code=201)
def add_book(payload: BookCreate):
    conn = get_connection()
    try:
        shelf = conn.execute("SELECT id FROM shelves WHERE id = ?", (payload.shelfId,)).fetchone()
        if not shelf:
            raise HTTPException(status_code=404, detail="shelf not found")

        position = conn.execute(
            "SELECT COUNT(*) FROM books WHERE shelf_id = ?", (payload.shelfId,)
        ).fetchone()[0]
        book_id = str(uuid4())
        conn.execute(
            """
            INSERT INTO books (id, shelf_id, key, title, author, year, cover_id, isbn, pages, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                book_id,
                payload.shelfId,
                payload.key,
                payload.title,
                payload.author or "Unknown author",
                payload.year,
                payload.coverId,
                payload.isbn,
                payload.pages,
                position,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        return book_row_to_dict(row)
    finally:
        conn.close()


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: str):
    conn = get_connection()
    try:
        existing = conn.execute("SELECT id FROM books WHERE id = ?", (book_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="book not found")
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()


# --- search -----------------------------------------------------------

@app.get("/api/search")
async def search_books(q: str = Query(..., min_length=1)):
    params = {
        "q": q,
        "fields": "key,title,author_name,first_publish_year,cover_i,isbn,number_of_pages_median",
        "limit": 12,
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(OPEN_LIBRARY_SEARCH_URL, params=params)
            resp.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach Open Library right now")

    docs = resp.json().get("docs", [])
    results = []
    for doc in docs:
        authors = doc.get("author_name") or []
        isbns = doc.get("isbn") or []
        results.append(
            {
                "key": doc.get("key"),
                "title": doc.get("title"),
                "author": authors[0] if authors else "Unknown author",
                "year": doc.get("first_publish_year"),
                "coverId": doc.get("cover_i"),
                "isbn": isbns[0] if isbns else None,
                "pages": doc.get("number_of_pages_median"),
            }
        )
    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 4000)), reload=True)
