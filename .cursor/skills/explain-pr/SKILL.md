---
name: explain-pr
description: Explain a pull request as multiple visual views (story, data flow, blast radius) using Figure. Use when asked to explain a PR, summarize code changes, show data flow before/after, assess blast radius, or generate an HTML visualization of what a diff does.
---

# Explain a PR with Figure

Produce a **single HTML page with three views** of the same PR:

1. **Story** — what changed, in claims a human can step through.
2. **Data** — what payload moved, which component processed it, **how** it did that before vs after.
3. **Blast radius** — public APIs, prod stores / DBs, callers who feel a mistake.

Copy `figure.css` and `figure.js` next to the page (or link them). Fonts and icons live in the CSS. `figure.js` only builds the **ask prompt** when a reviewer opens a component. Views and Next are CSS (hidden radios + labels). No npm, no build.

Do not write a prose essay. Each view is 3–5 scenes (8 max). The reader switches views with tabs, advances with **Next**.

## Output skeleton

```html
<link rel="stylesheet" href="figure.css" />
...
<nav class="fig-view-tabs">
  <label class="fig-view-tab" for="view-story">Story<small>what changed</small></label>
  <label class="fig-view-tab" for="view-data">Data<small>who processed what, how</small></label>
  <label class="fig-view-tab" for="view-blast">Blast radius<small>APIs, stores, callers</small></label>
</nav>
<input type="radio" name="view" id="view-story" checked>
<input type="radio" name="view" id="view-data">
<input type="radio" name="view" id="view-blast">

<div class="fig-view" data-view="story">
  <input type="radio" name="walk" id="s1" checked>
  <input type="radio" name="walk" id="s2">
  <div class="fig-scenes"> ... sections with ids s1/s2 ... </div>
</div>
<div class="fig-view" data-view="data">
  <input type="radio" name="data" id="d1" checked>
  <div class="fig-scenes"> ... </div>
</div>
<div class="fig-view" data-view="blast">
  <input type="radio" name="blast" id="b1" checked>
  <div class="fig-scenes"> ... </div>
</div>
...
<script src="figure.js"></script>
```

Scene radios: Story `#s1`–`#s8`, Data `#d1`–`#d8`, Blast `#b1`–`#b8`. Put a `.fig-repo` link and the PR title in `.fig-mast h1` — the prompt composer reads those.

If this repo is not on disk, copy `figure.css` and `figure.js` verbatim.

## How to think

1. Read the PR title, body, and the shape of the diff (not every line).
2. Name the system. Then split work into the three views — do not dump everything into Story.
3. One claim per scene.
4. Story: before → after → mechanism → consequence.
5. Data: name the **payload**, the **processor**, and the **HOW** (parse, copy, cache, serialize, walk twice, …). Draw before and after. Highlight the component whose HOW changed.
6. Blast: public API / plugin contract / prod DB or cache / who callers are. Use `.fig-risk` with `data-level="hot|watch|safe"`. End with a “do not merge if…” gate.
7. Extra depth is a node the reviewer can open and **ask**, not extra slides.

## Data view (required)

Ask, per stage: *what is the data, who touches it, how did they touch it, how do they now?*

Typical cards:

- payload: `file`, `js`, `html`, `token`, `ast`, `stream`
- processor: `babel`, `scan`, `server`, `worker`, `adapter`
- store: `cache`, `graph`, `arena`, `db`

Edge labels are the operation (`parse`, `serialize`, `walk #2`, `store`).

Do **not** make Data a copy of Story with different titles. If Story said “three front doors,” Data says “Babel tree serializes into Rust; OXC maps in-process; HIR lives as indices.”

## Blast radius (required)

Put four `.fig-risk` tiles on scene 1:

```html
<div class="fig-risk" data-level="hot"><em>public API</em><strong>Environment API</strong><span>…</span></div>
<div class="fig-risk" data-level="watch"><em>compat</em><strong>Old server API</strong><span>…</span></div>
<div class="fig-risk" data-level="safe"><em>prod databases</em><strong>None</strong><span>…</span></div>
```

