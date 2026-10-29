---
name: yoshibase
description: A Solari split-flap departure board for the GitHub README, and a drenched-colour media player for yoshibase.com.
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
  field-github: "#C6FF3D"
  field-linkedin: "#2F5BFF"
  field-activefactor: "#FF4F1F"
  field-about: "#FFB52E"
  field-ink: "#0B0B0C"
  field-ink-light: "#FFFFFF"
  shell: "#121214"
  shell-2: "#1A1A1E"
  shell-edge: "#000000"
  shell-text: "#E9E9EC"
  shell-dim: "#A3A3AB"
  lcd: "#0B1A0E"
  lcd-on: "#9CFF6E"
  lcd-mid: "#8EDF74"
  viz-well: "#0E0E11"
  eq-track: "#2C2C32"
  peak-cap: "#F2F2F4"
  cover-paper: "#F4F2EC"
  cover-paper-ink: "#14171F"
  sticker-yellow: "#FFE14D"
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
  player-display:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(3.2rem, 7.4vw, 8.2rem)"
    fontWeight: 900
    lineHeight: 0.84
    letterSpacing: "-0.045em"
    fontVariation: "'wdth' 125"
  player-cover-title:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "calc(var(--cs) * .13)"
    fontWeight: 900
    lineHeight: 0.92
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 125"
  player-track-title:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.3rem, 1rem + 1vw, 1.8rem)"
    fontWeight: 800
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 115"
  player-bio:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.1rem, 1rem + .45vw, 1.35rem)"
    fontWeight: 500
    lineHeight: 1.55
    fontVariation: "'wdth' 96"
  player-body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 500
    lineHeight: 1.5
  player-chip:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: ".88rem"
    fontWeight: 650
    letterSpacing: "0.01em"
    fontVariation: "'wdth' 85"
  player-label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: ".95rem"
    fontWeight: 700
    letterSpacing: "0.2em"
    fontVariation: "'wdth' 75"
  player-nav:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: ".82rem"
    fontWeight: 650
    letterSpacing: "0.06em"
    fontVariation: "'wdth' 88"
  lcd-marquee:
    fontFamily: "Doto, monospace"
    fontSize: "1.5rem"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "0.03em"
  lcd-readout:
    fontFamily: "Doto, monospace"
    fontSize: ".82rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.06em"
  badge-88:
    fontFamily: "Doto, monospace"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.02em"
rounded:
  flap-sm: "2px"
  flap: "3px"
  plate-stacked: "8px"
  plate: "10px"
  button: "10px"
  housing-stacked: "16px"
  housing: "18px"
  cover: "6px"
  art: "4px"
  viz: "10px"
  well: "14px"
  deck: "24px"
  deck-phone: "20px"
  focus: "8px"
  pill: "999px"
  round: "50%"
