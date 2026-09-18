import { useState } from 'react';
import { fallbackSpineColor, spineWidth } from '../spineColor';
import { coverUrl } from '../api';

export default function BookSpine({ book, onRemove }) {
  const [open, setOpen] = useState(false);
  const cover = coverUrl(book.coverId, 'M');
  const width = spineWidth(book.title, book.pages);

  const background = cover
    ? { backgroundImage: `url(${cover})` }
    : { backgroundColor: fallbackSpineColor(book.title) };

  return (
    <div
      className="spine"
      style={{ width: `${width}px`, ...background }}
      onClick={() => setOpen((v) => !v)}
      title={`${book.title} — ${book.author}`}
    >
      <div className="spine__grain" />
      <div className="spine__shade" />
      <div className="spine__rule spine__rule--top" />
      <span className="spine__title">{book.title}</span>
      <div className="spine__rule spine__rule--bottom" />
      {open && (
        <button
          className="spine__remove"
          onClick={(e) => {
            e.stopPropagation();
            onRemove(book.id);
          }}
          aria-label={`Remove ${book.title}`}
        >
          ×
        </button>
      )}
    </div>
  );
}