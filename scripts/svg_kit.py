"""
Hand-rolled SVG component kit for the split-flap board.

Why plain template strings: the README shows each asset through <img>, so
GitHub's HTML sanitizer never touches what is *inside* the .svg — embedded
@font-face, CSS keyframes and media queries all survive. Template-string
generation is what capsule-render / github-readme-stats do too, and it keeps
the nightly run on the Python standard library.

Motion: every flap cell flips through a few random glyphs and settles, once
per page load. The settled glyph is visible by default and only *hidden*
while its cell is still flipping, so a renderer without CSS animation (or a
visitor with prefers-reduced-motion) sees the finished board, never blanks.
"""
from __future__ import annotations
import base64
import os
import random
from xml.sax.saxutils import escape as _xml_escape

from font_metrics import ADVANCES
from tokens import BOARD, FLAP_GLYPHS, FLAP_SIZES, FONT_FACES, FONTS_DIR, HOUSING

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)


def esc(text) -> str:
    """Escape text for safe use inside SVG element content or attributes."""
    if text is None:
        return ""
    return _xml_escape(str(text), {"'": "&apos;", '"': "&quot;"})


def num(v: float) -> str:
    """Compact coordinate formatting — keeps the generated files small."""
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


# ---------------------------------------------------------------------------
# Text measurement (exact advances from font_metrics.py)
# ---------------------------------------------------------------------------

def _advance(ch: str, face: str) -> float:
    table = ADVANCES[face]
    if ch in table:
        return table[ch]
    # Wide scripts fall back to the system CJK face at roughly a full em.
    return 1000 if ord(ch) >= 0x2E80 else 560


def text_width(text: str, face: str, size: float, letter_spacing: float = 0) -> float:
    if not text:
        return 0.0
    return sum(_advance(c, face) for c in text) * size / 1000 + letter_spacing * max(0, len(text) - 1)


def fit(text: str, face: str, size: float, max_w: float, letter_spacing: float = 0) -> str:
    """Truncate with an ellipsis so the measured width never exceeds max_w."""
    text = " ".join((text or "").split())
    if text_width(text, face, size, letter_spacing) <= max_w:
        return text
    while text and text_width(text + "…", face, size, letter_spacing) > max_w:
        text = text[:-1]
    return text.rstrip(" ,.;:-—·") + "…"


def wrap(text: str, face: str, size: float, max_w: float, max_lines: int) -> list[str]:
    """Greedy word wrap on measured widths; the last line is ellipsized."""
    words = " ".join((text or "").split()).split(" ")
    if words == [""]:
        return []
    lines: list[str] = []
    cur = ""
    for i, w in enumerate(words):
        trial = f"{cur} {w}".strip()
        if text_width(trial, face, size) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        cur = w
        if len(lines) == max_lines - 1:
            cur = " ".join(words[i:])
            break
    if cur:
        lines.append(cur)
    lines = lines[:max_lines]
    if lines:
        lines[-1] = fit(lines[-1], face, size, max_w)
    return lines


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_FONT_CACHE: dict[str, str] = {}


def _font_base64(filename: str) -> str:
    if filename not in _FONT_CACHE:
        with open(os.path.join(_REPO_ROOT, FONTS_DIR, filename), "rb") as f:
            _FONT_CACHE[filename] = base64.b64encode(f.read()).decode("ascii")
    return _FONT_CACHE[filename]


def font_face_css(keys: list[str]) -> str:
    """@font-face blocks with base64 woff2, so rendering is identical
    everywhere the SVG is viewed."""
    blocks = []
    for key in keys:
        spec = FONT_FACES[key]
        blocks.append(
            f"@font-face{{font-family:'{spec['family']}';font-weight:{spec['weight']};"
            f"src:url(data:font/woff2;base64,{_font_base64(spec['file'])}) format('woff2')}}"
        )
    return "\n".join(blocks)


def text_el(x: float, y: float, content: str, face: str, size: float, color: str,
            anchor: str = "start", letter_spacing: float | None = None, extra: str = "") -> str:
    spec = FONT_FACES[face]
    ls = f' letter-spacing="{num(letter_spacing)}"' if letter_spacing else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{num(x)}" y="{num(y)}" font-family="{spec["family"]}" font-weight="{spec["weight"]}" '
        f'font-size="{num(size)}" fill="{color}"{a}{ls}{" " + extra if extra else ""}>{esc(content)}</text>'
    )


def label_el(x: float, y: float, content: str, size: float, color: str, anchor: str = "start",
             extra: str = "") -> str:
    """Printed signage label: condensed caps with open tracking."""
    return text_el(x, y, content.upper(), "label", size, color, anchor, letter_spacing=round(size * 0.14, 2), extra=extra)


def label_width(content: str, size: float) -> float:
    return text_width(content.upper(), "label", size, round(size * 0.14, 2))


# ---------------------------------------------------------------------------
# Split-flap cells
# ---------------------------------------------------------------------------

