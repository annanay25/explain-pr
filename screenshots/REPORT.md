# Screenshot pass

Captured against http://127.0.0.1:43147 with Playwright (Chromium, 1280×800 @2x, plus one 390×844 mobile frame). Each walkthrough scene is one click of **Next**.

## How well the library worked

The four walks were written the way `explain-pr` instructs: read the PR, name the system, one claim per scene.

**What landed**

- Glyphs stay readable at a glance. User, cloud, server, db, cache, worker, and file do not need a legend.
- Tones do the heavy lifting. Reviewers can see “this is new” vs “this path died” without reading labels.
- Scene titles as claims (`After a fallback is served, generate the route shell`) beat file-centric summaries.
- `fig-pipe`, `fig-timeline`, and `fig-compare` fit compiler/scanner PRs and request-path PRs equally well.
- Two-line `fig-code` blocks are the right density. A 20-file Next diff did not need a file dump.
- Mobile: the Next.js walk stacks, and the Next button stays usable at 390px.
- Navigation is obvious. Dots match scene count; Back/Next never needed a caption.

**What we had to fix after the first capture**

- A `dir="down"` edge at the *end* of a row does not feed the next row. Wrap rows in `fig-col` with the down-edge between them. The skill now states this.
- `fig-dots` wrapped a stray point onto a second line. The grid is now single-row.
- A `fig-legend` under a row crowded glyph labels. Legends belong on a scene that actually uses several tones.

**Still weak (accepted limits)**

- Sparse scenes (four glyphs and a caption) can look empty because the stage has a fixed min-height so Next does not jump.
- There is no way to pin a callout to one glyph. Callouts are banners under the drawing.
- Ghost tone is easy to miss next to idle.
- The library cannot show a graph with crossing edges. Nested `fig-row` / `fig-col` is the whole layout language — enough for these PRs, not enough for a service mesh.

## Index

| Page | Scene | Claim | File |
|------|-------|-------|------|
| Gallery | — | Gallery | `gallery.png` |
| Catalog | — | Catalog | `catalog.png` |
| react/react #36173 | 1 | A pass-by-pass port, not a new compiler | `react-compiler-s01.png` |
| react/react #36173 | 2 | Before: one TypeScript plugin behind Babel | `react-compiler-s02.png` |
| react/react #36173 | 3 | After: one Rust core, three front doors | `react-compiler-s03.png` |
| react/react #36173 | 4 | Inside, the pipeline is the old one | `react-compiler-s04.png` |
| react/react #36173 | 5 | Correctness was checked at two depths | `react-compiler-s05.png` |
| react/react #36173 | 6 | What to watch next | `react-compiler-s06.png` |
| vitejs/vite #16471 | 1 | Vite 5 hid two environments inside one server | `vite-environments-s01.png` |
| vitejs/vite #16471 | 2 | The problem: production has more rooms than client and SSR | `vite-environments-s02.png` |
| vitejs/vite #16471 | 3 | After: one process, N named environments | `vite-environments-s03.png` |
| vitejs/vite #16471 | 4 | Work happens on an environment, not on “the server” | `vite-environments-s04.png` |
| vitejs/vite #16471 | 5 | Runtimes are factories, not hard-coded Node | `vite-environments-s05.png` |
| vitejs/vite #16471 | 6 | Compatibility is the release strategy | `vite-environments-s06.png` |
| vercel/next.js #69282 | 1 | PPR already splits a page into a shell and holes | `next-ppr-s01.png` |
| vercel/next.js #69282 | 2 | Before this PR: a fallback shell never grew up | `next-ppr-s02.png` |
| vercel/next.js #69282 | 3 | After a fallback is served, generate the route shell | `next-ppr-s03.png` |
| vercel/next.js #69282 | 4 | Later requests skip the cold path | `next-ppr-s04.png` |
| vercel/next.js #69282 | 5 | A small, surgical diff in the fallback pipeline | `next-ppr-s05.png` |
| tailwindlabs/tailwindcss #19632 | 1 | Adapters ask the scanner for three things | `tailwind-oxide-s01.png` |
| tailwindlabs/tailwindcss #19632 | 2 | Bug 1: walking the tree twice | `tailwind-oxide-s02.png` |
| tailwindlabs/tailwindcss #19632 | 3 | Bug 2: parallel walkers have a cover charge | `tailwind-oxide-s03.png` |
| tailwindlabs/tailwindcss #19632 | 4 | Fix: sync the first time, parallel after that | `tailwind-oxide-s04.png` |
| tailwindlabs/tailwindcss #19632 | 5 | mtime is tracked only after the first pass | `tailwind-oxide-s05.png` |
| tailwindlabs/tailwindcss #19632 | 6 | The rest is smaller, hotter code | `tailwind-oxide-s06.png` |
| vercel/next.js #69282 | 1 | Mobile viewport | `next-ppr-mobile.png` |
