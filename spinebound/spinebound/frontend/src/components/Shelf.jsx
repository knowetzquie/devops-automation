import BookSpine from './BookSpine.jsx';

export default function Shelf({ label, books, onRemove }) {
  return (
    <section className="shelf">
      <h2 className="shelf__label">{label}</h2>
      <div className="shelf__row">
        {books.length === 0 && (
          <p className="shelf__empty">Nothing here yet — search a title to add it.</p>
        )}
        {books.map((book) => (
          <BookSpine key={book.id} book={book} onRemove={onRemove} />
        ))}
      </div>
      <div className="shelf__plank" />
    </section>
  );
}
