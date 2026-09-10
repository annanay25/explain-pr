const ICONS = {
  user: `
    <circle class="wire" cx="32" cy="20" r="8"/>
    <path class="wire" d="M14 50c2-12 9-18 18-18s16 6 18 18"/>`,
  users: `
    <circle class="wire" cx="24" cy="20" r="7"/>
    <path class="wire" d="M10 50c2-11 8-16 14-16s12 5 14 16"/>
    <circle class="wire" cx="42" cy="22" r="6"/>
    <path class="wire" d="M32 50c1-9 6-14 12-14s11 5 12 14"/>`,
  server: `
    <rect class="wire" x="12" y="10" width="40" height="13" rx="2"/>
    <rect class="wire" x="12" y="26" width="40" height="13" rx="2"/>
    <rect class="wire" x="12" y="42" width="40" height="13" rx="2"/>
    <circle class="solid" cx="20" cy="16.5" r="1.8"/>
    <circle class="solid" cx="20" cy="32.5" r="1.8"/>
    <circle class="solid" cx="20" cy="48.5" r="1.8"/>`,
  db: `
    <ellipse class="wire" cx="32" cy="16" rx="16" ry="7"/>
    <path class="wire" d="M16 16v26c0 4 7 8 16 8s16-4 16-8V16"/>
    <path class="wire" d="M16 28c0 4 7 7 16 7s16-3 16-7"/>
    <path class="wire" d="M16 38c0 4 7 7 16 7s16-3 16-7"/>`,
  box: `
    <rect class="wire" x="12" y="12" width="40" height="40" rx="6"/>
    <path class="wire" d="M32 12v40M12 32h40"/>`,
  file: `
    <path class="wire" d="M20 10h16l12 12v32H20z"/>
    <path class="wire" d="M36 10v12h12"/>
    <path class="wire" d="M26 34h16M26 42h12"/>`,
  folder: `
    <path class="wire" d="M10 20h14l6 6h24v24H10z"/>
    <path class="wire" d="M10 26h44"/>`,
  cloud: `
    <path class="wire" d="M18 42h26a10 10 0 0 0 2-20 14 14 0 0 0-27-3A10 10 0 0 0 18 42z"/>`,
  cache: `
    <path class="wire" d="M32 8 52 20v24L32 56 12 44V20z"/>
    <circle class="wire" cx="32" cy="32" r="8"/>`,
  queue: `
    <rect class="wire" x="8" y="18" width="20" height="28" rx="3"/>
    <rect class="wire" x="22" y="14" width="20" height="28" rx="3"/>
    <rect class="wire" x="36" y="10" width="20" height="28" rx="3"/>`,
  api: `
    <path class="wire" d="M32 8 54 32 32 56 10 32z"/>
    <circle class="wire" cx="32" cy="32" r="6"/>`,
  browser: `
    <rect class="wire" x="10" y="12" width="44" height="40" rx="4"/>
    <path class="wire" d="M10 22h44"/>
    <circle class="solid" cx="18" cy="17" r="1.5"/>
    <circle class="solid" cx="24" cy="17" r="1.5"/>`,
  worker: `
    <circle class="wire" cx="32" cy="32" r="10"/>
    <path class="wire" d="M32 12v8M32 44v8M12 32h8M44 32h8M18 18l6 6M40 40l6 6M46 18l-6 6M24 40l-6 6"/>`,
  lock: `
    <rect class="wire" x="18" y="28" width="28" height="22" rx="3"/>
    <path class="wire" d="M24 28v-6a8 8 0 0 1 16 0v6"/>`,
  key: `
    <circle class="wire" cx="22" cy="32" r="10"/>
    <path class="wire" d="M32 32h22v6M46 32v8M52 32v8"/>`,
  flag: `
    <path class="wire" d="M18 10v44"/>
    <path class="wire" d="M18 12h26l-6 10 6 10H18z"/>`,
  test: `
    <circle class="wire" cx="32" cy="32" r="18"/>
    <path class="wire" d="M22 33l7 7 14-16"/>`,
  event: `
    <circle class="wire" cx="32" cy="32" r="6"/>
    <circle class="wire" cx="32" cy="32" r="14"/>
    <circle class="wire" cx="32" cy="32" r="22"/>`,
  token: `
    <rect class="wire" x="10" y="24" width="44" height="16" rx="8"/>
    <circle class="wire" cx="22" cy="32" r="4"/>`,
  mobile: `
    <rect class="wire" x="20" y="8" width="24" height="48" rx="4"/>
    <path class="wire" d="M28 12h8M32 50h0.1"/>`,
  globe: `
    <circle class="wire" cx="32" cy="32" r="18"/>
    <ellipse class="wire" cx="32" cy="32" rx="8" ry="18"/>
    <path class="wire" d="M14 32h36M18 22h28M18 42h28"/>`,
  clock: `
    <circle class="wire" cx="32" cy="32" r="18"/>
    <path class="wire" d="M32 18v14l10 6"/>`,
  filter: `
    <path class="wire" d="M12 16h40L38 32v16l-12-6V32z"/>`,
  branch: `
    <circle class="wire" cx="20" cy="16" r="6"/>
    <circle class="wire" cx="20" cy="48" r="6"/>
    <circle class="wire" cx="46" cy="32" r="6"/>
    <path class="wire" d="M20 22v20M26 16c12 0 14 8 14 16"/>`,
  bucket: `
    <path class="wire" d="M14 20h36l-4 32H18z"/>
    <path class="wire" d="M12 20c0-6 9-10 20-10s20 4 20 10"/>`,
  transform: `
    <rect class="wire" x="18" y="18" width="28" height="28" rx="4"/>
    <path class="wire" d="M8 32h10M46 32h10"/>
    <path class="wire" d="M52 26l6 6-6 6"/>`,
};

