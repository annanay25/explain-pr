#!/usr/bin/env python3
"""Emit figure.css with inlined woff2 fonts and SVG glyph icons."""
from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
OUT = ROOT / "figure.css"

# Distinct silhouettes. Kind names are used as .fig-{name} and data-kind="{name}".
ICONS = {
    "user": '<circle cx="32" cy="18" r="8"/><path d="M12 52c3-14 10-20 20-20s17 6 20 20"/>',
    "users": '<circle cx="24" cy="18" r="7"/><path d="M8 52c3-13 9-18 16-18s13 5 16 18"/><circle cx="44" cy="20" r="6"/><path d="M32 52c2-11 7-16 13-16s12 5 14 16"/>',
    "server": '<rect x="12" y="10" width="40" height="13" rx="2"/><rect x="12" y="26" width="40" height="13" rx="2"/><rect x="12" y="42" width="40" height="13" rx="2"/><circle fill="#1a1714" stroke="none" cx="20" cy="16.5" r="1.8"/><circle fill="#1a1714" stroke="none" cx="20" cy="32.5" r="1.8"/><circle fill="#1a1714" stroke="none" cx="20" cy="48.5" r="1.8"/>',
    "db": '<ellipse cx="32" cy="16" rx="16" ry="7"/><path d="M16 16v26c0 4 7 8 16 8s16-4 16-8V16"/><path d="M16 28c0 4 7 7 16 7s16-3 16-7"/><path d="M16 38c0 4 7 7 16 7s16-3 16-7"/>',
    "box": '<rect x="12" y="12" width="40" height="40" rx="6"/><path d="M32 12v40M12 32h40"/>',
    "file": '<path d="M20 10h16l12 12v32H20z"/><path d="M36 10v12h12"/><path d="M26 34h16M26 42h12"/>',
    "folder": '<path d="M10 20h14l6 6h24v24H10z"/><path d="M10 26h44"/>',
    "cloud": '<path d="M18 42h26a10 10 0 0 0 2-20 14 14 0 0 0-27-3A10 10 0 0 0 18 42z"/>',
    "cache": '<path d="M32 8 52 20v24L32 56 12 44V20z"/><circle cx="32" cy="32" r="8"/>',
    "queue": '<rect x="8" y="18" width="20" height="28" rx="3"/><rect x="22" y="14" width="20" height="28" rx="3"/><rect x="36" y="10" width="20" height="28" rx="3"/>',
    "api": '<path d="M32 8 54 32 32 56 10 32z"/><circle cx="32" cy="32" r="6"/>',
    "browser": '<rect x="10" y="12" width="44" height="40" rx="4"/><path d="M10 22h44"/><circle fill="#1a1714" stroke="none" cx="18" cy="17" r="1.5"/><circle fill="#1a1714" stroke="none" cx="24" cy="17" r="1.5"/>',
    "worker": '<circle cx="32" cy="32" r="10"/><path d="M32 12v8M32 44v8M12 32h8M44 32h8M18 18l6 6M40 40l6 6M46 18l-6 6M24 40l-6 6"/>',
    "lock": '<rect x="18" y="28" width="28" height="22" rx="3"/><path d="M24 28v-6a8 8 0 0 1 16 0v6"/>',
    "key": '<circle cx="22" cy="32" r="10"/><path d="M32 32h22v6M46 32v8M52 32v8"/>',
    "flag": '<path d="M18 10v44"/><path d="M18 12h26l-6 10 6 10H18z"/>',
    "test": '<circle cx="32" cy="32" r="18"/><path d="M22 33l7 7 14-16"/>',
    "event": '<circle cx="32" cy="32" r="6"/><circle cx="32" cy="32" r="14"/><circle cx="32" cy="32" r="22"/>',
    "token": '<rect x="10" y="24" width="44" height="16" rx="8"/><circle cx="22" cy="32" r="4"/>',
    "mobile": '<rect x="20" y="8" width="24" height="48" rx="4"/><path d="M28 12h8"/>',
    "globe": '<circle cx="32" cy="32" r="18"/><ellipse cx="32" cy="32" rx="8" ry="18"/><path d="M14 32h36M18 22h28M18 42h28"/>',
    "clock": '<circle cx="32" cy="32" r="18"/><path d="M32 18v14l10 6"/>',
    "filter": '<path d="M12 16h40L38 32v16l-12-6V32z"/>',
    "branch": '<circle cx="20" cy="16" r="6"/><circle cx="20" cy="48" r="6"/><circle cx="46" cy="32" r="6"/><path d="M20 22v20M26 16c12 0 14 8 14 16"/>',
    "bucket": '<path d="M14 20h36l-4 32H18z"/><path d="M12 20c0-6 9-10 20-10s20 4 20 10"/>',
    "transform": '<rect x="18" y="18" width="28" height="28" rx="4"/><path d="M8 32h10M46 32h10"/><path d="M52 26l6 6-6 6"/>',
    "babel": '<path d="M20 14c-8 0-8 10-8 18s0 18 8 18M44 14c8 0 8 10 8 18s0 18-8 18"/><path d="M28 22h8M28 32h8M28 42h8"/>',
    "oxc": '<path d="M22 38 34 10l4 16 12-4L32 56l-4-16z"/>',
    "swc": '<path d="M12 32h22"/><path d="M26 22l16 10-16 10"/><path d="M36 18l16 14-16 14"/>',
    "rust": '<path d="M32 8 54 20v24L32 56 10 44V20z"/><circle cx="32" cy="32" r="8"/><path d="M32 18v6M32 40v6M18 32h6M40 32h6"/>',
    "compiler": '<rect x="6" y="22" width="14" height="20" rx="2"/><rect x="44" y="22" width="14" height="20" rx="2"/><circle cx="32" cy="32" r="11"/><path d="M21 32h22"/>',
    "parser": '<path d="M10 16h18M10 24h18M10 32h12"/><circle cx="44" cy="18" r="5"/><circle cx="34" cy="46" r="5"/><circle cx="54" cy="46" r="5"/><path d="M44 23v12M44 35l-8 6M44 35l8 6"/>',
    "ast": '<circle cx="32" cy="12" r="6"/><circle cx="32" cy="32" r="5"/><circle cx="14" cy="50" r="6"/><circle cx="50" cy="50" r="6"/><path d="M32 18v9M29 36 17 46M35 36 47 46"/>',
    "ir": '<rect x="10" y="14" width="44" height="10" rx="2"/><rect x="10" y="28" width="28" height="10" rx="2"/><rect x="10" y="42" width="36" height="10" rx="2"/>',
    "hir": '<rect x="8" y="14" width="20" height="14" rx="2"/><rect x="36" y="14" width="20" height="14" rx="2"/><rect x="22" y="38" width="20" height="14" rx="2"/><path d="M18 28v6c0 4 8 4 12 4M46 28v6c0 4-8 4-12 4"/>',
    "plugin": '<rect x="10" y="10" width="26" height="26" rx="4"/><rect x="28" y="28" width="26" height="26" rx="4"/><circle cx="23" cy="23" r="3"/><circle cx="41" cy="41" r="3"/>',
    "env": '<rect x="18" y="10" width="34" height="20" rx="3"/><rect x="12" y="22" width="34" height="20" rx="3"/><rect x="6" y="34" width="34" height="20" rx="3"/>',
    "scan": '<circle cx="28" cy="28" r="14"/><path d="M38 38l14 14"/><path d="M28 20v10h10"/>',
    "crate": '<path d="M12 22 32 12 52 22 52 44 32 54 12 44z"/><path d="M12 22 32 32 52 22M32 32v22"/>',
    "wasm": '<path d="M32 8 54 21v22L32 56 10 43V21z"/><path d="M32 22v20M22 28h20"/>',
    "hook": '<circle cx="22" cy="12" r="5"/><path d="M22 17v22a12 12 0 1 0 24 0V30"/>',
    "runtime": '<path d="M32 8 54 21v22L32 56 10 43V21z"/><path d="M26 22 44 32 26 42z"/>',
    "doc": '<rect x="14" y="8" width="36" height="48" rx="3"/><path d="M22 20h20M22 28h20M22 36h14"/>',
    "term": '<rect x="8" y="14" width="48" height="36" rx="4"/><path d="M8 24h48"/><path d="M16 34l7 5-7 5M28 44h14"/>',
    "fallback": '<path d="M20 10h16l12 12v32H20z" stroke-dasharray="4 3"/><path d="M36 10v12h12" stroke-dasharray="4 3"/>',
    "route": '<circle cx="12" cy="32" r="5"/><circle cx="52" cy="16" r="5"/><circle cx="52" cy="48" r="5"/><path d="M17 32h12M29 32c8 0 8-16 18-16M29 32c8 0 8 16 18 16"/>',
    "module": '<rect x="10" y="10" width="18" height="18" rx="3"/><rect x="36" y="10" width="18" height="18" rx="3"/><rect x="10" y="36" width="18" height="18" rx="3"/><rect x="36" y="36" width="18" height="18" rx="3"/>',
    "graph": '<circle cx="16" cy="18" r="6"/><circle cx="48" cy="18" r="6"/><circle cx="18" cy="48" r="6"/><circle cx="48" cy="46" r="6"/><path d="M22 18h20M19 24l2 18M46 24l1 16M24 48h18"/>',
    "css": '<path d="M18 16h28M18 32h28M18 48h28M26 10v44M38 10v44"/>',
    "js": '<path d="M22 14c-10 0-10 10-10 18s0 18 10 18M42 14c10 0 10 10 10 18s0 18-10 18"/>',
    "snippet": '<path d="M26 18 14 32 26 46M38 18 50 32 38 46M36 16 28 48"/>',
    "html": '<path d="M24 16 10 32 24 48M40 16 54 32 40 48"/>',
    "stream": '<path d="M8 22c8 0 8 20 16 20s8-20 16-20 8 20 16 20"/><path d="M8 42c8 0 8-20 16-20s8 20 16 20 8-20 16-20"/>',
    "arena": '<rect x="10" y="10" width="44" height="44" rx="3"/><path d="M10 32h44M32 10v44M10 21h44M10 43h44M21 10v44M43 10v44"/>',
    "bundler": '<rect x="14" y="24" width="16" height="16" rx="1"/><rect x="34" y="24" width="16" height="16" rx="1"/><rect x="24" y="12" width="16" height="16" rx="1"/><rect x="24" y="36" width="16" height="16" rx="1"/>',
    "adapter": '<rect x="6" y="24" width="18" height="16" rx="2"/><rect x="40" y="24" width="18" height="16" rx="2"/><path d="M24 32h16"/><circle cx="20" cy="32" r="2.2"/><circle cx="44" cy="32" r="2.2"/>',
    "snapshot": '<rect x="18" y="16" width="30" height="36" rx="2"/><rect x="12" y="10" width="30" height="36" rx="2"/><path d="M18 22h18M18 30h12"/>',
    "tree": '<circle cx="32" cy="12" r="6"/><circle cx="14" cy="50" r="6"/><circle cx="50" cy="50" r="6"/><path d="M32 18v14M32 32 17 46M32 32 47 46"/>',
    "config": '<path d="M14 20h36M14 32h36M14 44h36"/><circle cx="24" cy="20" r="4"/><circle cx="42" cy="32" r="4"/><circle cx="28" cy="44" r="4"/>',
    "log": '<path d="M14 16h36M14 28h36M14 40h26M14 50h30"/>',
    "error": '<path d="M32 10 54 50H10z"/><path d="M32 26v14M32 46v.5"/>',
    "request": '<path d="M8 32h40"/><path d="M38 22l16 10-16 10"/><rect x="8" y="26" width="8" height="12" rx="1"/>',
    "response": '<path d="M56 32H16"/><path d="M26 22 10 32l16 10"/><rect x="48" y="26" width="8" height="12" rx="1"/>',
    "client": '<rect x="10" y="12" width="44" height="28" rx="3"/><path d="M24 40v6M40 40v6M20 52h24"/>',
    "package": '<path d="M12 22 32 12 52 22v24L32 56 12 46z"/><path d="M12 22h40M32 12v44"/>',
    "build": '<rect x="10" y="40" width="14" height="12" rx="1"/><rect x="26" y="40" width="14" height="12" rx="1"/><rect x="42" y="40" width="12" height="12" rx="1"/><rect x="18" y="26" width="14" height="12" rx="1"/><rect x="34" y="26" width="14" height="12" rx="1"/><rect x="26" y="12" width="14" height="12" rx="1"/>',
    "pipeline": '<rect x="6" y="24" width="14" height="16" rx="2"/><rect x="25" y="24" width="14" height="16" rx="2"/><rect x="44" y="24" width="14" height="16" rx="2"/><path d="M20 32h5M39 32h5"/>',
}


