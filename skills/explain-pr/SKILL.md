---
name: explain-pr
description: Use when asked to explain a PR, summarize code changes, show data flow, assess blast radius, or generate an HTML visualization of what a diff does.
---

# Explain a PR

Build one short HTML walk that explains the PR to a teammate who has not read the diff. The walk should answer three questions: What changed? How does it work now? What could it affect?

The usual walk has three scenes. Two is enough for a very small PR; five is the absolute limit. Each scene makes one claim, and every walk ends with a blast scene.

## 1. Understand the change

Read the PR title, body, and diff before drawing. Find:

- the old behavior and the new behavior;
- the runtime, request, or data path that changed;
- the entry point and the calls below it;
- the systems that are affected and the systems that are not;
- the condition that should block the merge.

Use only names and relationships supported by the PR. Never invent a subsystem to make the picture look complete.

## 2. Choose the three claims

A strong walk usually follows this shape:

1. **What changed** — show old and new behavior together.
2. **How it works now** — show the real path through the changed code.
3. **What is in the blast** — separate affected from unaffected parts.

This is a guide, not a template. You may omit the middle how scene when the PR has no meaningful implementation path, but never omit the final blast scene. Put supporting facts inside expandable component panels, not on extra slides.

Do not create Story, Data, or Blast tabs. This is one walk with Back and Next controls.

## 3. Write for a human

Write every visible sentence in plain, spoken English. Code names are labels; they are not explanations.

- A scene title states the claim without requiring knowledge of the diff.
- The sentence below it explains the consequence.
- A card may use the real type, function, field, or service name in `<strong>`.
- The line below the name explains its role in ordinary language.
- The expandable panel may use precise identifiers and technical detail.

Avoid unexplained jargon, sentence fragments, and decorative metaphors. Read each title and opening sentence aloud. If a teammate would need to ask what a term means, rewrite it.

Bad: “ReadIndex. Incomplete metas. Fast.”

Better: “The page reads one catalog instead of listing every file in storage.”

## 4. Draw the walk

Open `catalog.html` and choose components by role. Use different `data-kind` values for different kinds of things. Use `.fig-box` only when no specific kind fits.

Useful layouts include `.fig-row`, `.fig-col`, `.fig-cluster`, `.fig-enclose`, `.fig-compare`, `.fig-stack`, `.fig-pipe`, `.fig-timeline`, `.fig-seq`, `.fig-code`, `.fig-metric`, `.fig-callout`, `.fig-datapoints`, and `.fig-risk`.

Use abstract shapes only. Do not use logos, animation, or autoplay.

### Scene 1: show what changed

Place Before and After in one `.fig-compare`, or show one flow with a struck-out path. Do not spend separate scenes describing the same change.

#### Mermaid decision

If the PR changes **behavior, data flow, or request flow**, Scene 1 **must contain at least one Mermaid `sequenceDiagram`**. This is a requirement, not a styling preference.

Use participants for the real clients, services, modules, stores, workers, or build phases. Use messages to show what moves between them. Use `autonumber`, `alt`, `loop`, and `Note` when they make the change easier to follow.

When old and new paths differ, put the Before and After sequence diagrams in separate panes of one `.fig-compare`. A single sequence diagram is enough when only the new path matters.

Skip Mermaid only when the PR does not change behavior or flow—for example, a documentation-only change, a test-only change, a rename, or a static style update.

Do not replace the code call tree in Scene 2 with a Mermaid flowchart.

```html
<div class="fig-seq">
  <details class="fig-node" data-kind="build" data-seq="Setup">…</details>
  <details class="fig-node" data-kind="config" data-seq="Build context">…</details>
  <div class="fig-mermaid-wrap" data-label="Configuration flow">
    <pre class="fig-mermaid">sequenceDiagram
      autonumber
      participant Setup
      participant Context as Build context
      Setup->>Context: Parse and store normalized configuration
    </pre>
  </div>
  <div class="fig-seq-inspect">
    <p class="fig-seq-hint">Click a participant or message to inspect it. Click again to close.</p>
  </div>
</div>
```

Every Mermaid participant needs a hidden `.fig-node` whose `data-seq` exactly matches the participant title. `figure.js` uses that match to open the component panel. It also loads Mermaid when it finds `.fig-mermaid`. Do not vendor Mermaid unless the walk must work offline.

### Scene 2: show how it works now

When the PR changes types or functions, draw one call tree.

- Put the clickable `data-kind="type"` header directly inside `.fig-enclose`.
- Put its method tree inside `.fig-enclose-body`, with one `.fig-col` holding the methods and edges.
- Start with the entry point. It is the only function that may have no incoming edge.
- Put each callee below its caller with `<div class="fig-edge down">` between them.
- Put alternative callees beside each other in `.fig-row`.
- Draw a shared helper once, then mention its other callers in the panel.
- If you cannot name the caller, leave the function out of the tree and explain it in a panel.

Every `type`, `fn`, and `var` card must show its origin through `data-tone`:

