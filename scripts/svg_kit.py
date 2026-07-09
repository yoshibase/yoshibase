"""
Hand-rolled SVG component kit.

Why not Satori/Tailwind-to-SVG: Satori can't emit animation, and self-playing
motion (floating emojis, name shimmer) is a hard requirement here. Plain
template-string SVG generation is exactly what capsule-render / readme-typing-svg
/ github-readme-stats do under the hood — it's the proven approach for this
exact problem (a Node/Python service that outputs a static image GitHub embeds
via <img>). This module is the shared "component library" so every generated
asset (banner, cards) looks like one system instead of one-off files.

GitHub strips <style>/<script>/inline style= from README *HTML*, but none of
that applies here: we are generating a standalone .svg *file* that GitHub
displays as an image. Everything inside the SVG — gradients, drop-shadow
filters, @font-face, SMIL animation — is untouched by that sanitizer.
"""
from __future__ import annotations
import base64
import os
import re
from xml.sax.saxutils import escape as _xml_escape

from tokens import FONTS_DIR, FONT_FACES

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)


def esc(text: str) -> str:
    """Escape text for safe use inside SVG element content."""
    if text is None:
        return ""
    return _xml_escape(str(text), {"'": "&apos;", '"': "&quot;"})


def truncate_to_width(text: str, font_size: float, max_width: float, avg_ratio: float = 0.56) -> str:
    """Cheap width estimate (no text-shaping engine available) — truncates
    with an ellipsis once the estimated pixel width would overflow max_width.
    Same heuristic technique used by most readme-badge generators."""
    if not text:
        return ""
    avg_char_w = font_size * avg_ratio
    max_chars = max(1, int(max_width / avg_char_w))
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 1)].rstrip() + "…"


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_FONT_CACHE: dict[str, str] = {}


def _font_base64(filename: str) -> str:
    if filename not in _FONT_CACHE:
        path = os.path.join(_REPO_ROOT, FONTS_DIR, filename)
        with open(path, "rb") as f:
            _FONT_CACHE[filename] = base64.b64encode(f.read()).decode("ascii")
    return _FONT_CACHE[filename]


def font_face_css(keys: list[str]) -> str:
    """Build @font-face blocks for the given FONT_FACES keys, embedded as
    base64 woff2 so rendering is identical everywhere the SVG is viewed."""
    blocks = []
    for key in keys:
        spec = FONT_FACES[key]
        b64 = _font_base64(spec["file"])
        blocks.append(
            f"""@font-face {{
        font-family: '{spec['family']}';
        font-weight: {spec['weight']};
        font-style: normal;
        src: url(data:font/woff2;base64,{b64}) format('woff2');
      }}"""
        )
    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# Defs: gradients + shadows
# ---------------------------------------------------------------------------

def linear_gradient_def(gid: str, stops: list[str], angle: int = 135) -> str:
    """stops: list of hex colors, evenly distributed. angle in degrees,
    135 = top-left to bottom-right (matches the original banner gradients)."""
    import math
    rad = math.radians(angle)
    x1 = 50 - 50 * math.cos(rad)
    y1 = 50 - 50 * math.sin(rad)
    x2 = 50 + 50 * math.cos(rad)
    y2 = 50 + 50 * math.sin(rad)
    n = len(stops)
    offsets = [f"{(i / (n - 1)) * 100:.1f}%" if n > 1 else "0%" for i in range(n)]
    stop_tags = "\n".join(
        f'      <stop offset="{off}" stop-color="{c}"/>' for off, c in zip(offsets, stops)
    )
    return f"""<linearGradient id="{gid}" x1="{x1:.1f}%" y1="{y1:.1f}%" x2="{x2:.1f}%" y2="{y2:.1f}%">
{stop_tags}
    </linearGradient>"""


