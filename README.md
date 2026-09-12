# Figure

A visual language for explaining pull requests. **One CSS file, one small JS file for the ask-prompt box. No npm, no build.**

A coding agent emits **three views** of the same PR:

- **Story** — what changed
- **Data** — which payload moved, which component processed it, how that HOW changed
- **Blast radius** — public APIs, prod stores, callers

Click a component, type a question, copy a preconstructed prompt back into the agent.

`figure.css` inlines Fraunces, IBM Plex, and the glyph icons. `figure.js` only fills the question box and copy button.

## Open it

```bash
python3 -m http.server 43147 --bind 127.0.0.1
```

Then open [http://127.0.0.1:43147](http://127.0.0.1:43147).

## Skill

Load `skills/explain-pr/SKILL.md`. Copy `figure.css` and `figure.js` next to the HTML the model emits.

## Walkthroughs

| Page | PR |
|------|----|
| [walks/react-compiler.html](walks/react-compiler.html) | [react/react #36173](https://github.com/facebook/react/pull/36173) |
| [walks/vite-environments.html](walks/vite-environments.html) | [vitejs/vite #16471](https://github.com/vitejs/vite/pull/16471) |
| [walks/next-ppr.html](walks/next-ppr.html) | [vercel/next.js #69282](https://github.com/vercel/next.js/pull/69282) |
| [walks/tailwind-oxide.html](walks/tailwind-oxide.html) | [tailwindlabs/tailwindcss #19632](https://github.com/tailwindlabs/tailwindcss/pull/19632) |

## Rebuild the stylesheet

```bash
python3 scripts/build-css.py
```
