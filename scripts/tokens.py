"""
Design tokens — single source of truth for every generated SVG asset.
Keep every generator importing from here so the whole profile reads as one
consistent system instead of a pile of one-off images.
"""

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
# Hero gradient — used on the name banner, matches the original capsule-render
# waving header/footer so the new pieces still feel like the same brand.
HERO_GRADIENT = ["#4158D0", "#C850C0", "#FFCC70"]

# Card gradient pool, lifted from the existing repo-of-day cards so the
# rebuilt version is a continuation of the palette, not a reset.
CARD_GRADIENTS = [
    ("#4158D0", "#C850C0"),
    ("#667eea", "#764ba2"),
    ("#f093fb", "#f5576c"),
    ("#4facfe", "#00f2fe"),
    ("#43e97b", "#38f9d7"),
    ("#fa709a", "#fee140"),
    ("#a18cd1", "#fbc2eb"),
    ("#fccb90", "#d57eeb"),
    ("#e0c3fc", "#8ec5fc"),
    ("#fad0c4", "#ffd1ff"),
    ("#b224ef", "#7579ff"),
    ("#fc5c7d", "#6a82fb"),
    ("#0fd850", "#f9f047"),
    ("#667db6", "#0082c8"),
    ("#ee9ca7", "#ffdde1"),
]

def gradient_for_index(i: int) -> tuple[str, str]:
    return CARD_GRADIENTS[i % len(CARD_GRADIENTS)]

# Theme surfaces — dark bg matches GitHub's own dark-mode panel color so
# generated images blend into the native theme instead of looking pasted on.
THEME = {
    "light": {
        "bg": "#FFFFFF",
        "panel": "#F6F8FA",
        "text_primary": "#1B1F27",
        "text_muted": "#57606A",
        "text_faint": "#8B949E",
        "border": "#D0D7DE",
    },
    "dark": {
        "bg": "#0D1117",
        "panel": "#161B22",
        "text_primary": "#F0F6FC",
        "text_muted": "#C9D1D9",
        "text_faint": "#8B949E",
        "border": "#30363D",
    },
}

# ---------------------------------------------------------------------------
# Type system — 3-tier: display (name/headers), body (labels/descriptions),
# mono (dates, star/fork counts, anything numeric-feeling).
# ---------------------------------------------------------------------------
FONTS_DIR = "fonts"

FONT_FACES = {
    "display_black": {"family": "Bricolage Grotesque", "weight": 800, "file": "bricolage-grotesque-800.woff2"},
    "display_bold":  {"family": "Bricolage Grotesque", "weight": 600, "file": "bricolage-grotesque-600.woff2"},
    "body_regular":  {"family": "Inter",                "weight": 400, "file": "inter-400.woff2"},
    "body_semibold": {"family": "Inter",                "weight": 600, "file": "inter-600.woff2"},
    "mono_regular":  {"family": "JetBrains Mono",        "weight": 400, "file": "jetbrains-mono-400.woff2"},
    "mono_medium":   {"family": "JetBrains Mono",        "weight": 500, "file": "jetbrains-mono-500.woff2"},
}

TYPE_SCALE = {
    "hero": 58,
    "section_title": 24,
    "card_title": 13,
    "card_body": 10.5,
    "meta": 9.5,
    "eyebrow": 11,
}

# ---------------------------------------------------------------------------
# Spacing scale (4px base, Tailwind-flavored)
# ---------------------------------------------------------------------------
SPACE = {k: v for k, v in zip(
    ["px1", "px2", "px3", "px4", "px5", "px6", "px8", "px10", "px12", "px16"],
    [4, 8, 12, 16, 20, 24, 32, 40, 48, 64],
)}

RADIUS = {"sm": 8, "md": 12, "lg": 16, "xl": 22, "pill": 999}

