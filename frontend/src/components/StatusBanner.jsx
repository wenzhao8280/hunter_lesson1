export function LoadingBanner({ label = "Loading…" }) {
  return <p className="status-banner">{label}</p>;
}

export function ErrorBanner({ message }) {
  return <p className="status-banner status-banner-error">{message}</p>;
}
