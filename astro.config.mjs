import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// BUILD_BASE lets a preview deploy build the same source under a subpath
// (e.g. "/lime/" on GitHub Pages) without changing the default — plain
// `npm run build`/`npm run dev` still target the real domain root.
const base = process.env.BUILD_BASE || "/";

export default defineConfig({
  site: "https://steinhauermedia.de",
  base,
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
