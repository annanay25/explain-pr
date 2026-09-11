import { defineConfig } from "vite";
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));

function copyLib() {
  mkdirSync(resolve(root, "public/lib"), { recursive: true });
  copyFileSync(resolve(root, "lib/figure.css"), resolve(root, "public/lib/figure.css"));
  copyFileSync(resolve(root, "lib/figure.js"), resolve(root, "public/lib/figure.js"));
}

copyLib();

export default defineConfig({
  root: ".",
  publicDir: "public",
  server: {
    host: true,
    port: 43147,
    strictPort: true,
  },
  preview: {
    host: true,
    port: 43147,
    strictPort: true,
  },
  plugins: [
    {
      name: "copy-figure-lib",
      buildStart: copyLib,
      configureServer() {
        copyLib();
      },
    },
  ],
  build: {
    outDir: "dist",
    rollupOptions: {
      input: {
        main: resolve(root, "index.html"),
        catalog: resolve(root, "catalog.html"),
        react: resolve(root, "walks/react-compiler.html"),
        vite: resolve(root, "walks/vite-environments.html"),
        next: resolve(root, "walks/next-ppr.html"),
        tailwind: resolve(root, "walks/tailwind-oxide.html"),
      },
    },
  },
});