# Floating background emoji set (tiled behind name banner + footer).
# Rendered from real Twemoji PNG assets (assets/emoji-src/*.png) rather than
# unicode text glyphs — guarantees identical rendering on every platform
# instead of depending on the viewer's OS emoji font. 11 items per the brief;
# the 12th slot is the custom studentemoji.
# Twemoji graphics licensed CC-BY 4.0 — credit "Twemoji" in the repo README.
EMOJI_ASSETS_DIR = "assets/emoji-src"
BACKGROUND_EMOJIS = [
    "computer", "coffee", "zap", "robot", "chart",
    "cloud", "wrench", "tools", "brain", "books", "globe",
]
CUSTOM_EMOJI_SLOT = "studentemoji"  # rendered as an <image> tile from a separate source

# ---------------------------------------------------------------------------
# Flag + category icons used on repo-of-day / trending cards. Ported from
# daily_profile_boost.py's COUNTRY_FLAGS / REPO_EMOJI_MAP keyword tables —
# same coverage, just resolved to Twemoji asset names instead of raw unicode
# (unicode emoji depend on the *viewer's* OS having a color-emoji font; a
# real PNG doesn't). fetch_trending.py writes these icon names straight into
# the JSON data files, so generate_cards.py never needs its own translation
# table — the data already says exactly which asset to draw.
# ---------------------------------------------------------------------------

# keyword (matched against "owner location", lowercased) -> flag icon name
COUNTRY_FLAG_ICON = {
    "usa": "flag-us", "united states": "flag-us",
    "uk": "flag-uk", "united kingdom": "flag-uk",
    "germany": "flag-de", "france": "flag-fr",
    "india": "flag-in", "canada": "flag-ca",
    "australia": "flag-au", "japan": "flag-jp",
    "china": "flag-cn", "brazil": "flag-br",
    "netherlands": "flag-nl", "switzerland": "flag-ch",
    "sweden": "flag-se", "spain": "flag-es",
    "italy": "flag-it", "south korea": "flag-kr",
    "russia": "flag-ru", "singapore": "flag-sg",
    "norway": "flag-no", "denmark": "flag-dk",
    "finland": "flag-fi", "turkey": "flag-tr",
    "portugal": "flag-pt", "poland": "flag-pl",
}
DEFAULT_FLAG_ICON = "flag-intl"

# keyword (matched against "repo-name description", lowercased) -> category icon name
REPO_CATEGORY_ICON = [
    ("ai", "robot"), ("agent", "brain"), ("llm", "robot"), ("code", "zap"),
    ("data", "chart"), ("python", "snake"), ("js", "yellow-square"), ("ts", "blue-diamond"),
    ("go", "blue-circle"), ("rust", "crab"), ("react", "atom"), ("web", "globe"),
    ("app", "mobile"), ("cli", "computer"), ("dev", "tools"), ("tool", "wrench"),
    ("doc", "books"), ("wiki", "open-book"), ("learn", "grad-cap"), ("model", "dna"),
    ("api", "plug"), ("db", "cabinet"), ("cloud", "cloud"), ("sec", "locked"),
    ("test", "test-tube"), ("ui", "palette"), ("design", "sparkles"), ("game", "video-game"),
    ("math", "ruler"), ("viz", "chart-up"), ("search", "search"), ("chat", "speech"),
    ("image", "picture"), ("audio", "music"), ("video", "clapper"), ("ocr", "search"),
    ("parse", "page"),
]
DEFAULT_CATEGORY_ICON = "package"

# Everything generate_cards.py might need to draw, registered in <defs> up
# front regardless of whether a given day's data uses all of them — keeps
# the generator simple (no need to scan data first) at a small, fixed size
# cost (~1-4KB per icon).
ALL_CARD_ICONS = sorted(set(
    [DEFAULT_FLAG_ICON, DEFAULT_CATEGORY_ICON, "star", "fork", "fire"]
    + list(COUNTRY_FLAG_ICON.values())
    + [icon for _, icon in REPO_CATEGORY_ICON]
))