def animated_linear_gradient_def(gid: str, stops: list[str], angle: int = 135, period: float = 6.0) -> str:
    """Same as linear_gradient_def but the stop positions sweep slowly —
    the 'shimmer' behind the name text. Self-playing, no hover needed."""
    base = linear_gradient_def(gid, stops, angle)
    # Inject a gentle animateTransform sweep on the gradient itself.
    anim = (
        f'<animateTransform attributeName="gradientTransform" type="translate" '
        f'values="-0.15 0; 0.15 0; -0.15 0" dur="{period}s" repeatCount="indefinite" '
        f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" additive="sum"/>'
    )
    return base.replace("</linearGradient>", f"  {anim}\n    </linearGradient>")


def drop_shadow_filter(fid: str, color: str, dy: float = 8, blur: float = 18, opacity: float = 0.35) -> str:
    return f"""<filter id="{fid}" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="{color}" flood-opacity="{opacity}"/>
    </filter>"""


def glow_filter(fid: str, color: str, blur: float = 10, opacity: float = 0.55) -> str:
    """Soft outward glow — stands in for the 'hover glow' since nothing in a
    README can be interactive. Always-on, so the card always reads as lifted."""
    return f"""<filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="{blur}" result="blur"/>
      <feFlood flood-color="{color}" flood-opacity="{opacity}" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>"""


# ---------------------------------------------------------------------------
# Cards / shapes
# ---------------------------------------------------------------------------

def rounded_card(x: float, y: float, w: float, h: float, rx: float, fill: str, filter_id: str | None = None, opacity: float = 1.0) -> str:
    f = f' filter="url(#{filter_id})"' if filter_id else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" opacity="{opacity}"{f}/>'


def text_el(x: float, y: float, content: str, font_key: str, size: float, color: str, anchor: str = "start", letter_spacing: float | None = None, extra: str = "") -> str:
    spec = FONT_FACES[font_key]
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{spec["family"]}" font-weight="{spec["weight"]}" '
        f'font-size="{size}" fill="{color}" text-anchor="{anchor}"{ls} {extra}>{esc(content)}</text>'
    )


def gradient_text_el(x: float, y: float, content: str, font_key: str, size: float, gradient_id: str, anchor: str = "middle", letter_spacing: float | None = None) -> str:
    spec = FONT_FACES[font_key]
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing is not None else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{spec["family"]}" font-weight="{spec["weight"]}" '
        f'font-size="{size}" fill="url(#{gradient_id})" text-anchor="{anchor}"{ls}>{esc(content)}</text>'
    )


def pill_badge(x: float, y: float, label: str, bg: str, fg: str, font_key: str = "mono_medium", size: float = 9.5, pad_x: float = 8, h: float = 17) -> str:
    text_w_est = len(label) * size * 0.62 + pad_x * 2
    return f"""<g transform="translate({x},{y})">
      <rect x="0" y="0" width="{text_w_est:.1f}" height="{h}" rx="{h/2:.1f}" fill="{bg}"/>
      {text_el(pad_x, h*0.68, label, font_key, size, fg, anchor="start")}
    </g>"""


# ---------------------------------------------------------------------------
# Mixed icon+text lines. Real emoji glyphs depend on the *viewer's* OS having
# a color-emoji font — true in effectively every modern browser, but we
# don't leave it to chance: every flag/category glyph is a real Twemoji PNG
# (same registered-once-in-defs, referenced-by-<use> pattern as the floating
# background field), so rendering is pixel-identical everywhere.
# ---------------------------------------------------------------------------

def icon_text_line(x: float, y: float, items: list[tuple], gap: float = 5) -> tuple[str, float]:
    """items: list of either
       ("icon", image_id, size)
       ("text", string, font_key, size, color)
    Lays them out left-to-right starting at (x, y) where y is the text
    baseline. Returns (svg_markup, total_width_estimate)."""
    parts = []
    cursor = x
    for item in items:
        kind = item[0]
        if kind == "icon":
            _, image_id, size = item
            icon_y = y - size * 0.78
            parts.append(f'<use href="#{image_id}" x="{cursor:.1f}" y="{icon_y:.1f}" width="{size}" height="{size}"/>')
            cursor += size + gap
        else:
            _, text, font_key, size, color = item
            parts.append(text_el(cursor, y, text, font_key, size, color, anchor="start"))
            cursor += len(text) * size * 0.56 + gap
    return "\n".join(parts), cursor - x


