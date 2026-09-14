/* Prompt composer for inspectable nodes. Next stays CSS-only. */
(function () {
  function text(el, sel) {
    return (el.querySelector(sel)?.textContent || "").replace(/\s+/g, " ").trim();
  }

  function knownText(node) {
    const panel = node.querySelector(".fig-node-panel");
    if (!panel) return "";
    const bits = [];
    panel.querySelectorAll(":scope > p").forEach((p) => bits.push(p.textContent.trim()));
    panel.querySelectorAll(":scope > .fig-fold").forEach((fold) => {
      const title = fold.querySelector("summary")?.textContent.trim();
      const body = [...fold.querySelectorAll(":scope > p")].map((p) => p.textContent.trim()).join(" ");
      if (title) bits.push(title + (body ? ": " + body : ""));
    });
    return bits.filter(Boolean).join("\n");
  }

  function buildPrompt(ask, questions) {
    const q = (questions || "").trim() || "(write your questions here)";
    const known = ask.dataset.known || "";
    return [
      "You wrote this PR and you generated the walk I'm looking at so I could understand the change. This is a follow-up about one piece of that picture — not a first look.",
      "",
      "PR: " + (ask.dataset.pr || "") + (ask.dataset.title ? " — " + ask.dataset.title : ""),
      "Component: " + (ask.dataset.component || "") + (ask.dataset.kind ? " (" + ask.dataset.kind + ")" : ""),
      "Scene: " + (ask.dataset.claim || ""),
      "",
      "What you already put on this card:",
      known || "(nothing extra on the card — go to the diff and the real files)",
      "",
      "Go deeper on this component. Quote file paths. If the walk oversimplified or is wrong, correct it.",
      "",
      "My questions:",
      q,
      "",
    ].join("\n");
  }

  function bind(ask) {
    const q = ask.querySelector(".fig-ask-q");
    const out = ask.querySelector(".fig-ask-prompt");
    const copy = ask.querySelector(".fig-copy");
    if (!q || !out) return;
    const render = () => {
      out.value = buildPrompt(ask, q.value);
    };
    q.addEventListener("input", render);
    render();
    if (!copy) return;
    copy.addEventListener("click", async () => {
      render();
      try {
        await navigator.clipboard.writeText(out.value);
      } catch {
        out.focus();
        out.select();
        document.execCommand("copy");
      }
      copy.classList.add("is-copied");
      const prev = copy.textContent;
      copy.textContent = "Copied";
      setTimeout(() => {
        copy.classList.remove("is-copied");
        copy.textContent = prev;
      }, 1600);
    });
  }

  function enhance(node) {
    let panel = node.querySelector(".fig-node-panel");
    if (!panel) {
      panel = document.createElement("div");
      panel.className = "fig-node-panel";
      node.appendChild(panel);
    }
    if (panel.querySelector(".fig-ask")) return panel.querySelector(".fig-ask");

    const deck = node.closest(".fig-deck");
    const scene = node.closest(".fig-scene");

    const ask = document.createElement("aside");
    ask.className = "fig-ask";
    ask.dataset.pr = (deck?.querySelector(".fig-repo")?.textContent || "").replace(/\s+/g, " ").trim();
    ask.dataset.title = (deck?.querySelector(".fig-mast h1")?.textContent || "").trim();
    ask.dataset.component = text(node, "strong") || node.getAttribute("data-kind") || "component";
    ask.dataset.kind = text(node, "em") || node.getAttribute("data-kind") || "";
    ask.dataset.claim = (scene?.querySelector("h2")?.textContent || "").trim();
    const role = text(node, ".fig-node-text span");
    const known = [role, knownText(node)].filter(Boolean).join("\n");
    ask.dataset.known = known;

    ask.innerHTML =
      '<div class="fig-ask-label">Your questions</div>' +
      '<textarea class="fig-ask-q" rows="3" placeholder="What should we go deeper on?"></textarea>' +
      '<div class="fig-ask-label">Prompt for your coding agent</div>' +
      '<textarea class="fig-ask-prompt" rows="8" readonly></textarea>' +
      '<button type="button" class="fig-btn fig-copy">Copy prompt</button>';
    panel.appendChild(ask);
    return ask;
  }

  document.querySelectorAll(".fig-node").forEach((node) => {
    bind(enhance(node));
  });
})();
