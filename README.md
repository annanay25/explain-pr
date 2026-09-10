# Figure

A tiny HTML library of abstract glyphs for explaining pull requests. An LLM (or a human) composes scenes; the reader clicks **Next**.

This repo is the library, a Cursor/Codex/Claude skill, and four walkthroughs built from real open-source PRs.

## Run locally

```bash
npm install
npm run dev
```

Open [http://127.0.0.1:43147](http://127.0.0.1:43147). The gallery, glyph catalog, and PR walks are all static pages.

```bash
npm run build
npm run preview
```

## Use it in an HTML page

```html
<link rel="stylesheet" href="/lib/figure.css" />
<fig-deck title="Add a request cache" repo="acme/app" pr="812" added="140" removed="33" files="6">
  <fig-scene title="Reads used to hit Postgres every time" caption="The handler had no memory.">
    <fig-row>
      <fig-user label="Client"></fig-user>
      <fig-edge></fig-edge>
      <fig-server label="API"></fig-server>
      <fig-edge></fig-edge>
      <fig-db label="Postgres" tone="changed"></fig-db>
    </fig-row>
  </fig-scene>
  <fig-scene title="A cache now sits on the hot path" caption="Misses still reach the database.">
    <fig-row>
      <fig-user label="Client"></fig-user>
      <fig-edge></fig-edge>
      <fig-cache label="Cache" tone="added" badge="new"></fig-cache>
      <fig-edge label="miss"></fig-edge>
      <fig-db label="Postgres"></fig-db>
    </fig-row>
  </fig-scene>
</fig-deck>
<script src="/lib/figure.js"></script>
```

Tones: `added`, `removed`, `changed`, `focus`, `ghost`. Full glyph list: [catalog](/catalog.html). Composition rules for models: [`skills/explain-pr/SKILL.md`](skills/explain-pr/SKILL.md).

## Skill

Load `skills/explain-pr/SKILL.md` into Cursor, Codex, or Claude. The model should read a PR, then emit a Figure HTML page — 5 to 8 scenes, one claim each, Next as the only transition.

## Walkthroughs

These pages were written the way the skill instructs, from merged PRs:

| PR | What the walkthrough argues |
|----|-----------------------------|
| [react/react #36173](https://github.com/facebook/react/pull/36173) | React Compiler ported to Rust; same HIR passes; Babel/OXC/SWC doors |
| [vitejs/vite #16471](https://github.com/vitejs/vite/pull/16471) | Vite 6 names N environments, each with its own module graph |
| [vercel/next.js #69282](https://github.com/vercel/next.js/pull/69282) | After a PPR fallback is served, promote a reusable route shell |
| [tailwindlabs/tailwindcss #19632](https://github.com/tailwindlabs/tailwindcss/pull/19632) | Oxide stops double-walking; sync first scan, parallel later |

## Screenshots

```bash
npx playwright install chromium
npm run dev   # in another terminal, if not already running
npm run capture
```

PNGs land in `screenshots/`. Notes from the first real-PR pass are in [`screenshots/REPORT.md`](screenshots/REPORT.md).
