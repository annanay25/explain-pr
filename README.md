# Figure

A visual language for explaining pull requests. **One CSS file. Plain HTML. No JavaScript, no npm, no build.**

`figure.css` already contains Fraunces and IBM Plex (woff2, inlined) plus the glyph icons. A skill that uses this library only needs to copy that file next to an HTML page.

## Open it

Double-click `index.html`, or from this folder:

```bash
python3 -m http.server 43147 --bind 127.0.0.1
```

Then open [http://127.0.0.1:43147](http://127.0.0.1:43147).

There is nothing to install.

## Skill

Load `skills/explain-pr/SKILL.md` into Cursor, Codex, or Claude. The model emits HTML that links `figure.css` and steps through scenes with Next labels.

## Walkthroughs

| Page | PR |
|------|----|
| [walks/react-compiler.html](walks/react-compiler.html) | [react/react #36173](https://github.com/facebook/react/pull/36173) |
| [walks/vite-environments.html](walks/vite-environments.html) | [vitejs/vite #16471](https://github.com/vitejs/vite/pull/16471) |
| [walks/next-ppr.html](walks/next-ppr.html) | [vercel/next.js #69282](https://github.com/vercel/next.js/pull/69282) |
| [walks/tailwind-oxide.html](walks/tailwind-oxide.html) | [tailwindlabs/tailwindcss #19632](https://github.com/tailwindlabs/tailwindcss/pull/19632) |

## Rebuild the stylesheet

Fonts live in `fonts/`. After changing icons or typefaces:

```bash
python3 scripts/build-css.py
```

That is optional. Using Figure does not require Python either — only `figure.css` and an HTML file.
