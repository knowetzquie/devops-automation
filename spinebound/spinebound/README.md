# Spinebound

A book tracker that renders your books as spines on a shelf instead of a
plain list — inspired by the "reorganize the bookshelf" TBR apps.

Full stack, two folders:

```
spinebound/
├── frontend/   React + Vite app (the bookshelf UI)
└── backend/    FastAPI app + local SQLite database
```

## Why there's no spine image API

No service provides real spine-only photography — publishers don't shoot or
license that. Apps that look like real spines are generating them: take the
front cover, pull its dominant color, and render a colored block with the
title set vertically. That's what this app does, in
`frontend/src/spineColor.js`.

## How it fits together

- **`backend/app.py`** is a single-file FastAPI app with three resources:
  `shelves`, `books`, and `search`. Shelves and books are stored in a
  **SQLite database** (`backend/spinebound.db`, created automatically on
  first run — no separate database server to install, just Python's
  built-in `sqlite3`). `search` proxies [Open Library's free search
  API](https://openlibrary.org/dev/docs/api/search) so the frontend never
  has to call a third party directly.
- **`frontend/`** is the React UI. It calls the backend for everything —
  fetching shelves, adding/removing books, searching — via
  `frontend/src/api.js`. Cover images are loaded straight from
  `covers.openlibrary.org` (that part doesn't need to go through the
  backend, it's just static images).

## Run it

Two terminals, one for each half:

```bash
# terminal 1 — backend
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload --port 4000

# terminal 2 — frontend
cd frontend
npm install
npm run dev       # http://localhost:5173
```

Open the frontend URL. It talks to the backend at `http://localhost:4000`
by default — override with `VITE_API_URL` (copy `frontend/.env.example` to
`.env.local` if you need a different backend address). FastAPI also gives
you interactive API docs for free at `http://localhost:4000/docs`.

## Deploying

- **Backend**: deploy `backend/` to any Python host (Railway, Render,
  Fly.io, a plain VPS with `uvicorn`/`gunicorn`). SQLite works well for a
  single instance backed by persistent disk; if your host wipes disk on
  redeploy, or you need multiple instances behind a load balancer, swap the
  connection logic in `backend/app.py` for a hosted Postgres (e.g. via
  `psycopg`/`SQLAlchemy`) instead.
- **Frontend**: deploy `frontend/` to Vercel, Netlify, or similar. Set
  `VITE_API_URL` to your deployed backend's URL in the host's environment
  variables.

## Ideas to extend

- User accounts (the backend currently has one shared shelf set, like a
  single-user local app)
- Drag-to-reorder spines within a shelf
- A "spine texture" overlay (subtle noise/grain) for more realism
- Swap the search/cover source for Google Books or ISBNdb if Open Library's
  coverage is too spotty for the books you read
