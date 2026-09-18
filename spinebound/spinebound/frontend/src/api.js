const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:4000';

async function request(path, options) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Request failed (${res.status})`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export function fetchShelves() {
  return request('/api/shelves');
}

export function createShelf(label) {
  return request('/api/shelves', { method: 'POST', body: JSON.stringify({ label }) });
}

export function addBookToShelf(shelfId, book) {
  return request('/api/books', { method: 'POST', body: JSON.stringify({ shelfId, ...book }) });
}

export function removeBook(bookId) {
  return request(`/api/books/${bookId}`, { method: 'DELETE' });
}

export function searchBooks(query) {
  return request(`/api/search?q=${encodeURIComponent(query)}`);
}

export function coverUrl(coverId, size = 'M') {
  if (!coverId) return null;
  return `https://covers.openlibrary.org/b/id/${coverId}-${size}.jpg`;
}
