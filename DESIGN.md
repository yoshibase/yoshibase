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
  hall: "#0B0C0E"
  stock: "#EDE8DC"
  stock-shade: "#E2DCCD"
  ink: "#1B1A17"
  ink-soft: "#4A463F"
  ink-faint: "#58534A"
  lining: "#4A2016"
  lining-deep: "#2E130C"
  metal: "#8C919A"
  kraft: "#C9A97B"
  kraft-ink: "#2A2015"
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
  site-lede:
    fontFamily: "Barlow"
    fontSize: "clamp(1.35rem, 1rem + 1.6vw, 2.05rem)"
    fontWeight: 500
    lineHeight: 1.22
    letterSpacing: "-0.012em"
  site-prose:
    fontFamily: "Barlow"
    fontSize: "1.0625rem"
    fontWeight: 500
    lineHeight: 1.6
  ticket-destination:
    fontFamily: "Barlow Condensed"
    fontSize: "clamp(1.7rem, 1.3rem + 1vw, 2.15rem)"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.01em"
  ticket-field:
    fontFamily: "Barlow Condensed"
    fontSize: "0.72rem"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.16em"
  ticket-fine:
    fontFamily: "Barlow"
    fontSize: "0.74rem"
    fontWeight: 500
    lineHeight: 1.35
rounded:
  flap-sm: "2px"
  flap: "3px"
  plate-stacked: "8px"
  plate: "10px"
  button: "10px"
  housing-stacked: "16px"
  housing: "18px"
  ticket: "10px"
  frame: "14px"
  case: "36px 36px 56px 56px"
  sign: "2px 4px 3px 2px"
spacing:
  hairline: "1px"
  flap-gap-sm: "3px"
  flap-gap-lg: "4px"
  housing-margin: "8px"
  plate-inset: "14px"
  content-inset: "28px"
  column-gap: "48px"
  site-gutter: "clamp(16px, 4vw, 56px)"
  site-max: "1440px"
  housing-ring: "12px"
  ticket-gap: "28px"
  ticket-stub: "86px"
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
  ticket:
    backgroundColor: "{colors.stock}"
    textColor: "{colors.ink}"
    typography: "{typography.ticket-destination}"
    rounded: "{rounded.ticket}"
    height: "176px"
  ticket-stub:
    backgroundColor: "{colors.stock-shade}"
    textColor: "{colors.ink}"
    width: "{spacing.ticket-stub}"
  ticket-stub-primary:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.amber-ink}"
    width: "{spacing.ticket-stub}"
  case-lining:
    backgroundColor: "{colors.lining}"
    rounded: "{rounded.case}"
  kraft-sign:
    backgroundColor: "{colors.kraft}"
    textColor: "{colors.kraft-ink}"
    rounded: "{rounded.sign}"
    padding: "11px 18px 10px"
  notice-plate:
    backgroundColor: "{colors.board-ground}"
    textColor: "{colors.glyph}"
    rounded: "{rounded.frame}"
    padding: "clamp(24px, 3.5vw, 44px)"
  poster-frame:
    backgroundColor: "{colors.housing-body}"
    rounded: "{rounded.frame}"
    padding: "12px"
  board-strip:
    backgroundColor: "{colors.housing-body}"
    textColor: "{colors.glyph}"
    padding: "12px clamp(16px, 4vw, 56px)"
  site-flap-clock:
    backgroundColor: "{colors.flap-bottom}"
    textColor: "{colors.glyph}"
    width: "20px"
    height: "28px"
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

### yoshibase.com: the board at room scale
On yoshibase.com the same world, free of the README sanitizer, becomes a station hall. A hall ground one step darker than the board sits under everything; a full-width graphite board strip carries the monogram and a live UTC flap clock; the name and role are HTML split-flap cells; the profile painting hangs as a station poster in a graphite frame with a printed plaque; the outbound links are pale ticket stock dropped into a busker's open guitar case; a graphite notice plate carries the announcement; the footer ends on a "Mind the gap" platform stripe. Ticket stock is the one pale material in the hall. The case lining and a kraft cardboard sign are the only warm materials, and both are dark or muted enough that amber stays the only signal. The page is complete as static HTML: the build bakes the clock time, rebuild stamp, today's pick and barcodes, and JS only animates.

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