def font_face(family: str, weight: int, filename: str) -> str:
    b64 = base64.b64encode((FONTS / filename).read_bytes()).decode("ascii")
    return (
        f"@font-face {{\n"
        f'  font-family: "{family}";\n'
        f"  font-style: normal;\n"
        f"  font-weight: {weight};\n"
        f"  font-display: swap;\n"
        f'  src: url("data:font/woff2;base64,{b64}") format("woff2");\n'
        f"}}\n"
    )


def icon_url(inner: str) -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" '
        'stroke="#1a1714" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        f"{inner}</svg>"
    )
    return "data:image/svg+xml," + quote(svg, safe="")


def comma(template: str) -> str:
    return ", ".join(template.replace("{n}", n) for n in ICONS)


glyph = comma(".fig-{n}")
glyph_before = comma(".fig-{n}::before")
glyph_after = comma(".fig-{n}::after")
glyph_note_after = comma(".fig-{n}[data-note]::after")

icon_rules = "".join(
    (
        f'.fig-{name}::before,\n'
        f'.fig-node[data-kind="{name}"] > summary > .fig-mark,\n'
        f'.fig-mark[data-kind="{name}"] {{\n'
        f'  background-image: url("{icon_url(inner)}");\n'
        f"}}\n"
    )
    for name, inner in ICONS.items()
)

