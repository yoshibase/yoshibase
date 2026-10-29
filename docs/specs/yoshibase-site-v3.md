# Spec: yoshibase.com v3 — minimal, light, guitar-thread personal site

Status: **DRAFT — awaiting owner review** (Phase 1 of 4: Specify → Plan → Tasks → Implement)
Owner: Hasan Ozdemir · Date: 2026-10-29
Previous versions preserved as git tags: `site-v1-busker` (2cd278a), `site-v2-player` (24fc75e).

---

## Assumptions (correct any of these before the plan is written)

1. The visual direction is **not chosen yet**. It will come from the owner's inspiration list, then from `/impeccable`, which the owner runs separately. This spec fixes *what* and *how well*, not *the look*.
2. The site stays a **static site on GitHub Pages** in this repo (`site/` → `scripts/build_site.py` → `.github/workflows/pages.yml`), at `yoshibase.com`.
3. The page is **light-themed only**. It does not follow the visitor's dark mode.
4. The site uses **no third-party runtime dependencies**: no frameworks, CDNs, analytics or trackers. Fonts are self-hosted.
5. **No image-generation tool is available** in this environment. The new avatar artwork will be authored by hand as **vector SVG** from the existing busker painting as reference, not generated as a raster.
6. "Morph it into mine" means: the new drawing should **read as Hasan's own illustrated avatar** (a stylised self-portrait as a guitarist), not as a copy of the stock-looking painting. If a likeness is wanted, the owner supplies a reference photo (see Open Questions).
7. The **nightly GitHub data is removed from the site entirely**. That covers contribution counts, the waveform, "rebuilt" stamps and repo of the day. The site no longer needs to redeploy nightly.
8. The README profile pipeline (`scripts/generate_*.py`, `render_readme.py`, `commit_booster.py`, `data/`) is **out of scope and must not change**.

---

## Objective

A personal landing page for Hasan Ozdemir that a technical or non-technical visitor understands and trusts within seconds, and that feels **super minimal, super elegant and effortless**. Motion is sleek, ultra-light and purposeful. A **music / guitar** thread runs through it quietly.

**Who:** recruiters, engineering leaders, prospective ActiveFactor clients, developers and friends who type `yoshibase.com` or follow a link.

**Job:**
1. Know who he is.
2. Go to one of three destinations.
3. Optionally read more on About.

**Success:** the visitor reaches one of the three cards in one click, without scrolling on common screens, and leaves with the impression of a senior, tasteful engineer.

### Content inventory (fixed by the owner)

**Home page (`/`)**
- Name: **Hasan Ozdemir**
- Role: **Product engineer**
- Keywords (four, no "Music"): **AI/ML · Automation · Knowledge Management · Data Processing**
- **Exactly three cards**, prominent near the top:
  | Card | Link | Card copy (draft, owner may edit) |
  |---|---|---|
  | GitHub | https://github.com/yoshibase/yoshibase | GitHub · yoshibase |
  | LinkedIn | https://www.linkedin.com/in/oz1127 | LinkedIn · in/oz1127 |
  | ActiveFactor | https://activefactor.net | **My company.** Software systems for local businesses · San Diego |
- **A small thumbnail** of the new avatar artwork.
- No slogans, no bio paragraph, no live data.

**About page (`/about.html`)**
- The **large** avatar artwork.
- The bio paragraph (carried over from v2, minus the GitHub-data sentence if the owner prefers; see Open Questions).
- **"Things I like: playing guitars, drums."**
- Links back to the three destinations.

### The new avatar artwork