spacing:
  hairline: "1px"
  flap-gap-sm: "3px"
  flap-gap-lg: "4px"
  housing-margin: "8px"
  plate-inset: "14px"
  content-inset: "28px"
  column-gap: "48px"
  player-gutter: "clamp(16px, 3.4vw, 48px)"
  player-max: "1440px"
  cover-size: "clamp(240px, 24vw, 360px)"
  cover-size-stacked: "min(64vw, 360px)"
  cover-pad: "7.5%"
  deck-pad: "16px"
  deck-gap: "16px"
  column-gap-player: "clamp(12px, 1.6vw, 24px)"
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
  nav-pill:
    textColor: "{colors.field-ink}"
    typography: "{typography.player-nav}"
    rounded: "{rounded.pill}"
    padding: "8px 14px"
  nav-pill-current:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.field-github}"
    typography: "{typography.player-nav}"
    rounded: "{rounded.pill}"
    padding: "8px 14px"
  keyword-chip:
    textColor: "{colors.field-ink}"
    typography: "{typography.player-chip}"
    rounded: "{rounded.pill}"
    padding: "7px 13px 6px"
  keyword-chip-music:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.field-github}"
    typography: "{typography.player-chip}"
    rounded: "{rounded.pill}"
    padding: "7px 13px 6px"
  cover:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.field-github}"
    typography: "{typography.player-cover-title}"
    rounded: "{rounded.cover}"
    padding: "{spacing.cover-pad}"
    size: "{spacing.cover-size}"
  cover-linkedin:
    backgroundColor: "{colors.cover-paper}"
    textColor: "{colors.field-linkedin}"
    rounded: "{rounded.cover}"
    padding: "{spacing.cover-pad}"
    size: "{spacing.cover-size}"
  flow-nudge:
    textColor: "{colors.field-ink}"
    rounded: "{rounded.round}"
    size: "40px"
  deck:
    backgroundColor: "{colors.shell}"
    textColor: "{colors.shell-text}"
    rounded: "{rounded.deck}"
    padding: "{spacing.deck-pad}"
  lcd:
    backgroundColor: "{colors.lcd}"
    textColor: "{colors.lcd-on}"
    typography: "{typography.lcd-marquee}"
    rounded: "{rounded.well}"
    padding: "12px"
  transport-button:
    textColor: "{colors.shell-text}"
    rounded: "{rounded.round}"
    size: "46px"
  transport-play:
    backgroundColor: "{colors.field-github}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.round}"
    size: "62px"
  visualizer:
    backgroundColor: "{colors.viz-well}"
    rounded: "{rounded.viz}"
    height: "64px"
  eq-panel:
    backgroundColor: "{colors.shell-2}"
    textColor: "{colors.shell-dim}"
    rounded: "{rounded.well}"
    padding: "12px 14px 10px"
  badge-88:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.field-github}"
    typography: "{typography.badge-88}"
    height: "31px"
    width: "88px"
  tracklist-row:
    textColor: "{colors.field-ink}"
    typography: "{typography.player-track-title}"
    padding: "14px 4px"
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

### yoshibase.com: the player
yoshibase.com is a separate world from the README boards: the page is a media player and the person is the record. A flat, drenched colour field fills the whole page and takes the colour of the selected album cover. On it sit the name in expanded black Archivo, a Cover Flow of three square typographic covers (the three links), and a near-black skinned player deck (Winamp and early iTunes lineage, held to 2010s flat discipline) with a dot-matrix LCD, gel transport buttons, a visualizer and a five-band equalizer whose bands are the keywords. The About page is the record's liner notes on an amber field. Everything expressive is progressive: without JS the page is three plain links on the field, and reduced motion stills it.

The README rules above (The One Amber Rule, The No-Glow Rule, no gradients, no second accent, no pills) govern the README boards only. The player's field colours, its hardware gloss, the LCD phosphor and its pill chips are native to its world and are governed by the yoshibase.com rules below.

**Key Characteristics (yoshibase.com):**
- A flat colour field that is the colour, not a tint, recolouring with the selected cover.
- One variable family, Archivo, spanning width 62-125%: expanded black for names and titles, condensed caps for labels.
- Three square Swiss-grid covers in a wrapping Cover Flow ring with jewel-case shine and reflections.
- A near-black player deck with one top gloss, a green dot-matrix LCD (Doto) and gel transport.
- Real data as graphics: contribution weeks as a cover waveform and as the visualizer at rest; real BiquadFilters behind the keyword EQ.

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

### Player field and deck (yoshibase.com)
A drenched two-colour field (one cover colour plus its ink) wrapped around a near-black device.
- **GitHub Lime** (`field-github`) with **Field Ink** (`field-ink`): the default field and the GitHub cover's lettering on a field-ink cover face.
- **Electric Blue** (`field-linkedin`) with **White Ink** (`field-ink-light`): the field while LinkedIn is centred; the LinkedIn cover is **Cover Paper** (`cover-paper`) lettered in electric blue, with its small print in **Paper Ink** (`cover-paper-ink`).
- **Vermilion** (`field-activefactor`) with field ink: the field while ActiveFactor is centred, and that cover's lettering on a field-ink face.
- **Liner Amber** (`field-about`) with field ink: the fixed field of the About page.
- **Shell** (`shell`), **Shell Raised** (`shell-2`), **Shell Edge** (`shell-edge`): the deck body, the EQ well and the 1px black outline around every deck part.
- **Shell Text** (`shell-text`) and **Shell Dim** (`shell-dim`): transport glyphs; EQ legend and band labels.
- **LCD Ground** (`lcd`), **LCD On** (`lcd-on`), **LCD Mid** (`lcd-mid`): the display face, the marquee and state, the secondary readout.
- **Visualizer Well** (`viz-well`), **EQ Track** (`eq-track`), **Peak Cap** (`peak-cap`): the analyser recess, the unfilled slider track, the 2px falling peak caps.
- **Sticker Yellow** (`sticker-yellow`): the round "Bonus track" sticker only.