scene_bits = [
    ".fig-view { display: none; }",
    '.fig-deck:has(#view-story:checked) .fig-view[data-view="story"] { display: block; }',
    '.fig-deck:has(#view-data:checked) .fig-view[data-view="data"] { display: block; }',
    '.fig-deck:has(#view-blast:checked) .fig-view[data-view="blast"] { display: block; }',
    ".fig-view:not(:has(input[type=radio]:checked)) .fig-scene:nth-of-type(1) { display: flex; }",
    ".fig-deck:not(:has(.fig-view)):not(:has(input:checked)) .fig-scene:nth-of-type(1) { display: flex; }",
]
for i in range(1, 9):
    scene_bits.append(
        f".fig-deck:not(:has(.fig-view)):has(#s{i}:checked) .fig-scene:nth-of-type({i}) {{ display: flex; }}"
    )
    for prefix in ("s", "d", "b"):
        scene_bits.append(
            f".fig-view:has(#{prefix}{i}:checked) .fig-scene:nth-of-type({i}) {{ display: flex; }}"
        )
scene_rules = "\n".join(scene_bits)

tone_before = {}
for tone in ("added", "removed", "changed", "focus", "ghost"):
    tone_before[tone] = (
        comma(f'.fig-{{n}}[data-tone="{tone}"]::before')
        + f', .fig-node[data-tone="{tone}"] > summary > .fig-mark'
        + f', .fig-glyph[data-tone="{tone}"] > .fig-mark'
    )

