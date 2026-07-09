"""
Generates the header + footer name banners, light + dark, as standalone
SVGs. Self-contained (fonts embedded, no external service calls at render
time — capsule-render.vercel.app is no longer a dependency).

Usage: python3 generate_banner.py <out_dir> [--emoji-src PATH]
"""
from __future__ import annotations
import argparse
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import HERO_GRADIENT, THEME, BACKGROUND_EMOJIS, SPACE, EMOJI_ASSETS_DIR, CARD_GRADIENTS, gradient_for_index
from svg_kit import (
    esc, font_face_css, linear_gradient_def, animated_linear_gradient_def,
    drop_shadow_filter, glow_filter, rounded_card, text_el, gradient_text_el,
    floating_emoji_field, emoji_image_defs, svg_document, style_block,
)

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import datetime as dt

NAME = "Hasan Ozdemir"
TAGLINE = "Product Engineer · AI/ML · Data Systems"
HANDLE_LINE = f"yoshibase · {dt.date.today().strftime('%b %d, %Y')}"

# Tech stack icons — same vibrant gradient, CSS-animated float
TECH_STACK = [
    ("Python", "#3776AB", "#FFFFFF"),
    ("JavaScript", "#F7DF1E", "#1B1F27"),
    ("TypeScript", "#3178C6", "#FFFFFF"),
    ("PostgreSQL", "#4169E1", "#FFFFFF"),
    ("Django", "#092E20", "#FFFFFF"),
    ("Docker", "#2496ED", "#FFFFFF"),
    ("GitHub Actions", "#2088FF", "#FFFFFF"),
    ("Git", "#F05032", "#FFFFFF"),
]


def generate_tech_stack(theme: str) -> str:
    """Card-style tech stack matching the stats card aesthetic.
    Each tech gets a gradient card with drop shadow and animated icon."""
    colors = THEME[theme]
    W = 1200
    H = 110
    card_w, card_h = 110, 80
    gap = 10
    n = len(TECH_STACK)
    total_w = n * card_w + (n - 1) * gap
    start_x = (W - total_w) / 2

    defs = [
        style_block(font_face_css(["display_bold", "body_regular", "body_semibold", "mono_regular"])),
    ]

    body = []
    for i, (name, bg, fg) in enumerate(TECH_STACK):
        x = start_x + i * (card_w + gap)
        y = 12
        g1, g2 = gradient_for_index(i)
        gid = f"techGrad{i}"
        sid = f"techShadow{i}"
        defs.append(f'<defs>{linear_gradient_def(gid, [g1, g2], angle=135)}</defs>')
        defs.append(f'<defs>{drop_shadow_filter(sid, g1, dy=4, blur=8, opacity=0.25 if theme=="light" else 0.4)}</defs>')

        # Card background
        body.append(f'<g transform="translate({x:.1f},{y})">')
        body.append(rounded_card(0, 0, card_w, card_h, 14, f"url(#{gid})", filter_id=sid))

        # Icon circle with SMIL float (nested <g> for safe animation)
        icon_cx = card_w / 2
        icon_cy = 28
        icon_r = 18
        # Outer group = static position, inner group = animated
        body.append(f'<g transform="translate({icon_cx:.1f},{icon_cy:.1f})">')
        body.append(f'<g>')
        body.append(
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0; 0 -3; 0 0" dur="{2.0 + i * 0.2:.2f}s" '
            f'begin="{i * 0.12:.2f}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" additive="sum"/>'
        )
        # White circle background for icon
        body.append(f'<circle r="{icon_r}" fill="rgba(255,255,255,0.22)"/>')
        # Tech initials
        body.append(
            f'<text y="1" font-family="Inter" font-weight="600" font-size="11" '
            f'fill="#FFFFFF" text-anchor="middle" dominant-baseline="middle">{esc(name[:2].upper())}</text>'
        )
        body.append('</g>')  # end animated group
        body.append('</g>')  # end static position group

        # Tech name label
        body.append(
            f'<text x="{card_w/2:.1f}" y="{card_h - 10}" font-family="Inter" font-weight="600" '
            f'font-size="9.5" fill="#FFFFFF" text-anchor="middle">{esc(name)}</text>'
        )
        body.append('</g>')

    return svg_document(W, H, "\n".join(defs), "\n".join(body))