**The Drench Rule.** The field is the colour, not a tint. The page background is one flat cover colour edge to edge, and everything on it is drawn in that field's ink (`currentColor`): type, chip and nav outlines, rules, the brand mark. No tints, gradients or second colours on the field.

**The Field-Follows-Cover Rule.** The field changes only when a cover is selected, and each cover carries its own field and ink pair (`data-color`, `data-ink`), chosen together for contrast. The theme colour meta follows the field. The About page fixes the field to liner amber.

**The Signal-on-Shell Rule.** Inside the deck the field colour appears only as signal: the play button, EQ slider fills, the visualizer bars and the deck's focus outlines. The LCD keeps its own green whatever the field.

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

### Player hierarchy (yoshibase.com)
**Display/Body Font:** Archivo variable (self-hosted woff2, `wght` 100-900, `wdth` 62-125%, `font-display:swap`, fallback system-ui)
**Device Font:** Doto dot-matrix (woff2, 500-900, fallback monospace)

**Character:** one grotesque stretched across its width axis carries every voice on the field, from expanded black names to condensed spaced caps; a dot-matrix face is the device speaking.
- **Display** (`player-display`): the name on the index, set in two stacked lines. The About title uses the same style at clamp(3rem, 6.4vw, 6.6rem).
- **Cover title** (`player-cover-title`): the link name on each cover, scaled from the cover size (ActiveFactor at 0.108x to fit). Cover corners carry a track number (900, 0.06x) and SIDE A in condensed 700 caps (0.034x, 0.14em); captions are condensed 650 caps at 0.028x.
- **Track title** (`player-track-title`): About tracklist names, led by a zero-padded number in condensed 700 caps.
- **Bio** (`player-bio`): the About paragraph, max 60ch, `text-wrap: pretty`.
- **Body** (`player-body`): the base, used for the "on GitHub since" line (condensed 88%), credits values and the footer (600, 88%, .85rem).
- **Label** (`player-label`): the role line, uppercase. The same condensed caps at smaller sizes set the EQ legend (.72rem, 0.2em), credits terms (.8rem, 0.14em) and the sleeve caption (650, 80%, .8rem, 0.12em). EQ band names go narrowest (650, 62%, .7rem).
- **Chip** (`player-chip`) and **Nav** (`player-nav`, uppercase): keywords and the Index/About pills.
- **LCD marquee** (`lcd-marquee`, 1.2rem under 620px) and **LCD readout** (`lcd-readout`): the scrolling title line and the state/time/bitrate row.
- **Badge** (`badge-88`): uppercase 88x31 footer badges with a 900 first line.

**The Width Axis Rule.** Hierarchy on the field is set by width as much as weight: names and titles go expanded (115-125%) and black (800-900); labels go condensed (62-88%) and tracked caps. One family; no second sans.

**The Device Voice Rule.** Doto belongs to the device: the LCD, the EQ value readout and the 88x31 badges. It never sets names, prose or links on the field.

## Layout

Every board is an SVG on a 1200px-wide viewBox, placed full-width (`width="100%"`) in the README's ~830px column. The housing sits 8px inside the SVG edge; the board plate sits 14-22px inside the housing; content sits 26-36px inside the plate. Bands within a board are separated by 1px printed rules. Flap rows fill the available width with blank cells (cell count = how many cells fit), so every row ends on the same lattice edge.

README flow: header board, centred row of three signage buttons (40px tall, `&nbsp;` gutters), a one-sentence lede, the contributions board, the trending strip, the repo of the day with a collapsible departure log, the "How this board works" details, the footer plate.

The trending strip (section plate plus three rows) is emitted on one line, so it is one HTML block with an even inline gutter; its housings drop the shadow and use the smaller stacked radii so they read as one stacked board.

