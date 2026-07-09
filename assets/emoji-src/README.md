# Swapping an icon

Every icon on the profile — the floating background tiles, the flags, the
category badges, star/fork/fire — is a real PNG in this folder, not a
unicode character. That's deliberate: unicode emoji render using whatever
color-emoji font the *viewer's* OS happens to have, which varies (Apple vs.
Google vs. Microsoft draw the same emoji differently, and some fonts are
missing them entirely). A PNG baked into the generated SVG looks identical
everywhere, every time.

To change one: replace the PNG (keep the same filename), then regenerate:

```
python3 scripts/generate_banner.py public-repo/assets/generated --emoji-src assets/emoji/studentemoji.png
python3 scripts/generate_cards.py public-repo/assets/generated --data-dir data
```

No code changes needed — every generator reads whatever's in this folder
at build time.

## What's in here

`computer / coffee / zap / robot / chart / cloud / wrench / tools / brain /
books / globe` — the 11 icons that float behind the name banner (header +
footer). Order/selection is in `scripts/tokens.py` → `BACKGROUND_EMOJIS`.

`flag-*` — one per country in `scripts/tokens.py` → `COUNTRY_FLAG_ICON`,
plus `flag-intl` as the default when a contributor's location is blank or
unrecognized. Resolved automatically per-repo from the contributor's GitHub
profile location by `fetch_trending.py`.

`snake / yellow-square / blue-diamond / blue-circle / crab / atom / ... ` —
category icons, one per keyword in `scripts/tokens.py` → `REPO_CATEGORY_ICON`
(matched against each repo's name + description — "agent" → brain, "rust" →
crab, and so on), plus `package` as the default.

`star / fork / fire` — used in the stat line and the "Trending Today" title.

`studentemoji.png` (in `assets/emoji/`, one level up — kept separate since
it's your photo, not a stock icon) — the 12th background tile. Reprocess it
any time with `scripts/process_emoji.py`, see SETUP.md.

## Adding a new category

1. Drop a PNG here (64×64 or so; anything square works, it gets scaled).
2. Add `("keyword", "your-filename-without-.png")` to `REPO_CATEGORY_ICON`
   in `scripts/tokens.py`.
3. Regenerate (commands above).

## About "JS animations"

Worth being direct about this one: there's no separate JavaScript-based
animation system here, and there can't be — GitHub strips `<script>` tags
out of README rendering entirely, so any JS-driven animation would just be
deleted before it ever reached a visitor's browser. All motion here (the
floating icons, the name shimmer) is SVG's own native animation (SMIL
`<animateTransform>`), which plays automatically with no script involved.
If there's a separate JS-based piece from your side that didn't make it
into this session, send it over and I'll fold in whatever it's doing —
but functionally, nothing JS-based can run in a README no matter how it's
built, so the icon-swap workflow above is the same one either way.

## License

Icons are [Twemoji](https://github.com/twitter/twemoji) (CC-BY 4.0).
Keep the attribution if you fork this.
