# Implementation Plan: yoshibase.com v3

Spec: [docs/specs/yoshibase-site-v3.md](../docs/specs/yoshibase-site-v3.md) · Status: **awaiting owner approval**

## Overview
Rebuild yoshibase.com as a light, super-minimal, effortless personal site:
- **Home page:** name, role, four keywords, a small avatar thumbnail and exactly three cards (GitHub, LinkedIn, ActiveFactor, marked "My company").
- **About page:** the large avatar artwork, the bio and the things he likes.
- **Avatar:** a new, even more abstract guitarist illustration made of flat colour patches that transform once on load and then stay still.
- **Visual language:** comes from the owner's inspiration list (TypeSafe-style retro-OS windows and type, smooth neo-brutal components, Walkman-ish 2D device shapes, a TUI touch), finalised in `/impeccable`.

## Architecture decisions
- **Static HTML/CSS plus optional vanilla JS** with no dependencies. The page is complete without JS, and motion is compositor-only (spec: Boundaries, Success criteria 5–7).
- **The site reads no nightly data** (Q-answer 7). `build_site.py` only copies files, fills `{{YEAR}}` and writes CNAME, and the deploy triggers only on `site/**`.
- **The avatar is one hand-authored SVG** (no image-generation tool exists here), grouped into patches so the load transform can animate groups with transform/opacity/clip. It is used at both thumbnail and large size.
- **The design direction is set by the owner's `/impeccable` run** before any visual code. This plan schedules around that gate.
- **D1 (pending confirmation):** move the site to its own repo `yoshibase/yoshibase.com` with apex and www. All tasks keep `site/` self-contained, so the move is a late, mechanical task.

## Dependency graph
```
Gate A: spec + D1 approved ─┐
Gate B: /impeccable direction ─┤
                               ├─ T1 decouple build from data ── T2 dev harness + budgets
                               │                                   │
                               └─ T3 tokens/type foundation ───────┤
                                                                   ├─ T4 avatar artwork (Gate C: owner approves art)
                                                                   ├─ T5 home page (static) ── T6 about page (static)
                                                                   │            └──────────────┬──────────┘
                                                                   │                           T7 load sequence + avatar transform
                                                                   │                           T8 micro-interactions + header/footer polish
                                                                   └───────────────────────────T9 review + docs ── T10 repo split (D1) ── T11 deploy
```

## Task list

### Phase 0: Gates (owner)
- [ ] **Gate A:** spec approved and D1 confirmed or declined
- [ ] **Gate B:** owner runs `/impeccable`, which settles the direction contract (world, type, palette, first viewport, signature motion)

### Phase 1: Foundation
- [ ] T1 Decouple the build from nightly data
- [ ] T2 Dev verification harness and budget tests
- [ ] T3 Design tokens, fonts and base stylesheet

**Checkpoint 1:**
- All test suites pass, `_site/` builds, and the README pipeline is untouched.

### Phase 2: Core
- [ ] T4 Avatar artwork (highest risk, so it comes first). **Gate C:** owner approves the art.
- [ ] T5 Home page, static and complete without JS
- [ ] T6 About page, static

**Checkpoint 2:**
- All three cards are above the fold at 1440×900 and 390×844.
- a11y checks pass.
- The owner reviews the screenshots.

### Phase 3: Motion and polish
- [ ] T7 Load sequence: optional boot/TUI line, then name, then a one-time avatar patch transform, then cards settle
- [ ] T8 Micro-interactions and header/footer polish, with reduced-motion parity

**Checkpoint 3:**
- Budgets met: ≤ 200 KB, LCP < 1.2 s, CLS < 0.02, JS ≤ 6 KB.
- Lighthouse a11y score is 100.

### Phase 4: Review and ship
- [ ] T9 Detector, finish review, fix round, and DESIGN.md/PRODUCT.md updates
- [ ] T10 Repo split (only if D1 is confirmed)
- [ ] T11 Deploy and live verification (the owner approves the push)

**Checkpoint 4:**
- All spec success criteria are met.
- The finish review says "ship".
- The live site is verified on apex (and www if DNS is set).

## Risks and mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| The hand-authored SVG avatar misses "Juxtapoz / Japanese ad" fine-grained quality | High | Do T4 early. Show 2–3 small variations to the owner at Gate C before building around it, and keep the SVG layered so it is cheap to revise. |
| The minimal brief and the "extravagant, stunning" brief pull apart | Med | Spend the extravagance on the one load moment and on type scale. Everything else stays calm (spec R2, R3). |
| Retro-OS windows read as costume | Med | The windows must be functional: a nav window, a clock window, a card frame. None are decorative. |
| A neo-brutal shadow-and-border grammar fights "smooth and flat" | Med | Use 1.5px borders, 3–4px soft offsets, small radii and one shadow recipe, recorded in DESIGN.md. |
| D1 repo move breaks the live domain during cutover | High | Build and verify the new repo on `*.github.io` first. Move the CNAME last; the apex A records are unchanged. |
| Font weight blows the budget | Low | Use latin subsets and one variable display face plus one mono; ≤ 120 KB total. |

## Open questions
- D1: own repo? (spec, Open Questions 1)
- Boot-window intro: yes or no? (spec, Open Questions 2)