**Responsive:** an SVG-internal `@media (max-width:600px){.t3{display:none}}` hides tertiary layers (stack legend, descriptions, meta captions, trending stats column) at phone width. It works inside `<img>`. Primary flaps, names and velocity always remain.

### Named Rules
**The Tertiary Layer Rule.** Anything not needed to read who, what, or how fast is wrapped in `t3` and must survive being hidden on phones.

### yoshibase.com
- **Frame:** the top bar, stage and footer run to 1440px (`player-max`) inside the fluid gutter (`player-gutter`).
- **Stage:** one 12-column module (`column-gap-player`). The identity column spans columns 1-5, the Cover Flow 6-12, and the deck spans all 12 below. Inside the deck the LCD, transport and EQ sit on 5:4:4 tracks with a 16px gap.
- **Cover Flow:** the cover size is `cover-size`; the flow is 1.34 cover heights tall to leave room for the reflection, with 1500px perspective. The pager sits just under it.
- **About:** the liner notes span the module as 5:7 tracks (sleeve, then title, bio, tracklist and credits), with a clamp(24px, 5vw, 80px) gap.
- **Under 1060px:** one column. The identity block dissolves (`display: contents`) so the order becomes name, role, since line, covers, keywords, deck; covers come straight after the name. Cover size becomes `cover-size-stacked`, the deck goes to two columns with the LCD full width, and the sleeve caps at 480px.
- **Under 620px:** the name goes to clamp(3rem, 16vw, 5rem), the deck stacks into one column (20px corners, 12px padding), and credits stack.

**The One Module Rule.** Every block on the player page sits on the 12-column stage, and every cover obeys the one cover grid: 7.5% padding, a top row (number, side), art, caption, title, subline.

**The Enhancement Rule.** Without JS the covers are three plain links wrapping in a row, and the pager is hidden. JS adds the ring, the recolouring, the audio and the visualizer. The page's facts (contribution weeks, rebuild stamp, counts) are baked in at build time.

## Elevation & Depth

Depth is physical and singular: the graphite housing casts one soft drop shadow, the board plate is recessed with a 1px black inner stroke at 60% opacity, and the housing carries a 1px top highlight. Flap depth comes from tonal halves and the hinge, not shadows.

### Shadow Vocabulary
- **Housing shadow** (`feDropShadow dx=0 dy=6 stdDeviation=9, #000 at 0.22`): standalone boards only (header, footer, contributions, repo of the day). Stacked trending boards have none.

### Named Rules
**The No-Glow Rule.** No gradients, glows or coloured shadows. Depth is housing, recess and flap tone.

