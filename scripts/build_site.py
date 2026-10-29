"""
Builds yoshibase.com into a static directory for GitHub Pages: fills
site/index.html and site/about.html with tonight's data (the contribution
weeks drawn on the GitHub cover, totals, build date), copies the static
files (CSS, JS, fonts, images) and writes the CNAME.

The page is complete as plain HTML; JavaScript only adds motion. Missing data
files fall back to quieter copy rather than failing the deploy.

Usage: python3 build_site.py <out_dir> [--data-dir DIR]
"""
from __future__ import annotations
import argparse
import datetime as dt
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_paths import REPO_ROOT, resolve_data_dir

SITE_DIR = os.path.join(REPO_ROOT, "site")
PAGES = ["index.html", "about.html"]
DOMAIN = "yoshibase.com"


def _load(path: str, fallback):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return fallback


def contribution_bars(weeks: list[int], w: int = 300, h: int = 150) -> str:
    """The GitHub cover's artwork: a year of weekly contributions, drawn as a
    centred waveform. Empty weeks keep a 2px stub so the rhythm still reads."""
    weeks = weeks[-53:] or [0] * 53
    peak = max(weeks) or 1
    step = w / len(weeks)
    bw = step * 0.62
    rects = []
    for i, n in enumerate(weeks):
        bh = max(2.0, (n / peak) ** 0.55 * h)
        rects.append(f'<rect x="{i * step:.2f}" y="{(h - bh) / 2:.2f}" width="{bw:.2f}" height="{bh:.2f}" rx="{bw / 2:.2f}"/>')
    return f'<svg class="bars" viewBox="0 0 {w} {h}" preserveAspectRatio="none">{"".join(rects)}</svg>'


def page_values(data_dir: str, now: dt.datetime) -> dict[str, str]:
    contrib = _load(os.path.join(data_dir, "contributions.json"), None)
    total = contrib.get("total") if contrib else None
    return {
        "GH_BARS": contribution_bars(contrib.get("weeks", []) if contrib else []),
        "GH_CAPTION": html.escape(f"{total} contributions · last 12 months" if total is not None else "A year of commits"),
        "GH_WEEKS": html.escape(json.dumps(contrib.get("weeks", [])[-53:] if contrib else [])),
        "GH_TOTAL": html.escape(str(total) if total is not None else "Many"),
        "BUILD_STAMP": html.escape(f"{now.day} {now.strftime('%b %Y')}"),
        "YEAR": str(now.year),
    }


def build(out_dir: str, data_dir: str, now: dt.datetime) -> None:
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(SITE_DIR, out_dir, ignore=shutil.ignore_patterns(*PAGES, ".DS_Store"))
    values = page_values(data_dir, now)
    for name in PAGES:
        with open(os.path.join(SITE_DIR, name)) as f:
            page = f.read()
        for key, value in values.items():
            page = page.replace("{{" + key + "}}", value)
        if "{{" in page:
            raise ValueError(f"unfilled placeholder in site/{name}: " + page[page.index("{{"):][:40])
        with open(os.path.join(out_dir, name), "w") as f:
            f.write(page)

    with open(os.path.join(out_dir, "CNAME"), "w") as f:
        f.write(DOMAIN + "\n")
    open(os.path.join(out_dir, ".nojekyll"), "w").close()
    print("built", out_dir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--data-dir", default=None)
    args = ap.parse_args()
    build(os.path.abspath(args.out_dir), resolve_data_dir(args.data_dir), dt.datetime.now(dt.timezone.utc))
