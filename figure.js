/* Prompt composer for inspectable nodes. Lazy-loads mermaid for .fig-mermaid. Next stays CSS-only. */
(function () {
  var MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.6.0/dist/mermaid.min.js";

  function figureDir() {
    var el = document.querySelector('script[src*="figure.js"]');
    if (!el) return "";
    var src = el.getAttribute("src") || "";
    var i = src.lastIndexOf("/");
    return i === -1 ? "" : src.slice(0, i + 1);
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = function () {
        resolve();
      };
      s.onerror = function () {
        reject(new Error("load failed: " + src));
      };
      document.head.appendChild(s);
    });
  }

  async function mermaidApi() {
    if (window.mermaid) return window.mermaid;
    var local = figureDir() + "mermaid.min.js";
    var tryLocal = location.protocol === "file:";
    if (!tryLocal) {
      try {
        tryLocal = (await fetch(local, { method: "HEAD" })).ok;
      } catch (e) {}
    }
    if (tryLocal) {
      try {
        await loadScript(local);
      } catch (e) {}
    }
    if (window.mermaid) return window.mermaid;
    await loadScript(MERMAID_CDN);
    return window.mermaid;
  }

  async function renderMermaid() {
    var nodes = document.querySelectorAll(".fig-mermaid");
    if (!nodes.length) return;
    var mermaid;
    try {
      mermaid = await mermaidApi();
    } catch (e) {
      return;
    }
    if (!mermaid || typeof mermaid.render !== "function") return;
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      fontFamily: "IBM Plex Sans, ui-sans-serif, system-ui, sans-serif",
      themeVariables: {
        fontFamily: "IBM Plex Sans, ui-sans-serif, system-ui, sans-serif",
        primaryColor: "#fffaf2",
        primaryTextColor: "#1a1714",
        primaryBorderColor: "#d8cfc2",
        lineColor: "#6f675e",
        secondaryColor: "#d6efe3",
        tertiaryColor: "#f3efe6",
        background: "#fffaf2",
        mainBkg: "#fffaf2",
        clusterBkg: "#f3efe6",
        clusterBorder: "#d8cfc2",
        titleColor: "#1a1714",
        edgeLabelBackground: "#f3efe6",
        nodeTextColor: "#1a1714",
        actorBkg: "#fffaf2",
        actorBorder: "#1a1714",
        actorTextColor: "#1a1714",
        actorLineColor: "#6f675e",
        signalColor: "#1a1714",
        signalTextColor: "#1a1714",
        labelBoxBkgColor: "#f6e3b8",
        labelBoxBorderColor: "#9a5b00",
        labelTextColor: "#1a1714",
        loopTextColor: "#1a1714",
        noteBkgColor: "#f6e3b8",
        noteTextColor: "#1a1714",
        noteBorderColor: "#9a5b00",
        sequenceNumberColor: "#f3efe6",
      },
      flowchart: {
        htmlLabels: false,
        useMaxWidth: true,
        curve: "polyline",
        padding: 12,
      },
      sequence: {
        mirrorActors: true,
        useMaxWidth: true,
        actorMargin: 40,
        messageMargin: 32,
        boxMargin: 8,
        noteMargin: 10,
        actorFontFamily: "IBM Plex Sans, ui-sans-serif, sans-serif",
        messageFontFamily: "IBM Plex Sans, ui-sans-serif, sans-serif",
        noteFontFamily: "IBM Plex Sans, ui-sans-serif, sans-serif",
      },
    });
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var src = (el.textContent || "").trim();
      if (!src) continue;
      el.dataset.src = src;
      try {
        var out = await mermaid.render("fig-mmd-" + i, src);
        el.innerHTML = out.svg;
        var wrap = el.closest(".fig-mermaid-wrap");
        if (wrap && el.querySelector("svg")) wrap.classList.add("is-ready");
        bindMermaidClicks(el, src);
      } catch (e) {}
    }
  }

  function normLabel(s) {
    return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function parseSequence(src) {
    var aliases = {};
    var messages = [];
    (src || "").split(/\n/).forEach(function (line) {
      line = line.trim();
      var p = line.match(/^(?:participant|actor)\s+(\S+)(?:\s+as\s+(.+))?$/i);
      if (p) {
        var display = (p[2] || p[1]).trim();
        aliases[normLabel(p[1])] = display;
        aliases[normLabel(display)] = display;
        return;
      }
      var m = line.match(/^(\S+)\s*(-->>?|--x|->>?|-\.->>?)\s*(\S+)\s*:\s*(.+)$/);
      if (m) {
        messages.push({
          from: aliases[normLabel(m[1])] || m[1],
          to: aliases[normLabel(m[3])] || m[3],
          text: m[4].trim(),
        });
      }
    });
    return { aliases: aliases, messages: messages };
  }

  function findSeqNode(root, label) {
    var k = normLabel(label);
    if (!k || /^\d+$/.test(k)) return null;
    var nodes = root.querySelectorAll(".fig-node");
    var i;
    for (i = 0; i < nodes.length; i++) {
      var seq = normLabel(nodes[i].getAttribute("data-seq"));
      var name = normLabel(text(nodes[i], "strong"));
      if (seq === k || name === k) return nodes[i];
    }
    for (i = 0; i < nodes.length; i++) {
      seq = normLabel(nodes[i].getAttribute("data-seq"));
      name = normLabel(text(nodes[i], "strong"));
      if ((seq && (k.indexOf(seq) !== -1 || seq.indexOf(k) !== -1)) ||
          (name && (k.indexOf(name) !== -1 || name.indexOf(k) !== -1))) {
        return nodes[i];
      }
    }
    return null;
  }

  function nodeKey(node) {
    return normLabel(node.getAttribute("data-seq") || "") + "\n" + normLabel(text(node, "strong"));
  }

  function showSeqInspect(node, dock) {
    if (!node || !dock) return;
    var key = nodeKey(node);
    if (dock.dataset.openKey === key) {
      dock.querySelectorAll(".fig-node").forEach(function (n) {
        n.remove();
      });
      delete dock.dataset.openKey;
      return;
    }
    bind(enhance(node));
    dock.querySelectorAll(".fig-node").forEach(function (n) {
      n.remove();
    });
    var clone = node.cloneNode(true);
    clone.hidden = false;
    clone.open = true;
    clone.removeAttribute("hidden");
    dock.appendChild(clone);
    dock.dataset.openKey = key;
    var ask = clone.querySelector(".fig-ask");
    if (ask) bind(ask);
  }

  function bindMermaidClicks(el, src) {
    var svg = el.querySelector("svg");
    var pane = el.closest(".fig-pane") || el.closest(".fig-seq") || el.closest(".fig-scene") || document;
    var dock = (el.closest(".fig-seq") || pane).querySelector(".fig-seq-inspect");
    if (!svg) return;
    var parsed = parseSequence(src);
    function inspect(label) {
      var node = findSeqNode(pane, label) || findSeqNode(document, label);
      if (!node && parsed.messages.length) {
        var hit = parsed.messages.find(function (m) {
          return normLabel(m.text) === normLabel(label);
        });
        if (hit) node = findSeqNode(pane, hit.to) || findSeqNode(pane, hit.from);
      }
      if (!node) return;
      showSeqInspect(node, dock);
    }
    var bound = [];
    svg.querySelectorAll("text").forEach(function (t) {
      var label = (t.textContent || "").replace(/\s+/g, " ").trim();
      if (!label || /^\d+$/.test(label)) return;
      var target = t.closest("g") || t;
      if (bound.indexOf(target) !== -1) return;
      bound.push(target);
      target.style.cursor = "pointer";
      target.addEventListener("click", function (ev) {
        ev.stopPropagation();
        inspect(label);
      });
    });
  }

  renderMermaid();
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
    const q = (questions || "").trim();
    const pr = (ask.dataset.pr || "").trim();
    const title = (ask.dataset.title || "").trim();
    const name = (ask.dataset.component || "this").trim();
    const kind = (ask.dataset.kind || "").trim();
    const scene = (ask.dataset.claim || "").trim();
    const caption = (ask.dataset.caption || "").trim();
    const known = (ask.dataset.known || "").trim();

    const who =
      kind && kind.toLowerCase() !== name.toLowerCase() ? name + " (" + kind + ")" : name;
    const from = pr && title ? pr + " — " + title : pr || title;

    const lines = [];
    lines.push(from ? "Look at " + who + " in " + from + "." : "Look at " + who + ".");
    if (scene || caption) {
      lines.push("");
      if (scene) lines.push(scene);
      if (caption && caption !== scene) lines.push(caption);
    }
    if (known) {
      lines.push("");
      lines.push(known);
    }
    lines.push("");
    lines.push("Here is my clarifying question:");
    if (q) lines.push(q);
    lines.push("");
    return lines.join("\n");
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
    ask.dataset.caption = (scene?.querySelector(".fig-scene-head p")?.textContent || "")
      .replace(/\s+/g, " ")
      .trim();
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
