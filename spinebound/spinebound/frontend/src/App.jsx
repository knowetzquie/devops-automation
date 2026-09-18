import { useEffect, useState } from 'react';
import { fetchShelves, createShelf, addBookToShelf, removeBook } from './api';
import Shelf from './components/Shelf.jsx';
import SearchModal from './components/SearchModal.jsx';

export default function App() {
  const [shelves, setShelves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeShelfId, setActiveShelfId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setShelves(await fetchShelves());
    } catch (err) {
      setError(err.message || 'Could not reach the Spinebound server — is the backend running?');
    } finally {
      setLoading(false);
    }
  }

  async function addBook(book) {
    const shelf = shelves.find((s) => s.id === activeShelfId);
    if (!shelf) return;
    if (shelf.books.some((b) => b.key === book.key)) {
      setActiveShelfId(null);
      return;
    }
    try {
      const saved = await addBookToShelf(shelf.id, book);
      setShelves((prev) =>
        prev.map((s) => (s.id === shelf.id ? { ...s, books: [...s.books, saved] } : s))
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setActiveShelfId(null);
    }
  }

  async function handleRemove(shelfId, bookId) {
    try {
      await removeBook(bookId);
      setShelves((prev) =>
        prev.map((s) => (s.id === shelfId ? { ...s, books: s.books.filter((b) => b.id !== bookId) } : s))
      );
    } catch (err) {
      setError(err.message);
    }
  }

  async function addShelf() {
    const label = window.prompt('Name this shelf:');
    if (!label) return;
    try {
      const shelf = await createShelf(label);
      setShelves((prev) => [...prev, shelf]);
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <div className="app__loading">Loading your shelves…</div>;

  const activeShelf = shelves.find((s) => s.id === activeShelfId);

  return (
    <div className="app">
      <header className="app__header">
        <h1>Spinebound</h1>
        <p>A shelf for what you're reading, what's next, and what's done.</p>
        {error && <p className="app__error">{error}</p>}
      </header>

      <main className="app__shelves">
        {shelves.map((shelf) => (
          <div key={shelf.id} className="shelf-wrapper">
            <Shelf label={shelf.label} books={shelf.books} onRemove={(bookId) => handleRemove(shelf.id, bookId)} />
            <button className="shelf__add" onClick={() => setActiveShelfId(shelf.id)}>
              + Add book
            </button>
          </div>
        ))}
        <button className="app__add-shelf" onClick={addShelf}>+ New shelf</button>
      </main>

      {activeShelf && (
        <SearchModal
          shelfLabel={activeShelf.label}
          onAdd={addBook}
          onClose={() => setActiveShelfId(null)}
        />
      )}
    </div>
  );
}