FLAP_CSS = """
.fi{opacity:0;animation:fl-on .07s steps(1,end)}
.ff{animation:fl-hold 0s steps(1,end)}
.fp{opacity:0;transform-box:fill-box;transform-origin:50% 100%;animation:fl-flip .07s cubic-bezier(.5,0,1,1) 0s 0}
@keyframes fl-on{from,to{opacity:1}}
@keyframes fl-hold{from,to{opacity:0}}
@keyframes fl-flip{from{opacity:.95;transform:scaleY(1)}to{opacity:.35;transform:scaleY(.04)}}
@media (prefers-reduced-motion:reduce){.fi,.fp{display:none}.ff{animation:none}}
@media (max-width:600px){.t3{display:none}}
"""

FLIP_STEP = 0.07  # seconds per flap — matches the .07s keyframe durations


def board_defs() -> str:
    """Shared paths every flap <use>s: halves, hinge and axle pins, per size."""
    parts = []
    for key, (w, h, _gap, _fs) in FLAP_SIZES.items():
        r = 3 if w >= 30 else 2
        half = h / 2
        parts.append(
            f'<g id="flap-{key}">'
            f'<rect width="{w}" height="{h}" rx="{r}" fill="{BOARD["flap_bottom"]}"/>'
            f'<path d="M0 {half}V{r}Q0 0 {r} 0H{w - r}Q{w} 0 {w} {r}V{half}Z" fill="{BOARD["flap_top"]}"/>'
            f'</g>'
            f'<g id="hinge-{key}">'
            f'<rect y="{num(half - 0.6)}" width="{w}" height="1.2" fill="{BOARD["hinge"]}"/>'
            f'<rect x="-1" y="{num(half - 2.5)}" width="2" height="5" rx="1" fill="#2E3136"/>'
            f'<rect x="{w - 1}" y="{num(half - 2.5)}" width="2" height="5" rx="1" fill="#2E3136"/>'
            f'</g>'
            f'<path id="flip-{key}" d="M0 {half}V{r}Q0 0 {r} 0H{w - r}Q{w} 0 {w} {r}V{half}Z" fill="#2A2D32"/>'
        )
    return "\n".join(parts)


def flap_width(n_cells: int, size: str) -> float:
    w, _h, gap, _fs = FLAP_SIZES[size]
    return n_cells * w + max(0, n_cells - 1) * gap


def flap_row(x: float, y: float, text: str, size: str, rnd: random.Random | None,
             start: float = 0.0, color: str | None = None, cells: int | None = None,
             stagger: float = 0.032, min_flips: int = 3, max_flips: int = 8) -> tuple[str, float]:
    """A run of flap cells spelling `text` (upper-cased), padded with blank
    cells to `cells`. Pass rnd=None for a static row. Returns (markup, end_time)."""
    w, h, gap, fs = FLAP_SIZES[size]
    color = color or BOARD["glyph"]
    text = text.upper()
    if cells is not None:
        text = text[:cells].ljust(cells)
    spec = FONT_FACES["flap"]
    baseline = h / 2 + fs * 0.35  # Barlow caps are ~0.7em tall: centre them on the hinge
    font_attr = f'font-family="{spec["family"]}" font-weight="{spec["weight"]}" font-size="{fs}" text-anchor="middle"'
    out = [f'<g transform="translate({num(x)},{num(y)})" {font_attr}>']
    end = start
    for i, ch in enumerate(text):
        cx = i * (w + gap)
        out.append(f'<g transform="translate({num(cx)},0)"><use href="#flap-{size}"/>')
        gx, gy = num(w / 2), num(baseline)
        if ch.strip() and rnd is not None:
            t0 = start + i * stagger
            flips = rnd.randint(min_flips, max_flips)
            pool = [g for g in FLAP_GLYPHS if g != ch]
            for j in range(flips):
                out.append(
                    f'<text class="fi" x="{gx}" y="{gy}" fill="{color}" '
                    f'style="animation-delay:{t0 + j * FLIP_STEP:.2f}s">{esc(rnd.choice(pool))}</text>'
                )
            settle = t0 + flips * FLIP_STEP
            out.append(
                f'<text class="ff" x="{gx}" y="{gy}" fill="{color}" '
                f'style="animation-duration:{settle:.2f}s">{esc(ch)}</text>'
            )
            out.append(
                f'<use class="fp" href="#flip-{size}" '
                f'style="animation-delay:{t0:.2f}s;animation-iteration-count:{flips}"/>'
            )
            end = max(end, settle)
        elif ch.strip():
            out.append(f'<text x="{gx}" y="{gy}" fill="{color}">{esc(ch)}</text>')
        out.append(f'<use href="#hinge-{size}"/></g>')
    out.append("</g>")
    return "".join(out), end


# ---------------------------------------------------------------------------
# Authored icons (no emoji, no font glyphs)
# ---------------------------------------------------------------------------

