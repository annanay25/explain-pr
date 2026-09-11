# Screenshot pass

Captured with Playwright (Chromium, 1280×900 @2x, plus 390×844 mobile).

## Before (CSS-only, broken)

Grouped selectors in `scripts/build-css.py` emitted `{glyph_list}::before`, so `::before` attached only to `.fig-transform`. Every other glyph was an empty dashed tile with no icon and no label. Babel, OXC, and SWC were identical blank squares. Native radios also leaked, and `.fig-page` / `.fig-shell` later collided with glyph names.

See `screenshots/before/`.

## After

- Each glyph has its own `::before`.
- Named components are `<details class="fig-node">` cards: kind, name, role, **Inspect**.
- Nested `.fig-fold` and nested nodes let a reviewer go as deep as they want (OXC → crate note; Rust compiler → Arena + index → “What an index buys”).
- Babel / OXC / SWC use distinct marks (`babel`, `oxc`, `swc`), not `.fig-box`.

See `screenshots/after/`.
