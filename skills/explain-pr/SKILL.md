---
name: explain-pr
description: Use when asked to explain a PR, summarize code changes, show data flow, assess blast radius, or generate an HTML visualization of what a diff does.
---

# Explain a PR

Build one short HTML walk that explains the PR to a teammate who has not read the diff. The walk should answer four questions: What changed? Why does that produce the claimed result? How does it work now? What could it affect?

These questions do not need one scene each. The usual walk has three scenes. Two is enough for a very small PR; five is the absolute limit. Each scene makes one claim, and every walk ends with a blast scene.

## 1. Understand the change

Read the PR title, body, diff, and relevant unchanged code and tests at the reviewed commit before drawing. Find:

- the old behavior and the new behavior;
- the runtime, request, or data path that changed;
- the downstream rule or behavior, changed or unchanged, that turns the change into its claimed benefit;
- the entry point and the calls below it;
- the systems that are affected and the systems that are not;
- the assumptions and edge cases that limit the claim;
- the condition that should block the merge.

Use only names and relationships supported by the PR or verified in the repository. Never invent a subsystem to make the diagram look complete.

## 2. Choose the claims

A strong walk usually follows this shape:

1. **What changed** — show old and new behavior together.
2. **Why that produces the claimed result** — a named person (or named request) asking for a few concrete things, in story order, so the reader sees which asks get cheaper and which do not.
3. **How it works now** — pair each logical change from the previous scene with the important git hunks that implement it.
4. **What is in the blast** — separate affected from unaffected parts.

### Explain the causal mechanism

For every claimed behavioral benefit or system outcome, show why the change produces that result, not only what changed. Identify and inspect the downstream rule or behavior that makes the change matter, even when that code is unchanged. Scene 2 is that proof: a short story of a few asks, not a second copy of the before-and-after path. Do not reuse scene 1’s actors just to relabel the same sequence. By the end, the reader should be able to repeat who asked for what, why that ask got cheaper (or did not), and what the change does not guarantee.

If the story would stop at the changed code, put the missing causal step in that same why-scene sequence (how a consumer reads the data, how a limit is applied, how retries propagate). Do not add a second diagram to hold it. When several limits or stages interact, label what each one controls. Illustrative values are welcome; state their assumptions.

The causal chain, concrete example, assumptions, edge case, and limits of the guarantee must all appear in visible scene content. When several controls interact, show those controls too. Panels may add evidence and detail, but the reader must not need them to understand the argument.

The shape above is a guide, not a template. Prefer why before how when both need a scene. You may omit the how scene when the PR has no meaningful implementation path, but causal reasoning must remain visible whenever the PR claims a benefit. Never omit the final blast scene. Put supporting facts—not essential reasoning—inside expandable component panels.

Do not create Story, Data, or Blast tabs. This is one walk with Back and Next controls.

## 3. Write for a human

Write every visible sentence in plain, spoken English. Code names are labels; they are not explanations. The open sentence must make sense to someone who has not read the diff.

- A scene title states the claim without requiring knowledge of the PR.
- The sentence below it explains the consequence. On the why scene, that sentence starts with “Let’s take an example:” and names the person, the numbers, and the few things they will ask for.
- Do not put function names, type names, or flag names in that open sentence.
- Wrap the few words a newcomer would not know in a marked term:

```html
<button type="button" class="fig-gloss" data-term="Bucket catalog" aria-expanded="false">index file</button>
```

`data-term` matches a component’s `data-seq` or `<strong>` in the same scene. The button text is the everyday phrase. First click shows that component’s one-line role. Second click, or “Show the full note”, opens the full panel. Function names belong only in that panel. Mark at most a few terms per sentence. If the sentence still needs a definition to be readable, rewrite the sentence.

- A card may use the real type, function, field, or service name in `<strong>`.
- The line below the name explains its role in ordinary language. That line is the peek.
- The expandable panel may use precise identifiers and technical detail.

Avoid unexplained jargon, sentence fragments, and decorative metaphors. Read each title and opening sentence aloud. If a teammate would need to ask what a term means, mark it or rewrite it.

Bad: “ReadIndex. Incomplete metas. Fast.”

Better: “The page reads one index file instead of listing every file in storage.”

## 4. Draw the walk

Open `catalog.html` and choose components by role. Use different `data-kind` values for different kinds of things. Use `.fig-box` only when no specific kind fits.

Useful layouts include `.fig-row`, `.fig-col`, `.fig-cluster`, `.fig-enclose`, `.fig-compare`, `.fig-stack`, `.fig-pipe`, `.fig-timeline`, `.fig-seq`, `.fig-code`, `.fig-metric`, `.fig-callout`, `.fig-datapoints`, and `.fig-risk`.

Use abstract shapes only. Do not use logos, animation, or autoplay.

### Mermaid for the what-changed and why scenes

If the PR changes **behavior, data flow, or request flow**, the what-changed and why scenes each need Mermaid `sequenceDiagram`s. This is a requirement, not a styling preference.

- **What-changed:** one sequence, or a Before/After pair in one `.fig-compare`. Two diagrams here are allowed only as old path vs new path.
- **Why:** **exactly one** sequence. Never two. Never a cheap pane beside an expensive pane.

Use participants for the real clients, services, stores, workers, data, limits, or request kinds the claim needs. Scene 2 may introduce people and components that did not appear in scene 1. Keep the diagram to the few actors the story needs. Prefer a chronological sequence of asks over `alt`/`opt` branches; `opt` without `end` will not render. Keep message text short and avoid commas (they break Mermaid parsing).

Do not reuse scene 1’s sequence with extra labels. Scene 1 answers “what path changed.” Scene 2 answers “what happens when this person asks for these things.”