| Requirement | Testable as |
|---|---|
| A new drawing that transforms the busker painting: **cartoonish, abstract, modern, neo-brutal but sleeker and smoother**, with a **new, dynamic colour setup** that matches the page palette | Owner approves the artwork before it ships (gate). |
| Built from **flat colour patches/areas** that can **transform effortlessly**, e.g. patches gently shifting shape or colour | Animation runs on the compositor only (transform/opacity, or SMIL/CSS on a light SVG) at ≥ 55 fps, and is fully static under `prefers-reduced-motion`. |
| Matches the whole page; reads as Hasan's own avatar | Owner approval. |
| Two renditions: a **thumbnail** on the home page and the **large artwork** on About, from one source SVG | One file, `site/img/avatar.svg`, used at both sizes and crisp at 2× and 3×. |
| Lightweight | Avatar SVG ≤ 40 KB (gzip ≤ 15 KB). |

---

## Tech stack

- **HTML5 + modern CSS + vanilla JS (ES2020)** for progressive enhancement only. The page is complete without JS.
- **Python 3.11 standard library** for the build (`scripts/build_site.py`).
- **Self-hosted woff2 fonts**, latin subset. The face is chosen with the design direction, at most two families and ≤ 120 KB total.
- **GitHub Pages via Actions** (`actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`).
- Dev-only tooling, never shipped:
  - Playwright Chromium for screenshot verification.
  - The Impeccable detector.
  - graphify for orientation.

## Commands

```bash
# Build the static site into _site/
python3 scripts/build_site.py _site

# Unit tests (all suites, stdlib runner pattern used across scripts/)
cd scripts && for t in test_*.py; do python3 "$t" | tail -1; done

# Local preview
python3 -m http.server 8000 -d _site        # → http://localhost:8000

# Visual verification (dev-only; desktop 1440×900 + mobile 390×844, both pages)
python3 scripts/dev/shoot_site.py _site .impeccable/review/v3

# Design-quality detector (run once per verification round)
~/.claude/skills/impeccable/scripts/impeccable detect --json site/

# Keep the code graph current after changes
graphify update .
```

## Project structure

```
site/                    → everything that ships (copied to _site/ by the build)
  index.html             → home page
  about.html             → about page
  site.css               → single stylesheet (replaces player.css)
  site.js                → optional progressive-enhancement motion (≤ 6 KB)
  img/avatar.svg         → the new artwork (thumbnail + large from one source)
  fonts/*.woff2          → self-hosted faces
  favicon.svg, og.jpg    → icon and share image
scripts/build_site.py    → stdlib build: copy site/, fill {{YEAR}}, write CNAME + .nojekyll
scripts/test_build_site.py
scripts/dev/shoot_site.py → dev-only screenshot harness (moved out of the scratchpad, not shipped)
docs/specs/              → this spec
tasks/plan.md, tasks/todo.md → Phase 2/3 outputs
.impeccable/surfaces/site-index-html.md → design direction contract (written in /impeccable)
```

Removed from the site: `player.css`, `player.js`, `fonts/archivo.woff2`, `fonts/doto.woff2`, the use of `img/busker.jpg` (the file is kept in git history and tags only), and all data placeholders.

## Code style

The site follows the existing repo idioms: tokens on `:root`, small single-purpose CSS blocks, comments that explain *why*, and no frameworks.

```css
/* Cards lift by transform only, so motion never triggers layout. */
.card{transition:transform .5s var(--ease), box-shadow .5s var(--ease)}
.card:hover,.card:focus-visible{transform:translateY(-2px)}
@media (prefers-reduced-motion:reduce){.card{transition:none}}
```

```python
def build(out_dir: str, now: dt.datetime) -> None:
    """Copy site/, fill {{YEAR}}, write CNAME. The site reads no nightly data."""
```

Conventions:
- **Naming:** kebab-case CSS classes and short semantic HTML: `<main>`, `<nav>`, `<a>` for cards, never `div`-buttons.
- **Motion:** compositor properties only (transform, opacity, and SVG attributes on small shapes). No layout animation.
- **Copy:** sentence case, no exclamation marks, no slogans.

## Testing strategy

