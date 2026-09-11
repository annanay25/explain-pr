---
name: explain-pr
description: Explain a pull request as a stepped visual walkthrough using Figure (one CSS file, plain HTML, no JavaScript). Use when asked to explain a PR, summarize code changes for humans, produce a change walkthrough, or generate an HTML visualization of what a diff does.
---

# Explain a PR with Figure

Produce a single HTML page. Copy `figure.css` next to it (or link it). That file already contains the fonts and the glyph icons. Do not add JavaScript, npm, or a build step.

Do not write a prose essay. Compose 5–8 scenes. The reader advances with **Next** (a `<label>` wired to a hidden radio). Depth lives **inside components**: a reviewer must be able to click a card and keep opening nested sections until they have enough.

## Output

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PR title — Figure</title>
    <link rel="stylesheet" href="figure.css" />
  </head>
  <body class="fig-page">
    <article class="fig-deck">
      <div class="fig-shell">
        <header class="fig-mast">
          <div>
            <p class="fig-kicker">Figure · PR walk</p>
            <h1>Short human title</h1>
            <div class="fig-repo"><a href="https://github.com/org/repo/pull/1234">org/repo #1234</a></div>
            <p class="fig-inspect-hint">Click a component to inspect. Nested folds go as deep as you want.</p>
          </div>
          <div class="fig-mast-side">
            <span class="fig-stat added">+318</span>
            <span class="fig-stat removed">−102</span>
            <span class="fig-stat">20 files</span>
          </div>
        </header>

        <input type="radio" name="walk" id="s1" checked>
        <input type="radio" name="walk" id="s2">
        <input type="radio" name="walk" id="s3">

        <div class="fig-scenes">
          <section class="fig-scene">
            <div class="fig-stage">
              <div class="fig-scene-head">
                <div class="fig-index">01</div>
                <div>
                  <h2>The static shell is reused after the first miss</h2>
                  <p>After a fallback is served, the route shell is generated and later requests skip the cold path.</p>
                </div>
              </div>
              <div class="fig-canvas">
                <div class="fig-row">
                  <div class="fig-user" data-label="Visitor"></div>
                  <div class="fig-edge" data-label="GET /p"></div>
                  <details class="fig-node" data-kind="cloud" data-tone="added">
                    <summary>
                      <i class="fig-mark"></i>
                      <span class="fig-node-text">
                        <em>cache</em>
                        <strong>CDN shell</strong>
                        <span>Promoted route shell, not a fallback.</span>
                      </span>
                      <b class="fig-node-go"></b>
                    </summary>
                    <div class="fig-node-panel">
                      <p>Future requests use this instead of regenerating a fallback.</p>
                      <details class="fig-fold">
                        <summary>What still hits origin</summary>
                        <p>Dynamic holes. Cookies, search, user. The frame around them is what got cached.</p>
                      </details>
                    </div>
                  </details>
                </div>
              </div>
            </div>
            <nav class="fig-nav">
              <span class="fig-btn is-disabled">Back</span>
              <div class="fig-dots-nav">
                <label class="fig-dot is-current" for="s1"></label>
                <label class="fig-dot" for="s2"></label>
                <label class="fig-dot" for="s3"></label>
              </div>
              <label class="fig-btn fig-next" for="s2">Next</label>
            </nav>
          </section>
          <!-- more scenes: Back is <label class="fig-btn" for="sN">Back</label> -->
        </div>
      </div>
    </article>
  </body>
</html>
```

If this repo is not on disk, copy the contents of `figure.css` verbatim. Do not rewrite the stylesheet.

## How to think

1. Read the PR title, body, and the shape of the diff (not every line).
2. Name the *system* the change lives in.
3. One claim per scene.
4. Prefer before → after, then the mechanism, then the consequence.
5. Stop at 8 scenes (the stylesheet only wires `#s1`–`#s8`). Extra depth goes inside nodes, not extra slides.
6. To stack two flows, wrap them in `.fig-col` with `<div class="fig-edge down">` **between** the rows.

## Inspectable nodes (required for named components)

