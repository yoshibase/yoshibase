"""
Builds the yoshibase.com landing page into a static directory for GitHub
Pages: fills site/index.html with tonight's data (repo of the day,
contribution total, build date), copies the page's static files and the
embedded fonts, and writes the CNAME.

The page is complete as plain HTML; JavaScript only adds motion. Missing data
files fall back to quieter copy rather than failing the deploy.

Usage: python3 build_site.py <out_dir> [--data-dir DIR]
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from repo_of_day_grid import build_repo_of_day_grid, profile_today
from repo_paths import REPO_ROOT, resolve_data_dir
from render_readme import repo_url
from tokens import PROFILE

SITE_DIR = os.path.join(REPO_ROOT, "site")
FONTS = ["barlow-condensed-500.woff2", "barlow-condensed-600.woff2", "barlow-500.woff2"]
DOMAIN = "yoshibase.com"


def _load(path: str, fallback):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return fallback


def barcode(seed: str, bars: int = 34, height: int = 44) -> str:
    """Decorative ticket barcode, deterministic per destination."""
    digest = hashlib.sha256(seed.encode()).digest()
    x, rects = 0.0, []
    for i in range(bars):
        b = digest[i % len(digest)]
        w = 1 + (b & 3) * 0.75
        if i % 2 == 0:
            rects.append(f'<rect x="{x:.2f}" width="{w:.2f}" height="{height}"/>')
        x += w + 1.1
    return (f'<svg class="barcode" viewBox="0 0 {x:.1f} {height}" preserveAspectRatio="none" '
            f'aria-hidden="true" focusable="false">{"".join(rects)}</svg>')


def page_values(data_dir: str, now: dt.datetime) -> dict[str, str]:
    today = profile_today(now.date())
    history = _load(os.path.join(data_dir, "repo_of_day.json"), [])
    pick = build_repo_of_day_grid(history, today=today)[0] if history else {}
    contrib = _load(os.path.join(data_dir, "contributions.json"), None)

    repo = pick.get("repo")
    url = repo_url(repo) if repo else None
    delta = pick.get("stars_today")
    desc = " ".join((pick.get("desc") or "").split())
    if len(desc) > 110:
        desc = desc[:109].rstrip(" ,.;:-") + "…"

    esc = lambda s: html.escape(s or "", quote=True)  # noqa: E731
    return {
        "TODAY_URL": esc(url or PROFILE["github"]),
        "TODAY_REPO": esc(repo or "No departure yet"),
        "TODAY_DETAIL": esc(
            f"{delta} stars since yesterday" if delta and delta != "+0"
            else ("Tonight's pick" if repo else "The board fills in after the nightly run")
        ),
        "TODAY_DESC": esc(desc or ("No description on GitHub yet." if repo else "Check back after midnight UTC.")),
        "TODAY_DATE": esc(f"{today.day} {today.strftime('%b')}".upper()),
        "TODAY_OWNER": esc((repo.split("/")[0][:12] if repo else "Tonight").upper()),
        # The clock is right without JS: it shows the build time until the script takes over.
        "CLOCK_H0": now.strftime("%H")[0], "CLOCK_H1": now.strftime("%H")[1],
        "CLOCK_M0": now.strftime("%M")[0], "CLOCK_M1": now.strftime("%M")[1],
        "CONTRIB_LINE": esc(f"{contrib['total']} contributions in the last 12 months" if contrib else ""),
        "BUILD_STAMP": esc(f"{now.day} {now.strftime('%b %Y · %H:%M')} UTC"),
        "BUILD_ISO": now.strftime("%Y-%m-%dT%H:%MZ"),
        "YEAR": str(now.year),
        "BARCODE_GITHUB": barcode(PROFILE["github"]),
        "BARCODE_LINKEDIN": barcode(PROFILE["linkedin"]),
        "BARCODE_REPOS": barcode(PROFILE["repos"]),
        "BARCODE_TODAY": barcode(url or "today"),
    }


def build(out_dir: str, data_dir: str, now: dt.datetime) -> None:
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(SITE_DIR, out_dir, ignore=shutil.ignore_patterns("index.html", ".DS_Store"))
    os.makedirs(os.path.join(out_dir, "fonts"), exist_ok=True)
    for name in FONTS:
        shutil.copy2(os.path.join(REPO_ROOT, "fonts", name), os.path.join(out_dir, "fonts", name))

    with open(os.path.join(SITE_DIR, "index.html")) as f:
        page = f.read()
    for key, value in page_values(data_dir, now).items():
        page = page.replace("{{" + key + "}}", value)
    if "{{" in page:
        raise ValueError("unfilled placeholder in site/index.html: " + page[page.index("{{"):][:40])
    with open(os.path.join(out_dir, "index.html"), "w") as f:
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
