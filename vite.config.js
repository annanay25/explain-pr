import { defineConfig } from "vite";
import { resolve } from "node:path";

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
  build: {
    outDir: "dist",
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        catalog: resolve(__dirname, "catalog.html"),
        react: resolve(__dirname, "walks/react-compiler.html"),
        vite: resolve(__dirname, "walks/vite-environments.html"),
        next: resolve(__dirname, "walks/next-ppr.html"),
        tailwind: resolve(__dirname, "walks/tailwind-oxide.html"),
      },
    },
  },
});
