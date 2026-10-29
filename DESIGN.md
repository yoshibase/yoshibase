---
name: yoshibase
description: A Solari split-flap departure board in one graphite housing, rebuilt nightly from data.
colors:
  amber: "#FFC233"
  amber-ink: "#1A1408"
  amber-edge: "#C99512"
  board-ground: "#0F1012"
  flap-top: "#1E2024"
  flap-bottom: "#191B1E"
  flip-panel: "#2A2D32"
  hinge: "#060607"
  axle-pin: "#2E3136"
  glyph: "#F3F0E8"
  glyph-dim: "#9A9EA6"
  label: "#8C919A"
  rule: "#26292E"
  housing-body: "#24272C"
  housing-edge: "#363A41"
  housing-highlight: "#3B4047"
typography:
  flap-xl:
    fontFamily: "Barlow Condensed"
    fontSize: "66px"
    fontWeight: 600
  flap-velocity:
    fontFamily: "Barlow Condensed"
    fontSize: "50px"
    fontWeight: 600
  flap-lg:
    fontFamily: "Barlow Condensed"
    fontSize: "37px"
    fontWeight: 600
  flap-md:
    fontFamily: "Barlow Condensed"
    fontSize: "26px"
    fontWeight: 600
  flap-sm:
    fontFamily: "Barlow Condensed"
    fontSize: "19px"
    fontWeight: 600
  title:
    fontFamily: "Barlow Condensed"
    fontSize: "42px"
    fontWeight: 600
  headline:
    fontFamily: "Barlow Condensed"
    fontSize: "22px"
    fontWeight: 500
    letterSpacing: "0.14em"
  label:
    fontFamily: "Barlow Condensed"
    fontSize: "16px"
    fontWeight: 500
    letterSpacing: "0.14em"
  body:
    fontFamily: "Barlow"
    fontSize: "21px"
    fontWeight: 500
rounded:
  flap-sm: "2px"
  flap: "3px"
  plate-stacked: "8px"
  plate: "10px"
  button: "10px"
  housing-stacked: "16px"
  housing: "18px"
spacing:
  hairline: "1px"
  flap-gap-sm: "3px"
  flap-gap-lg: "4px"
  housing-margin: "8px"
  plate-inset: "14px"
  content-inset: "28px"
  column-gap: "48px"
components:
  flap-xl:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.glyph}"
    typography: "{typography.flap-xl}"
    rounded: "{rounded.flap}"
    width: "60px"
    height: "84px"
  flap-velocity:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.amber}"
    typography: "{typography.flap-velocity}"
    rounded: "{rounded.flap}"
    width: "46px"
    height: "64px"
  flap-lg:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.glyph}"
    typography: "{typography.flap-lg}"
    rounded: "{rounded.flap}"
    width: "34px"
    height: "48px"
  flap-md:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.glyph}"
    typography: "{typography.flap-md}"
    rounded: "{rounded.flap-sm}"
    width: "25px"
    height: "34px"
  flap-sm:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.glyph}"
    typography: "{typography.flap-sm}"
    rounded: "{rounded.flap-sm}"
    width: "19px"
    height: "26px"
  button-primary:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.amber-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    height: "52px"
  button-secondary:
    backgroundColor: "{colors.board-ground}"
    textColor: "{colors.glyph}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    height: "52px"
  board-plate:
    backgroundColor: "{colors.board-ground}"
    rounded: "{rounded.plate}"
  housing:
    backgroundColor: "{colors.housing-body}"
    rounded: "{rounded.housing}"
  line-bullet:
    rounded: "28%"
    size: "14px"
---

# Design System: yoshibase

## Overview

**Creative North Star: "The Departure Board"**

The profile is a Solari split-flap departure board: a precise, mechanical instrument that flips and settles into place on load and reports what is moving today. Every visual is a physical object, a near-black flap board recessed in a graphite housing, and the same object hangs on GitHub's white page and its dark one, the way a real board is black in a sunlit hall and at midnight alike. The field is achromatic; colour is confined to one Solari amber (what is moving: velocity, today, the primary action) and to transit line bullets in each language's own colour.

Density is that of signage, not of a dashboard: few rows, large flaps, printed condensed caps for labels, hairline rules between bands. Every glyph that matters sits on the flap cell lattice; the velocity number of a trending row is the row's largest element. Text is laid out from exact font advance widths, so right-alignment and truncation are measured, never guessed.

The world was built for one hostile renderer. GitHub's sanitizer strips `style`, `class` and `script` from README HTML and splits `<a><picture>`, so every board is one theme-independent SVG inside a plain `<a><img>`. This amends the original aluminium/graphite plan: the housing is a single graphite for both themes. Everything expressive (embedded fonts, keyframes, media queries) lives inside the SVG, where the sanitizer cannot reach. Confirmed rejections from the direction: no gradient-name capsule banner, no emoji, no skill-icon wall, no badge soup, no gradients, no glow.