fonts = "".join(
    [
        font_face("Fraunces", 500, "fraunces.woff2"),
        font_face("Fraunces", 600, "fraunces-600.woff2"),
        font_face("IBM Plex Sans", 400, "ibm-plex-sans.woff2"),
        font_face("IBM Plex Sans", 500, "ibm-plex-sans-500.woff2"),
        font_face("IBM Plex Sans", 600, "ibm-plex-sans-600.woff2"),
        font_face("IBM Plex Mono", 400, "ibm-plex-mono.woff2"),
        font_face("IBM Plex Mono", 500, "ibm-plex-mono-500.woff2"),
    ]
)

css = fonts + f"""
:root {{
  --fig-paper: #f3efe6;
  --fig-paper-2: #ebe4d6;
  --fig-ink: #1a1714;
  --fig-muted: #6f675e;
  --fig-rule: #d8cfc2;
  --fig-added: #1b6b48;
  --fig-added-bg: #d6efe3;
  --fig-removed: #b42318;
  --fig-removed-bg: #f8ddd8;
  --fig-changed: #9a5b00;
  --fig-changed-bg: #f6e3b8;
  --fig-focus: #1e4d8c;
  --fig-focus-bg: #d7e4f5;
  --fig-ghost: #a39a8e;
  --fig-shadow: 0 18px 40px rgba(26, 23, 20, 0.08);
  --fig-radius: 18px;
}}

* {{ box-sizing: border-box; }}
html, body {{
  margin: 0;
  min-height: 100%;
  background:
    radial-gradient(circle at 1px 1px, rgba(26, 23, 20, 0.05) 1px, transparent 0) 0 0 / 22px 22px,
    var(--fig-paper);
  color: var(--fig-ink);
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif;
}}
body.fig-page {{ min-height: 100vh; }}

.fig-deck {{
  display: block;
  max-width: 1120px;
  margin: 32px auto;
  padding: 0 20px 48px;
  position: relative;
}}
.fig-deck input[type="radio"] {{
  appearance: none;
  -webkit-appearance: none;
  position: fixed;
  left: 0;
  top: 0;
  width: 0;
  height: 0;
  margin: 0;
  padding: 0;
  border: 0;
  opacity: 0;
  pointer-events: none;
}}
.fig-shell {{
  background: rgba(255, 252, 247, 0.92);
  border: 1px solid var(--fig-rule);
  border-radius: var(--fig-radius);
  box-shadow: var(--fig-shadow);
  overflow: hidden;
}}
.fig-mast {{
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  padding: 22px 28px 18px;
  border-bottom: 1px solid var(--fig-rule);
  background: linear-gradient(180deg, #fffaf2, transparent);
}}
.fig-kicker {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--fig-muted);
  margin: 0 0 6px;
}}
.fig-mast h1 {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: clamp(22px, 3vw, 32px);
  font-weight: 550;
  letter-spacing: -0.03em;
  margin: 0;
  line-height: 1.15;
}}
.fig-repo {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12px;
  color: var(--fig-muted);
  margin-top: 8px;
}}
.fig-repo a {{ color: inherit; text-decoration: none; border-bottom: 1px solid var(--fig-rule); }}
.fig-mast-side {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }}
.fig-stat {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--fig-rule);
  background: #fff;
}}
.fig-stat.added {{ color: var(--fig-added); border-color: color-mix(in srgb, var(--fig-added) 35%, white); background: var(--fig-added-bg); }}
.fig-stat.removed {{ color: var(--fig-removed); border-color: color-mix(in srgb, var(--fig-removed) 35%, white); background: var(--fig-removed-bg); }}
.fig-inspect-hint {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  color: var(--fig-muted);
  margin-top: 10px;
}}
.fig-view-tabs {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 28px 0;
  background: #fffaf2;
}}
.fig-view-tab {{
  font-family: "IBM Plex Sans", ui-sans-serif, sans-serif;
  font-size: 13px;
  font-weight: 550;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid var(--fig-rule);
  background: #fff;
  cursor: pointer;
  color: var(--fig-ink);
}}
.fig-view-tab:hover {{ border-color: var(--fig-ink); }}
.fig-deck:has(#view-story:checked) .fig-view-tab[for="view-story"],
.fig-deck:has(#view-data:checked) .fig-view-tab[for="view-data"],
.fig-deck:has(#view-blast:checked) .fig-view-tab[for="view-blast"] {{
  background: var(--fig-ink);
  color: var(--fig-paper);
  border-color: var(--fig-ink);
}}
.fig-view-tab small {{
  display: block;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 10px;
  font-weight: 400;
  letter-spacing: 0.04em;
  opacity: 0.72;
  margin-top: 1px;
}}

.fig-scene {{
  display: none;
  flex-direction: column;
  min-height: 420px;
}}
{scene_rules}

.fig-stage {{
  flex: 1;
  padding: 24px 28px 10px;
  display: flex;
  flex-direction: column;
}}
.fig-scene-head {{
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: start;
  margin-bottom: 12px;
}}
.fig-index {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  border: 1px solid var(--fig-ink);
  background: var(--fig-ink);
  color: var(--fig-paper);
}}
.fig-scene-head h2 {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: clamp(20px, 2.4vw, 28px);
  margin: 0 0 6px;
  letter-spacing: -0.03em;
  font-weight: 550;
}}
.fig-scene-head p {{
  margin: 0;
  color: var(--fig-muted);
  line-height: 1.45;
  max-width: 68ch;
}}
.fig-canvas {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 16px;
  padding: 12px 0 12px;
}}
.fig-nav {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 0 -28px 4px;
  padding: 10px 28px 12px;
  border-top: 1px solid var(--fig-rule);
  border-bottom: 1px solid var(--fig-rule);
  background: #faf6ee;
  flex-shrink: 0;
}}
.fig-dots-nav {{ display: flex; gap: 7px; flex-wrap: wrap; justify-content: center; }}
.fig-dot {{
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--fig-rule);
  cursor: pointer;
  display: inline-block;
}}
.fig-dot.is-current {{ background: var(--fig-ink); transform: scale(1.2); }}
.fig-btn {{
  font-family: "IBM Plex Sans", ui-sans-serif, sans-serif;
  font-size: 14px;
  font-weight: 550;
  border: 1px solid var(--fig-ink);
  background: #fff;
  color: var(--fig-ink);
  border-radius: 999px;
  padding: 10px 16px;
  min-width: 96px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  display: inline-block;
}}
label.fig-btn {{ cursor: pointer; }}
.fig-btn:hover {{ background: var(--fig-paper-2); }}
.fig-btn.is-disabled {{ opacity: 0.35; cursor: default; pointer-events: none; }}
.fig-btn.fig-next {{ background: var(--fig-ink); color: var(--fig-paper); }}
.fig-btn.fig-next:hover {{ background: #2b2622; }}

.fig-row, .fig-col, .fig-cluster, .fig-compare, .fig-stack, .fig-pipe, .fig-timeline {{ display: flex; }}
.fig-row, .fig-pipe {{
  flex-direction: row;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px 10px;
}}
.fig-row:has(details[open]) {{ align-items: flex-start; }}
.fig-col, .fig-stack {{ flex-direction: column; align-items: center; gap: 10px; }}
.fig-cluster {{
  flex-direction: column;
  align-items: stretch;
  gap: 14px;
  border: 1.5px dashed var(--fig-rule);
  border-radius: 16px;
  padding: 22px 16px 14px;
  position: relative;
  min-width: min(100%, 220px);
  background: rgba(255,255,255,0.35);
}}
.fig-cluster::before {{
  content: attr(data-label);
  position: absolute;
  top: -10px;
  left: 14px;
  background: #fffaf2;
  padding: 0 8px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.fig-compare {{ gap: 18px; align-items: stretch; justify-content: center; flex-wrap: wrap; }}
.fig-pane {{
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex: 1 1 280px;
  border: 1px solid var(--fig-rule);
  border-radius: 14px;
  padding: 16px 14px 14px;
  background: #fff;
}}
.fig-pane::before {{
  content: attr(data-label);
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.fig-pane[data-tone="added"] {{ background: color-mix(in srgb, var(--fig-added-bg) 55%, white); }}
.fig-pane[data-tone="removed"] {{ background: color-mix(in srgb, var(--fig-removed-bg) 50%, white); }}
.fig-pane[data-tone="changed"] {{ background: color-mix(in srgb, var(--fig-changed-bg) 50%, white); }}
.fig-layer {{
  display: block;
  width: min(280px, 100%);
  border: 1.5px solid var(--fig-ink);
  border-radius: 10px;
  padding: 11px 14px;
  text-align: center;
  font-weight: 500;
  background: #fff;
}}
.fig-stack .fig-layer:nth-child(even) {{ transform: translateX(10px); }}
.fig-stack .fig-layer:nth-child(odd) {{ transform: translateX(-6px); }}
.fig-phase {{
  min-width: 92px;
  text-align: center;
  border: 1.5px solid currentColor;
  border-radius: 12px;
  padding: 12px 10px;
  background: #fff;
  font-size: 13px;
  font-weight: 500;
}}
.fig-timeline {{ align-items: center; justify-content: center; gap: 0; flex-wrap: wrap; }}
.fig-step {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 108px;
  position: relative;
  padding: 0 12px;
  font-size: 13px;
  text-align: center;
}}
.fig-step::before {{
  content: "";
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid var(--fig-ink);
  background: #fff;
}}
.fig-step:not(:last-child)::after {{
  content: "";
  position: absolute;
  top: 6px;
  left: calc(50% + 14px);
  width: calc(100% - 28px);
  height: 2px;
  background: var(--fig-rule);
}}

{glyph} {{
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 84px;
  color: var(--fig-ink);
  position: relative;
  font-size: 12.5px;
  font-weight: 500;
  text-align: center;
}}
{glyph_before} {{
  content: "";
  width: 64px;
  height: 64px;
  border-radius: 18px;
  border: 1px solid var(--fig-rule);
  background-color: #fff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 42px;
}}
{glyph_after} {{
  content: attr(data-label);
  max-width: 110px;
  line-height: 1.25;
}}
{glyph_note_after} {{
  content: attr(data-label) "\\A" attr(data-note);
  white-space: pre-line;
}}
ICON_RULES_HERE
[data-tone="added"] {{ color: var(--fig-added); }}
[data-tone="removed"] {{ color: var(--fig-removed); }}
[data-tone="changed"] {{ color: var(--fig-changed); }}
[data-tone="focus"] {{ color: var(--fig-focus); }}
[data-tone="ghost"] {{ color: var(--fig-ghost); opacity: 0.72; }}
{tone_before["added"]} {{ background-color: var(--fig-added-bg); border-color: color-mix(in srgb, var(--fig-added) 35%, white); }}
{tone_before["removed"]} {{ background-color: var(--fig-removed-bg); border-color: color-mix(in srgb, var(--fig-removed) 35%, white); }}
{tone_before["changed"]} {{ background-color: var(--fig-changed-bg); border-color: color-mix(in srgb, var(--fig-changed) 35%, white); }}
{tone_before["focus"]} {{ background-color: var(--fig-focus-bg); border-color: color-mix(in srgb, var(--fig-focus) 35%, white); }}
{tone_before["ghost"]} {{ background-color: transparent; border-style: dashed; }}
.fig-layer[data-tone="added"], .fig-phase[data-tone="added"] {{ background: var(--fig-added-bg); }}
.fig-layer[data-tone="removed"], .fig-phase[data-tone="removed"] {{ background: var(--fig-removed-bg); }}
.fig-layer[data-tone="changed"], .fig-phase[data-tone="changed"] {{ background: var(--fig-changed-bg); }}
.fig-layer[data-tone="focus"], .fig-phase[data-tone="focus"] {{ background: var(--fig-focus-bg); }}
.fig-layer[data-tone="ghost"] {{ background: transparent; border-style: dashed; }}
.fig-step[data-tone="added"]::before {{ background: var(--fig-added); border-color: var(--fig-added); }}
.fig-step[data-tone="removed"]::before {{ background: var(--fig-removed); border-color: var(--fig-removed); }}
.fig-step[data-tone="changed"]::before {{ background: var(--fig-changed); border-color: var(--fig-changed); }}
.fig-step[data-tone="focus"]::before {{ background: var(--fig-focus); border-color: var(--fig-focus); }}

.fig-mark {{
  width: 48px;
  height: 48px;
  flex: 0 0 48px;
  border-radius: 14px;
  border: 1px solid var(--fig-rule);
  background-color: #fff;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 30px;
  display: inline-block;
}}
.fig-glyph {{
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 84px;
  font-size: 12.5px;
  font-weight: 500;
  text-align: center;
  position: relative;
}}

.fig-node {{
  display: inline-flex;
  flex-direction: column;
  align-items: stretch;
  width: 248px;
  max-width: 100%;
  background: #fffaf2;
  border: 1px solid var(--fig-rule);
  border-radius: 16px;
  box-shadow: 0 8px 22px rgba(26, 23, 20, 0.05);
  color: var(--fig-ink);
  opacity: 1;
  position: relative;
  text-align: left;
}}
.fig-node.tight {{ width: 168px; }}
.fig-node.wide {{
  width: min(100%, 720px);
  flex: 1 1 100%;
}}
.fig-node > summary {{
  display: grid;
  grid-template-columns: 48px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 12px 12px 12px 12px;
  cursor: pointer;
  list-style: none;
  border-radius: 16px;
}}
.fig-node > summary::-webkit-details-marker,
.fig-fold > summary::-webkit-details-marker {{ display: none; }}
.fig-node > summary::marker,
.fig-fold > summary::marker {{ content: ""; }}
.fig-node > summary:hover {{ background: #fff6ea; }}
.fig-node > summary:focus-visible,
.fig-fold > summary:focus-visible {{
  outline: 2px solid var(--fig-ink);
  outline-offset: -2px;
}}
.fig-node[open] > summary {{
  border-bottom: 1px solid var(--fig-rule);
  border-radius: 16px 16px 0 0;
}}
.fig-node-text {{
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}}
.fig-node-text em {{
  font-style: normal;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.fig-node-text strong {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.03em;
  color: var(--fig-ink);
}}
.fig-node-text span {{
  font-size: 12px;
  line-height: 1.35;
  color: var(--fig-muted);
}}
.fig-node.tight .fig-node-text em,
.fig-node.tight .fig-node-text span {{ display: none; }}
.fig-node.tight > summary {{ grid-template-columns: 40px 1fr auto; padding: 10px; }}
.fig-node.tight .fig-mark {{ width: 40px; height: 40px; flex-basis: 40px; border-radius: 12px; }}
.fig-node-go {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--fig-muted);
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  align-self: stretch;
  display: grid;
  place-items: center;
}}
.fig-node-go::before {{ content: "Ask"; }}
.fig-node[open] > summary .fig-node-go::before {{ content: "Close"; }}
.fig-node-panel {{
  padding: 12px 14px 14px;
  font-size: 13.5px;
  line-height: 1.5;
  color: #3f3a34;
}}
.fig-node-panel p {{ margin: 0 0 10px; }}
.fig-node-panel p:last-child {{ margin-bottom: 0; }}
.fig-node-panel .fig-code {{
  width: 100%;
  margin: 8px 0 0;
}}
.fig-node-panel .fig-node {{
  width: 100%;
  margin-top: 10px;
}}
.fig-node[data-tone="added"] {{ border-color: color-mix(in srgb, var(--fig-added) 35%, var(--fig-rule)); }}
.fig-node[data-tone="removed"] {{ border-color: color-mix(in srgb, var(--fig-removed) 35%, var(--fig-rule)); }}
.fig-node[data-tone="changed"] {{ border-color: color-mix(in srgb, var(--fig-changed) 35%, var(--fig-rule)); }}
.fig-node[data-tone="focus"] {{ border-color: color-mix(in srgb, var(--fig-focus) 35%, var(--fig-rule)); }}
.fig-node[data-tone="ghost"] {{ opacity: 0.78; border-style: dashed; }}

.fig-fold {{
  border: 1px solid var(--fig-rule);
  border-radius: 10px;
  background: #fff;
  margin: 8px 0 0;
}}
.fig-fold > summary {{
  cursor: pointer;
  padding: 9px 12px;
  font-weight: 550;
  font-size: 13px;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.fig-fold > summary::before {{
  content: "";
  width: 7px;
  height: 7px;
  border-right: 1.6px solid currentColor;
  border-bottom: 1.6px solid currentColor;
  transform: rotate(-45deg);
  flex: 0 0 auto;
}}
.fig-fold[open] > summary::before {{ transform: rotate(45deg); }}
.fig-fold > :not(summary) {{
  padding: 0 12px 12px;
  font-size: 13px;
  line-height: 1.5;
  color: #3f3a34;
}}
.fig-fold .fig-fold {{ margin-top: 8px; }}

.fig-chip {{
  position: absolute;
  top: -8px;
  right: 4px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 10px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 999px;
  border: 1px solid currentColor;
  background: #fff;
  z-index: 1;
}}
.fig-node .fig-chip {{
  top: 8px;
  right: 28px;
}}

.fig-ask {{
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--fig-rule);
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.fig-ask-label {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.fig-ask-q, .fig-ask-prompt {{
  width: 100%;
  border: 1px solid var(--fig-rule);
  border-radius: 10px;
  font-family: "IBM Plex Sans", ui-sans-serif, sans-serif;
  font-size: 13px;
  line-height: 1.45;
  padding: 10px 12px;
  background: #fff;
  color: var(--fig-ink);
  resize: vertical;
}}
.fig-ask-q {{ min-height: 72px; }}
.fig-ask-prompt {{
  min-height: 140px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  line-height: 1.45;
  background: #1a1714;
  color: #f3efe6;
  border-color: #1a1714;
}}
.fig-ask .fig-btn {{ align-self: flex-start; min-width: 0; }}
.fig-ask .fig-btn.is-copied {{ background: var(--fig-added-bg); color: var(--fig-added); border-color: var(--fig-added); }}

.fig-risk {{
  width: 220px;
  max-width: 100%;
  border: 1px solid var(--fig-rule);
  border-radius: 14px;
  padding: 12px 14px;
  background: #fff;
  text-align: left;
}}
.fig-risk em {{
  display: block;
  font-style: normal;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.fig-risk strong {{
  display: block;
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 18px;
  margin: 4px 0 6px;
  letter-spacing: -0.03em;
}}
.fig-risk span {{ font-size: 12.5px; color: #3f3a34; line-height: 1.4; }}
.fig-risk[data-level="hot"] {{ background: var(--fig-removed-bg); }}
.fig-risk[data-level="watch"] {{ background: var(--fig-changed-bg); }}
.fig-risk[data-level="safe"] {{ background: var(--fig-added-bg); }}

.fig-edge {{
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 56px;
  min-height: 28px;
  color: var(--fig-muted);
}}
.fig-edge::before {{
  content: "";
  width: 48px;
  height: 10px;
  background: currentColor;
  clip-path: polygon(0 4px, 38px 4px, 38px 0, 48px 5px, 38px 10px, 38px 6px, 0 6px);
}}
.fig-edge::after {{
  content: attr(data-label);
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 10px;
  margin-top: 4px;
  max-width: 90px;
  text-align: center;
  line-height: 1.2;
}}
.fig-edge.down {{ min-width: 24px; min-height: 44px; }}
.fig-edge.down::before {{
  width: 10px;
  height: 36px;
  clip-path: polygon(4px 0, 6px 0, 6px 26px, 10px 26px, 5px 36px, 0 26px, 4px 26px);
}}
.fig-edge.strike::before {{
  width: 48px;
  height: 2px;
  clip-path: none;
  background: repeating-linear-gradient(90deg, currentColor 0 6px, transparent 6px 10px);
}}

.fig-code {{
  display: block;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12.5px;
  line-height: 1.55;
  background: #1a1714;
  color: #f3efe6;
  border-radius: 12px;
  padding: 12px 0;
  overflow: auto;
  width: min(100%, 560px);
  margin: 0 auto;
}}
.fig-code::before {{
  content: attr(data-caption);
  display: block;
  color: #b3aa9d;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 0 14px 8px;
}}
.fig-line {{ display: block; padding: 1px 14px; white-space: pre; }}
.fig-line.added {{ background: rgba(46, 160, 90, 0.22); color: #b6ebcc; }}
.fig-line.removed {{ background: rgba(180, 50, 40, 0.22); color: #f5b7b0; text-decoration: line-through; }}
.fig-line.changed {{ background: rgba(196, 130, 20, 0.22); color: #f3d48a; }}

.fig-metric {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 110px;
  padding: 10px;
  font-size: 12px;
  color: var(--fig-muted);
  text-align: center;
  max-width: 160px;
}}
.fig-metric::before {{
  content: attr(data-value);
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 36px;
  letter-spacing: -0.04em;
  line-height: 1;
  color: var(--fig-ink);
}}
.fig-metric[data-tone="added"] {{ color: var(--fig-added); }}
.fig-metric[data-tone="removed"] {{ color: var(--fig-removed); }}
.fig-metric[data-tone="changed"] {{ color: var(--fig-changed); }}
.fig-metric[data-tone="focus"] {{ color: var(--fig-focus); }}
.fig-metric[data-tone="added"]::before {{ color: var(--fig-added); }}
.fig-metric[data-tone="removed"]::before {{ color: var(--fig-removed); }}
.fig-metric[data-tone="changed"]::before {{ color: var(--fig-changed); }}
.fig-metric[data-tone="focus"]::before {{ color: var(--fig-focus); }}

.fig-callout {{
  display: block;
  max-width: 720px;
  margin: 4px auto 0;
  padding: 12px 16px;
  border-left: 3px solid var(--fig-ink);
  background: #fff;
  color: var(--fig-ink);
  font-size: 14px;
  line-height: 1.45;
}}
.fig-callout[data-tone="added"] {{ border-color: var(--fig-added); background: var(--fig-added-bg); }}
.fig-callout[data-tone="removed"] {{ border-color: var(--fig-removed); background: var(--fig-removed-bg); }}
.fig-callout[data-tone="changed"] {{ border-color: var(--fig-changed); background: var(--fig-changed-bg); }}
.fig-callout[data-tone="focus"] {{ border-color: var(--fig-focus); background: var(--fig-focus-bg); }}

.fig-datapoints {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}}
.fig-dotgrid {{ display: flex; flex-wrap: nowrap; gap: 6px; }}
.fig-datapoints::after {{
  content: attr(data-label);
  font-size: 12px;
  color: var(--fig-muted);
}}
.fig-datapoints i {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--fig-rule);
  display: inline-block;
}}
.fig-datapoints i.on {{ background: var(--fig-ink); }}
.fig-datapoints[data-tone="focus"] i.on {{ background: var(--fig-focus); }}
.fig-datapoints[data-tone="added"] i.on {{ background: var(--fig-added); }}

.fig-legend {{
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  justify-content: center;
  font-size: 12px;
  color: var(--fig-muted);
  margin-top: 8px;
}}
.fig-legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
.fig-legend i {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
.fig-legend i.add {{ background: var(--fig-added); }}
.fig-legend i.rem {{ background: var(--fig-removed); }}
.fig-legend i.chg {{ background: var(--fig-changed); }}
.fig-legend i.foc {{ background: var(--fig-focus); }}

.site {{ max-width: 1100px; margin: 0 auto; padding: 36px 20px 80px; }}
.wordmark {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 13px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--fig-muted);
}}
.hero h1 {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: clamp(40px, 7vw, 72px);
  letter-spacing: -0.045em;
  line-height: 0.95;
  margin: 10px 0 16px;
  font-weight: 550;
}}
.hero p {{ max-width: 58ch; font-size: 18px; line-height: 1.5; color: #3f3a34; margin: 0 0 28px; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
.card {{
  display: block;
  text-decoration: none;
  color: inherit;
  background: #fffaf2;
  border: 1px solid var(--fig-rule);
  border-radius: 16px;
  padding: 18px;
  min-height: 180px;
  box-shadow: var(--fig-shadow);
}}
.card:hover {{ border-color: var(--fig-ink); }}
.card .meta {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  color: var(--fig-muted);
  letter-spacing: 0.04em;
}}
.card h3 {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 22px;
  margin: 10px 0 8px;
  letter-spacing: -0.03em;
}}
.card p {{ margin: 0; color: var(--fig-muted); font-size: 14px; line-height: 1.4; }}
.catalog-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 18px; }}
.catalog-item {{
  background: #fffaf2;
  border: 1px solid var(--fig-rule);
  border-radius: 14px;
  padding: 18px 10px 14px;
  text-align: center;
}}
.catalog-item code {{
  display: block;
  margin-top: 8px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  color: var(--fig-muted);
}}
.site h2 {{
  font-family: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
  font-size: 28px;
  margin: 48px 0 16px;
  letter-spacing: -0.03em;
}}
.back {{
  color: var(--fig-ink);
  text-decoration: none;
  font-size: 14px;
  border-bottom: 1px solid var(--fig-rule);
}}
@media (max-width: 700px) {{
  .fig-mast {{ flex-direction: column; padding: 18px 16px 14px; }}
  .fig-stage, .fig-nav {{ padding-left: 16px; padding-right: 16px; }}
  .fig-nav {{ margin-left: -16px; margin-right: -16px; }}
  .fig-scene {{ min-height: 320px; }}
  .fig-btn {{ min-width: 84px; }}
  .fig-deck {{ margin-top: 16px; }}
  .fig-node {{ width: 100%; }}
  .fig-node.tight {{ width: 100%; }}
  .fig-view-tabs {{ padding-left: 16px; padding-right: 16px; }}
}}
"""

OUT.write_text(css.replace("ICON_RULES_HERE", icon_rules))
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
