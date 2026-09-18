// The spine's background is the book's real cover photo (see BookSpine.jsx),
// so this file only needs to handle the case where there's no cover art at
// all, and how wide a spine should be.

const FALLBACK_PALETTE = [
  "#6B4A3D",
  "#3E5C4A",
  "#4A5A70",
  "#7A4B5C",
  "#8A6D3F",
  "#4B4A6B",
  "#5C6B3E",
];

export function fallbackSpineColor(seed) {
  let hash = 0;
  for (let i = 0; i < seed.length; i++)
    hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  return FALLBACK_PALETTE[Math.abs(hash) % FALLBACK_PALETTE.length];
}

export function spineWidth(title, pages) {
  if (pages) return Math.min(56, Math.max(24, Math.round(pages / 12)));
  const base = 28 + (title.length % 20);
  return Math.min(52, base);
}
