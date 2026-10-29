"""
Generates the daily board pieces as standalone SVGs:

  today-pick.svg               repo of the day (today's departure)
  trending-<n>.svg             one row per trending repo (n = 1..3)

Each piece is its own file so render_readme.py can wrap it in a link —
a single combined image could never be clicked through to a repo.

Usage: python3 generate_cards.py <out_dir> [--data-dir DIR]
Reads data/repo_of_day.json and data/trending.json if present, otherwise
falls back to sample_data.py so the pipeline always produces something.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import BOARD, DEFAULT_LANGUAGE_COLOR, FLAP_SIZES, LANGUAGE_COLORS, origin_code
from sample_data import REPO_OF_DAY, TRENDING
from repo_of_day_grid import build_repo_of_day_grid, profile_today
from repo_paths import resolve_data_dir
from svg_kit import (
    FLAP_CSS, board_defs, board_plate, fit, flap_row, flap_width, font_face_css, fork_icon,
    housing, label_el, label_width, line_bullet, shadow_filter, star_icon, svg_document,
    text_el, up_arrow_icon, wrap,
)

W = 1200
TRENDING_COUNT = 3


def load_json_or(path: str | None, fallback):
    if path and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return fallback


def _cells_that_fit(width: float, size: str) -> int:
    w, _h, gap, _fs = FLAP_SIZES[size]
    return int((width + gap) // (w + gap))


def _defs() -> str:
    return shadow_filter() + board_defs()


def meta_item(x: float, y: float, kind: str, value: str, size: float = 18, color: str | None = None) -> tuple[str, float]:
    """One 'icon + value' unit; kind is 'lang', 'star' or 'fork'. Returns (markup, width)."""
    color = color or BOARD["glyph_dim"]
    icon = 15
    if kind == "lang":
        mark = line_bullet(x, y - icon + 1.5, icon, LANGUAGE_COLORS.get(value, DEFAULT_LANGUAGE_COLOR))
    elif kind == "star":
        mark = star_icon(x + icon / 2, y - icon / 2 + 1, icon + 1, BOARD["glyph_dim"])
    else:
        mark = fork_icon(x + icon / 2, y - icon / 2 + 1, icon, BOARD["glyph_dim"])
    tx = x + icon + 8
    return mark + label_el(tx, y, value, size, color), icon + 8 + label_width(value, size)


# ---------------------------------------------------------------------------
# Repo of the day
# ---------------------------------------------------------------------------

def generate_today_pick(entry: dict, today: dt.date) -> str:
    rnd = random.Random(today.isoformat() + "pick")
    x0 = 22 + 30
    inner_w = W - 44 - 60
    # The card grows with its description (0-2 lines) instead of leaving a hole.
    desc_lines = wrap(entry.get("desc") or "", "body", 21, inner_w * 0.78, 2) if "repo" in entry else []
    shift = (2 - max(1, len(desc_lines))) * 30
    H = 330 - shift
    px, py, pw, ph = 22, 20, W - 44, 278 - shift
    right = px + pw - 30
    body = [housing(8, 6, W - 16, 306 - shift), board_plate(px, py, pw, ph)]

    # Title strip
    body.append(line_bullet(x0, py + 22, 18, BOARD["amber"]))
    body.append(label_el(x0 + 30, py + 38, "Repo of the day", 22, BOARD["glyph"]))
    date = (today.strftime("%a ") + str(today.day) + today.strftime(" %b")).upper()
    dw = flap_width(len(date), "sm")
    markup, _ = flap_row(right - dw, py + 18, date, "sm", rnd, start=0.1, stagger=0.02, max_flips=5)
    body.append(markup)
    body.append(f'<rect x="{x0}" y="{py + 60}" width="{inner_w}" height="1" fill="{BOARD["rule"]}"/>')

    if "repo" not in entry:
        body.append(label_el(x0, py + 130, "No departure today — the board fills in after the nightly run", 22, BOARD["label"]))
        title = "Repo of the day: no pick recorded yet"
        return svg_document(W, H, _defs(), "\n".join(body), title, font_face_css(["flap", "label"]) + FLAP_CSS)

    # Repository name on a full-width flap row.
    cells = _cells_that_fit(inner_w, "md")
    name = entry["repo"]
    flap_name = name if len(name) <= cells else name[: cells - 1] + "-"
    markup, _ = flap_row(x0, py + 80, flap_name, "md", rnd, start=0.3, cells=cells, stagger=0.025)
    body.append(markup)

    # Description
    for i, line in enumerate(desc_lines):
        body.append(text_el(x0, py + 156 + i * 30, line, "body", 21, BOARD["desc"], extra='class="t3"'))
    if not desc_lines:
        body.append(text_el(x0, py + 156, "No description on GitHub yet — open the repository for the README.",
                            "body", 21, BOARD["label"], extra='class="t3"'))

    # Meta row
    my = py + 248 - shift
    body.append(f'<rect x="{x0}" y="{my - 30}" width="{inner_w}" height="1" fill="{BOARD["rule"]}"/>')
    cx = x0
    for kind, value in (("lang", entry.get("lang")), ("star", entry.get("stars")), ("fork", entry.get("forks"))):
        if not value:
            continue
        markup, w = meta_item(cx, my, kind, value)
        body.append(markup)
        cx += w + 30
    origin = origin_code(entry.get("flag"))
    if origin:
        body.append(label_el(cx, my, f"Origin {origin}", 18, BOARD["label"]))

    delta = entry.get("stars_today")
    if delta and delta != "+0":
        txt = f"{delta} stars since yesterday"
        tw = label_width(txt, 18)
        body.append(up_arrow_icon(right - tw - 14, my - 6.5, 12, BOARD["amber"]))
        body.append(label_el(right, my, txt, 18, BOARD["amber"], anchor="end"))

    css = font_face_css(["flap", "label", "body"]) + FLAP_CSS
    title = f"Repo of the day: {name} — {entry.get('desc') or ''}"
    return svg_document(W, H, _defs(), "\n".join(body), title, css)


# ---------------------------------------------------------------------------
# Trending rows
# ---------------------------------------------------------------------------

def generate_trending_row(entry: dict, rank: int, today: dt.date) -> str:
    rnd = random.Random(f"{today.isoformat()}trend{rank}")
    # No drop shadow: the rows stack under the section plate as one board.
    H = 160
    px, py, pw, ph = 22, 12, W - 44, 136
    right = px + pw - 28
    body = [housing(8, 0, W - 16, 160, rx=16, shadow=False), board_plate(px, py, pw, ph)]

    # Rank — two lg flaps, vertically centred.
    _w, lh, _g, _fs = FLAP_SIZES["lg"]
    markup, _ = flap_row(px + 26, py + (ph - lh) / 2, f"{rank:02d}", "lg", rnd, start=0.15 + rank * 0.15)
    body.append(markup)

    # Velocity — the number that ranked this row, the row's largest element.
    delta = entry.get("stars_today") or "+0"
    dcells = max(5, len(delta))
    dw = flap_width(dcells, "vx")
    dx = right - dw
    markup, _ = flap_row(dx, py + 16, delta.rjust(dcells), "vx", rnd, start=0.35 + rank * 0.15, color=BOARD["amber"])
    body.append(markup)
    body.append(label_el(right, py + 112, "Stars since yesterday", 16, BOARD["amber"], anchor="end", extra='class="t3"'))

    # Stats column
    mx = dx - 190
    for i, (kind, value) in enumerate((("lang", entry.get("lang") or "—"), ("star", entry.get("stars")),
                                       ("fork", entry.get("forks")))):
        if value:
            markup, _ = meta_item(mx, py + 40 + i * 32, kind, value, 19)
            body.append(f'<g class="t3">{markup}</g>')

    # Owner / name / description
    nx = px + 26 + flap_width(2, "lg") + 30
    name_w = mx - nx - 34
    owner, _, repo_name = entry["repo"].partition("/")
    body.append(text_el(nx, py + 36, fit(owner, "body", 20, name_w) + " /", "body", 20, BOARD["label"], extra='class="t3"'))
    body.append(text_el(nx, py + 80, fit(repo_name, "flap", 42, name_w), "flap", 42, BOARD["glyph"]))
    desc = fit(entry.get("desc") or "No description provided.", "body", 21, name_w)
    body.append(text_el(nx, py + 116, desc, "body", 21, BOARD["desc"], extra='class="t3"'))

    css = font_face_css(["flap", "label", "body"]) + FLAP_CSS
    title = (f"#{rank} trending: {entry['repo']} — {delta} stars since yesterday, "
             f"{entry.get('stars', '?')} stars total. {entry.get('desc') or ''}")
    return svg_document(W, H, _defs(), "\n".join(body), title, css)


# ---------------------------------------------------------------------------
# Contributions (replaces the third-party streak widget)
# ---------------------------------------------------------------------------

def _short_date(iso: str | None) -> str:
    if not iso:
        return ""
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def generate_contributions(summary: dict | None, today: dt.date) -> str:
    rnd = random.Random(today.isoformat() + "contrib")
    H = 214
    px, py, pw, ph = 22, 20, W - 44, 164
    x0 = px + 30
    right = px + pw - 30
    body = [housing(8, 6, W - 16, 192), board_plate(px, py, pw, ph)]
    body.append(line_bullet(x0, py + 22, 18, BOARD["amber"]))
    body.append(label_el(x0 + 30, py + 38, "Contributions", 22, BOARD["glyph"]))
    body.append(f'<rect x="{x0}" y="{py + 60}" width="{right - x0}" height="1" fill="{BOARD["rule"]}"/>')

    if not summary:
        body.append(label_el(x0, py + 118, "Contribution data appears after the next nightly run", 20, BOARD["label"]))
        return svg_document(W, H, _defs(), "\n".join(body), "Contributions: no data yet",
                            font_face_css(["flap", "label"]) + FLAP_CSS)

    span = f"{_short_date(summary.get('from'))} – {_short_date(summary.get('to'))}"
    body.append(label_el(right, py + 37, f"Last 12 months · {span}", 16, BOARD["label"], anchor="end", extra='class="t3"'))

    stats = [("Total", str(summary["total"])), ("Active days", str(summary["active_days"])),
             ("Longest run", f"{summary['longest_run']}D")]
    sx = x0
    for i, (label, value) in enumerate(stats):
        body.append(label_el(sx, py + 92, label, 16, BOARD["label"], extra='class="t3"'))
        cells = max(4, len(value))
        markup, _ = flap_row(sx, py + 104, value.rjust(cells), "lg", rnd, start=0.2 + i * 0.15)
        body.append(markup)
        sx += flap_width(cells, "lg") + 56

    # Weekly activity: one bar per week, height by count, amber like the
    # rest of what is "moving" on the board. Empty weeks are hairline ticks.
    weeks = summary.get("weeks") or []
    if weeks:
        bx0, by = sx + 10, py + 152
        step = (right - bx0) / len(weeks)
        bw = max(2.0, step - 2.5)
        peak = max(weeks) or 1
        bars = []
        for i, n in enumerate(weeks):
            x = bx0 + i * step
            if n:
                h = 6 + 58 * (n / peak) ** 0.6
                bars.append(f'<rect x="{x:.1f}" y="{by - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="1.5" '
                            f'fill="{BOARD["amber"]}" opacity="{0.45 + 0.55 * n / peak:.2f}"/>')
            else:
                bars.append(f'<rect x="{x:.1f}" y="{by - 2}" width="{bw:.1f}" height="2" fill="{BOARD["rule"]}"/>')
        body.append(label_el(bx0, py + 92, "Weekly activity", 16, BOARD["label"], extra='class="t3"'))
        body.append("".join(bars))

    title = (f"Contributions in the last 12 months: {summary['total']} total, "
             f"{summary['active_days']} active days, longest run {summary['longest_run']} days")
    return svg_document(W, H, _defs(), "\n".join(body), title, font_face_css(["flap", "label"]) + FLAP_CSS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--data-dir", default=None)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    data_root = resolve_data_dir(args.data_dir)

    repo_history = load_json_or(os.path.join(data_root, "repo_of_day.json"), REPO_OF_DAY)
    trending_entries = load_json_or(os.path.join(data_root, "trending.json"), TRENDING)
    today = profile_today()
    todays = build_repo_of_day_grid(repo_history, today=today)[0]

    contributions = load_json_or(os.path.join(data_root, "contributions.json"), None)
    outputs = {
        "today-pick.svg": generate_today_pick(todays, today),
        "contributions.svg": generate_contributions(contributions, today),
    }
    for i, entry in enumerate(trending_entries[:TRENDING_COUNT], start=1):
        outputs[f"trending-{i}.svg"] = generate_trending_row(entry, i, today)

    for name, svg in outputs.items():
        path = os.path.join(args.out_dir, name)
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path, len(svg), "bytes")


if __name__ == "__main__":
    main()