### yoshibase.com shadow vocabulary
The field is flat; depth belongs only to the objects on it. Covers float and reflect, the deck is moulded hardware with recessed wells, and the field and its type never cast or carry shadow.
- **Cover float** (`box-shadow: 0 34px 50px -22px rgba(0,0,0,.5), 0 2px 4px rgba(0,0,0,.18)`): covers and the About sleeve (first layer only).
- **Cover reflection** (`-webkit-box-reflect: below 8px linear-gradient(transparent 64%, rgba(255,255,255,.26))`): covers only.
- **Jewel-case shine:** one 152deg hard-edged white sheen (22% to 6%, cut at 34%) in screen blend over each cover.
- **Deck** (`box-shadow: inset 0 1px 0 rgba(255,255,255,.1), 0 0 0 1px #000, 0 30px 50px -26px rgba(0,0,0,.55)`), plus one top gloss (white 7% fading to 0 at 46%).
- **LCD recess** (`box-shadow: inset 0 2px 10px rgba(0,0,0,.7), 0 0 0 1px #000, 0 1px 0 rgba(255,255,255,.06)`); the marquee glows faintly (`text-shadow: 0 0 6px rgba(156,255,110,.35)`), like phosphor.
- **EQ and visualizer wells** (`inset 0 1px 6px rgba(0,0,0,.5)`, `inset 0 1px 6px rgba(0,0,0,.6)`).
- **Gel button** (`box-shadow: inset 0 1px 0 rgba(255,255,255,.28), 0 0 0 1px #000, 0 3px 6px rgba(0,0,0,.5)`) over a top-to-bottom gradient (#45454C to #1C1C20). The play button's gradient is mixed from the field (55% toward white, the field at 55%, then 80% toward black).
- **Slider thumb** (#F4F4F6 to #9C9CA3, `0 0 0 1px #000, 0 2px 3px rgba(0,0,0,.6)`).
- **Round sticker** (`0 4px 8px rgba(0,0,0,.35)`).

**The Hardware Gloss Rule.** Gloss is for hardware and jewel cases only: one shine per cover, one top gloss on the deck, gel on the transport buttons and slider thumbs. The field, the type and the chips stay flat.

## Shapes

Nested rounded rectangles, tightening inward: housing 18px (16px stacked), plate 10px (8px stacked), flap 3px (2px below 30px cell width). Line bullets are rounded squares (radius 28% of size); the monogram is a rounded square (16%). Icons are authored SVG strokes and polygons: star, fork, north-east arrow, solid up-triangle. No circles as containers, no pills.

On yoshibase.com:
- **Covers and sleeve:** square (aspect 1:1), 6px corners. The LCD avatar is 72px square, 4px corners.
- **Deck:** 24px (20px under 620px). LCD and EQ wells 14px, visualizer 10px, slider thumbs 4px, tracks 2px.
- **Round:** transport buttons, Cover Flow nudges and pager pips are circles; keyword chips and nav links are full pills. Outlines are 1.5px inset strokes in the field ink.
- **Stickers:** Parental Advisory is a hard-cornered black-bordered box with a white ring; Bonus track is a yellow circle rotated 12deg.
- **88x31 badges:** square-cornered, the web-badge format played straight.
- **Rules:** the tracklist and credits use 1.5px inset lines in the field ink.
- **Brand mark:** a field-ink rounded square (8px on 32px) with a stroked Y in the field colour.

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

### Cover (yoshibase.com signature)
A square album cover per link, Swiss-grid typography over real data art: a top row (track number, SIDE A), art, a condensed caption, the link name in the cover title style, and a subline.
- **GitHub:** lime on field ink. The art is the last 12 months of real contribution weeks drawn as a waveform; caption "N contributions · last 12 months". Carries the Parental Advisory "explicit commits" sticker.
- **LinkedIn:** electric blue on cover paper, a network-graph art, small print in paper ink.
- **ActiveFactor:** vermilion on field ink, a mark-and-bars art. Carries the round "Bonus track" sticker.
- **Finish:** jewel-case shine, cover float shadow, reflection below. Focus: 3px field-ink outline offset 6px.

### Cover Flow
A wrapping ring of three covers, so both neighbours are always in view. Each slot is placed by its offset d from centre: translateX(d x 0.84 cover widths), translateZ(-200px per step), rotateY(d x -42deg), dimmed 14% per step, on 0.75s `cubic-bezier(.16,1,.3,1)`.
- **Input:** drag (40px commits a step, 6px marks it a drag), left/right arrow keys anywhere on the page, the two nudge buttons, and focus.
- **Links:** side covers select; only the centre cover follows its link.
- **Pager:** two 40px circular nudges (1.5px ink outline, fill to ink on hover) around 8px pips; the current pip fills and scales 1.35x.
- **Selection** recolours the field and ink, the theme-colour meta, the LCD marquee line and clock, and restarts the track if playing.

### Player Deck
Near-black shell, 16px padding, a 1px black edge and one top gloss, holding three parts.
- **LCD:** a 72px avatar thumbnail beside a Doto marquee ("HASAN OZDEMIR · GITHUB · 2:00 · 320 KBPS · STEREO ·") scrolling as a doubled run over 16s, and a readout row (state in LCD on; time, bitrate, sample rate in LCD mid).
- **Transport:** previous and next as 46px gel buttons, play as a 62px gel button in the field colour with an ink glyph, toggling pause via `aria-pressed`. Hover brightens 15%; press sinks 1px and scales 0.97. Focus: 3px field outline.
- **Visualizer:** a 28-bar canvas in the visualizer well. At rest it shows the real contribution year resampled to 28 bars, breathing gently; while playing it shows the live analyser spectrum (FFT 256) with 2px peak caps that fall back slowly. Bars are drawn in the current field colour.
- **Equalizer:** a fieldset with five vertical sliders. The bands are the keywords (AI/ML, Automation, Knowledge, Data, Music), feeding real BiquadFilters at 110, 420, 1100, 2800 and 7000 Hz (low shelf, three peaking, high shelf; Q 0.9). Four bands run 0-10; Music runs to 11 and starts there, with a Doto "11" readout. Tracks fill from below in the field colour.

### Keyword Chips
Pills with a 1.5px ink outline in the chip style. The last chip, Music, is inverted (ink face, field lettering).

### Top Bar Navigation
The brand mark and "yoshibase" (800, 112% width) on the left; Index and About as uppercase nav pills on the right. Hover draws a 1.5px outline; the current page is an inverted pill. A skip link drops in on focus as an ink tab with 8px corners.

### Liner Notes (About)
- **Sleeve:** the cover painting, square, cover float shadow, with a condensed caps caption below.
- **Tracklist:** numbered rows (01-03) of the three links in the track title style with a condensed handle at the right, ruled below in 1.5px ink. Hover inverts the row to ink on field.
- **Credits:** a two-column definition list under a 1.5px rule: condensed caps terms (Focus, Words & code, Mixed, Mastered, Guitar), 550-weight values.

### 88x31 Badges
Footer badges in the 88x31 web-badge format: ink face, field lettering, an inner 1px field line and outer ink ring, Doto caps with a 900 first line. The alternate is transparent with a 1.5px ink outline. Contents are baked facts (best viewed at, rebuilt date, contribution count).

### Player Motion
- **Arrival:** the name lines land (0.9s, rising 0.3em out of a clip), and the covers swing in once from 30vw right, -400px deep and -70deg (1.1s, staggered 0.15s + n x 0.12s).
- **Recolour:** the field and ink transition over 0.8s on `cubic-bezier(.16,1,.3,1)`; the play button follows.
- **Loops:** the marquee scrolls; the visualizer breathes at rest and runs live while playing.
- **Reduced motion:** no arrival, transitions cut to 0.01ms, the marquee stops (ellipsis), dragging no longer moves covers, and the visualizer draws one still frame of the year.

## Do's and Don'ts

### Do:
- **Do** ship every board as one theme-independent SVG in a plain `<img>` (inside `<a>` when linked), with `width="100%"` on board rows.
- **Do** keep contact-button lines in the `<a href="https://github.com` / `<a href="https://www.linkedin.com` line format; `scripts/commit_booster.py` matches them, and its badge regex relies on board rows carrying `width="100%"`.
- **Do** emit the trending strip and its rows on one line so they share one HTML block and an even gutter.
- **Do** embed fonts as base64 woff2 and keep all CSS inside the SVG.
- **Do** keep the settled glyph visible by default and honour `prefers-reduced-motion` with the settled board.
- **Do** wrap tertiary content in `t3` so the 600px media query can drop it.
- **Do** keep the nightly pipeline Python stdlib only, laying out text with `scripts/font_metrics.py`.
- **Do** read the README rules (One Amber, No-Glow, no gradients, no second accent, no pills) as governing the README boards only; yoshibase.com follows its own player rules.
- **Do** keep the yoshibase.com field one flat cover colour, with everything on it drawn in that field's ink.
- **Do** give every new cover its own field and ink pair, checked for contrast together, and set the theme-colour meta from it.
- **Do** keep the page usable as plain links without JS, and still under `prefers-reduced-motion`.
- **Do** draw real data (contribution weeks, counts) into covers, the visualizer and badges, baked in at build time.
- **Do** set player type in Archivo along its width axis; keep Doto inside the device and the 88x31 badges.

### Don't:
- **Don't** use `<picture>`, `prefers-color-scheme`, or light/dark asset pairs; GitHub splits `<a><picture>`.
- **Don't** put `style`, `class` or `script` in README HTML; the sanitizer strips them.
- **Don't** use emoji or font glyphs as icons; flags render as two-letter origin codes and icons are authored SVG.
- **Don't** use gradients, glow or coloured shadows.
- **Don't** introduce a second accent; colour beyond amber appears only as line bullets.
- **Don't** tint, gradient or shadow the yoshibase.com field or the type on it; gloss belongs to covers and deck hardware only.
- **Don't** set small text in the field colour on the shell; inside the deck the field colour is signal fill.
- **Don't** let a side cover follow its link; it selects first.
