"""
Design tokens — single source of truth for every generated SVG asset.

The profile is drawn as a Solari split-flap departure board: near-black flap
boards carried as physical objects in both GitHub themes, warm-white signage
caps, one amber accent for what is moving today, and transit "line" bullets
for languages. Every generator imports from here so the README reads as one
instrument instead of a pile of one-off images.
"""

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
# The board never changes with the GitHub theme — it is an object, the way a
# real departures board is black in a sunlit hall and at midnight alike.
BOARD = {
    "ground": "#0F1012",       # board backplate between flaps
    "flap_top": "#1E2024",     # upper flap half (catches the light)
    "flap_bottom": "#191B1E",  # lower flap half
    "hinge": "#060607",        # split line across every flap
    "glyph": "#F3F0E8",        # warm white flap lettering
    "glyph_dim": "#9A9EA6",    # secondary flap lettering
    "desc": "#BEC2C9",         # mixed-case descriptions on the board
    "label": "#8C919A",        # printed labels on the board (≥4.5:1 on ground)
    "rule": "#26292E",         # printed hairlines on the board
    "amber": "#FFC233",        # Solari amber: today, velocity, primary action
    "amber_ink": "#1A1408",    # text set on amber
}

# The housing is graphite, so the same object reads on GitHub's white page
# and on its dark one. One file per asset (no light/dark pair) also keeps
# every board linkable: GitHub's renderer splits <a><picture> apart, but
# leaves a plain <a><img> intact.
HOUSING = {
    "body": "#24272C",
    "edge": "#363A41",
    "highlight": "#3B4047",
    "shadow": 0.22,
}

# ---------------------------------------------------------------------------
# Type — one signage family. Barlow Condensed for flaps and labels (it comes
# from highway/transit signage), Barlow for mixed-case descriptions.
# Advance widths for exact layout live in font_metrics.py.
# ---------------------------------------------------------------------------
FONTS_DIR = "fonts"

FONT_FACES = {
    "flap":  {"family": "Barlow Condensed", "weight": 600, "file": "barlow-condensed-600.woff2"},
    "label": {"family": "Barlow Condensed", "weight": 500, "file": "barlow-condensed-500.woff2"},
    "body":  {"family": "Barlow",           "weight": 500, "file": "barlow-500.woff2"},
}

# Characters a flap may cycle through before it settles.
FLAP_GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Flap cell sizes: (cell width, cell height, gap, font size)
FLAP_SIZES = {
    "xl": (60, 84, 5, 66),
    "vx": (46, 64, 4, 50),   # velocity: the focal number of a trending row
    "lg": (34, 48, 4, 37),
    "md": (25, 34, 3, 26),
    "sm": (19, 26, 3, 19),
}

# ---------------------------------------------------------------------------
# Profile content
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Hasan Ozdemir",
    "handle": "yoshibase",
    "role": "Product Engineer",
    # Laid out row-major over two columns: short areas left, long areas right.
    "focus": ["AI / ML", "Knowledge Management", "Automation", "Data Processing"],
    "github": "https://github.com/yoshibase",
    "linkedin": "https://www.linkedin.com/in/oz1127",
    "repos": "https://github.com/yoshibase?tab=repositories",
}

# Stack legend, drawn as transit line bullets in each technology's own colour.
STACK = [
    ("Python", "#3776AB"),
    ("TypeScript", "#3178C6"),
    ("JavaScript", "#F7DF1E"),
    ("Django", "#44B78B"),
    ("PostgreSQL", "#4169E1"),
    ("Docker", "#2496ED"),
    ("GitHub Actions", "#2088FF"),
    ("Git", "#F05032"),
]

# GitHub linguist colours — each language is a "line" on the board.
LANGUAGE_COLORS = {
    "Python": "#3572A5", "JavaScript": "#F1E05A", "TypeScript": "#3178C6",
    "Go": "#00ADD8", "Rust": "#DEA584", "C++": "#F34B7D", "C": "#555555",
    "C#": "#178600", "Java": "#B07219", "Kotlin": "#A97BFF", "Swift": "#F05138",
    "Objective-C": "#438EFF", "Ruby": "#701516", "PHP": "#4F5D95",
    "Shell": "#89E051", "HTML": "#E34C26", "CSS": "#663399", "Vue": "#41B883",
    "Svelte": "#FF3E00", "Dart": "#00B4AB", "Lua": "#000080", "Zig": "#EC915C",
    "Elixir": "#6E4A7E", "Haskell": "#5E5086", "Scala": "#C22D40",
    "Jupyter Notebook": "#DA5B0B", "Lean": "#7B68EE", "Perl": "#0298C3",
    "MDX": "#FCB32C", "Nix": "#7E7EFF", "OCaml": "#EF7A08", "R": "#198CE7",
}
DEFAULT_LANGUAGE_COLOR = "#6E7681"

# ---------------------------------------------------------------------------
# Flag + category resolution, used by fetch_trending.py. The data files keep
# these icon *names* (stable schema); the board renders flags as two-letter
# origin codes instead of emoji.
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


def origin_code(flag_icon: str | None) -> str:
    """'flag-kr' -> 'KR'; unknown or international -> '' (no origin shown)."""
    if not flag_icon or flag_icon == DEFAULT_FLAG_ICON or not flag_icon.startswith("flag-"):
        return ""
    return flag_icon[5:].upper()


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