| Level | What | Where / how |
|---|---|---|
| Unit | Build output: both pages exist; no `{{` left; CNAME written; no references to removed assets; external links are exactly the three URLs plus internal links | `scripts/test_build_site.py` (stdlib, existing pattern) |
| Static checks | HTML has one `<h1>` per page; every `<img>` has alt; no inline `style=` with secrets; total `_site/` weight within budget | Assertions in the same test file |
| Visual | Desktop 1440×900 and mobile 390×844, both pages: all three cards visible in the first viewport, no horizontal overflow, no console errors | `scripts/dev/shoot_site.py` with Playwright, captures into `.impeccable/review/v3/` |
| Accessibility | Keyboard order (cards reachable in ≤ 4 tabs), visible focus, WCAG AA contrast, `prefers-reduced-motion` honoured | Playwright checks plus manual review |
| Design quality | Impeccable detector once per round; finish review by the Impeccable reviewer | `impeccable detect`, then the review agent |
| Regression | README pipeline untouched | Existing suites (`test_render_readme`, `test_fetch_*`, `test_commit_booster`) still pass |

## Boundaries

- **Always:**
  - Run all test suites before committing.
  - Keep the page complete without JS.
  - Honour `prefers-reduced-motion`.
  - Self-host every asset.
  - Run `graphify update .` after code changes.
  - Commit the spec, plan and decisions with the code.
- **Ask first:**
  - The visual direction (from the inspiration list).
  - Approval of the new avatar artwork before it ships.
  - Adding any font family or JS dependency.
  - Changing `pages.yml` triggers or Pages settings.
  - Any change to card copy beyond this spec.
  - Pushing to `main` (deploying).
- **Never:**
  - Touch the README pipeline or `data/`.
  - Add analytics or trackers.
  - Ship third-party scripts.
  - Invent facts about Hasan or ActiveFactor.
  - Force-push or rewrite the tagged history.

## Success criteria

1. At **1440×900** and **390×844**, the name, role, avatar thumbnail and **all three cards are visible without scrolling** on the home page.
2. The home page contains **no slogan, no bio and no live data**. Its keywords are exactly the four listed.
3. The **ActiveFactor card states it is Hasan's company**.
4. About contains the large artwork, the bio and "Things I like: playing guitars, drums."
5. **Performance:**
   - Home page transfer ≤ **200 KB** (all assets, uncached).
   - **LCP < 1.2 s** on a local Lighthouse desktop run, **CLS < 0.02**.
   - JS ≤ 6 KB and not required.
6. **Accessibility:**
   - Lighthouse a11y score = 100.
   - All text passes WCAG AA.
   - Cards are reachable by keyboard with visible focus.
   - Reduced motion produces a fully static page.
7. **Motion:** at most **one** entrance moment plus hover/focus micro-interactions and the avatar's patch transformation. Everything is compositor-only.
8. All existing and new tests pass. The detector shows no unresolved non-system findings. The finish review returns **ship**.
9. `pages.yml` no longer redeploys on nightly `data/**` pushes; the site changes only when `site/**` changes.
10. `DESIGN.md` documents the v3 site world and keeps the README board sections intact.

## Open questions (owner input needed)

1. **Inspiration list (blocking).** Please send sites, designers or studios, products, album covers, movements or moods. For each, one line on *what* you like: type, spacing, colour, motion, illustration style or interaction. For the avatar, the illustrators or neo-brutal and cartoon styles you have in mind help most.
2. **Avatar likeness.** Should the drawing resemble *you* (send a reference photo), or stay an abstract guitarist figure that you adopt as your avatar?
3. **Patch transformation.** Do you picture the colour patches **slowly morphing on their own** (ambient), **responding to the cursor or scroll**, or **transforming once** when the page loads?
4. **ActiveFactor card wording.** Is "My company. Software systems for local businesses · San Diego" right, or would you like different words (e.g. "Founder")?
5. **Bio.** Keep the v2 sentence about the GitHub profile rebuilding itself nightly, or drop it now that the site shows no live data?
6. **www.yoshibase.com.** Will you add the Porkbun CNAME `www → yoshibase.github.io`, or should the spec treat `www` as out of scope?
