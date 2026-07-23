"""
Fills the TRENDING / REPO_OF_DAY marker sections in README.template.md and
writes the final README.md. Run *after* generate_cards.py so the link list
underneath each gallery image always matches what's actually in the image
that day — a hand-edited README would drift from the data within a week.

Usage: python3 render_readme.py <public_repo_dir> [--data-dir DIR]
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_cards import load_json_or
from repo_of_day_grid import build_repo_of_day_grid, profile_today, validate_consecutive_grid
from repo_paths import resolve_data_dir, resolve_repo_dir
from sample_data import TRENDING

TRENDING_START = "<!--TRENDING_START-->"
TRENDING_END = "<!--TRENDING_END-->"
REPO_START = "<!--REPO_OF_DAY_START-->"
REPO_END = "<!--REPO_OF_DAY_END-->"
SYNCED_START = "<!--SYNCED_AT_START-->"
SYNCED_END = "<!--SYNCED_AT_END-->"

# Flag emoji mapping for trending/repo cards
FLAG_EMOJI = {
    "flag-us": "🇺🇸", "flag-uk": "🇬🇧", "flag-de": "🇩🇪", "flag-fr": "🇫🇷",
    "flag-in": "🇮🇳", "flag-ca": "🇨🇦", "flag-au": "🇦🇺", "flag-jp": "🇯🇵",
    "flag-cn": "🇨🇳", "flag-br": "🇧🇷", "flag-nl": "🇳🇱", "flag-ch": "🇨🇭",
    "flag-se": "🇸🇪", "flag-es": "🇪🇸", "flag-it": "🇮🇹", "flag-kr": "🇰🇷",
    "flag-ru": "🇷🇺", "flag-sg": "🇸🇬", "flag-no": "🇳🇴", "flag-dk": "🇩🇰",
    "flag-fi": "🇫🇮", "flag-tr": "🇹🇷", "flag-pt": "🇵🇹", "flag-pl": "🇵🇱",
    "flag-intl": "🌍", "flag-sg": "🇸🇬",
}


def _get_flag(entry: dict) -> str:
    """Convert flag icon name to emoji."""
    flag = entry.get("flag", "flag-intl")
    return FLAG_EMOJI.get(flag, "🌍")


def _cat_emoji(entry: dict) -> str:
    """Convert category icon to emoji."""
    cat = entry.get("cat", "package")
    cat_map = {
        "robot": "🤖", "brain": "🧠", "zap": "⚡", "chart": "📊",
        "snake": "🐍", "package": "📦", "globe": "🌐", "mobile": "📱",
        "computer": "💻", "tools": "🔧", "wrench": "🔧", "books": "📚",
        "dna": "🧬", "plug": "🔌", "cabinet": "🗄️", "cloud": "☁️",
        "locked": "🔒", "test-tube": "🧪", "palette": "🎨", "sparkles": "✨",
        "video-game": "🎮", "ruler": "📏", "chart-up": "📈", "search": "🔍",
        "speech": "💬", "picture": "🖼️", "music": "🎵", "clapper": "🎬",
        "page": "📄", "fire": "🔥", "star": "⭐", "fork": "🍴",
        "yellow-square": "🟨", "blue-diamond": "💎", "blue-circle": "🔵",
        "crab": "🦀", "atom": "⚛️",
    }
    return cat_map.get(cat, "📦")


def render_trending_block(entries: list[dict]) -> str:
    """Render trending as a vibrant styled HTML table — no SVG image, no expandable."""
    rows = []
    for i, e in enumerate(entries):
        flag = _get_flag(e)
        cat = _cat_emoji(e)
        repo = e["repo"]
        desc = e.get("desc", "")
        stars = e.get("stars", "")
        forks = e.get("forks", "")
        stars_today = e.get("stars_today", "")
        trend = (
            f' <span style="color:#3FB950;font-weight:600">{stars_today} today</span>'
            if stars_today
            else ""
        )
        owner, _, name = repo.partition("/")
        rows.append(
            f'<tr>'
            f'<td style="text-align:center;font-size:11px;font-weight:600;color:#C850C0">#{i+1}</td>'
            f'<td style="font-size:12px">{flag} {cat}</td>'
            f'<td style="font-size:11px"><a href="https://github.com/{repo}"><b>{owner}/{name}</b></a></td>'
            f'<td style="font-size:10px;color:#8B949E">{desc}</td>'
            f'<td style="text-align:right;font-size:10px;color:#C850C0">⭐{stars} 🍴{forks}{trend}</td>'
            f'</tr>'
        )

    return f'''<div align="center">

<h3>🔥 Trending Today</h3>

<table style="border-collapse:collapse;font-family:Inter,sans-serif;width:100%;max-width:900px;margin:0 auto">
<tr style="background:linear-gradient(135deg,#4158D0,#C850C0);color:#fff;font-size:10px">
<th style="padding:6px 10px">#</th>
<th style="padding:6px 10px"></th>
<th style="padding:6px 10px;text-align:left">Repo</th>
<th style="padding:6px 10px;text-align:left">Description</th>
<th style="padding:6px 10px;text-align:right">Stats</th>
</tr>
{"".join(rows)}
</table>

</div>'''


def render_repo_of_day_block(entries: list[dict]) -> str:
    """Render repo-of-day as a 3-column, 10-row vibrant table — all 30 picks visible, links in cells."""
    today = profile_today().strftime("%b %-d, %Y") if os.name != "nt" else profile_today().strftime("%b %#d, %Y")
    cells = []
    for e in entries:
        date = e.get("date", "")
        if "repo" not in e:
            cells.append(
                f'<td style="padding:8px;border:1px solid #30363D;border-radius:8px;vertical-align:top;width:33%">'
                f'<div style="font-size:10px;color:#8B949E;margin-bottom:2px">{date}</div>'
                f'<div style="font-size:11px;color:#484F58;font-style:italic">No pick</div>'
                f'</td>'
            )
            continue
        flag = _get_flag(e)
        cat = _cat_emoji(e)
        repo = e["repo"]
        desc = e.get("desc", "")
        stars = e.get("stars", "")
        owner, _, name = repo.partition("/")
        cells.append(
            f'<td style="padding:8px;border:1px solid #30363D;border-radius:8px;vertical-align:top;width:33%">'
            f'<div style="font-size:10px;color:#8B949E;margin-bottom:2px">{date}</div>'
            f'<div style="font-size:12px;font-weight:600">{flag} {cat} <a href="https://github.com/{repo}"><b>{owner}/{name}</b></a></div>'
            f'<div style="font-size:10px;color:#C9D1D9;margin-top:2px">{desc}</div>'
            f'<div style="font-size:9px;color:#8B949E;margin-top:3px">⭐{stars}</div>'
            f'</td>'
        )

    # Pad to fill 3x10 grid
    while len(cells) % 3 != 0:
        cells.append('<td style="padding:8px;border:1px solid #30363D;border-radius:8px"></td>')

    table_rows = []
    for i in range(0, len(cells), 3):
        table_rows.append(f'<tr>{cells[i]}{cells[i+1]}{cells[i+2]}</tr>')

    return f'''<div align="center">

<h3>📦 Repo of the Day — Last 30 Days</h3>

<table style="border-collapse:separate;border-spacing:6px;font-family:Inter,sans-serif;width:100%;max-width:1000px;margin:0 auto">
{"".join(table_rows)}
</table>

<sub>Last synced {today} · automated daily</sub>

</div>'''


def render(template_path: str, out_path: str, data_dir: str | None) -> None:
    data_root = resolve_data_dir(data_dir)
    repo_history_path = os.path.join(data_root, "repo_of_day.json")
    trending_path = os.path.join(data_root, "trending.json")

    if not os.path.isfile(repo_history_path):
        raise FileNotFoundError(
            f"Missing {repo_history_path} — refusing sample_data fallback for repo-of-day grid"
        )

    repo_history = load_json_or(repo_history_path, [])
    trending_entries = load_json_or(trending_path if os.path.isfile(trending_path) else None, TRENDING)
    repo_entries = build_repo_of_day_grid(repo_history, today=profile_today())
    validate_consecutive_grid(repo_entries, today=profile_today())

    with open(template_path) as f:
        tpl = f.read()

    tpl = _replace_between(tpl, TRENDING_START, TRENDING_END, render_trending_block(trending_entries))
    tpl = _replace_between(tpl, REPO_START, REPO_END, render_repo_of_day_block(repo_entries))
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tpl = _replace_between(tpl, SYNCED_START, SYNCED_END, f"<!-- synced: {now} -->")

    with open(out_path, "w") as f:
        f.write(tpl)
    print("wrote", out_path)


def _replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i, j = text.index(start), text.index(end)
    return text[: i + len(start)] + "\n" + replacement + "\n" + text[j:]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("public_repo_dir", nargs="?", default=".")
    ap.add_argument("--data-dir", default=None)
    args = ap.parse_args()
    repo_dir = resolve_repo_dir(args.public_repo_dir)
    render(
        os.path.join(repo_dir, "README.template.md"),
        os.path.join(repo_dir, "README.md"),
        args.data_dir,
    )
