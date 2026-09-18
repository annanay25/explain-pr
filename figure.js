/* Scene tabs, prompt composer, and lazy-loaded Mermaid diagrams. */
(function () {
  var MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.6.0/dist/mermaid.min.js";

  function buildSceneTabs() {
    document.querySelectorAll(".fig-shell").forEach(function (shell) {
      var existingWalk = shell.querySelector(":scope > .fig-walk");
      if (existingWalk) {
        bindSceneTabs(shell, existingWalk.querySelector(".fig-scene-tabs"));
        return;
      }

      var directScenes = shell.querySelector(":scope > .fig-scenes");
      var views = Array.from(shell.querySelectorAll(":scope > .fig-view"));
      if (!directScenes && !views.length) return;

      var oldViewTabs = shell.querySelector(":scope > .fig-view-tabs");
      var walk = document.createElement("div");
      walk.className = "fig-walk";
      var tabs = document.createElement("nav");
      tabs.className = "fig-scene-tabs";
      tabs.setAttribute("aria-label", "Walk views");
      tabs.innerHTML = '<p class="fig-scene-tabs-title">Views</p>';
      var content = document.createElement("div");
      content.className = "fig-walk-content";

      shell.insertBefore(walk, oldViewTabs || directScenes || views[0]);
      walk.appendChild(tabs);
      walk.appendChild(content);
      if (oldViewTabs) content.appendChild(oldViewTabs);
      if (directScenes) content.appendChild(directScenes);
      views.forEach(function (view) {
        content.appendChild(view);
      });

      var scenes = Array.from(content.querySelectorAll(".fig-scene"));
      scenes.forEach(function (scene, index) {
        var dot = scene.querySelector(".fig-dot.is-current");
        var sceneId = dot && dot.getAttribute("for");
        var sceneRadio = sceneId && shell.querySelector("#" + CSS.escape(sceneId));
        if (!sceneRadio) return;

        var view = scene.closest(".fig-view");
        var viewRadio = null;
        var group = "";
        if (view) {
          group = view.getAttribute("data-view") || "";
          viewRadio = shell.querySelector("#view-" + CSS.escape(group));
        }

        var button = document.createElement("button");
        button.type = "button";
        button.className = "fig-scene-tab";
        button.dataset.scene = sceneId;
        if (group) button.dataset.view = group;
        var number = (scene.querySelector(".fig-index")?.textContent || String(index + 1).padStart(2, "0")).trim();
        var fullTitle = (scene.querySelector("h2")?.textContent || "View " + (index + 1)).trim();
        var title = (scene.getAttribute("data-tab") || abridgeTabTitle(fullTitle)).trim();
        button.innerHTML = '<span class="fig-scene-tab-index"></span><strong></strong>';
        button.querySelector("span").textContent = number;
        button.querySelector("strong").textContent = title;
        button.addEventListener("click", function () {
          if (viewRadio) {
            viewRadio.checked = true;
            viewRadio.dispatchEvent(new Event("change", { bubbles: true }));
          }
          sceneRadio.checked = true;
          sceneRadio.dispatchEvent(new Event("change", { bubbles: true }));
        });
        tabs.appendChild(button);
      });

      bindSceneTabs(shell, tabs);
    });
  }

  function abridgeTabTitle(title) {
    var words = (title || "").replace(/\s+/g, " ").trim().split(" ");
    if (words.length <= 6) return words.join(" ");
    return words.slice(0, 6).join(" ").replace(/[.,;:!?]+$/, "") + "…";
  }

  function bindSceneTabs(shell, tabs) {
    if (!tabs) return;
    function sync() {
      var selectedView = shell.querySelector('input[name="view"]:checked');
      var selectedViewName = selectedView ? selectedView.id.replace(/^view-/, "") : "";
      tabs.querySelectorAll(".fig-scene-tab").forEach(function (tab) {
        var radio = shell.querySelector("#" + CSS.escape(tab.dataset.scene || tab.getAttribute("for") || ""));
        var inSelectedView = !tab.dataset.view || tab.dataset.view === selectedViewName;
        var current = Boolean(radio && radio.checked && inSelectedView);
        tab.classList.toggle("is-current", current);
        if (current) tab.setAttribute("aria-current", "page");
        else tab.removeAttribute("aria-current");
      });
    }
    shell.querySelectorAll('input[type="radio"]').forEach(function (radio) {
      radio.addEventListener("change", sync);
    });
    sync();
  }

  function addOriginalDiffLinks() {
    var repoLink = document.querySelector(".fig-repo a[href]");
    if (!repoLink) return;

    var pull;
    try {
      pull = new URL(repoLink.href);
    } catch (e) {
      return;
    }
    if (!/^\/[^/]+\/[^/]+\/pull\/\d+\/?$/.test(pull.pathname)) return;

    pull.pathname = pull.pathname.replace(/\/$/, "") + "/files";
    pull.search = "";
    pull.hash = "";
    if (repoLink.parentElement.querySelector(".fig-original-diff")) return;
    var link = document.createElement("a");
    link.className = "fig-original-diff";
    link.href = pull.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "View original diff ↗";
    link.setAttribute("aria-label", "View the original pull request diff on GitHub");
    repoLink.after(link);
  }

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
        sequenceNumberColor: "#fffaf2",
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
        var svg = el.querySelector("svg");
        if (svg) namespaceSvgIds(svg, "fig-mmd-" + i);
        var wrap = el.closest(".fig-mermaid-wrap");
        if (wrap && svg) wrap.classList.add("is-ready");
        bindMermaidClicks(el, src);
      } catch (e) {}
    }
  }

  function namespaceSvgIds(svg, prefix) {
    var ids = {};
    svg.querySelectorAll("[id]").forEach(function (node) {
      var oldId = node.id;
      var newId = prefix + "-" + oldId;
      ids[oldId] = newId;
      node.id = newId;
    });
    if (!Object.keys(ids).length) return;

    var refAttrs = ["marker-start", "marker-mid", "marker-end", "clip-path", "mask", "filter", "fill", "stroke", "href", "xlink:href"];
    svg.querySelectorAll("*").forEach(function (node) {
      refAttrs.forEach(function (attr) {
        var value = node.getAttribute(attr);
        if (!value) return;
        Object.keys(ids).forEach(function (oldId) {
          value = value.replaceAll("url(#" + oldId + ")", "url(#" + ids[oldId] + ")");
          if (value === "#" + oldId) value = "#" + ids[oldId];
        });
        node.setAttribute(attr, value);
      });
    });
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

  function bindMermaidClicks(el, src) {
    var svg = el.querySelector("svg");
    var pane = el.closest(".fig-pane") || el.closest(".fig-seq") || el.closest(".fig-scene") || document;
    if (!svg) return;
    var parsed = parseSequence(src);
    function inspect(label, anchor) {
      var node = findSeqNode(pane, label) || findSeqNode(document, label);
      if (!node && parsed.messages.length) {
        var hit = parsed.messages.find(function (m) {
          return normLabel(m.text) === normLabel(label);
        });
        if (hit) node = findSeqNode(pane, hit.to) || findSeqNode(pane, hit.from);
      }
      if (!node) return;
      showFollowUp(node, anchor, label);
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
        inspect(label, t);
      });
    });
  }

  buildSceneTabs();
  addOriginalDiffLinks();
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
      '<textarea class="fig-ask-q" aria-label="Your questions" rows="3" placeholder="What should we go deeper on?"></textarea>' +
      '<div class="fig-ask-label">Prompt for your coding agent</div>' +
      '<textarea class="fig-ask-prompt" aria-label="Prompt for your coding agent" rows="8" readonly></textarea>' +
      '<button type="button" class="fig-btn fig-copy">Copy prompt</button>';
    panel.appendChild(ask);
    return ask;
  }

  // One native dialog keeps notes and questions out of the scene layout.
  const followUp = document.createElement("dialog");
  followUp.className = "fig-follow-up";
  followUp.innerHTML = '<form method="dialog" class="fig-follow-up-bar">' +
    '<strong class="fig-follow-up-title"></strong><button class="fig-btn" autofocus>Close</button></form>' +
    '<div class="fig-follow-up-content"></div>';
  document.body.appendChild(followUp);
  const followUpContent = followUp.querySelector(".fig-follow-up-content");
  let followUpSource;
  let followUpAnchor;

  function positionFollowUp() {
    if (!followUp.open || !followUpAnchor) return;
    const r = followUpAnchor.getBoundingClientRect();
    const gap = 12, edge = 16;
    const vw = document.documentElement.clientWidth;
    const vh = window.innerHeight;
    const right = vw - r.right - gap - edge;
    const left = r.left - gap - edge;
    const beside = Math.max(right, left) >= 340;
    const width = Math.min(460, beside ? Math.max(right, left) : vw - edge * 2);
    const below = vh - r.bottom - gap - edge;
    const above = r.top - gap - edge;
    const under = below >= Math.min(360, above);
    const height = beside ? vh - edge * 2 : Math.max(160, under ? below : above);
    followUp.style.width = width + "px";
    followUp.style.maxHeight = Math.min(height, vh - edge * 2) + "px";
    const h = followUp.getBoundingClientRect().height;
    const x = beside ? (right >= left ? r.right + gap : r.left - gap - width) : r.left;
    const y = beside ? r.top : (under ? r.bottom + gap : r.top - gap - h);
    followUp.style.left = Math.max(edge, Math.min(x, vw - width - edge)) + "px";
    followUp.style.top = Math.max(edge, Math.min(y, vh - h - edge)) + "px";
  }
  window.addEventListener("resize", positionFollowUp);
  document.addEventListener("scroll", (ev) => {
    if (!followUp.contains(ev.target)) positionFollowUp();
  }, true);
  followUp.addEventListener("close", () => {
    if (followUpSource) {
      followUpSource.querySelector(".fig-ask-q").value =
        followUpContent.querySelector(".fig-ask-q").value;
    }
    followUpContent.replaceChildren();
    followUpSource = null;
    followUpAnchor?.classList.remove("fig-follow-up-anchor");
    followUpAnchor = null;
  });
  followUp.addEventListener("click", (ev) => {
    const rect = followUp.getBoundingClientRect();
    if (ev.target === followUp &&
        (ev.clientX < rect.left || ev.clientX > rect.right ||
         ev.clientY < rect.top || ev.clientY > rect.bottom)) followUp.close();
  });

  function showFollowUp(node, anchor, clickedLabel) {
    enhance(node);
    followUpSource = node;
    followUpAnchor = anchor;
    anchor.classList.add("fig-follow-up-anchor");
    const title = (clickedLabel || text(node, "strong") || "component").replace(/\s+/g, " ").trim();
    const clone = node.cloneNode(true);
    clone.hidden = false;
    clone.open = true;
    clone.removeAttribute("id");
    clone.querySelectorAll("[id]").forEach((el) => el.removeAttribute("id"));
    followUpContent.replaceChildren(clone);
    followUp.querySelector(".fig-follow-up-title").textContent = title;
    followUp.setAttribute("aria-label", title);
    const ask = clone.querySelector(".fig-ask");
    if (title !== ask.dataset.component) {
      ask.dataset.known = "Related component: " + ask.dataset.component + ".\n" + ask.dataset.known;
      ask.dataset.component = title;
      ask.dataset.kind = "";
    }
    bind(ask);
    followUp.showModal();
    positionFollowUp();
  }

  document.addEventListener("click", (ev) => {
    if (ev.target.closest(".fig-follow-up")) {
      // Keep the component heading expanded; nested fact folds still work.
      if (ev.target.closest("summary") === followUpContent.querySelector("summary")) {
        ev.preventDefault();
      }
      return;
    }
    const btn = ev.target.closest(".fig-gloss");
    const summary = ev.target.closest(".fig-node > summary");
    const node = btn
      ? findSeqNode(btn.closest(".fig-scene") || document, btn.dataset.term || btn.textContent)
      : summary?.parentElement;
    if (!node) return;
    ev.preventDefault();
    showFollowUp(node, btn || summary, btn ? btn.textContent : text(node, "strong"));
  });
})();
