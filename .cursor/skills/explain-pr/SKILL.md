---
name: explain-pr
description: Use when asked to explain a PR, summarize code changes, show data flow, assess blast radius, or generate an HTML visualization of what a diff does.
---

# Explain a PR with Figure

Produce **one short HTML walk** of the PR. Not three parallel views. The author should understand the change in a few Next clicks.

Copy `figure.css` and `figure.js` next to the page (or link them). Fonts and icons live in the CSS. `figure.js` only builds the **ask prompt** when a reviewer opens a component. Next is CSS (hidden radios + labels). No npm, no build, **no local server**. Open the `.html` file from disk (`file://`). Do not start Python, `npx serve`, or anything else to preview it.

Do not write a prose essay. **3 scenes. 5 is the hard max.** One claim per scene.

The component palette is `catalog.html`. Pick nodes, clusters, compare panes, metrics, risk tiles, and arrows that fit **this** PR. Do not invent a Story / Data / Blast tab set, and do not emit empty slides to “cover” those old views.

## Language

The reader is a teammate who has not opened the diff. Headlines, the sentence under them, and the line under each card name must make sense **out loud**.

**Visible text is English. Code names are labels.**

- Scene titles and captions: spoken English. A query param, function, or HTTP header does not belong in that sentence unless you immediately say what it does in plain words.
- Card **strong** may be the real name (`BlocksHandler`, `bucket index`). The **span** under it is still a plain sentence, not a stack of jargon.
- Panels may quote identifiers. That is what **Ask** is for — extra depth after the picture is clear.

**Forbidden texture**

- Metaphors that do not explain: “the old door”, “rooms”, “payload out”.
- Telegraphic stacks: “ReadIndex. Incomplete metas. Fast.”
- Assuming the reader already knows `scan_bucket=on`, `Accept: application/json`, `hydrate`, `thin Meta`.

**Check:** read the scene title and first sentence to someone who has not opened the diff. If they have to ask what a word is, rewrite it.

Bad: “The page reads that one object instead of walking the prefix. `scan_bucket=on` is the old door.”

Good: “The page reads that catalog instead of listing every file in storage. A Scan bucket checkbox still does the old, slower listing when you need brand-new blocks.”

## Length

The old three-view walk was too long. Compress.

- Merge before and after onto **one** compare (or one flow with a strike). Do not spend a scene on “it was slow” and another on “here is the new file.”
- Extra facts go in **panels**, not extra slides.
- If two sentences would retell the same claim, delete a scene.
- Typical shape (not a template): (1) what changed, (2) how it works now, (3) what still hurts / do not merge if. Skip a beat that this PR does not have.

## Output skeleton

No view tabs. Radios `#s1`–`s5` on the deck. Put **Back / dots / Next above the graphic** (nav is a sibling of `.fig-stage`; CSS puts it between the title and the canvas).

```html
<link rel="stylesheet" href="figure.css" />
<article class="fig-deck">
  <div class="fig-shell">
    <header class="fig-mast">
      <div>
        <p class="fig-kicker">Figure · PR walk</p>
        <h1>Plain-English title</h1>
        <div class="fig-repo"><a href="PR_URL">org/repo #123</a></div>
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
              <h2>One spoken claim</h2>
              <p>One sentence of consequence.</p>
            </div>
          </div>
          <div class="fig-canvas">…components from the catalog…</div>
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
      <!-- more scenes -->
    </div>
  </div>
</article>
<script src="figure.js"></script>
```

Put a `.fig-repo` link and the PR title in `.fig-mast h1` — the prompt composer reads those. If this repo is not on disk, copy `figure.css` and `figure.js` verbatim.

## How to think

1. Read the PR title, body, and the shape of the diff (not every line).
2. Name the system. Cut to **three claims** an author can hold. Drop the rest into panels.
3. Draw. Open `catalog.html` and pick marks that match roles. Distinct `data-kind` for distinct components.
4. If the diff changes types or functions, draw that layout on the “how” scene: a `.fig-cluster` per type, `fn` cards inside, arrows labeled `calls`. Function names label cards; they must not be the claim.
5. If a public API, prod store, or caller can break, put `.fig-risk` tiles (`hot|watch|safe`) on the last scene and a “Do not merge if…” node. If blast is none, one `safe` tile is enough — do not add a view for it.

## Inspect + ask prompt

Every named component is `<details class="fig-node" data-kind="…">` with kind, name, role, and a short panel of facts.

`figure.js` appends, on every node: **Your questions**, a **Prompt for your coding agent**, **Copy prompt**.

Do not omit panel facts — they become `data-known` in the prompt.

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
| `type` / `fn` / `var` | Class/struct/object, function/method, variable/field |
| `box` | Last resort unnamed module |

Arrow: `<div class="fig-edge" data-label="GET"></div>`. Add `down` or `strike`.

## Layout

`.fig-row`, `.fig-col`, `.fig-cluster`, `.fig-compare` + `.fig-pane`, `.fig-stack` + `.fig-layer`, `.fig-pipe` + `.fig-phase`, `.fig-timeline` + `.fig-step`, `.fig-code` + `.fig-line.added|.removed`, `.fig-metric`, `.fig-callout`, `.fig-datapoints`, `.fig-risk`.

To stack flows: `.fig-col` with `<div class="fig-edge down">` **between** rows. For code layout, put functions in a `.fig-cluster` labeled with the type name; `calls` arrows go between `fn` cards.

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

## Rules

- Abstract shapes only. No logos.
- No CSS animations, no autoplay. `figure.js` is only the prompt composer.
- Real names from the PR. Do not invent subsystems. Put those names on cards; keep claims in English.
- **One walk. No Story / Data / Blast tabs.** Extra depth is a node the reviewer can open, not another view.
- Distinct `data-kind` for distinct components.
- Open the HTML file in a browser (File → Open, or double-click). Nothing to install. Do not start a server.
- Re-read every visible sentence against the Language section before you stop.
- If you have more than five scenes, you failed to compress. Merge, then stop.