### Hall materials (yoshibase.com)
- **Hall Ground** (`hall`): page background and theme colour. It is darker than board ground, so plates, frames and housings read as objects hung in the hall.
- **Ticket Stock** (`stock`) and **Stub Shade** (`stock-shade`): the ticket face and its tear-off stub.
- **Ticket Ink** (`ink`): destinations, field values, barcodes. **Soft Ink** (`ink-soft`): the one-line destination description. **Faint Ink** (`ink-faint`): route codes, field labels, seat captions and fine print. It holds 6.2:1 on stock and 5.6:1 on the stub.
- **Case Lining** (`lining`) and **Lining Deep** (`lining-deep`): the open case interior and its inner shading, top and bottom.
- **Latch Metal** (`metal`): case latches. It has the same value as printed label grey but is named for its material.
- **Kraft** (`kraft`) and **Kraft Ink** (`kraft-ink`): the cardboard sign propped in the case (7.2:1).

### Named Rules
**The One Amber Rule.** Amber means moving or act-now: velocity, today, gain, activity, the primary action. Nothing static or decorative is amber beyond the board-title bullet, field labels and the monogram.

**The Object Rule.** Board colours never change with the GitHub theme. No light/dark pairs, no `<picture>`, no `prefers-color-scheme`.

**The Hall Amber Rule.** On yoshibase.com, amber marks four things in the content: the clock colon, the primary (GitHub) ticket stub with its amber-ink barcode, the today dot on the live ticket, and the Mind-the-gap stripe. Beyond those, amber appears only in the inherited monogram and the interaction layer (focus ring, text selection). Secondary tickets stay on stock, and the case, the sign and the case props are never amber.

**The One Pale Material Rule.** Ticket stock is the only light surface in the hall, and it is reserved for the outbound destination tickets. Everything else sits on hall, board, graphite, lining or kraft.

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

### Hall hierarchy (yoshibase.com)
Fonts are self-hosted woff2 files (Barlow Condensed 500/600, Barlow 500) with `font-display:swap`. The condensed fallback is Arial Narrow and the Barlow fallback is system-ui.
- **Name flaps** (600, glyph = cell x 1.1, cell 1:1.4, cells up to 64px): fluid, so 13 cells fill the identity column. Below a 560px column the name wraps to 7 columns and the space cell drops out.
- **Role flaps** (600, cells up to 34px, 4px gap).
- **Clock flaps** (600, 20px cells, 3px gap) with a 22px amber colon.
- **Lede** (`site-lede`): one balanced sentence, max 34ch, with its emphasised phrase in warm white.
- **Prose** (`site-prose`): the page body. The announcement sets it larger (1.08-1.25rem, line-height 1.62, max 64ch).
- **Ticket destination** (`ticket-destination`), **field label** (`ticket-field`, uppercase, over a 600 0.95rem uppercase value), **fine print** (`ticket-fine`, italic).
- **Printed caps:** the existing Label style (condensed 500, uppercase, 0.14em) sets the strip caption, the focus list, the plaque, the notice heading and the footer.

## Layout

Every board is an SVG on a 1200px-wide viewBox, placed full-width (`width="100%"`) in the README's ~830px column. The housing sits 8px inside the SVG edge; the board plate sits 14-22px inside the housing; content sits 26-36px inside the plate. Bands within a board are separated by 1px printed rules. Flap rows fill the available width with blank cells (cell count = how many cells fit), so every row ends on the same lattice edge.

README flow: header board, centred row of three signage buttons (40px tall, `&nbsp;` gutters), a one-sentence lede, the contributions board, the trending strip, the repo of the day with a collapsible departure log, the "How this board works" details, the footer plate.

The trending strip (section plate plus three rows) is emitted on one line, so it is one HTML block with an even inline gutter; its housings drop the shadow and use the smaller stacked radii so they read as one stacked board.

**Responsive:** an SVG-internal `@media (max-width:600px){.t3{display:none}}` hides tertiary layers (stack legend, descriptions, meta captions, trending stats column) at phone width. It works inside `<img>`. Primary flaps, names and velocity always remain.

### Named Rules
**The Tertiary Layer Rule.** Anything not needed to read who, what, or how fast is wrapped in `t3` and must survive being hidden on phones.

### yoshibase.com
- **Frame:** content runs to a 1440px maximum (`site-max`) inside a fluid gutter (`site-gutter`). The board strip and the footer run full-bleed.
- **Hero:** a 7fr identity column beside a 5fr poster (max 460px). It stacks below 860px.
- **The case from 1380px:** an aspect-locked authored SVG (viewBox 1320x560). The 2x2 ticket grid sits in the case body (left 10%, top 12%, width 48%), with the kraft sign at the head.
- **The case below 1380px:** a lined CSS panel with a neck, two latches and a two-column ticket grid (`ticket-gap`). It drops to one column under 700px.
- **Ticket placement:** tickets alternate small rotations (about 1-2deg either way) and vertical offsets. The offsets zero out in one column.
- **Notice plate:** max 880px.

