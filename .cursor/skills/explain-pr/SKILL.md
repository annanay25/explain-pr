---
name: explain-pr
description: Explain a pull request as a stepped visual walkthrough using the Figure HTML component library. Use when asked to explain a PR, summarize code changes for humans, produce a change walkthrough, or generate an HTML visualization of what a diff does.
---

# Explain a PR with Figure

Produce a single HTML page that walks a human through a pull request, one idea per scene, using the **Figure** library (`lib/figure.css` + `lib/figure.js`).

Do not write a prose essay. Do not invent animations. Compose abstract glyphs into 5–8 scenes and let the built-in **Next** button advance the story.

## Output

A complete HTML file. Link the library relatively (or copy the two files next to the page):

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PR title — Figure</title>
    <link rel="stylesheet" href="/lib/figure.css" />
  </head>
  <body class="fig-page">
    <fig-deck
      title="Short human title"
      repo="org/repo"
      pr="1234"
      href="https://github.com/org/repo/pull/1234"
      added="318"
      removed="102"
      files="20"
    >
      <!-- scenes -->
    </fig-deck>
    <script src="/lib/figure.js"></script>
  </body>
</html>
```

If this repo is not on disk, inline `figure.css` and `figure.js` from the library files rather than paraphrasing new styles.

## How to think

1. Read the PR title, body, and the shape of the diff (not every line).
2. Name the *system* the change lives in: who talks to whom, what is stored, what runs at build vs request vs client.
3. Split the story into scenes. Each scene has **one claim**.
4. Prefer before → after, then the mechanism, then the consequence.
5. Stop at 8 scenes. If you need more, you do not understand it yet.
6. To stack two flows, wrap them in `fig-col` with `<fig-edge dir="down">` **between** the rows. A down-edge at the end of a `fig-row` does not connect to the next row.

Typical arc:

| # | Purpose |
|---|---------|
| 1 | What problem existed |
| 2 | The old path, drawn |
| 3 | What this PR inserts, removes, or splits |
| 4 | The new path, drawn |
| 5 | An important detail (cache, API, data shape) |
| 6 | How to tell it worked (tests, metrics) |

## Scene markup

```html
<fig-scene
  title="The static shell is reused after the first miss"
  caption="After a fallback is served, the route shell is generated and later requests skip the cold path."
>
  <fig-row>
    <fig-user label="Browser"></fig-user>
    <fig-edge label="GET /p"></fig-edge>
    <fig-cloud label="CDN" tone="changed" badge="hit"></fig-cloud>
    <fig-edge label="holes"></fig-edge>
    <fig-server label="Origin"></fig-server>
  </fig-row>
  <fig-callout tone="focus">Future requests use the new route shell instead of regenerating a fallback.</fig-callout>
</fig-scene>
```

`title` is the claim. `caption` is one or two sentences a reviewer could read aloud.

## Visual language

Tones (put on glyphs, layers, panes, edges, lines):

- `added` — new
- `removed` — gone or skipped
- `changed` — same object, new behaviour
- `focus` — look here
- `ghost` — present but no longer on the hot path

Keep a scene to about 4–7 glyphs. If you need more, split the scene.

### Actors and machines

| Tag | Use for |
|-----|---------|
| `fig-user` / `fig-users` | Person, requester, developer |
| `fig-browser` / `fig-mobile` | Client surface |
| `fig-server` | Process, origin, node |
| `fig-worker` | Background job, thread, compiler backend |
| `fig-db` | Database |
| `fig-bucket` | Object storage |
| `fig-cache` | Cache, memo table |
| `fig-queue` | Queue, buffer, pending work |
| `fig-cloud` | CDN, edge, hosted plane |
| `fig-api` | Gateway, public interface, diamond |
| `fig-box` | Module, component, package |
| `fig-file` / `fig-folder` | Source artifact |
| `fig-lock` / `fig-key` | Auth, secret, permission |
| `fig-flag` | Feature flag |
| `fig-test` | Check, CI, assertion |
| `fig-event` | Signal, pub/sub, HMR ping |
| `fig-token` | Ticket, cookie, capability |
| `fig-globe` | Network, public internet |
| `fig-clock` | Time, TTL, mtime |
| `fig-filter` | Filter, ignore rules |
| `fig-branch` | Git, control-flow fork |
| `fig-transform` | Compiler pass, rewriter |
| `fig-dots` | Data points (`n`, `on`, `label`) |

Glyph attributes: `label`, `note` (small second line), `tone`, `badge` (tiny chip, e.g. `+`, `hit`, `new`).

### Structure

| Tag | Use for |
|-----|---------|
| `fig-row` / `fig-col` | Flow vs stack |
| `fig-edge` | Arrow. `label`, `dir="down"` or `dir="left"`, `tone`, `strike` for a blocked path |
| `fig-cluster label="Build time"` | Dashed group |
| `fig-compare` + `fig-pane label="Before"` | Split |
| `fig-stack` + `fig-layer` | Layers of a system |
| `fig-pipe` + `fig-phase` | Named pipeline stages |
| `fig-timeline` + `fig-step` | Ordered time |
| `fig-code` + `fig-line tone="added"` | Tiny diff, not a file dump |
| `fig-metric value="3×" label="faster"` | One number |
| `fig-callout` | One sentence under the drawing |
| `fig-legend` | Optional key; auto-fills if empty |

Code samples: at most 6 lines. Show the idea, not the patch.

## Rules

- Abstract shapes only. No logos, no screenshots of the product, no architecture-tool clipart.
- No CSS animations, no timers, no autoplay. The Next button is the transition.
- Real names from the PR (`Scanner`, `postponedState`, `server.environments`). Do not invent subsystems.
- If unsure, draw fewer boxes and a longer caption.
- Empty, loading, and error: a deck with no `fig-scene` already shows an empty state. Do not add fake scenes when the PR is unreadable; one scene that says what is missing is enough.

## Done when

A teammate who has not read the diff can click Next and answer: what broke, what was added, and what to watch in review.