**Key Characteristics:**
- Theme-independent near-black boards in one graphite housing, identical in light and dark GitHub themes.
- Split-flap cells with two-tone halves, a hinge line and axle pins; a once-per-load flip cascade that settles.
- One amber accent for motion and the primary action; language colour only as line bullets.
- One signage family: Barlow Condensed for flaps and printed labels, Barlow for mixed-case descriptions.
- Every asset generated nightly by Python stdlib, laid out from measured advance widths.

## Colors

An achromatic instrument field with a single Solari amber and data-driven line colours.

### Primary
- **Solari Amber** (`amber`): the only accent. It marks what is moving: velocity flaps and their "stars since yesterday" caption, the up-arrow gain on the repo of the day, weekly contribution bars, the Focus/Stack field labels on the header, the amber line bullet that heads each board title, the Y monogram, and the LinkedIn primary button.
- **Amber Ink** (`amber-ink`): text and strokes set on amber (button label, monogram Y and its split line).
- **Amber Edge** (`amber-edge`): the 1px stroke around the primary button only.

### Neutral
- **Board Ground** (`board-ground`): the recessed backplate under every flap, and the face of secondary buttons.
- **Flap Top / Flap Bottom** (`flap-top`, `flap-bottom`): the two halves of every cell; the upper half is lighter because it catches the light.
- **Flip Panel** (`flip-panel`): the falling half-flap drawn during the cascade.
- **Hinge** (`hinge`) and **Axle Pin** (`axle-pin`): the 1.2px split across every flap and the 2x5px pins at its ends.
- **Warm White Glyph** (`glyph`): flap lettering, board titles, repo names, the handle.
- **Dim Glyph** (`glyph-dim`): secondary lettering: stack names, stat values, star/fork icons.
- **Printed Label Grey** (`label`): small printed captions and meta (≥4.5:1 on board ground).
- **Printed Rule** (`rule`): 1px hairlines between board bands; empty-week ticks in the contribution chart.
- **Graphite Housing** (`housing-body`, `housing-edge`, `housing-highlight`): the casing, its 1px stroke, and the 1px top highlight line.

### Line colours (data, not palette)
Language and stack bullets take each technology's own colour from `STACK` and GitHub linguist `LANGUAGE_COLORS` in `scripts/tokens.py` (fallback `#6E7681`). They appear only as line bullets, never as text, fills or borders.

### Named Rules
**The One Amber Rule.** Amber means moving or act-now: velocity, today, gain, activity, the primary action. Nothing static or decorative is amber beyond the board-title bullet, field labels and the monogram.

**The Object Rule.** Board colours never change with the GitHub theme. No light/dark pairs, no `<picture>`, no `prefers-color-scheme`.

## Typography

**Display Font:** Barlow Condensed 600 (embedded woff2, no fallback needed)
**Label Font:** Barlow Condensed 500
**Body Font:** Barlow 500

**Character:** One highway/transit signage family. Condensed caps carry the flaps and printed labels; regular-width Barlow carries the only mixed-case prose (repository descriptions).

### Hierarchy
- **Flap XL** (600, 66px in 60x84 cells): the name row on the header board.
- **Flap Velocity** (600, 50px in 46x64 cells, amber): the star-velocity number on each trending row.
- **Flap LG** (600, 37px in 34x48 cells): the role row, trending rank, contribution stats.
- **Flap MD** (600, 26px in 25x34 cells): focus rows, repo-of-the-day name, footer date stamp.
- **Flap SM** (600, 19px in 19x26 cells): date strips.
- **Title** (600, 42px, mixed case, Barlow Condensed): the trending repository name, set as text rather than flaps.
- **Headline** (500, 22-24px, uppercase, 0.14em tracking): board titles ("Repo of the day", "Contributions", "Trending now").
- **Label** (500, 16-19px, uppercase, 0.14em tracking): printed captions, stack names, meta, button labels.
- **Body** (500, 20-21px, Barlow): owner names and repository descriptions; one line on trending rows, up to two on the repo of the day (30px line step), ellipsized by measured width.

### Named Rules
**The Measured Text Rule.** All width-dependent layout (truncation, right-alignment, wrapping, legend spacing) uses the exact advances in `scripts/font_metrics.py`. Never estimate glyph widths; regenerate the table if a font file changes.

**The Flap Baseline Rule.** Flap glyphs centre on the hinge (baseline = cell height / 2 + font size x 0.35). Flap text is always uppercase; cells pad to the row's cell count with blank flaps.

## Layout

Every board is an SVG on a 1200px-wide viewBox, placed full-width (`width="100%"`) in the README's ~830px column. The housing sits 8px inside the SVG edge; the board plate sits 14-22px inside the housing; content sits 26-36px inside the plate. Bands within a board are separated by 1px printed rules. Flap rows fill the available width with blank cells (cell count = how many cells fit), so every row ends on the same lattice edge.

