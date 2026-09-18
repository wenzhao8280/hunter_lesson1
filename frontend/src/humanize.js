// Category/type fields are stored as snake_case machine values (e.g.
// "academic_integrity_office") since they're only meant for cross-school
// filtering, not display. This turns one into readable text for the UI.
export function humanize(value) {
  if (!value) return value;
  return value
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