- `added` — new in this PR;
- `changed` — existed and was edited;
- `ghost` — existed and is shown only for context;
- `removed` — deleted by the PR.

The CSS creates the new, changed, existed, and removed pills. Do not write those pills by hand. A changed type may contain an unchanged, `ghost` method.

### Scene 3: show the blast

The final scene is always a two-pane `.fig-compare`:

```html
<div class="fig-compare">
  <div class="fig-pane" data-label="Not in the blast" data-tone="added">
    <!-- unchanged APIs, stores, callers, and safe checks -->
  </div>
  <div class="fig-pane" data-label="In the blast" data-tone="changed">
    <!-- breakable behavior, residual risks, and the merge gate -->
  </div>
</div>
```

Use those pane labels exactly. Every card belongs in one pane. Put untouched contracts and dependencies in **Not in the blast**. Put behavior the PR can break and the “Do not merge if…” condition in **In the blast**.

Risk tiles (`hot`, `watch`, or `safe`) may sit inside the panes, but they do not replace them. Even a low-risk PR keeps both panes.

## 5. Make components inspectable

Every named thing drawn as a visual component is a `<details class="fig-node">` with a kind, name, role, and short fact panel. Names used only in prose or Mermaid messages do not need their own card. `figure.js` adds **Your questions**, **Prompt for your coding agent**, and **Copy prompt**.

The generated prompt must:

1. name the selected component and PR;
2. say where the component appears in the walk;
3. include the facts from its panel;
4. end with “Here is my clarifying question:” and the reviewer’s question.

Write the prompt as a natural follow-up in an active working session. Do not say “you wrote this PR.” Do not omit panel facts; they become `data-known`.

Use `.tight` or `.wide` when needed. Use `open` once per scene for its main component. Anonymous people may remain simple `.fig-user` elements.

## 6. Assemble the page

Copy or link `figure.css` and `figure.js` beside the HTML file. Fonts and icons are already in the CSS. The JavaScript builds follow-up prompts and lazy-loads Mermaid.

Use hidden radios named `walk`, with IDs `s1` through `s5`, to control the scenes. Put the Back / dots / Next navigation first inside every `.fig-stage`, above the scene title.

The mast must contain the PR title in `.fig-mast h1` and a linked repository reference in `.fig-repo`; the prompt composer reads both.

```html
<link rel="stylesheet" href="figure.css" />
<article class="fig-deck">
  <div class="fig-shell">
    <header class="fig-mast">
      <div>
        <p class="fig-kicker">explain-pr · walk</p>
        <h1>Plain-English PR title</h1>
        <div class="fig-repo"><a href="PR_URL">org/repo #123</a></div>
      </div>
    </header>
    <input type="radio" name="walk" id="s1" checked>
    <input type="radio" name="walk" id="s2">
    <input type="radio" name="walk" id="s3">
    <div class="fig-scenes">…three scenes…</div>
  </div>
</article>
<script src="figure.js"></script>
```

The page must open directly from disk with `file://`. Do not run npm, build the page, or start a local server.

## Component kinds

- People: `user`, `users`
- Clients: `browser`, `client`, `mobile`
- Processes: `server`, `worker`, `runtime`
- Stores and edge: `db`, `bucket`, `cache`, `queue`, `cloud`
- Gateways and environments: `api`, `env`
- Compiler hosts: `babel`, `oxc`, `swc`, `rust`
- Compiler stages: `compiler`, `parser`, `ast`, `ir`, `hir`
- Integrations: `plugin`, `adapter`, `transform`
- Storage and packaging: `arena`, `crate`, `bundler`, `scan`
- Artifacts: `file`, `folder`, `doc`, `term`, `fallback`, `route`
- Graphs and packages: `module`, `graph`, `package`
- Web shapes: `html`, `css`, `js`, `wasm`, `stream`, `hook`
- Signals: `lock`, `key`, `flag`, `test`, `event`, `token`
- Operations: `clock`, `filter`, `branch`, `tree`, `config`, `log`, `error`
- Flow: `request`, `response`, `snapshot`, `build`, `pipeline`
- Code: `type`, `fn`, `var`
- Last resort: `box`

Create arrows with `<div class="fig-edge" data-label="…"></div>`. Add `down` for a vertical connection or `strike` for a removed path.

## Final check

Before stopping, verify all of the following:

- The walk has two to five scenes, usually three, and ends with the blast scene.
- Every scene makes one distinct claim in plain English.
- The page has no Story / Data / Blast tabs.
- A behavior, data-flow, or request-flow change includes `.fig-mermaid` with a `sequenceDiagram`.
- Every Mermaid participant has a matching `data-seq` component.
- The how scene uses a connected call tree when functions changed; it has no orphan function cards.
- Every type, function, and field card shows whether it existed, changed, was added, or was removed.
- The last scene uses **Not in the blast** and **In the blast** panes.
- Every named component opens a useful fact panel and follow-up prompt.
- `figure.css` and `figure.js` are available beside the page.
- The HTML opens from disk without a build or local server.
