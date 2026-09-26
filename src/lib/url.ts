// Prefixes root-absolute paths with Astro's configured `base`, so the same
// pages/components work whether the site is deployed at a domain root
// (base: "/", the production default) or under a subpath (base: "/x/",
// used for preview deployments on GitHub Pages).
export function url(path: string): string {
  const base = import.meta.env.BASE_URL;
  const rel = path.replace(/^\//, "");
  return rel ? base + rel : base;
}
