const STORAGE_KEY = "watchlist";

export function getWatchlist() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}

export function addToWatchlist(ticker) {
  const list = getWatchlist();
  const upper = ticker.toUpperCase();

  if (!list.includes(upper)) {
    const updated = [upper, ...list];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return updated;
  }

  return list;
}

export function removeFromWatchlist(ticker) {
  const list = getWatchlist();
  const updated = list.filter((t) => t !== ticker.toUpperCase());
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  return updated;
}