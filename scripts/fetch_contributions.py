"""
Fetches the profile's contribution calendar (last ~12 months) from GitHub's
GraphQL API and writes a small summary to data/contributions.json for the
contributions board. Replaces the third-party streak-stats widget: the
numbers now come from the same nightly run as everything else.

Fails soft: on any API error the previous data/contributions.json is left
untouched, so the board shows the last good snapshot instead of breaking.

Env:
  GITHUB_TOKEN   auth for the GraphQL API (Actions provides this automatically)
Usage:
  python3 fetch_contributions.py <data_dir> [--user LOGIN]
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import PROFILE

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def fetch_calendar(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        method="POST",
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "profile-readme-automation")
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode())
    if payload.get("errors"):
        raise ValueError(payload["errors"][0].get("message", "GraphQL error"))
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


# ---------------------------------------------------------------------------
# Summary (pure — unit tested)
# ---------------------------------------------------------------------------

def longest_run(counts: list[int]) -> int:
    """Longest run of consecutive days with at least one contribution."""
    best = cur = 0
    for c in counts:
        cur = cur + 1 if c > 0 else 0
        best = max(best, cur)
    return best


def summarize(calendar: dict, fetched: dt.datetime) -> dict:
    days = [d for w in calendar["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    return {
        "total": calendar["totalContributions"],
        "active_days": sum(1 for c in counts if c > 0),
        "longest_run": longest_run(counts),
        "weeks": [sum(d["contributionCount"] for d in w["contributionDays"]) for w in calendar["weeks"]],
        "from": days[0]["date"] if days else None,
        "to": days[-1]["date"] if days else None,
        "fetched": fetched.strftime("%Y-%m-%dT%H:%MZ"),
    }


def run(data_dir: str, login: str, token: str | None) -> int:
    path = os.path.join(data_dir, "contributions.json")
    if not token:
        print("[fetch_contributions] no GITHUB_TOKEN; keeping last snapshot.", file=sys.stderr)
        return 0
    try:
        calendar = fetch_calendar(login, token)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError) as e:
        print(f"[fetch_contributions] fetch failed ({e}); keeping last snapshot.", file=sys.stderr)
        return 0
    summary = summarize(calendar, dt.datetime.now(dt.timezone.utc))
    os.makedirs(data_dir, exist_ok=True)
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[fetch_contributions] OK — {summary['total']} contributions, longest run {summary['longest_run']} days")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir", nargs="?", default=None)
    ap.add_argument("--user", default=PROFILE["handle"])
    args = ap.parse_args()
    from repo_paths import resolve_data_dir

    sys.exit(run(resolve_data_dir(args.data_dir), args.user, os.environ.get("GITHUB_TOKEN")))