Be honest. A 123k-line compiler port with **no** DB and **no** ReactDOM change should say that. A 20-file cache write that can leak cookies into a CDN object is **hot** even if the diff is small.

Name callers (framework authors, later visitors, PostCSS adapters). End with a gate node: “Do not merge if…”

`.fig-page` and `.fig-shell` are chrome. Glyphs for documents/terminals are `data-kind="doc"` / `data-kind="term"`.

## Inspect + ask prompt

Every named component is `<details class="fig-node" data-kind="…">` with kind, name, role, and a short panel of facts.

`figure.js` appends, on every node:

- a **Your questions** textarea
- a **Prompt for your coding agent** textarea, prefilled from the PR title, view, scene claim, and panel text
- **Copy prompt**

Do not omit panel facts — they become `data-known` in the prompt. The reviewer types what the walkthrough did not answer. They paste the prompt back into Cursor / Codex / Claude.

Example node:

```html
<details class="fig-node" data-kind="oxc" data-tone="added">
  <summary>
    <i class="fig-mark"></i>
    <span class="fig-node-text">
      <em>parser host</em>
      <strong>OXC</strong>
      <span>Rust parser. Thin adapter crate in this repo.</span>
    </span>
    <b class="fig-node-go"></b>
  </summary>
  <div class="fig-node-panel">
    <p>What this component actually does in this PR, including HOW it processes data.</p>
  </div>
</details>
```

Modifiers: `.tight`, `.wide`, `open` to start expanded (use once per scene for the main object).

Anonymous extras may stay `<div class="fig-user" data-label="Visitor A"></div>`.

Tones: `added`, `removed`, `changed`, `focus`, `ghost`.

## Kinds

Pick the mark that explains the **role**. Babel / OXC / SWC / named environments / fallback vs route shell are never all `.fig-box`.

| Kind | Use for |
|------|---------|
| `user` / `users` | Person, reviewer, visitor |
| `browser` / `client` / `mobile` | Client |
| `server` / `worker` / `runtime` | Process, origin, job, executable env |
| `db` / `bucket` / `cache` / `queue` / `cloud` | Stores and edge |
| `api` / `env` | Gateway, named environment |
| `babel` / `oxc` / `swc` / `rust` | Specific compiler hosts |
| `compiler` / `parser` / `ast` / `ir` / `hir` | Compiler pipeline |
| `plugin` / `adapter` / `transform` | Integrations and passes |
| `arena` / `crate` / `bundler` / `scan` | Storage, package, pack, filesystem scan |
| `file` / `folder` / `doc` / `term` / `fallback` / `route` | Artifacts |
| `module` / `graph` / `package` | Graphs and packages |
| `html` / `css` / `js` / `wasm` / `stream` / `hook` | Web shapes |
| `lock` / `key` / `flag` / `test` / `event` / `token` | Signals |
| `clock` / `filter` / `branch` / `tree` / `config` / `log` / `error` | Ops |
| `request` / `response` / `snapshot` / `build` / `pipeline` | Flow |
| `box` | Last resort unnamed module |

Arrow: `<div class="fig-edge" data-label="GET"></div>`. Add `down` or `strike`.

## Layout

`.fig-row`, `.fig-col`, `.fig-cluster`, `.fig-compare` + `.fig-pane`, `.fig-stack` + `.fig-layer`, `.fig-pipe` + `.fig-phase`, `.fig-timeline` + `.fig-step`, `.fig-code` + `.fig-line.added|.removed`, `.fig-metric`, `.fig-callout`, `.fig-datapoints`, `.fig-risk`.

To stack flows: `.fig-col` with `<div class="fig-edge down">` **between** rows.

## Rules

- Abstract shapes only. No logos.
- No CSS animations, no autoplay. `figure.js` is only the prompt composer.
- Real names from the PR. Do not invent subsystems.
- Always emit all three views. If blast is “none,” say so with `.fig-risk` `safe` tiles — do not skip the view.
- Distinct `data-kind` for distinct components.
- Open the HTML file in a browser. Nothing to install.