const GLYPHS = Object.keys(ICONS);

function svg(name) {
  return `<svg viewBox="0 0 64 64" aria-hidden="true">${ICONS[name]}</svg>`;
}

function glyphHTML(name, el) {
  const label = el.getAttribute("label") || name;
  const note = el.getAttribute("note") || "";
  const badge = el.getAttribute("badge") || "";
  return `
    <span class="fig-mark">${svg(name)}</span>
    <span class="fig-label">${escapeHtml(label)}</span>
    ${note ? `<span class="fig-sub">${escapeHtml(note)}</span>` : ""}
    ${badge ? `<span class="fig-chip">${escapeHtml(badge)}</span>` : ""}
  `;
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

class FigGlyph extends HTMLElement {
  static get observedAttributes() {
    return ["label", "tone", "note", "badge"];
  }
  connectedCallback() {
    this.classList.add("fig-glyph");
    this.render();
  }
  attributeChangedCallback() {
    if (this.isConnected) this.render();
  }
  render() {
    const name = this.tagName.toLowerCase().replace("fig-", "");
    this.setAttribute("role", "img");
    this.setAttribute("aria-label", this.getAttribute("label") || name);
    this.innerHTML = glyphHTML(name, this);
  }
}

for (const name of GLYPHS) {
  if (!customElements.get(`fig-${name}`)) {
    customElements.define(`fig-${name}`, class extends FigGlyph {});
  }
}

class FigEdge extends HTMLElement {
  connectedCallback() {
    const label = this.getAttribute("label") || "";
    this.innerHTML = `<span class="fig-shaft"></span>${label ? `<span class="fig-elabel">${escapeHtml(label)}</span>` : ""}`;
  }
}
customElements.define("fig-edge", FigEdge);

class FigMetric extends HTMLElement {
  connectedCallback() {
    const value = this.getAttribute("value") || this.textContent.trim();
    const label = this.getAttribute("label") || "";
    this.innerHTML = `<span class="fig-num">${escapeHtml(value)}</span><span class="fig-mlabel">${escapeHtml(label)}</span>`;
  }
}
customElements.define("fig-metric", FigMetric);

class FigDots extends HTMLElement {
  connectedCallback() {
    const n = Number(this.getAttribute("n") || 8);
    const on = Number(this.getAttribute("on") || 0);
    const label = this.getAttribute("label") || "";
    const dots = Array.from({ length: n }, (_, i) => `<i class="fig-datapoint${i < on ? " on" : ""}"></i>`).join("");
    this.innerHTML = `<div class="fig-dotgrid">${dots}</div>${label ? `<div class="fig-dlabel">${escapeHtml(label)}</div>` : ""}`;
  }
}
customElements.define("fig-dots", FigDots);

class FigLegend extends HTMLElement {
  connectedCallback() {
    if (this.childElementCount) return;
    this.innerHTML = `
      <span><i class="add"></i> added</span>
      <span><i class="rem"></i> removed</span>
      <span><i class="chg"></i> changed</span>
      <span><i class="foc"></i> focus</span>
    `;
  }
}
customElements.define("fig-legend", FigLegend);

class FigDeck extends HTMLElement {
  connectedCallback() {
    if (this._built) return;
    this._built = true;
    this.scenes = [...this.querySelectorAll("fig-scene")];
    if (!this.scenes.length) {
      this.innerHTML = `<div class="fig-empty">No scenes yet. Add <code>&lt;fig-scene&gt;</code> children.</div>`;
      return;
    }
    const title = this.getAttribute("title") || "Change walkthrough";
    const repo = this.getAttribute("repo") || "";
    const pr = this.getAttribute("pr") || "";
    const href = this.getAttribute("href") || (repo && pr ? `https://github.com/${repo}/pull/${pr}` : "");
    const added = this.getAttribute("added");
    const removed = this.getAttribute("removed");
    const files = this.getAttribute("files");

    const shell = document.createElement("div");
    shell.className = "fig-shell";

    const mast = document.createElement("div");
    mast.className = "fig-mast";
    mast.innerHTML = `
      <div>
        <p class="fig-kicker">Figure · PR walk</p>
        <h1>${escapeHtml(title)}</h1>
        <div class="fig-repo">${href ? `<a href="${escapeHtml(href)}">${escapeHtml(repo)} #${escapeHtml(pr)}</a>` : escapeHtml(repo)}</div>
      </div>
      <div class="fig-mast-side">
        ${added != null ? `<span class="fig-stat" data-kind="added">+${escapeHtml(added)}</span>` : ""}
        ${removed != null ? `<span class="fig-stat" data-kind="removed">−${escapeHtml(removed)}</span>` : ""}
        ${files != null ? `<span class="fig-stat">${escapeHtml(files)} files</span>` : ""}
      </div>
    `;

    const stage = document.createElement("div");
    stage.className = "fig-stage";

    const head = document.createElement("div");
    head.className = "fig-scene-head";
    head.innerHTML = `<div class="fig-index"></div><div><h2></h2><p></p></div>`;

    const canvas = document.createElement("div");
    canvas.className = "fig-canvas";

    for (const scene of this.scenes) {
      canvas.appendChild(scene);
    }

    stage.append(head, canvas);

    const nav = document.createElement("div");
    nav.className = "fig-nav";
    nav.innerHTML = `
      <button class="fig-btn fig-prev" type="button">Back</button>
      <div class="fig-dots-nav"></div>
      <button class="fig-btn fig-next" type="button">Next</button>
    `;

    shell.append(mast, stage, nav);

    this.replaceChildren(shell);

    this._head = head;
    this._prev = nav.querySelector(".fig-prev");
    this._next = nav.querySelector(".fig-next");
    this._dots = nav.querySelector(".fig-dots-nav");
    this.scenes.forEach((_, i) => {
      const b = document.createElement("button");
      b.className = "fig-dot";
      b.type = "button";
      b.setAttribute("aria-label", `Scene ${i + 1}`);
      b.addEventListener("click", () => this.go(i));
      this._dots.appendChild(b);
    });

    this._prev.addEventListener("click", () => this.go(this.index - 1));
    this._next.addEventListener("click", () => this.go(this.index + 1));
    this.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "n") this.go(this.index + 1);
      if (e.key === "ArrowLeft" || e.key === "p") this.go(this.index - 1);
    });
    this.tabIndex = 0;

    const fromHash = Number((location.hash.match(/s=(\d+)/) || [])[1]);
    this.go(Number.isFinite(fromHash) && fromHash > 0 ? fromHash - 1 : 0);
  }

  go(i) {
    const max = this.scenes.length - 1;
    this.index = Math.max(0, Math.min(max, i));
    this.scenes.forEach((scene, n) => scene.classList.toggle("fig-active", n === this.index));
    const scene = this.scenes[this.index];
    const title = scene.getAttribute("title") || `Scene ${this.index + 1}`;
    const caption = scene.getAttribute("caption") || "";
    this._head.querySelector(".fig-index").textContent = String(this.index + 1).padStart(2, "0");
    this._head.querySelector("h2").textContent = title;
    this._head.querySelector("p").textContent = caption;
    this._prev.disabled = this.index === 0;
    this._next.disabled = this.index === max;
    this._next.textContent = this.index === max ? "Done" : "Next";
    [...this._dots.children].forEach((dot, n) => dot.setAttribute("aria-current", n === this.index ? "true" : "false"));
    this.setAttribute("data-active", String(this.index));
    history.replaceState(null, "", `#s=${this.index + 1}`);
  }
}

customElements.define("fig-deck", FigDeck);

window.Figure = { glyphs: GLYPHS };