def star_icon(x: float, y: float, size: float, color: str) -> str:
    """Five-point star, outer radius size/2, centred on (x, y)."""
    import math
    pts = []
    for k in range(10):
        r = size / 2 if k % 2 == 0 else size * 0.2
        a = math.radians(-90 + k * 36)
        pts.append(f"{x + r * math.cos(a):.1f},{y + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'


def fork_icon(x: float, y: float, size: float, color: str) -> str:
    """Git-fork glyph: two branch nodes joining into one, centred on (x, y)."""
    s = size / 16
    sw = num(1.6 * s)
    return (
        f'<g transform="translate({num(x - 8 * s)},{num(y - 8 * s)})" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round">'
        f'<circle cx="{num(4 * s)}" cy="{num(3 * s)}" r="{num(2 * s)}"/>'
        f'<circle cx="{num(12 * s)}" cy="{num(3 * s)}" r="{num(2 * s)}"/>'
        f'<circle cx="{num(8 * s)}" cy="{num(13 * s)}" r="{num(2 * s)}"/>'
        f'<path d="M{num(4 * s)} {num(5 * s)}v{num(1.5 * s)}q0 {num(2 * s)} {num(2 * s)} {num(2 * s)}h{num(4 * s)}'
        f'q{num(2 * s)} 0 {num(2 * s)} {num(-2 * s)}v{num(-1.5 * s)}M{num(8 * s)} {num(8.5 * s)}v{num(2.5 * s)}"/>'
        f'</g>'
    )


def arrow_icon(x: float, y: float, size: float, color: str, stroke: float = 2) -> str:
    """North-east arrow (external link), centred on (x, y)."""
    h = size / 2
    return (
        f'<path d="M{num(x - h)} {num(y + h)}L{num(x + h)} {num(y - h)}M{num(x - h * 0.3)} {num(y - h)}'
        f'H{num(x + h)}V{num(y + h * 0.3)}" fill="none" stroke="{color}" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def up_arrow_icon(x: float, y: float, size: float, color: str) -> str:
    """Solid up-pointing triangle: 'gaining', centred on (x, y)."""
    h = size / 2
    return f'<path d="M{num(x)} {num(y - h)}L{num(x + h)} {num(y + h * 0.8)}H{num(x - h)}Z" fill="{color}"/>'


def line_bullet(x: float, y: float, size: float, color: str) -> str:
    """Transit line bullet: rounded square in the line colour, top-left at (x, y)."""
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(size)}" height="{num(size)}" rx="{num(size * 0.28)}" '
        f'fill="{color}"/>'
    )


def monogram(x: float, y: float, size: float) -> str:
    """The yoshibase mark: a single split flap showing a Y, top-left at (x, y)."""
    s = size
    half = s / 2
    r = s * 0.16
    return (
        f'<g transform="translate({num(x)},{num(y)})">'
        f'<rect width="{num(s)}" height="{num(s)}" rx="{num(r)}" fill="{BOARD["amber"]}"/>'
        f'<path d="M{num(s * 0.27)} {num(s * 0.2)}L{num(half)} {num(s * 0.5)}L{num(s * 0.73)} {num(s * 0.2)}'
        f'M{num(half)} {num(s * 0.5)}V{num(s * 0.8)}" fill="none" stroke="{BOARD["amber_ink"]}" '
        f'stroke-width="{num(s * 0.13)}" stroke-linecap="square"/>'
        f'<rect y="{num(half - s * 0.02)}" width="{num(s)}" height="{num(max(1, s * 0.04))}" '
        f'fill="{BOARD["amber_ink"]}" opacity=".55"/>'
        f'</g>'
    )


# ---------------------------------------------------------------------------
# Housing + document
# ---------------------------------------------------------------------------

def shadow_filter() -> str:
    return (
        '<filter id="housing-shadow" x="-5%" y="-10%" width="110%" height="130%">'
        f'<feDropShadow dx="0" dy="6" stdDeviation="9" flood-color="#000" flood-opacity="{HOUSING["shadow"]}"/>'
        '</filter>'
    )


def housing(x: float, y: float, w: float, h: float, rx: float = 18, shadow: bool = True) -> str:
    """Graphite housing with a 1px top highlight, wrapping a board.
    With shadow, pair with shadow_filter() registered as 'housing-shadow'."""
    f = ' filter="url(#housing-shadow)"' if shadow else ""
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" '
        f'fill="{HOUSING["body"]}" stroke="{HOUSING["edge"]}"{f}/>'
        f'<path d="M{num(x + rx)} {num(y + 1.5)}H{num(x + w - rx)}" stroke="{HOUSING["highlight"]}" '
        f'stroke-width="1"/>'
    )


def board_plate(x: float, y: float, w: float, h: float, rx: float = 10) -> str:
    """The recessed black backplate the flaps sit on."""
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" fill="{BOARD["ground"]}"/>'
        f'<rect x="{num(x + 0.5)}" y="{num(y + 0.5)}" width="{num(w - 1)}" height="{num(h - 1)}" rx="{rx}" '
        f'fill="none" stroke="#000" stroke-opacity=".6"/>'
    )


def svg_document(width: int, height: int, defs: str, body: str, title: str, css: str = "") -> str:
    style = f"<style>{css}</style>" if css else ""
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">'
        f"<title>{esc(title)}</title>{style}<defs>{defs}</defs>\n{body}\n</svg>\n"
    )
