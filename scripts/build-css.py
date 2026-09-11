#!/usr/bin/env python3
"""Emit figure.css with inlined woff2 fonts and SVG glyph icons."""
from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
OUT = ROOT / "figure.css"

ICONS = {
    "user": '<circle cx="32" cy="20" r="8"/><path d="M14 50c2-12 9-18 18-18s16 6 18 18"/>',
    "users": '<circle cx="24" cy="20" r="7"/><path d="M10 50c2-11 8-16 14-16s12 5 14 16"/><circle cx="42" cy="22" r="6"/><path d="M32 50c1-9 6-14 12-14s11 5 12 14"/>',
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


glyph_list = ", ".join(f".fig-{name}" for name in ICONS)
icon_rules = "".join(
    f'.fig-{name}::before {{ background-image: url("{icon_url(inner)}"); }}\n'
    for name, inner in ICONS.items()
)
scene_rules = "\n".join(
    f".fig-deck:has(#s{i}:checked) .fig-scene:nth-of-type({i}) {{ display: flex; }}"
    for i in range(1, 9)
)

css = f"""{font_face("Fraunces", 500, "fraunces.woff2")}{font_face("Fraunces", 600, "fraunces-600.woff2")}{font_face("IBM Plex Sans", 400, "ibm-plex-sans.woff2")}{font_face("IBM Plex Sans", 500, "ibm-plex-sans-500.woff2")}{font_face("IBM Plex Sans", 600, "ibm-plex-sans-600.woff2")}{font_face("IBM Plex Mono", 400, "ibm-plex-mono.woff2")}{font_face("IBM Plex Mono", 500, "ibm-plex-mono-500.woff2")}
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
  max-width: 1080px;
  margin: 32px auto;
  padding: 0 20px 48px;
}}
.fig-deck > input {{
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
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

.fig-scene {{
  display: none;
  flex-direction: column;
  min-height: 430px;
}}
.fig-deck:not(:has(input:checked)) .fig-scene:nth-of-type(1) {{ display: flex; }}
{scene_rules}

.fig-stage {{
  flex: 1;
  padding: 28px 28px 8px;
  display: flex;
  flex-direction: column;
}}
.fig-scene-head {{
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: start;
  margin-bottom: 22px;
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
  max-width: 62ch;
}}
.fig-canvas {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 22px;
  padding: 8px 0 16px;
}}
.fig-nav {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 28px 20px;
  border-top: 1px solid var(--fig-rule);
  background: #faf6ee;
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
  gap: 10px 8px;
}}
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

{glyph_list} {{
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
{glyph_list}::before {{
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
{glyph_list}::after {{
  content: attr(data-label);
  max-width: 110px;
  line-height: 1.25;
}}
{glyph_list}[data-note]::after {{
  content: attr(data-label) "\\A" attr(data-note);
  white-space: pre-line;
}}
{icon_rules}
[data-tone="added"] {{ color: var(--fig-added); }}
[data-tone="removed"] {{ color: var(--fig-removed); }}
[data-tone="changed"] {{ color: var(--fig-changed); }}
[data-tone="focus"] {{ color: var(--fig-focus); }}
[data-tone="ghost"] {{ color: var(--fig-ghost); opacity: 0.72; }}
{glyph_list}[data-tone="added"]::before {{ background-color: var(--fig-added-bg); border-color: color-mix(in srgb, var(--fig-added) 35%, white); }}
{glyph_list}[data-tone="removed"]::before {{ background-color: var(--fig-removed-bg); border-color: color-mix(in srgb, var(--fig-removed) 35%, white); }}
{glyph_list}[data-tone="changed"]::before {{ background-color: var(--fig-changed-bg); border-color: color-mix(in srgb, var(--fig-changed) 35%, white); }}
{glyph_list}[data-tone="focus"]::before {{ background-color: var(--fig-focus-bg); border-color: color-mix(in srgb, var(--fig-focus) 35%, white); }}
{glyph_list}[data-tone="ghost"]::before {{ background-color: transparent; border-style: dashed; }}
.fig-layer[data-tone="added"], .fig-phase[data-tone="added"] {{ background: var(--fig-added-bg); }}
.fig-layer[data-tone="removed"], .fig-phase[data-tone="removed"] {{ background: var(--fig-removed-bg); }}
.fig-layer[data-tone="changed"], .fig-phase[data-tone="changed"] {{ background: var(--fig-changed-bg); }}
.fig-layer[data-tone="focus"], .fig-phase[data-tone="focus"] {{ background: var(--fig-focus-bg); }}
.fig-layer[data-tone="ghost"] {{ background: transparent; border-style: dashed; }}
.fig-step[data-tone="added"]::before {{ background: var(--fig-added); border-color: var(--fig-added); }}
.fig-step[data-tone="removed"]::before {{ background: var(--fig-removed); border-color: var(--fig-removed); }}
.fig-step[data-tone="changed"]::before {{ background: var(--fig-changed); border-color: var(--fig-changed); }}
.fig-step[data-tone="focus"]::before {{ background: var(--fig-focus); border-color: var(--fig-focus); }}

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
  max-width: 640px;
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
  .fig-scene {{ min-height: 360px; }}
  .fig-btn {{ min-width: 84px; }}
  .fig-deck {{ margin-top: 16px; }}
}}
"""

OUT.write_text(css)
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