# ---------------------------------------------------------------------------
# Floating / tiled emoji background — self-playing SMIL drift, no hover.
# ---------------------------------------------------------------------------

_IMG_CACHE: dict[str, str] = {}


def _image_base64(path: str) -> str:
    if path not in _IMG_CACHE:
        with open(path, "rb") as f:
            _IMG_CACHE[path] = base64.b64encode(f.read()).decode("ascii")
    return _IMG_CACHE[path]


def emoji_image_defs(emoji_dir: str, names: list[str], custom_path: str | None = None) -> tuple[str, list[str]]:
    """Loads each PNG once and registers it in <defs> as a reusable <symbol>,
    so 30+ tiles/icons can each just <use> it (with their own width/height)
    instead of repeating base64 data. Note: <use> only honors width/height
    when the target is a <symbol> or <svg> — wrapping in <symbol> with a
    viewBox is what makes per-instance resizing actually work; a bare
    <image> ignores width/height set on the referencing <use>.
    Returns (defs_xml, ordered_ids)."""
    defs = []
    ids = []
    for name in names:
        path = os.path.join(emoji_dir, f"{name}.png")
        b64 = _image_base64(path)
        img_id = f"emoji-{name}"
        defs.append(
            f'<symbol id="{img_id}" viewBox="0 0 64 64">'
            f'<image width="64" height="64" href="data:image/png;base64,{b64}"/>'
            f'</symbol>'
        )
        ids.append(img_id)
    if custom_path and os.path.exists(custom_path):
        b64 = _image_base64(custom_path)
        defs.append(
            '<symbol id="emoji-custom" viewBox="0 0 256 256">'
            f'<image width="256" height="256" href="data:image/png;base64,{b64}"/>'
            '</symbol>'
        )
        ids.append("emoji-custom")
    return "\n".join(defs), ids


def floating_emoji_field(width: float, height: float, image_ids: list[str], seed: int = 0, opacity: float = 0.16, cols: int = 11, rows: int = 3) -> str:
    """Tiles emojis across width x height with matrix-style continuous falling.
    Each emoji rains down at constant speed, pre-scattered via negative begin
    so the field is always mid-animation — never static."""
    import random
    rnd = random.Random(seed)
    tiles = []
    cell_w, cell_h = width / cols, height / rows

    idx = 0
    for r in range(rows):
        for c in range(cols):
            img_id = image_ids[idx % len(image_ids)]
            idx += 1
            is_custom = img_id == "emoji-custom"
            cx = c * cell_w + cell_w / 2 + rnd.uniform(-cell_w * 0.15, cell_w * 0.15)
            cy = r * cell_h + cell_h / 2 + rnd.uniform(-cell_h * 0.2, cell_h * 0.2)
            size = rnd.uniform(20, 30) * (1.15 if is_custom else 1.0)
            fall_dist = height + size * 2
            dur = rnd.uniform(5.0, 9.0)
            delay = rnd.uniform(-dur, 0)
            rot = rnd.uniform(-6, 6)
            tile_opacity = opacity + 0.03 if is_custom else opacity

            anim = (
                f'<animateTransform attributeName="transform" type="translate" '
                f'values="0 {-size:.1f}; 0 {fall_dist:.1f}" dur="{dur:.2f}s" '
                f'begin="{delay:.2f}s" repeatCount="indefinite" '
                f'calcMode="linear" additive="sum"/>'
            )
            tiles.append(
                f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot:.1f})" opacity="{tile_opacity:.2f}">'
                f'<use href="#{img_id}" x="{-size/2:.1f}" y="{-size/2:.1f}" width="{size:.1f}" height="{size:.1f}"/>'
                f'{anim}</g>'
            )
    return "\n".join(tiles)


# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

def svg_document(width: int, height: int, defs: str, body: str, extra_attrs: str = "") -> str:
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" {extra_attrs}>
  <defs>
{defs}
  </defs>
{body}
</svg>"""


def style_block(css: str) -> str:
    return f"<style>\n{css}\n</style>"
