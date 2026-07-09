"""
Picks "repo of the day" and "trending today" using GitHub's search API plus
a day-over-day star-velocity snapshot (there is no official trending API,
so velocity vs. yesterday is the real, defensible signal instead of just
"popular" — a repo with 80k stars sitting still isn't trending, one that
gained 4k stars today is).

Flag + category resolution ported from the daily_profile_boost.py mechanism
you already had (COUNTRY_FLAGS / REPO_EMOJI_MAP keyword tables) — same
coverage, resolved to Twemoji icon *names* instead of raw unicode so
generate_cards.py can draw a real PNG instead of hoping the viewer's OS has
a matching emoji glyph. Owner-location lookups are only done for the repos
actually selected (≤4/day) rather than every search result (~50/day in the
original script), since an extra API call per candidate isn't needed until
a candidate is actually going on a card.

Talks to api.github.com — this needs normal outbound internet, which the
GitHub Actions runner has (this dev sandbox does not, so the HTTP calls
were not live-tested end-to-end here; see test_fetch_trending.py for what
*is* covered: every pure function — dedup, delta math, flag/category
resolution, selection — with no network involved).

Fails soft: on any API error this leaves data/*.json untouched so the
workflow falls back to yesterday's picks instead of breaking the README.

Env:
  GITHUB_TOKEN   auth for the search API (Actions provides this automatically)
Usage:
  python3 fetch_trending.py <data_dir>
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import random
import re
import sys
import urllib.request
import urllib.error
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import COUNTRY_FLAG_ICON, DEFAULT_FLAG_ICON, REPO_CATEGORY_ICON, DEFAULT_CATEGORY_ICON

API = "https://api.github.com"
HISTORY_DAYS = 30
REPO_OF_DAY_POOL = 5  # pick randomly among the top N not-yet-featured candidates, not always #1


def _get(path: str, token: str | None) -> dict:
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-readme-automation")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def search_candidates(token: str | None, min_stars: int = 300, created_within_days: int = 45, per_page: int = 60) -> list[dict]:
    since = (dt.date.today() - dt.timedelta(days=created_within_days)).isoformat()
    q = f"created:>{since} stars:>{min_stars}"
    path = f"/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page={per_page}"
    data = _get(path, token)
    return data.get("items", [])


def fetch_owner_location(login: str, token: str | None) -> str | None:
    try:
        user = _get(f"/users/{login}", token)
        return user.get("location")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return None  # a missing flag just falls back to 🌍 — not worth failing the run over


# ---------------------------------------------------------------------------
# Flag / category resolution (pure — unit tested)
# ---------------------------------------------------------------------------

def _word_match(keyword: str, text: str) -> bool:
    """Word-boundary match, not bare substring — the original
    daily_profile_boost.py used plain `kw in text`, which false-positives
    a lot for short keywords (e.g. "go" matching inside "google" or
    "algorithm", "uk" matching inside "Ukraine"). \\b keeps "go" out of
    "google" while still matching "nextjs"-style compounds where the
    keyword sits at a real word edge."""
    return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None


def resolve_flag_icon(location: str | None) -> str:
    if not location:
        return DEFAULT_FLAG_ICON
    loc = location.lower().strip()
    for keyword, icon in COUNTRY_FLAG_ICON.items():
        if _word_match(keyword, loc):
            return icon
    return DEFAULT_FLAG_ICON


def pick_category_icon(repo_name: str, description: str | None) -> str:
    text = (repo_name + " " + (description or "")).lower()
    for keyword, icon in REPO_CATEGORY_ICON:
        if _word_match(keyword, text):
            return icon
    return DEFAULT_CATEGORY_ICON


# ---------------------------------------------------------------------------
# Ranking / selection (pure — unit tested)
# ---------------------------------------------------------------------------

def compute_deltas(candidates: list[dict], prev_snapshot: dict[str, int]) -> list[dict]:
    """Attach a `delta` (stars gained since the last snapshot) to each
    candidate. Repos absent from the previous snapshot (first time seen)
    get delta=0 so a brand-new huge repo doesn't falsely look like it grew
    thousands of stars in one day."""
    out = []
    for repo in candidates:
        full_name = repo["full_name"]
        stars = repo["stargazers_count"]
        prev = prev_snapshot.get(full_name)
        delta = (stars - prev) if prev is not None else 0
        out.append({**repo, "delta": delta})
    return out


def pick_repo_of_day(ranked: list[dict], already_featured: set[str], date_seed: str, pool_size: int = REPO_OF_DAY_POOL) -> dict | None:
    """Randomly (but deterministically for a given date, so re-running the
    same day is idempotent) picks among the top `pool_size` not-yet-featured
    candidates, instead of always robotically taking #1 — daily_profile_boost.py's
    offset-rotation solved the same "don't always show the literal top repo"
    problem with a persisted offset counter; a date-seeded random pick over a
    small top pool gets the same variety without an extra state file to keep
    in sync with repo_of_day.json."""
    available = [r for r in ranked if r["full_name"] not in already_featured]
    pool = available or ranked
    if not pool:
        return None
    pool = pool[:pool_size]
    rnd = random.Random(date_seed)
    return rnd.choice(pool)


def update_repo_of_day_history(history: list[dict], new_entry: dict | None, today_label: str) -> list[dict]:
    """Prepend today's pick (if any), de-dupe by date, keep the most recent
    HISTORY_DAYS entries — the rotating 30-day window. A repo naturally
    becomes eligible again once it rolls out of this window, rather than
    being permanently excluded — with a small, fast-moving candidate pool,
    a forever-growing exclusion list would eventually run dry."""
    history = [e for e in history if e.get("date") != today_label]
    if new_entry:
        history = [new_entry] + history
    return history[:HISTORY_DAYS]


def build_card(repo: dict, location: str | None, date_label: str | None = None) -> dict:
    """Pure — no I/O. Takes an already-resolved `location` string (or None)
    so this can be unit tested without a network mock. to_card() below is
    the thin wrapper that actually fetches the location."""
    entry = {
        "flag": resolve_flag_icon(location),
        "cat": pick_category_icon(repo["full_name"], repo.get("description")),
        "repo": repo["full_name"],
        "desc": (repo.get("description") or "").strip(),
        "lang": repo.get("language"),
        "stars": _human(repo["stargazers_count"]),
        "forks": _human(repo["forks_count"]),
    }
    if date_label:
        entry = {"date": date_label, **entry}
    return entry


def to_card(repo: dict, token: str | None, date_label: str | None = None) -> dict:
    location = fetch_owner_location(repo["owner"]["login"], token)
    return build_card(repo, location, date_label)


def _human(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}m"
    if n >= 1_000:
        return f"{n/1000:.1f}k"
    return str(n)


def load(path: str, fallback):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return fallback


def save(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run(data_dir: str, token: str | None) -> int:
    today = dt.date.today()
    today_label = today.strftime("%b ") + str(today.day)
    snapshot_path = os.path.join(data_dir, "star_snapshot.json")
    repo_of_day_path = os.path.join(data_dir, "repo_of_day.json")
    trending_path = os.path.join(data_dir, "trending.json")

    prev_snapshot = load(snapshot_path, {})
    repo_of_day_history = load(repo_of_day_path, [])

    try:
        candidates = search_candidates(token)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"[fetch_trending] API call failed ({e}); leaving existing data/*.json untouched.", file=sys.stderr)
        return 1

    if not candidates:
        print("[fetch_trending] No candidates returned; leaving existing data/*.json untouched.", file=sys.stderr)
        return 1

    ranked = sorted(compute_deltas(candidates, prev_snapshot), key=lambda r: r["delta"], reverse=True)

    already_featured = {e["repo"] for e in repo_of_day_history}
    repo_pick = pick_repo_of_day(ranked, already_featured, date_seed=today.isoformat())

    if repo_pick:
        new_entry = to_card(repo_pick, token, date_label=today_label)
        repo_of_day_history = update_repo_of_day_history(repo_of_day_history, new_entry, today_label)
        save(repo_of_day_path, repo_of_day_history)

    trending_entries = [to_card(r, token) for r in ranked[:3]]
    if trending_entries:
        save(trending_path, trending_entries)

    new_snapshot = {r["full_name"]: r["stargazers_count"] for r in candidates}
    save(snapshot_path, new_snapshot)

    print(f"[fetch_trending] OK — repo of day: {repo_pick['full_name'] if repo_pick else 'none'}, "
          f"trending: {[e['repo'] for e in trending_entries]}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    args = ap.parse_args()
    sys.exit(run(args.data_dir, os.environ.get("GITHUB_TOKEN")))
