# yoshibase.com v3 — tasks

Spec: docs/specs/yoshibase-site-v3.md · Plan: tasks/plan.md

## Gates
- [ ] Gate A — owner approves spec; D1 (own repo) confirmed/declined; boot-intro yes/no
- [ ] Gate B — owner runs `/impeccable` → direction contract in `.impeccable/surfaces/site-index-html.md`

## Phase 1 — Foundation
- [ ] **T1 Decouple build from nightly data** (S)
  - Acceptance:
    - `build_site.py` reads no `data/`; it only copies `site/`, fills `{{YEAR}}` and writes CNAME + .nojekyll.
    - `pages.yml` paths no longer include `data/**` or `fonts/**`.
  - Verify: `cd scripts && python3 test_build_site.py` (rewritten: no data, no `{{` left, CNAME, only the three external URLs).
  - Files: scripts/build_site.py, scripts/test_build_site.py, .github/workflows/pages.yml
- [ ] **T2 Dev verification harness + budgets** (S)
  - Acceptance:
    - `scripts/dev/shoot_site.py` captures both pages at 1440×900 and 390×844 and fails on console errors or horizontal overflow.
    - Tests assert `_site/` home transfer ≤ 200 KB and JS ≤ 6 KB.
  - Verify: run the harness on the current build; budget test passes or fails meaningfully.
  - Files: scripts/dev/shoot_site.py, scripts/test_build_site.py
- [ ] **T3 Tokens, fonts, base stylesheet** (M) — needs Gate B
  - Acceptance:
    - `site/site.css` has the tokens from the direction contract.
    - Fonts are self-hosted at ≤ 120 KB.
    - `player.css`, `player.js`, `archivo` and `doto` are removed.
    - Text selection, focus and scrollbar are themed.
  - Verify: build passes; the detector shows no font or contrast findings on an empty page.
  - Files: site/site.css, site/fonts/*, removals
- [ ] **Checkpoint 1** — all suites green; README pipeline tests unchanged

## Phase 2 — Core
- [ ] **T4 Avatar artwork** (M, high risk)
  - Acceptance:
    - `site/img/avatar.svg` is an even more abstract guitarist made of flat patches in the contract palette.
    - Patches are grouped for one load transform.
    - ≤ 40 KB, and crisp from 64 px to 640 px.
  - Verify: render at 64/160/640 px; the owner approves at **Gate C**.
  - Files: site/img/avatar.svg (+ 2 variations for review in .impeccable/review/)
- [ ] **T5 Home page (static)** (M)
  - Acceptance:
    - Header/nav, then name and role, then the four keywords, the avatar thumbnail and exactly three cards (ActiveFactor reads "My company. AI driven automation systems for small businesses"), then the footer.
    - No slogan, bio or data.
    - All three cards are above the fold on both viewports.
  - Verify: harness screenshots; keyboard tab order reaches the cards in ≤ 4 tabs.
  - Files: site/index.html, site/site.css
- [ ] **T6 About page (static)** (S)
  - Acceptance:
    - Large avatar, the bio without the nightly-rebuild sentence, "Things I like: playing guitars, drums.", and the three links.
  - Verify: harness screenshots; one h1; alt text present.
  - Files: site/about.html, site/site.css
- [ ] **Checkpoint 2** — owner reviews screenshots of both pages

## Phase 3 — Motion & polish
- [ ] **T7 Load sequence** (M)
  - Acceptance:
    - One orchestrated entrance of ≤ 1.6 s: an optional boot/TUI line, then the name, then the avatar patches transforming once into the final art, then the cards settling.
    - The page is still afterwards.
    - Reduced motion shows the final state immediately.
  - Verify: frame captures at 0 / 400 / 900 / 1600 ms; performance trace stays ≥ 55 fps; no CLS.
  - Files: site/site.js, site/site.css, site/img/avatar.svg
- [ ] **T8 Micro-interactions + header/footer polish** (S)
  - Acceptance:
    - Card hover/focus lift, nav indicator, optional live clock or blinking cursor, footer detail.
    - All compositor-only, with reduced-motion parity.
  - Verify: Lighthouse a11y 100, LCP < 1.2 s, CLS < 0.02; JS ≤ 6 KB.
  - Files: site/site.js, site/site.css, site/index.html
- [ ] **Checkpoint 3** — budgets and a11y met

## Phase 4 — Review & ship
- [ ] **T9 Review + docs** (M)
  - Acceptance:
    - Detector run once.
    - Finish reviewer verdict "ship" after at most two fix rounds.
    - DESIGN.md site section rewritten (README sections intact); PRODUCT.md updated.
  - Verify: reviewer report; docs diff.
  - Files: site/*, DESIGN.md, .impeccable/design.json, PRODUCT.md
- [ ] **T10 Repo split** (M) — only if D1 confirmed
  - Acceptance:
    - New public repo `yoshibase/yoshibase.com` with site/, build, tests and a Pages workflow.
    - Verified on github.io, then CNAME `yoshibase.com` moved.
    - Profile repo cleaned of site/, build_site and pages.yml.
  - Verify: both repos' tests pass; profile README pipeline unchanged.
  - Files: new repo; profile repo removals
- [ ] **T11 Deploy + live verification** (S) — the owner approves the push
  - Acceptance:
    - https://yoshibase.com serves v3 with HTTPS enforced.
    - www redirects to the apex once the owner adds `www CNAME yoshibase.github.io` at Porkbun.
  - Verify: curl status codes, live screenshots, Pages cert state.
- [ ] **Checkpoint 4** — every spec success criterion checked off