**The Baked Page Rule.** `scripts/build_site.py` bakes every fact on the page: clock time, rebuild stamp, contribution line, today's pick and barcodes. JS only animates and keeps the clock current, so the page is complete with scripting off.

## Elevation & Depth

Depth is physical and singular: the graphite housing casts one soft drop shadow, the board plate is recessed with a 1px black inner stroke at 60% opacity, and the housing carries a 1px top highlight. Flap depth comes from tonal halves and the hinge, not shadows.

### Shadow Vocabulary
- **Housing shadow** (`feDropShadow dx=0 dy=6 stdDeviation=9, #000 at 0.22`): standalone boards only (header, footer, contributions, repo of the day). Stacked trending boards have none.

### Named Rules
**The No-Glow Rule.** No gradients, glows or coloured shadows. Depth is housing, recess and flap tone.

### yoshibase.com shadow vocabulary
The hall is lit from above. Every hung or dropped object casts one soft black shadow downward, and nothing glows.
- **Frame and notice plate** (`box-shadow: 0 16px 24px -10px rgba(0,0,0,.7)`).
- **Case outline** (SVG `feDropShadow dx=0 dy=16 stdDeviation=14`, #000 at 0.6).
- **Ticket at rest** (`filter: drop-shadow(0 14px 16px rgba(0,0,0,.55))`) and **ticket lifted** (`drop-shadow(0 24px 24px rgba(0,0,0,.62))`), cast by the list item.
- **Kraft sign** (`box-shadow: 0 6px 10px -4px rgba(0,0,0,.6)`).
- **HTML flap cell** (`box-shadow: 0 1px 0 rgba(255,255,255,.035) inset, 0 2px 3px rgba(0,0,0,.45)`).
- **Housing ring:** the graphite housing around the case panel and the notice plate is drawn as spread shadows (12px and 10px of housing, then a 1px housing-edge ring), not as an extra element.
- **Lining shade:** inset shading in lining-deep at the top and bottom of the case panel.

**The Shadow Carrier Rule.** A masked element cannot cast its own shadow. Its parent casts it with `filter: drop-shadow`, and the parent also draws the focus ring.

**The Hard-Stop Rule.** The No-Glow Rule bans visible colour gradients, not gradient syntax. Hard-stop gradients that draw flap halves, dashed route lines, the platform stripe and mask notches are drawing tools. Inner shading in a material's own deep tone (lining-deep on lining) is depth, not a coloured shadow.

## Shapes

Nested rounded rectangles, tightening inward: housing 18px (16px stacked), plate 10px (8px stacked), flap 3px (2px below 30px cell width). Line bullets are rounded squares (radius 28% of size); the monogram is a rounded square (16%). Icons are authored SVG strokes and polygons: star, fork, north-east arrow, solid up-triangle. No circles as containers, no pills.

On yoshibase.com:
- **Tickets:** 10px corners, with two 9px semicircular notches cut by a mask at the stub line and a 1.5px dashed perforation.
- **Frame and notice plate:** 14px. The poster image inside the frame is 6px.
- **CSS case panel:** 36/36/56/56px corners (28/28/44/44px under 700px). Its neck has 22px top corners.
- **Kraft sign:** deliberately uneven corners (2/4/3/2px), rotated -2.2 to -3deg.
- **Latches:** 2px.
- **Authored case outline:** a guitar-case silhouette (body, waist, neck, head) with a neck pocket, three latches and two picks.
- **Dots:** route lines end in a small dot. The today dot (7px, ringed 2px in amber ink) is a marker, not a container.

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

### Ticket (yoshibase.com signature)
Ticket stock printed like a rail ticket, laid out as a main body plus a stub (`ticket-stub`, 86px; 76px in the wide case; 74px under 480px).
- **Main body:** a route line (origin code, dashed rule ending in a dot, destination code), the destination, a one-line description, Gate/Class fields and italic fine print.
- **Stub:** a seat code, a data-derived barcode (baked from the link URL), and "Board" with a north-east arrow.
- **Perforation:** notches cut with a CSS mask. The list item therefore carries the drop shadow and the 2px amber focus ring (offset 6px).
- **Hover / focus:** lifts 6px and the arrow nudges up-right, on `cubic-bezier(.16,1,.3,1)`. With a hover pointer, the ticket also tilts toward the pointer (up to 3.5deg on each axis, perspective 900px).
- **Primary (GitHub):** the stub is amber, with an amber-ink barcode and seat caption. Always first.
- **Live (today's pick):** the route's origin is today's date with the amber today dot. A Momentum field replaces Gate/Class.

### Open Guitar Case
The container for the tickets.
- **From 1380px:** an authored inline SVG outline (viewBox 1320x560). It has a lining fill with a lining-deep inner band, a 26px graphite rim with a 1.5px housing-edge line, metal latches, a neck pocket and two picks.
- **Below 1380px:** a lined CSS panel with a graphite housing ring, a neck silhouette drawn as a pseudo-element, and metal latches on both flanks.

### Kraft Sign
A cardboard sign propped in the case: kraft face, kraft-ink condensed caps (600 1rem, 0.12em) with a smaller 500 second line, uneven corners and a slight counter-clockwise rotation. It is the case's heading.

### HTML Split-Flap Cells and Board Clock
The HTML version of the Split-Flap Row: the same two-tone halves, hinge and falling flip panel, sized by a `--cell` variable (height 1.4x, radius 0.07x).
- **Name and role:** cascade left to right once. Each cell runs 3-8 random flips at 70ms, cells are staggered 38ms, and rows start 260ms apart.
- **Board clock:** shows UTC hours and minutes in 20px cells with an amber colon. It resyncs on each minute boundary and flips only the digits that changed.
- **Without JS:** the settled glyphs and the build-time clock are in the markup.

### Board Strip and Footer
Full-bleed graphite bands (housing body, 1px housing-edge rule, 1px top highlight). The strip carries the 28px monogram, YOSHIBASE in condensed 600 caps and the clock. The footer carries the rebuild stamp, the contribution line, the platform stripe and the copyright in printed label grey.

### Poster Frame and Plaque
A graphite frame (12px padding, 1px edge, top highlight, hung shadow) around a square painting with 6px corners. Below it, a museum-style plaque: a warm-white condensed caps title on the left and a label-grey caption on the right.

### Notice Plate
A board-ground plate with a 1px black edge inside a 10px graphite housing ring. It holds a printed-caps heading with an authored speaker icon in label grey, and Barlow prose with underlined links in label grey (warm white on hover).

### Platform Stripe
A 28x4px repeating amber/amber-ink hazard stripe (7px steps) before "Mind the gap" in the footer.

### Hall Motion
There is one arrival moment. The flap cascade runs, then the tickets drop into the case by transform only: 0.8s on `cubic-bezier(.16,1,.3,1)`, delayed 0.4s + i x 0.09s, from 34px higher and 4deg further rotated. Under `prefers-reduced-motion` the flaps set instantly, and the drop, the tilt and the ticket lift transition are off.

## Do's and Don'ts

### Do:
- **Do** ship every board as one theme-independent SVG in a plain `<img>` (inside `<a>` when linked), with `width="100%"` on board rows.
- **Do** keep contact-button lines in the `<a href="https://github.com` / `<a href="https://www.linkedin.com` line format; `scripts/commit_booster.py` matches them, and its badge regex relies on board rows carrying `width="100%"`.
- **Do** emit the trending strip and its rows on one line so they share one HTML block and an even gutter.
- **Do** embed fonts as base64 woff2 and keep all CSS inside the SVG.
- **Do** keep the settled glyph visible by default and honour `prefers-reduced-motion` with the settled board.
- **Do** wrap tertiary content in `t3` so the 600px media query can drop it.
- **Do** keep the nightly pipeline Python stdlib only, laying out text with `scripts/font_metrics.py`.
- **Do** bake every fact on yoshibase.com into the static HTML at build time; JS only animates and keeps the clock current.
- **Do** cast a masked element's shadow and focus ring from its parent.
- **Do** animate hall arrivals by transform only, and turn off flaps, drops, tilt and transitions under `prefers-reduced-motion`.
- **Do** flip only the clock digits that changed.
- **Do** keep faint ticket ink at 4.5:1 or better on both stock and stub shade.

### Don't:
- **Don't** use `<picture>`, `prefers-color-scheme`, or light/dark asset pairs; GitHub splits `<a><picture>`.
- **Don't** put `style`, `class` or `script` in README HTML; the sanitizer strips them.
- **Don't** use emoji or font glyphs as icons; flags render as two-letter origin codes and icons are authored SVG.
- **Don't** use gradients, glow or coloured shadows.
- **Don't** introduce a second accent; colour beyond amber appears only as line bullets.
- **Don't** print anything except the outbound destination tickets on ticket stock.
- **Don't** put amber on secondary tickets, the case, the sign or the case props.
