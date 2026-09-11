---
name: explain-pr
description: Explain a pull request as a stepped visual walkthrough using Figure (one CSS file, plain HTML, no JavaScript). Use when asked to explain a PR, summarize code changes for humans, produce a change walkthrough, or generate an HTML visualization of what a diff does.
---

# Explain a PR with Figure

Produce a single HTML page. Copy `figure.css` next to it (or link it). That file already contains the fonts and the glyph icons. Do not add JavaScript, npm, or a build step.

Do not write a prose essay. Compose 5–8 scenes. The reader advances with **Next** (a `<label>` wired to a hidden radio).

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
                  <div class="fig-user" data-label="Browser"></div>
                  <div class="fig-edge" data-label="GET /p"></div>
                  <div class="fig-cloud" data-label="CDN" data-tone="changed"><b class="fig-chip">hit</b></div>
                  <div class="fig-edge" data-label="holes"></div>
                  <div class="fig-server" data-label="Origin"></div>
                </div>
                <div class="fig-callout" data-tone="focus">Future requests use the new route shell instead of regenerating a fallback.</div>
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
5. Stop at 8 scenes (the stylesheet only wires `#s1`–`#s8`).
6. To stack two flows, wrap them in `.fig-col` with `<div class="fig-edge down">` **between** the rows.

## Glyphs

`<div class="fig-user" data-label="Browser" data-tone="added" data-note="optional"></div>`

Optional chip: `<b class="fig-chip">new</b>` inside the glyph.

Tones on `data-tone`: `added`, `removed`, `changed`, `focus`, `ghost`.

| Class | Use for |
|-------|---------|
| `.fig-user` / `.fig-users` | Person, requester |
| `.fig-browser` / `.fig-mobile` | Client |
| `.fig-server` | Process, origin |
| `.fig-worker` | Job, compiler backend |
| `.fig-db` | Database |
| `.fig-bucket` | Object storage |
| `.fig-cache` | Cache |
| `.fig-queue` | Queue |
| `.fig-cloud` | CDN, edge |
| `.fig-api` | Gateway |
| `.fig-box` | Module, package |
| `.fig-file` / `.fig-folder` | Artifact |
| `.fig-lock` / `.fig-key` | Auth |
| `.fig-flag` | Feature flag |
| `.fig-test` | Check, CI |
| `.fig-event` | Signal, HMR |
| `.fig-token` | Ticket, cookie |
| `.fig-globe` | Network |
| `.fig-clock` | Time, mtime |
| `.fig-filter` | Filter |
| `.fig-branch` | Git / fork |
| `.fig-transform` | Compiler pass |

Arrow: `<div class="fig-edge" data-label="GET"></div>`. Add class `down` or `strike`.

Keep a scene to about 4–7 glyphs.

## Layout

`.fig-row`, `.fig-col`, `.fig-cluster` (`data-label`), `.fig-compare` + `.fig-pane`, `.fig-stack` + `.fig-layer`, `.fig-pipe` + `.fig-phase`, `.fig-timeline` + `.fig-step`, `.fig-code` (`data-caption`) + `.fig-line.added|.removed`, `.fig-metric` (`data-value`), `.fig-callout`, `.fig-datapoints` with `<i class="on">` dots.

Code samples: at most 6 lines.

## Rules

- Abstract shapes only. No logos, no product screenshots.
- No `<script>`, no CSS animations, no autoplay.
- Real names from the PR. Do not invent subsystems.
- Open the HTML file in a browser. Nothing to install.
