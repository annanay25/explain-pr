---
name: explain-pr
description: Use when asked to explain a PR, summarize code changes, show data flow, assess blast radius, or generate an HTML visualization of what a diff does.
---

# Explain a PR

Produce **one short HTML walk** of the PR. Not three parallel views. The author should understand the change in a few Next clicks.

Copy `figure.css` and `figure.js` next to the page (or link them). Fonts and icons live in the CSS. `figure.js` builds the **follow-up prompt** when someone opens a component, and lazy-loads mermaid.js for any `.fig-mermaid` sequence diagram. Next is CSS (hidden radios + labels). No npm, no build, **no local server**. Open the `.html` file from disk (`file://`). Do not start Python, `npx serve`, or anything else to preview it.

Do not write a prose essay. **3 scenes. 5 is the hard max.** One claim per scene.

The component palette is `catalog.html`. Pick nodes, clusters, compare panes, metrics, risk tiles, and arrows that fit **this** PR. Do not invent a Story / Data / Blast tab set, and do not emit empty slides to “cover” those old views.

## Language

The reader is a teammate who has not opened the diff. Headlines, the sentence under them, and the line under each card name must make sense **out loud**.

**Visible text is English. Code names are labels.**

- Scene titles and captions: spoken English. A query param, function, or HTTP header does not belong in that sentence unless you immediately say what it does in plain words.
- Card **strong** may be the real name (`BlocksHandler`, `bucket index`). The **span** under it is still a plain sentence, not a stack of jargon.
- Panels may quote identifiers. Extra depth lives there after the picture is clear.

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
- Typical shape (not a template): (1) what changed, (2) how it works now, (3) blast as **hit vs not-hit**. Skip a beat that this PR does not have.

## Output skeleton

No view tabs. Radios `#s1`–`s5` on the deck. Put **Back / dots / Next above the scene title** (first child inside `.fig-stage`; CSS `order: -1` keeps it there even if the HTML is later in the file).

```html
<link rel="stylesheet" href="figure.css" />
<article class="fig-deck">
  <div class="fig-shell">
    <header class="fig-mast">
      <div>
        <p class="fig-kicker">explain-pr · walk</p>
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
          <nav class="fig-nav">
            <span class="fig-btn is-disabled">Back</span>
            <div class="fig-dots-nav">
              <label class="fig-dot is-current" for="s1"></label>
              <label class="fig-dot" for="s2"></label>
              <label class="fig-dot" for="s3"></label>
            </div>
            <label class="fig-btn fig-next" for="s2">Next</label>
          </nav>
          <div class="fig-scene-head">
            <div class="fig-index">01</div>
            <div>
              <h2>One spoken claim</h2>
              <p>One sentence of consequence.</p>
            </div>
          </div>
          <div class="fig-canvas">…components from the catalog…</div>
        </div>
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
4. If the diff changes types or functions, the how scene (the old data walk) is **one call tree**, not a bag of functions. Wrap methods in `.fig-enclose` whose header is a clickable `data-kind="type"` card. Function names label cards; they must not be the claim. **Every type, function, and field must show origin.** `added` = new in this PR, `changed` = existed and this PR edited it, `ghost` (or omit) = pre-existed, drawn only for context, `removed` = deleted. CSS paints an existed / new / changed / removed pill from that tone — do not hand-write chips. A type can be `changed` while a method inside is `ghost`. Do not mark an old helper `added`. **No orphan `fn`.** The entry point is the only function with no incoming edge. Every other function sits under the thing that calls it, with `.fig-edge down` between them. Package helpers belong in that same tree under their caller — not as a sibling of the enclose, the pane, or the canvas. If two callers share a helper, draw it once under the first and mention the other in the panel. Alternatives are a `.fig-row` of callees under one caller, not a vertical stack labeled `or` (that reads as A calls B). If you cannot name who calls it, do not draw the card; put the fact in a panel. Do **not** put a mermaid flowchart on this scene.
5. Last scene **is** the blast picture, not a pile of leftover facts. Use `.fig-compare` with two panes labeled exactly `Not in the blast` (`data-tone="added"`) and `In the blast` (`data-tone="changed"`). Every card goes in one pane. Untouched APIs, stores, and callers go in Not-hit. What this PR can break, plus the “Do not merge if…” node, go in Hit. `.fig-risk` tiles (`hot|watch|safe`) may sit **inside** those panes; they must not replace the two-pane layout. Do not emit a collage of unrelated cards (scope, validation, pipeline, filter, test) with no hit/not-hit split. If blast is none, keep both panes anyway — Not-hit holds the `safe` tiles, Hit holds one residual watch or the merge gate. Do not add a Blast tab.

## Inspect + follow-up prompt

Every named component is `<details class="fig-node" data-kind="…">` with kind, name, role, and a short panel of facts.

`figure.js` appends, on every node: **Your questions**, a **Prompt for your coding agent**, **Copy prompt**.

The prompt is a short briefing about **the selected card**, written like a follow-up in a working session: name the piece, name the PR, say where you are in the walk, paste the card’s facts, then “Here is my clarifying question:” and the reviewer’s question. Plain English. No “you wrote this PR.” Do not omit panel facts — they become `data-known` in the prompt.

Modifiers: `.tight`, `.wide`, `open` to start expanded (use once per scene for the main object).

Anonymous extras may stay `<div class="fig-user" data-label="Visitor A"></div>`.

Tones: `added`, `removed`, `changed`, `focus`, `ghost`. On `type` / `fn` / `var`, those become **new / removed / changed / existed** pills. Use `ghost` (not `focus`) for an unchanged helper you only drew for context.

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

`.fig-row`, `.fig-col`, `.fig-cluster`, `.fig-enclose` + `.fig-enclose-body`, `.fig-compare` + `.fig-pane`, `.fig-stack` + `.fig-layer`, `.fig-pipe` + `.fig-phase`, `.fig-timeline` + `.fig-step`, `.fig-seq` + `.fig-mermaid`, `.fig-code` + `.fig-line.added|.removed`, `.fig-metric`, `.fig-callout`, `.fig-datapoints`, `.fig-risk`.

Last scene uses compare as **hit / not-hit**, not Before / After (Before / After belongs on the “what changed” scene):

```html
<div class="fig-compare">
  <div class="fig-pane" data-label="Not in the blast" data-tone="added">
    <!-- untouched APIs, stores, callers; safe risk tiles -->
  </div>
  <div class="fig-pane" data-label="In the blast" data-tone="changed">
    <!-- what this PR can break; hot/watch tiles; Do not merge if… -->
  </div>