Do **not** draw Babel, OXC, SWC, Vite environments, scanners, shells, etc. as identical `.fig-box` squares. Each named part of the system is a `<details class="fig-node">` with:

- `data-kind` matching a catalog glyph (so the icon explains the role)
- a **kind** line (`<em>parser host</em>`)
- a **name** (`<strong>OXC</strong>`)
- a **one-line role** (`<span>Rust parser. New front door.</span>`)
- a panel the reviewer can open, with nested `.fig-fold` (and nested `.fig-node` if needed) so they can go as deep as they want

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
    <p>What this component actually does in this PR.</p>
    <details class="fig-fold">
      <summary>A sharper question</summary>
      <p>Answer. Nest another .fig-fold if the reviewer might still ask “why.”</p>
    </details>
  </div>
</details>
```

Modifiers:

- `.tight` — icon + name only on the card; panel still has full detail
- `.wide` — full-width inspector under a row of cards
- `open` on `<details>` — start expanded (use once per scene to teach, or for the scene’s main object)

Anonymous extras (Visitor A, a generic arrow) may stay compact glyphs: `<div class="fig-user" data-label="Visitor A"></div>`.

Optional chip: `<b class="fig-chip">new</b>` inside a glyph or node.

Tones on `data-tone`: `added`, `removed`, `changed`, `focus`, `ghost`.

## Kinds (`data-kind` / `.fig-{kind}`)

Pick the mark that explains the **role**, not a generic box.

| Kind | Use for |
|------|---------|
| `user` / `users` | Person, reviewer, visitor |
| `browser` / `client` / `mobile` | Client |
| `server` / `worker` / `runtime` | Process, origin, job, executable env |
| `db` / `bucket` / `cache` / `queue` / `cloud` | Stores and edge |
| `api` / `env` | Gateway, named environment |
| `babel` / `oxc` / `swc` / `rust` | Specific compiler hosts — never reuse `box` for these |
| `compiler` / `parser` / `ast` / `ir` / `hir` | Compiler pipeline |
| `plugin` / `adapter` / `transform` | Integrations and passes |
| `arena` / `crate` / `bundler` / `scan` | Storage, package, pack, filesystem scan |
| `file` / `folder` / `doc` / `term` / `fallback` / `route` | Artifacts, documents, CLI, fallback HTML |
| `module` / `graph` / `package` | Graphs and packages |
| `html` / `css` / `js` / `wasm` / `stream` / `hook` | Web shapes |
| `lock` / `key` / `flag` / `test` / `event` / `token` | Signals |
| `clock` / `filter` / `branch` / `tree` / `config` / `log` / `error` | Ops |
| `request` / `response` / `snapshot` / `build` / `pipeline` | Flow |
| `snippet` | Generic code mark |
| `box` | Last resort unnamed module |

Arrow: `<div class="fig-edge" data-label="GET"></div>`. Add class `down` or `strike`.

A scene can hold 3–6 nodes. Put extra questions inside the panel, not as more cards.

## Layout

`.fig-row`, `.fig-col`, `.fig-cluster` (`data-label`), `.fig-compare` + `.fig-pane`, `.fig-stack` + `.fig-layer`, `.fig-pipe` + `.fig-phase`, `.fig-timeline` + `.fig-step`, `.fig-code` (`data-caption`) + `.fig-line.added|.removed`, `.fig-metric` (`data-value`), `.fig-callout`, `.fig-datapoints` with `<i class="on">` dots.

Code samples: at most 6 lines, usually inside a node panel.

## Rules

- Abstract shapes only. No logos, no product screenshots.
- No `<script>`, no CSS animations, no autoplay.
- Real names from the PR. Do not invent subsystems.
- Distinct `data-kind` for distinct components. Babel is not a box. An environment is not a box. A fallback is not a cloud unless it is actually a CDN.
- `.fig-page` and `.fig-shell` are page chrome, not glyphs. Use `data-kind="doc"` / `data-kind="term"` for documents and terminals.
- Every important component is inspectable. If a reviewer would ask “what is this?”, it needs a panel.
- Open the HTML file in a browser. Nothing to install.