Skip Mermaid on the how scene, the blast scene, and when the PR does not change behavior or flow—for example, a documentation-only change, a test-only change, a rename, or a static style update.

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

### Scene 1: show what changed

Place Before and After in one `.fig-compare`, or show one flow with a struck-out path. Do not spend separate scenes describing the same change. When old and new paths differ, put the Before and After sequence diagrams in separate panes of one `.fig-compare`. A single sequence diagram is enough when only the new path matters.

### Scene 2: walk one example as a story

This scene is a story about a few asks, not a restatement of the mechanism and not a second architecture diagram.

1. **Title** is the punchline of the example (who got cheaper, who did not). It is not scene 1’s claim again.
2. **Opening sentence** starts with “Let’s take an example:”, names a person or a specific request, gives the numbers, and says we will watch a few things they ask for.
3. **Two to four `.fig-callout`s** tell those asks in story order, each one sentence a newcomer can repeat: who asked for what, how much expensive work it caused, and whether the change helped. Usual order: the everyday ask that is now cheap, then a heavier ask that still stays bounded, then an ask this change does not help.
4. **Exactly one** Mermaid `sequenceDiagram` under those callouts. It plays the same asks in the same order as one conversation. Different actors than scene 1 are allowed and often required.

```html
<div class="fig-col">
  <div class="fig-callout" data-tone="added"><strong>First she opens the table.</strong> …the win…</div>
  <div class="fig-callout" data-tone="added"><strong>Later she asks for more.</strong> …still bounded…</div>
  <div class="fig-callout" data-tone="changed"><strong>Last she runs her export.</strong> …this change does not help…</div>
</div>
<div class="fig-seq">
  <!-- hidden .fig-node cards, then one .fig-mermaid-wrap -->
</div>
```

Do not:

- put two `.fig-mermaid` blocks on this scene;
- split the scene into cheap vs expensive panes with matching sequences;
- use `alt`/`opt` to stack those two paths inside one diagram;
- name cases after stages or functions (Filter, Trim, `ReadIndex`) instead of after what the person asked for.

### Scene 3: map each logical change to the important diffs

Do not draw another sequence diagram. Do not explain the implementation as a list of function-name cards.

Take the logical steps the previous scene already established. For each important step, use one `.fig-compare`:

- **Left pane** (`data-label="Logical change"`): that step in plain English, plus the same components the previous scene used for it.
- **Right pane** (`data-label="Important diff"`): the corresponding git hunks as `.fig-code` with `.fig-line.added` and `.fig-line.removed`.

Show the hunks that change behavior or data/request flow. Skip cosmetics: HTML/CSS polish, formatting-only edits, changelog wording, and tests that only lock behavior already shown. Elide uninteresting lines with a context `.fig-line`; do not dump the whole file.

```html
<div class="fig-compare">
  <div class="fig-pane" data-label="Logical change">
    <div class="fig-callout">The page reads one catalog instead of listing every folder.</div>
    <details class="fig-node" data-kind="file">…Bucket catalog…</details>
  </div>
  <div class="fig-pane" data-label="Important diff">
    <div class="fig-code" data-caption="path/to/file.go">
      <span class="fig-line removed">oldCall()</span>
      <span class="fig-line added">newCall()</span>
    </div>
  </div>
</div>
```

Omit this scene when the PR has no meaningful implementation path.

If a `type`, `fn`, or `var` card does appear, show its origin through `data-tone`:

- `added` — new in this PR;
- `changed` — existed and was edited;
- `ghost` — existed and is shown only for context;
- `removed` — deleted by the PR.

The CSS creates the new, changed, existed, and removed pills. Do not write those pills by hand. A changed type may contain an unchanged, `ghost` method.

### Final scene: show the blast

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
    <!-- Add s4 when the causal mechanism needs its own scene. -->
    <div class="fig-scenes">…two to five scenes…</div>
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
- For every claimed behavioral benefit, the visible diagrams connect the changed code to the relevant downstream mechanism, including unchanged behavior when the claim depends on it.
- The why scene is a named person’s (or named request’s) story: punchline title, “Let’s take an example:” opening, two to four callouts in story order, then exactly one chronological sequence.
- That scene has exactly one `.fig-mermaid`. It is not a relabel of scene 1, not a cheap-vs-expensive pair, and not `alt`/`opt` stacked as two diagrams.
- Interacting limits or stages, when present, are individually labelled.
- Assumptions, a distinguishing edge case, and what the change does not guarantee are visible.
- The page has no Story / Data / Blast tabs.
- The what-changed scene includes one sequence, or a Before/After pair. The why scene includes exactly one sequence. Both use `sequenceDiagram` when the PR changes behavior or flow.
- The how scene maps each logical change from the previous scene to the important git hunks; it has no Mermaid diagram and no function-name card tree.
- Cosmetic hunks are omitted from the how scene; the remaining diffs are the ones that change behavior.
- Every Mermaid participant has a matching `data-seq` component.
- Every type, function, and field card shows whether it existed, changed, was added, or was removed.
- The last scene uses **Not in the blast** and **In the blast** panes.
- Every named component opens a useful fact panel and follow-up prompt.
- Unknown words in the open sentence are marked terms. First click is a one-line role; the full note waits behind a second click.
- `figure.css` and `figure.js` are available beside the page.
- The HTML opens from disk without a build or local server.

**Causal completeness:** For every claimed behavioral benefit, can someone unfamiliar with the code use only the visible diagrams to trace changed code → downstream mechanism → claimed benefit, then explain the old/new example, assumptions, edge case, limits of the guarantee, and any interacting controls? If they must open a panel or ask about a relevant unchanged downstream operation, the walk is missing an essential step.
