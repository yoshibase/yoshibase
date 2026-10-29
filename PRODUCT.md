# Product

<!-- impeccable:product-schema 1 -->

> Inferred from the repository and the owner's redesign brief (owner asked for fully autonomous work; no interview round was held). Items marked *(inferred)* are assumptions to confirm.

## Platform

web

## Users

- **Primary:** engineering directors, hiring managers and senior developers who land on github.com/yoshibase from a link, a PR or a search, and decide within seconds whether this engineer is worth a closer look. *(inferred from brief: "strike any corporate director or developer visitor")*
- **Secondary:** developers who return for the daily repo picks as a lightweight discovery feed.

## Product Purpose

The GitHub profile README of Hasan Ozdemir (`yoshibase`). It introduces him as a product engineer working across AI/ML, automation, knowledge management and data processing, and it proves craft by being a live, self-maintaining system: a nightly pipeline picks a repo of the day, ranks trending repos, regenerates every visual and commits the result.

Success: a visitor leaves knowing who he is, what he builds, how to reach him, and with the impression of a senior engineer who ships carefully made systems.

## Positioning

The picks are ranked by measured **star velocity** (stars gained since yesterday's snapshot), not by raw popularity. GitHub has no trending API, so the pipeline keeps its own day-over-day snapshot. The whole thing runs on the Python standard library inside GitHub Actions, with no third-party rendering services for its own assets.

## Operating Context

- Rendered by GitHub's Markdown sanitizer: no `style`, `class`, `<script>` or CSS in the README HTML. Allowed: `<picture>`/`<source media="(prefers-color-scheme)">`, `<img>`, `<a>`, `<table>`, `<details>`, `<sub>`, `<samp>`, `align`/`width`/`height` attributes.
- `<a><picture>` is split apart by GitHub's renderer, so linked visuals must be a plain `<a><img>`.
- Generated visuals are standalone SVG files shown through `<img>`: embedded fonts, gradients, filters, SMIL and CSS animation all work; links inside SVGs do not.
- Visitors see it in GitHub light or dark theme, on desktop (~830px content column) and on mobile.
- Nightly workflow `.github/workflows/daily-update.yml` (00:00 UTC): fetch → generate assets → render README → commit.

## Capabilities and Constraints

- `fetch_trending.py`: GitHub search plus a star snapshot gives the repo of the day (date-seeded pick from the top 5 by velocity, deduplicated over 30 days) and the top 3 trending repos, with owner-location flags and keyword categories.
- `render_readme.py`: fills the marker blocks in `README.template.md`; the repo-of-day grid must always be 30 consecutive UTC days, and missing days stay visible as gaps.
- `commit_booster.py` relies on: badge lines starting with `<a href="https://github.com` / `<a href="https://www.linkedin.com`, the `<br>\n\n<div align="center">` header spacer, and the `<!--SYNCED_AT_START-->` marker.
- The daily run must stay standard-library only.
- `fetch_contributions.py` reads the contribution calendar over GraphQL with the workflow token and fails soft to the last snapshot; no third-party widgets remain.

## Brand Commitments

- Name **Hasan Ozdemir**, handle **yoshibase**, LinkedIn `oz1127`.
- Role line: "Product Engineer · AI/ML · Data Systems".
- Self-description: a software evangelizer focused on AI/ML, automation, knowledge management and data processing, building tools that make a meaningful change.
- Tech stack: Python, JavaScript, TypeScript, PostgreSQL, Django, Docker, GitHub Actions, Git.
- Custom `studentemoji.png` avatar-style emoji exists in `assets/emoji/`.

## Evidence on Hand

- Live data: `data/repo_of_day.json` (30-day history), `data/trending.json`, `data/star_snapshot.json`.
- Contribution summary in `data/contributions.json` (12-month total, active days, longest run, weekly totals).
- No testimonials, employers, metrics or project case studies are in the repo; do not invent any.

## Product Principles

1. Prove, don't claim: the live pipeline is the portfolio piece.
2. Respect the visitor's ten seconds: identity, focus and contact come first.
3. Every pixel is generated from data and survives GitHub's sanitizer in both themes.
4. Fail soft: a missed fetch shows yesterday's data, never a broken README.
