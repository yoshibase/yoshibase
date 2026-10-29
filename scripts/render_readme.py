"""
Fills the TRENDING / REPO_OF_DAY marker sections in README.template.md and
writes the final README.md. Run *after* generate_cards.py so every linked
board row matches the image generated for it that night.

GitHub's README sanitizer drops style/class attributes, so everything here is
structure only: a plain <a><img> around each board (SVG content itself can't
hold links, and GitHub's renderer splits an <a><picture> apart), and a plain
Markdown table for the log.
Repository descriptions are untrusted input and are escaped before use.

Usage: python3 render_readme.py <public_repo_dir> [--data-dir DIR]
"""
from __future__ import annotations
import argparse
import datetime as dt
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_cards import TRENDING_COUNT, load_json_or
from repo_of_day_grid import build_repo_of_day_grid, profile_today, validate_consecutive_grid
from repo_paths import resolve_data_dir, resolve_repo_dir
from sample_data import TRENDING

TRENDING_START = "<!--TRENDING_START-->"
TRENDING_END = "<!--TRENDING_END-->"
REPO_START = "<!--REPO_OF_DAY_START-->"
REPO_END = "<!--REPO_OF_DAY_END-->"
SYNCED_START = "<!--SYNCED_AT_START-->"
SYNCED_END = "<!--SYNCED_AT_END-->"

ASSETS = "assets/generated"
_REPO_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_MD_PUNCT_RE = re.compile(r"([\\`*_\[\]~])")


def md_text(text: str | None, limit: int | None = None) -> str:
    """Untrusted text -> inert Markdown/HTML: one line, entities escaped,
    Markdown punctuation backslash-escaped, table pipes neutralised."""
    text = " ".join((text or "").split())
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip(" ,.;:-—") + "…"
    # Markdown escapes first, then entities: escaping after html.escape would
    # break the entities it produces. Quotes need no escaping in cell text.
    text = _MD_PUNCT_RE.sub(r"\\\1", text)
    return html.escape(text, quote=False).replace("|", "&#124;")


def repo_url(repo: str) -> str | None:
    """Only well-formed owner/name pairs become links."""
    return f"https://github.com/{repo}" if _REPO_NAME_RE.match(repo or "") else None


def board_img(stem: str, alt: str) -> str:
    """A full-width generated board; the boards read on both GitHub themes."""
    alt = html.escape(" ".join(alt.split()), quote=True)
    return f'<img src="{ASSETS}/{stem}.svg" width="100%" alt="{alt}">'


def linked(url: str | None, inner: str) -> str:
    return f'<a href="{url}">{inner}</a>' if url else inner


def render_trending_block(entries: list[dict]) -> str:
    lines = [board_img("section-trending", "Trending now — ranked by stars gained since yesterday")]
    for rank, e in enumerate(entries[:TRENDING_COUNT], start=1):
        alt = (f"#{rank} {e['repo']}: {e.get('stars_today') or '+0'} stars since yesterday, "
               f"{e.get('stars', '?')} total. {' '.join((e.get('desc') or '').split())[:140]}")
        lines.append(linked(repo_url(e["repo"]), board_img(f"trending-{rank}", alt)))
    # One line = one HTML block, so the strip and its rows share the same
    # tight inline gutter instead of a paragraph margin.
    return "".join(lines)


def render_log_table(entries: list[dict]) -> str:
    rows = [
        "| Date | Repository | Language | Stars | Gained |",
        "|:--|:--|:--|--:|--:|",
    ]
    for e in entries:
        date = md_text(e.get("date"))
        if "repo" not in e:
            rows.append(f"| {date} | <sub>No pick recorded</sub> | | | |")
            continue
        url = repo_url(e["repo"])
        name = f"**{md_text(e['repo'])}**"
        cell = f"[{name}]({url})" if url else name
        desc = md_text(e.get("desc"), limit=96)
        if desc:
            cell += f"<br><sub>{desc}</sub>"
        rows.append(
            f"| {date} | {cell} | {md_text(e.get('lang')) or '—'} | {md_text(e.get('stars')) or '—'} "
            f"| {md_text(e.get('stars_today')) or '—'} |"
        )
    return "\n".join(rows)


def render_repo_of_day_block(entries: list[dict]) -> str:
    today = entries[0]
    if "repo" in today:
        desc = " ".join((today.get("desc") or "").split())[:160]
        alt = f"Repo of the day: {today['repo']}" + (f" — {desc}" if desc else "")
        card = linked(repo_url(today["repo"]), board_img("today-pick", alt))
    else:
        card = board_img("today-pick", "Repo of the day: no pick recorded yet")
    picks = sum(1 for e in entries if "repo" in e)
    return f"""{card}

<details>
<summary><b>Departure log</b> · {picks} picks over the last {len(entries)} days</summary>
<br>

{render_log_table(entries)}

</details>"""


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