def _wave_path(w: float, y: float, amp: float) -> str:
    return (
        f"M0,{y} C {w*0.25:.1f},{y-amp:.1f} {w*0.25:.1f},{y+amp:.1f} {w*0.5:.1f},{y:.1f} "
        f"S {w*0.75:.1f},{y-amp:.1f} {w:.1f},{y:.1f} L {w:.1f},{y+140:.1f} L 0,{y+140:.1f} Z"
    )


def generate(theme: str, variant: str, emoji_src: str | None) -> str:
    colors = THEME[theme]
    is_header = variant == "header"
    W = 1200
    H = 320 if is_header else 180
    margin = 6
    panel_w, panel_h = W - margin * 2, H - margin * 2
    rx = 28

    defs = []
    body = []

    defs.append(linear_gradient_def("waveGrad", HERO_GRADIENT, angle=100))
    defs.append(animated_linear_gradient_def("nameGrad", HERO_GRADIENT, angle=95, period=3))
    defs.append(drop_shadow_filter("panelShadow", "#4158D0", dy=10, blur=22, opacity=0.28 if theme == "light" else 0.5))
    defs.append(f"<clipPath id='panelClip'><rect x='{margin}' y='{margin}' width='{panel_w}' height='{panel_h}' rx='{rx}'/></clipPath>")

    font_keys = ["display_black", "display_bold", "body_regular", "body_semibold", "mono_regular"]
    defs.append(style_block(font_face_css(font_keys)))

    # base panel
    body.append(rounded_card(margin, margin, panel_w, panel_h, rx, colors["panel"], filter_id="panelShadow"))

    # clipped decorative layer: wave + floating emoji (no glow bubble — cleaner modern look)
    body.append("<g clip-path='url(#panelClip)'>")
    wave_y = panel_h * (0.62 if is_header else 0.5)
    body.append(f'<path d="{_wave_path(panel_w, wave_y, 26 if is_header else 16)}" fill="url(#waveGrad)" opacity="{0.16 if theme=="dark" else 0.12}" transform="translate({margin},{margin})"/>')

    emoji_dir = os.path.join(_REPO_ROOT, EMOJI_ASSETS_DIR)
    emoji_defs, emoji_ids = emoji_image_defs(emoji_dir, BACKGROUND_EMOJIS, custom_path=emoji_src)
    defs.append(emoji_defs)
    body.append(f'<g transform="translate({margin},{margin})">')
    rows = 3 if is_header else 2
    body.append(floating_emoji_field(panel_w, panel_h, emoji_ids, seed=1 if is_header else 2,
                                      opacity=1.0, rows=rows))
    body.append("</g>")
    body.append("</g>")  # end clip group

    if is_header:
        body.append(gradient_text_el(W/2, margin + panel_h*0.46, NAME, "display_black", 62, "nameGrad", anchor="middle", letter_spacing=0.5))
        body.append(text_el(W/2, margin + panel_h*0.46 + 34, TAGLINE.upper(), "body_semibold", 13, colors["text_muted"], anchor="middle", letter_spacing=3))
    else:
        body.append(gradient_text_el(W/2, margin + panel_h*0.56, NAME.upper(), "display_bold", 22, "nameGrad", anchor="middle", letter_spacing=6))
        body.append(text_el(W/2, margin + panel_h*0.56 + 24, HANDLE_LINE, "mono_regular", 11, colors["text_faint"], anchor="middle", letter_spacing=2))

    # thin inner border for crispness
    body.append(f'<rect x="{margin}" y="{margin}" width="{panel_w}" height="{panel_h}" rx="{rx}" fill="none" stroke="{colors["border"]}" stroke-width="1" opacity="0.6"/>')

    return svg_document(W, H, "\n".join(defs), "\n".join(body))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--emoji-src", default=None)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    for variant in ("header", "footer"):
        for theme in ("light", "dark"):
            svg = generate(theme, variant, args.emoji_src)
            out_path = os.path.join(args.out_dir, f"banner-{variant}-{theme}.svg")
            with open(out_path, "w") as f:
                f.write(svg)
            print("wrote", out_path, len(svg), "bytes")

    # Tech stack icons
    for theme in ("light", "dark"):
        svg = generate_tech_stack(theme)
        out_path = os.path.join(args.out_dir, f"tech-stack-{theme}.svg")
        with open(out_path, "w") as f:
            f.write(svg)
        print("wrote", out_path, len(svg), "bytes")


if __name__ == "__main__":
    main()
