"""
Generates the board's static pieces as standalone SVGs (one per asset; the
graphite housing reads on both GitHub themes):

  board-header.svg            the split-flap name board (hero)
  board-footer.svg            last-rebuild plate
  section-trending.svg        section heading for the trending rows
  button-<name>.svg           signage buttons for the contact links

Self-contained: fonts embedded, no external service at render time.
Usage: python3 generate_banner.py <out_dir>
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import BOARD, FLAP_SIZES, HOUSING, PROFILE, STACK
from svg_kit import (
    FLAP_CSS, arrow_icon, board_defs, board_plate, flap_row, flap_width, font_face_css,
    housing, label_el, label_width, line_bullet, monogram, shadow_filter, svg_document,
)

W = 1200


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def board_date(now: dt.datetime) -> str:
    """'THU 29 OCT 2026' — the flap date strip."""
    return now.strftime("%a ") + str(now.day) + now.strftime(" %b %Y")


def _cells_that_fit(width: float, size: str) -> int:
    w, _h, gap, _fs = FLAP_SIZES[size]
    return int((width + gap) // (w + gap))


# ---------------------------------------------------------------------------
# Header board
# ---------------------------------------------------------------------------

def generate_header(now: dt.datetime) -> str:
    H = 512
    rnd = random.Random(now.date().isoformat())  # same day, same flip choreography
    px, py, pw, ph = 28, 26, W - 56, 456
    x0 = px + 36
    inner_w = pw - 72

    body = [housing(8, 6, W - 16, 492), board_plate(px, py, pw, ph)]

    # Top strip: mark, wordmark, live date.
    body.append(monogram(x0, py + 22, 30))
    body.append(label_el(x0 + 44, py + 43, PROFILE["handle"], 17, BOARD["glyph"]))
    date = board_date(now).upper()
    date_w = flap_width(len(date), "sm")
    date_x = px + pw - 36 - date_w
    body.append(label_el(date_x - 14, py + 43, "Updated", 16, BOARD["label"], anchor="end"))
    markup, _ = flap_row(date_x, py + 24, date, "sm", rnd, start=0.1, stagger=0.02, max_flips=5)
    body.append(markup)
    body.append(f'<rect x="{x0}" y="{py + 70}" width="{inner_w}" height="1" fill="{BOARD["rule"]}"/>')

    # Name — full-width row of xl flaps, blanks padding out the board.
    name_cells = _cells_that_fit(inner_w, "xl")
    markup, t = flap_row(x0, py + 92, PROFILE["name"], "xl", rnd, start=0.25, cells=name_cells, stagger=0.04)
    body.append(markup)

    # Role
    role_cells = _cells_that_fit(inner_w, "lg")
    markup, _ = flap_row(x0, py + 190, PROFILE["role"], "lg", rnd, start=0.55, cells=role_cells)
    body.append(markup)
    body.append(f'<rect x="{x0}" y="{py + 262}" width="{inner_w}" height="1" fill="{BOARD["rule"]}"/>')

    # Focus — two columns of md flap rows; the left one is sized to its
    # longest entry so "Knowledge Management" fits unabbreviated on the right.
    col_gap = 48
    left = PROFILE["focus"][0::2]
    left_cells = max(len(a) for a in left) + 2
    right_x = x0 + flap_width(left_cells, "md") + col_gap
    right_cells = _cells_that_fit(x0 + inner_w - right_x, "md")
    body.append(label_el(x0, py + 290, "Focus", 16, BOARD["amber"]))
    for i, area in enumerate(PROFILE["focus"]):
        cx, cells = (x0, left_cells) if i % 2 == 0 else (right_x, right_cells)
        cy = py + 302 + (i // 2) * 44
        markup, _ = flap_row(cx, cy, area, "md", rnd, start=0.85 + i * 0.12, cells=cells)
        body.append(markup)
    body.append(f'<rect x="{x0}" y="{py + 404}" width="{inner_w}" height="1" fill="{BOARD["rule"]}"/>')

    # Stack legend — printed line bullets along the bottom of the board.
    sy = py + 433
    body.append('<g class="t3">')  # tertiary: dropped when the board renders phone-narrow
    body.append(label_el(x0, sy, "Stack", 16, BOARD["amber"]))
    items = [(name, color, label_width(name, 17)) for name, color in STACK]
    sx = x0 + 80
    spacing = (px + pw - 36 - sx - sum(14 + 8 + w for _, _, w in items)) / (len(items) - 1)
    for name, color, w in items:
        body.append(line_bullet(sx, sy - 13, 14, color))
        body.append(label_el(sx + 22, sy, name, 17, BOARD["glyph_dim"]))
        sx += 14 + 8 + w + spacing
    body.append("</g>")

    defs = shadow_filter() + board_defs()
    css = font_face_css(["flap", "label"]) + FLAP_CSS
    title = f"{PROFILE['name']} — {PROFILE['role']}. Focus: {', '.join(PROFILE['focus'])}."
    return svg_document(W, H, defs, "\n".join(body), title, css)


# ---------------------------------------------------------------------------
# Footer plate
# ---------------------------------------------------------------------------

def generate_footer(now: dt.datetime) -> str:
    H = 150
    rnd = random.Random(now.date().isoformat() + "footer")
    px, py, pw, ph = 22, 18, W - 44, 100
    x0 = px + 28
    body = [housing(8, 6, W - 16, 124), board_plate(px, py, pw, ph)]

    body.append(monogram(x0, py + 30, 40))
    body.append(label_el(x0 + 56, py + 46, PROFILE["handle"], 17, BOARD["glyph"]))
    body.append(label_el(x0 + 56, py + 70, "Rebuilt nightly · GitHub Actions", 16, BOARD["label"], extra='class="t3"'))

    stamp = (str(now.day) + now.strftime(" %b %Y")).upper()
    sw = flap_width(len(stamp), "md")
    sx = px + pw - 28 - sw
    markup, _ = flap_row(sx, py + 46, stamp, "md", rnd, start=0.1, stagger=0.02, max_flips=5)
    body.append(markup)
    body.append(label_el(sx + sw, py + 34, f"Last rebuild · {now.strftime('%H:%M')} UTC", 16, BOARD["label"], anchor="end", extra='class="t3"'))

    # Centre: how the picks are chosen, in one line.
    mid = (x0 + 56 + 280 + sx - 40) / 2
    body.append(label_el(mid, py + 46, "Ranked by star velocity", 17, BOARD["glyph_dim"], anchor="middle", extra='class="t3"'))
    body.append(label_el(mid, py + 70, "Python stdlib · no external renderers", 16, BOARD["label"], anchor="middle", extra='class="t3"'))

    defs = shadow_filter() + board_defs()
    css = font_face_css(["flap", "label"]) + FLAP_CSS
    title = f"{PROFILE['handle']} — last rebuild {now.strftime('%d %b %Y %H:%M')} UTC"
    return svg_document(W, H, defs, "\n".join(body), title, css)


# ---------------------------------------------------------------------------
# Section heading — a slim plate, so it reads the same on both GitHub themes
# ---------------------------------------------------------------------------

def generate_section(title: str, meta: str) -> str:
    # Same housing geometry as the trending rows (no shadow), so the plate
    # and the rows under it read as one stacked board.
    H = 76
    px, py, pw, ph = 22, 12, W - 44, 52
    body = [
        housing(8, 0, W - 16, 76, rx=16, shadow=False),
        board_plate(px, py, pw, ph, rx=8),
        line_bullet(px + 24, py + 16, 18, BOARD["amber"]),
        label_el(px + 54, py + 33, title, 24, BOARD["glyph"]),
        label_el(px + pw - 24, py + 33, meta, 17, BOARD["label"], anchor="end", extra='class="t3"'),
    ]
    return svg_document(W, H, shadow_filter(), "\n".join(body), f"{title} — {meta}", font_face_css(["label"]) + FLAP_CSS)


# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------

BUTTONS = [
    ("linkedin", "LinkedIn", True),
    ("github", "GitHub", False),
    ("repositories", "Repositories", False),
]


def generate_button(label: str, primary: bool) -> str:
    size = 19
    tw = label_width(label, size)
    h = 52
    w = int(26 + tw + 14 + 14 + 26)
    if primary:
        fill, edge, ink = BOARD["amber"], "#C99512", BOARD["amber_ink"]
    else:
        fill, edge, ink = BOARD["ground"], HOUSING["highlight"], BOARD["glyph"]
    body = [
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 4}" rx="10" fill="{fill}" stroke="{edge}"/>',
        f'<rect x="1" y="{h / 2 - 2}" width="{w - 2}" height="1" fill="#000" opacity=".22"/>',
        label_el(26, h / 2 + 5, label, size, ink),
        arrow_icon(26 + tw + 14 + 7, h / 2 - 2, 11, ink, stroke=2.2),
    ]
    return svg_document(w, h, "", "\n".join(body), label, font_face_css(["label"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    now = utc_now()

    outputs = {
        "board-header.svg": generate_header(now),
        "board-footer.svg": generate_footer(now),
        "section-trending.svg": generate_section("Trending now", "Ranked by stars gained since yesterday"),
    }
    for slug, label, primary in BUTTONS:
        outputs[f"button-{slug}.svg"] = generate_button(label, primary)

    for name, svg in outputs.items():
        path = os.path.join(args.out_dir, name)
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path, len(svg), "bytes")


if __name__ == "__main__":
    main()