README flow: header board, centred row of three signage buttons (40px tall, `&nbsp;` gutters), a one-sentence lede, the contributions board, the trending strip, the repo of the day with a collapsible departure log, the "How this board works" details, the footer plate.

The trending strip (section plate plus three rows) is emitted on one line, so it is one HTML block with an even inline gutter; its housings drop the shadow and use the smaller stacked radii so they read as one stacked board.

**Responsive:** an SVG-internal `@media (max-width:600px){.t3{display:none}}` hides tertiary layers (stack legend, descriptions, meta captions, trending stats column) at phone width. It works inside `<img>`. Primary flaps, names and velocity always remain.

### Named Rules
**The Tertiary Layer Rule.** Anything not needed to read who, what, or how fast is wrapped in `t3` and must survive being hidden on phones.

## Elevation & Depth

Depth is physical and singular: the graphite housing casts one soft drop shadow, the board plate is recessed with a 1px black inner stroke at 60% opacity, and the housing carries a 1px top highlight. Flap depth comes from tonal halves and the hinge, not shadows.

### Shadow Vocabulary
- **Housing shadow** (`feDropShadow dx=0 dy=6 stdDeviation=9, #000 at 0.22`): standalone boards only (header, footer, contributions, repo of the day). Stacked trending boards have none.

### Named Rules
**The No-Glow Rule.** No gradients, glows or coloured shadows. Depth is housing, recess and flap tone.

## Shapes

Nested rounded rectangles, tightening inward: housing 18px (16px stacked), plate 10px (8px stacked), flap 3px (2px below 30px cell width). Line bullets are rounded squares (radius 28% of size); the monogram is a rounded square (16%). Icons are authored SVG strokes and polygons: star, fork, north-east arrow, solid up-triangle. No circles as containers, no pills.

## Components

### Split-Flap Row (signature)
A run of cells, each a two-tone flap (`flap-top` over `flap-bottom`) with a hinge line and axle pins. On load each non-blank cell flips through 3-8 random glyphs at 0.07s per flip (falling half-panel scaling to 0.04 on `cubic-bezier(.5,0,1,1)`), staggered 0.02-0.04s per cell, then settles. Choreography is seeded by date, so a day's board is stable. **The settled glyph is visible by default** and only hidden while its cell flips, so renderers without CSS animation never show blanks; `prefers-reduced-motion` hides the flip layers and shows the settled board.

### Buttons
- **Shape:** gently rounded signage plate (10px), 52px tall in the SVG, shown at 40px in the README.
- **Primary (LinkedIn):** amber face, amber-edge stroke, amber-ink label in uppercase Label 19px, north-east arrow.
- **Secondary (GitHub, Repositories):** board-ground face, housing-highlight stroke, warm-white label and arrow.
- **Split:** a 1px black line at 22% opacity across the middle, echoing a flap hinge.
- **States:** none inside the SVG; GitHub provides link behaviour. Each button is a plain `<a href><img></a>` on its own line.

### Board Plate + Housing
Graphite housing (1px edge stroke, 1px top highlight, optional shadow) wrapping a recessed board-ground plate. Every board uses this pair.

### Line Bullet
A rounded-square swatch in a language or stack colour beside an uppercase label; amber when it heads a board title.

### Monogram
A single amber flap showing a stroked Y in amber ink, with a split line at 55% opacity. Used in header (30px) and footer (40px).

### Stat Item
Icon (line bullet, star or fork, 15px) plus an uppercase label value in `glyph-dim`, 8px apart, items 30px apart.

## Do's and Don'ts

### Do:
- **Do** ship every board as one theme-independent SVG in a plain `<img>` (inside `<a>` when linked), with `width="100%"` on board rows.
- **Do** keep contact-button lines in the `<a href="https://github.com` / `<a href="https://www.linkedin.com` line format; `scripts/commit_booster.py` matches them, and its badge regex relies on board rows carrying `width="100%"`.
- **Do** emit the trending strip and its rows on one line so they share one HTML block and an even gutter.
- **Do** embed fonts as base64 woff2 and keep all CSS inside the SVG.
- **Do** keep the settled glyph visible by default and honour `prefers-reduced-motion` with the settled board.
- **Do** wrap tertiary content in `t3` so the 600px media query can drop it.
- **Do** keep the nightly pipeline Python stdlib only, laying out text with `scripts/font_metrics.py`.

### Don't:
- **Don't** use `<picture>`, `prefers-color-scheme`, or light/dark asset pairs; GitHub splits `<a><picture>`.
- **Don't** put `style`, `class` or `script` in README HTML; the sanitizer strips them.
- **Don't** use emoji or font glyphs as icons; flags render as two-letter origin codes and icons are authored SVG.
- **Don't** use gradients, glow or coloured shadows.
- **Don't** introduce a second accent; colour beyond amber appears only as line bullets.
