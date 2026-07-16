"""
Generates the repo-of-day gallery (30-day rotating grid) and the trending
row (top 3), light + dark, as standalone SVGs.

Usage: python3 generate_cards.py <out_dir> [--data-dir DIR]
Reads data/repo_of_day.json and data/trending.json if present, otherwise
falls back to sample_data.py so the pipeline always produces something.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import (
    THEME, gradient_for_index, FONT_FACES, EMOJI_ASSETS_DIR,
    ALL_CARD_ICONS, DEFAULT_FLAG_ICON, DEFAULT_CATEGORY_ICON,
)
from sample_data import REPO_OF_DAY, TRENDING, LANGUAGE_COLORS
from repo_of_day_grid import build_repo_of_day_grid
from svg_kit import (
    esc, font_face_css, linear_gradient_def, drop_shadow_filter, glow_filter,
    rounded_card, text_el, truncate_to_width, svg_document, style_block,
    emoji_image_defs, icon_text_line,
)

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EMOJI_DIR = os.path.join(_REPO_ROOT, EMOJI_ASSETS_DIR)
# entries already carry Twemoji icon *names* directly (see sample_data.py /
# fetch_trending.py) — register every possible one up front so the
# generator never needs to scan the data first.
_ALL_ICON_NAMES = ALL_CARD_ICONS


def load_json_or(path: str, fallback):
    if path and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return fallback


def _avatar_color(name: str) -> tuple[str, str]:
    h = hashlib.md5(name.encode()).hexdigest()
    idx = int(h[:4], 16)
    return gradient_for_index(idx)


def initials_avatar(cx: float, cy: float, r: float, owner: str) -> str:
    g1, g2 = _avatar_color(owner)
    gid = f"av-{hashlib.md5(owner.encode()).hexdigest()[:8]}"
    initials = "".join([p[0] for p in owner.replace("-", " ").replace("_", " ").split()[:2]]).upper() or "?"
    return f"""<defs>{linear_gradient_def(gid, [g1, g2], angle=135)}</defs>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>
    {text_el(cx, cy + r*0.36, initials, "display_bold", r * 0.85, "#FFFFFF", anchor="middle")}"""


def lang_pill(x_right: float, y: float, lang: str | None) -> str:
    if not lang:
        return ""
    color, fg = LANGUAGE_COLORS.get(lang, LANGUAGE_COLORS[None])
    label = lang
    w = len(label) * 6.2 + 16
    x = x_right - w
    return f"""<g transform="translate({x:.1f},{y:.1f})">
      <rect width="{w:.1f}" height="16" rx="8" fill="{color}"/>
      {text_el(w/2, 11.5, label, "body_semibold", 8.5, fg, anchor="middle")}
    </g>"""


def stat_group(x_right: float, y: float, stars: str, forks: str, color: str) -> str:
    """Right-aligned '⭐ 3.5k  🍴 313' built from real icon widths so it
    lands flush against x_right instead of being character-count-guessed."""
    size = 10
    fork_w = len(forks) * 9 * 0.56
    star_w = len(stars) * 9 * 0.56
    fork_x = x_right - fork_w
    icon_fork_x = fork_x - size - 4
    star_x = icon_fork_x - 14 - star_w
    icon_star_x = star_x - size - 4
    markup = (
        f'<use href="#emoji-star" x="{icon_star_x:.1f}" y="{y-size*0.78:.1f}" width="{size}" height="{size}"/>'
        + text_el(star_x, y, stars, "mono_regular", 9, color, anchor="start")
        + f'<use href="#emoji-fork" x="{icon_fork_x:.1f}" y="{y-size*0.78:.1f}" width="{size}" height="{size}"/>'
        + text_el(fork_x, y, forks, "mono_regular", 9, color, anchor="start")
    )
    return markup


# ---------------------------------------------------------------------------
# Repo-of-day grid
# ---------------------------------------------------------------------------

def generate_repo_gallery(theme: str, entries: list[dict]) -> str:
    colors = THEME[theme]
    cols, rows = 2, 15
    card_w, card_h = 578, 74
    gap = 12
    margin = 16
    W = margin * 2 + cols * card_w + (cols - 1) * gap
    H = margin * 2 + rows * card_h + (rows - 1) * gap + 54  # +54 for header row

    defs = [style_block(font_face_css(["display_black", "display_bold", "body_regular", "body_semibold", "mono_regular", "mono_medium"]))]
    icon_defs, _ = emoji_image_defs(_EMOJI_DIR, _ALL_ICON_NAMES)
    defs.append(icon_defs)
    body = []

    body.append(rounded_card(0, 0, W, H, 20, colors["bg"]))
    title_markup, _ = icon_text_line(margin, 38, [
        ("icon", "emoji-package", 20),
        ("text", "Repo of the Day — Last 30 Days", "display_bold", 19, colors["text_primary"]),
    ])
    body.append(title_markup)
    body.append(text_el(W - margin, 38, "one pick per day · refreshed daily", "body_regular", 10.5, colors["text_faint"], anchor="end"))

    top = 54
    for i, entry in enumerate(entries[:cols * rows]):
        col = i % cols
        row = i // cols
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        g1, g2 = gradient_for_index(i)
        gid = f"cardGrad-{theme}-{i}"
        sid = f"cardShadow-{theme}-{i}"
        defs.append(f"<defs>{linear_gradient_def(gid, [g1, g2])}</defs>")
        defs.append(f"<defs>{drop_shadow_filter(sid, g1, dy=5, blur=10, opacity=0.30 if theme=='light' else 0.45)}</defs>")

        body.append(f'<g transform="translate({x},{y})">')
        body.append(rounded_card(0, 0, card_w, card_h, 14, f"url(#{gid})", filter_id=sid))

        pad = 14
        date_w = len(entry["date"]) * 5.6 + 14
        body.append(f'<rect x="{pad}" y="10" width="{date_w:.1f}" height="15" rx="7.5" fill="rgba(255,255,255,0.22)"/>')
        body.append(text_el(pad + date_w/2, 20.5, entry["date"], "mono_medium", 8.5, "#FFFFFF", anchor="middle"))

        if "repo" not in entry:
            body.append(text_el(pad, 44, "No pick", "body_regular", 10, "rgba(255,255,255,0.55)", anchor="start"))
            body.append("</g>")
            continue

        # flag + category icon + repo name
        name_x = pad + date_w + 10
        max_name_w = card_w - name_x - pad - 66
        repo_name = truncate_to_width(entry["repo"], 12, max_name_w - 44, avg_ratio=0.6)
        flag_icon = entry.get("flag") or DEFAULT_FLAG_ICON
        cat_icon = entry.get("cat") or DEFAULT_CATEGORY_ICON
        line_markup, _ = icon_text_line(name_x, 21, [
            ("icon", f"emoji-{flag_icon}", 13),
            ("icon", f"emoji-{cat_icon}", 13),
            ("text", repo_name, "body_semibold", 12, "#FFFFFF"),
        ], gap=4)
        body.append(line_markup)

        # stars/forks top-right
        body.append(stat_group(card_w - pad, 20.5, entry["stars"], entry["forks"], "rgba(255,255,255,0.85)"))

        # description
        desc = truncate_to_width(entry.get("desc") or "", 9.5, card_w - pad*2 - 70, avg_ratio=0.52)
        body.append(text_el(pad, 40, desc, "body_regular", 9.5, "rgba(255,255,255,0.72)", anchor="start"))

        # language pill bottom-right
        if entry.get("lang"):
            body.append(lang_pill(card_w - pad, 48, entry["lang"]))

        body.append("</g>")

    return svg_document(int(W), int(H), "\n".join(defs), "\n".join(body))


# ---------------------------------------------------------------------------
# Trending row (3-up)
# ---------------------------------------------------------------------------

def generate_trending_row(theme: str, entries: list[dict]) -> str:
    colors = THEME[theme]
    cols = 3
    card_w, card_h = 384, 190
    gap = 16
    margin = 16
    W = margin * 2 + cols * card_w + (cols - 1) * gap
    H = margin * 2 + card_h + 46

    defs = [style_block(font_face_css(["display_black", "display_bold", "body_regular", "body_semibold", "mono_regular", "mono_medium"]))]
    icon_defs, _ = emoji_image_defs(_EMOJI_DIR, _ALL_ICON_NAMES)
    defs.append(icon_defs)
    body = []

    body.append(rounded_card(0, 0, W, H, 20, colors["bg"]))
    title_markup, _ = icon_text_line(margin, 32, [
        ("icon", "emoji-fire", 20),
        ("text", "Trending Today", "display_bold", 19, colors["text_primary"]),
    ])
    body.append(title_markup)
    body.append(text_el(W - margin, 32, "top 3 · updated daily", "body_regular", 10.5, colors["text_faint"], anchor="end"))

    top = 46
    for i, entry in enumerate(entries[:cols]):
        x = margin + i * (card_w + gap)
        y = top
        g1, g2 = gradient_for_index(i * 3)
        gid = f"trendGrad-{theme}-{i}"
        sid = f"trendShadow-{theme}-{i}"
        glid = f"trendGlow-{theme}-{i}"
        defs.append(f"<defs>{linear_gradient_def(gid, [g1, g2], angle=150)}</defs>")
        defs.append(f"<defs>{drop_shadow_filter(sid, g1, dy=8, blur=16, opacity=0.32 if theme=='light' else 0.48)}</defs>")
        defs.append(f"<defs>{glow_filter(glid, g2, blur=14, opacity=0.4)}</defs>")

        body.append(f'<g transform="translate({x},{y})">')
        body.append(rounded_card(0, 0, card_w, card_h, 18, f"url(#{gid})", filter_id=sid))

        pad = 18
        rank_label = f"#{i+1} TRENDING"
        rw = len(rank_label) * 6.4 + 18
        body.append(f'<rect x="{pad}" y="14" width="{rw:.1f}" height="20" rx="10" fill="rgba(255,255,255,0.24)" filter="url(#{glid})"/>')
        body.append(text_el(pad + rw/2, 28, rank_label, "mono_medium", 9.5, "#FFFFFF", anchor="middle"))
        flag_icon = entry.get("flag") or DEFAULT_FLAG_ICON
        body.append(f'<use href="#emoji-{flag_icon}" x="{card_w-pad-18:.1f}" y="15" width="18" height="18"/>')

        owner, _, repo_name = entry["repo"].partition("/")
        av_cy = 68
        body.append(initials_avatar(pad + 20, av_cy, 20, owner))
        name_x = pad + 52
        body.append(text_el(name_x, av_cy - 4, truncate_to_width(owner, 10.5, card_w - name_x - pad, 0.56), "body_regular", 10.5, "rgba(255,255,255,0.75)", anchor="start"))
        body.append(text_el(name_x, av_cy + 13, truncate_to_width(repo_name, 15, card_w - name_x - pad, 0.56), "display_bold", 15, "#FFFFFF", anchor="start"))

        desc_lines = _wrap(entry.get("desc") or "", 10.5, card_w - pad * 2, avg_ratio=0.5, max_lines=2)
        for li, line in enumerate(desc_lines):
            body.append(text_el(pad, 108 + li * 15, line, "body_regular", 10.5, "rgba(255,255,255,0.82)", anchor="start"))

        body.append(f'<line x1="{pad}" y1="144" x2="{card_w-pad}" y2="144" stroke="rgba(255,255,255,0.25)" stroke-width="1"/>')
        if entry.get("lang"):
            body.append(lang_pill(pad + 70, 154, entry["lang"]))
        body.append(stat_group(card_w - pad, 166, entry["stars"], entry["forks"], "rgba(255,255,255,0.9)"))

        body.append("</g>")

    return svg_document(int(W), int(H), "\n".join(defs), "\n".join(body))


def _wrap(text: str, size: float, max_w: float, avg_ratio: float, max_lines: int) -> list[str]:
    if not text:
        return []
    max_chars = max(1, int(max_w / (size * avg_ratio)))
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
        if len(lines) == max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len(" ".join(words)) > sum(len(l) for l in lines) + max_lines:
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--data-dir", default=None)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    repo_history = load_json_or(
        os.path.join(args.data_dir, "repo_of_day.json") if args.data_dir else None, REPO_OF_DAY
    )
    trending_entries = load_json_or(
        os.path.join(args.data_dir, "trending.json") if args.data_dir else None, TRENDING
    )
    repo_entries = build_repo_of_day_grid(repo_history)

    for theme in ("light", "dark"):
        svg = generate_repo_gallery(theme, repo_entries)
        out = os.path.join(args.out_dir, f"repo-of-day-{theme}.svg")
        open(out, "w").write(svg)
        print("wrote", out, len(svg), "bytes")

        svg = generate_trending_row(theme, trending_entries)
        out = os.path.join(args.out_dir, f"trending-{theme}.svg")
        open(out, "w").write(svg)
        print("wrote", out, len(svg), "bytes")


if __name__ == "__main__":
    main()