</div>
```

To stack flows: `.fig-col` with `<div class="fig-edge down">` **between** rows. For code layout, the type **encloses** its functions. That body is a call tree: entry point first, then callee, then the next callee. Do not list methods as unconnected peers.

```html
<div class="fig-enclose" data-tone="changed">
  <details class="fig-node" data-kind="type" data-tone="changed">
    <summary>
      <i class="fig-mark"></i>
      <span class="fig-node-text">
        <em>type</em>
        <strong>StoreGateway</strong>
        <span>Owns the blocks page handler.</span>
      </span>
    </summary>
    <div class="fig-node-panel">
      <p>Methods live on this struct. Ask here about the type as a whole.</p>
    </div>
  </details>
  <div class="fig-enclose-body">
    <div class="fig-col">
      <details class="fig-node" data-kind="fn" data-tone="changed">
        <summary>
          <i class="fig-mark"></i>
          <span class="fig-node-text">
            <em>function</em>
            <strong>BlocksHandler</strong>
            <span>Entry point. Now chooses catalog or full listing.</span>
          </span>
        </summary>
        <div class="fig-node-panel">
          <p>After this PR it parses page options, then calls loadBlocksPageData.</p>
        </div>
      </details>
      <div class="fig-edge down" data-label="calls"></div>
      <details class="fig-node" data-kind="fn" data-tone="added">
        <summary>
          <i class="fig-mark"></i>
          <span class="fig-node-text">
            <em>function</em>
            <strong>loadBlocksPageData</strong>
            <span>New. Picks catalog first.</span>
          </span>
        </summary>
        <div class="fig-node-panel">
          <p>Added in this PR. Called by BlocksHandler.</p>
        </div>
      </details>
      <div class="fig-edge down" data-label="then"></div>
      <details class="fig-node" data-kind="fn" data-tone="ghost">
        <summary>
          <i class="fig-mark"></i>
          <span class="fig-node-text">
            <em>function</em>
            <strong>filterBlocks</strong>
            <span>Already on the type. Not edited.</span>
          </span>
        </summary>
        <div class="fig-node-panel">
          <p>Called after the load. Ghost means it pre-existed and this PR did not change it.</p>
        </div>
      </details>
    </div>
  </div>
</div>
```

On the **what changed** scene, if the PR changes a request/response path, draw Before and After as mermaid `sequenceDiagram`s (lifelines, numbered messages, `alt`/`loop`/`Note`) — not a function flowchart, and not a second Cards view. Keep a hidden `.fig-node` per participant, with `data-seq` matching the participant title. `figure.js` opens that card’s inspect + prompt on click, and closes it on a second click of the same participant or message. Do not vendor mermaid unless the walk must work offline.

```html
<div class="fig-compare">
  <div class="fig-pane" data-label="Before" data-tone="removed">
    <div class="fig-seq">
      <details class="fig-node" data-kind="client" data-seq="Client">…</details>
      <details class="fig-node" data-kind="server" data-seq="Origin">…</details>
      <div class="fig-mermaid-wrap" data-label="Request / response">
        <pre class="fig-mermaid">sequenceDiagram
    autonumber
    participant Client
    participant Origin
    Client->>Origin: GET /index
    Origin-->>Client: one object
        </pre>
      </div>
      <div class="fig-seq-inspect">
        <p class="fig-seq-hint">Click a participant or message to inspect it. Click again to close.</p>
      </div>
    </div>
  </div>
  <div class="fig-pane" data-label="After" data-tone="added">
    <div class="fig-seq">…matching after sequence…</div>
  </div>
</div>
```

## Rules

- Abstract shapes only. No logos.
- No CSS animations, no autoplay. `figure.js` is the prompt composer plus a mermaid lazy-load.
- Real names from the PR. Do not invent subsystems. Put those names on cards; keep claims in English.
- **One walk. No Story / Data / Blast tabs.** Extra depth is a node the reviewer can open, not another view.
- Last scene is two panes: **Not in the blast** / **In the blast**. No leftover-card collage.
- Type / function / field cards always show origin (existed / new / changed / removed). Use `ghost` for unchanged helpers.
- How scene is a call tree. No orphan `fn` cards. Entry point excepted; every other function has an incoming `.fig-edge down` from its caller.
- Sequence mermaid is the before/after request path. Clicks inspect the matching card; a second click closes it. No function flowcharts.
- Distinct `data-kind` for distinct components.
- Open the HTML file in a browser (File → Open, or double-click). Nothing to install. Do not start a server.
- Re-read every visible sentence against the Language section before you stop.
- If you have more than five scenes, you failed to compress. Merge, then stop.
