import { useState } from 'react';
import { searchBooks, coverUrl } from '../api';

export default function SearchModal({ shelfLabel, onAdd, onClose }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      setResults(await searchBooks(query));
    } catch {
      setError('Could not reach Open Library — check your connection and try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal__header">
          <h3>Add a book to {shelfLabel}</h3>
          <button className="modal__close" onClick={onClose} aria-label="Close">×</button>
        </div>
        <form onSubmit={handleSearch} className="modal__search">
          <input
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search title or author…"
          />
          <button type="submit">Search</button>
        </form>
        {loading && <p className="modal__status">Searching…</p>}
        {error && <p className="modal__status modal__status--error">{error}</p>}
        <div className="modal__results">
          {results.map((book) => (
            <button key={book.key} className="modal__result" onClick={() => onAdd(book)}>
              {book.coverId ? (
                <img src={coverUrl(book.coverId, 'S')} alt="" />
              ) : (
                <div className="modal__result-noimg">No cover</div>
              )}
              <span>
                <span className="modal__result-title">{book.title}</span>
                <span className="modal__result-author">
                  {book.author}{book.year ? ` · ${book.year}` : ''}
                </span>
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
