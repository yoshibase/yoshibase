"""
Owns every git operation against the public profile repo. Decides how many
commits today gets — random 1-3, seeded by date so re-running the same day
doesn't reroll — always makes one real commit for whatever
fetch_trending.py / generate_banner.py / generate_cards.py / render_readme.py
actually changed, and only if the roll calls for more than one, layers on
small, genuinely different filler edits so commit #2 and #3 carry real,
distinct diff content instead of being empty or duplicate commits.

Ported from the spirit of your daily_profile_boost.py's
_swap_two_badges / _bump_timestamp / _toggle_blank_before_footer — same
idea (make the "extra" commits look like real incremental edits), rewritten
so each tweak touches a different, predictable part of README.md instead of
scanning for style-attribute strings that no longer exist in the rebuilt
file (the old tweaks matched inline CSS text that this version doesn't use
any more — see the chat writeup for why that CSS never rendered anyway).

This is cosmetic, not deceptive — every commit's diff is real and readable
if anyone opens it. Worth knowing regardless: a very regular N-commits-
every-day pattern is still a pattern to anyone checking your contribution
history closely. To turn this off and just make one honest commit a day,
run with --max-commits 1.

Usage:
  python3 commit_booster.py <public_repo_dir>                # live
  python3 commit_booster.py <public_repo_dir> --dry-run       # print-only
  python3 commit_booster.py <public_repo_dir> --max-commits 1 # always 1 commit
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import random
import re
import subprocess
import sys

BADGE_LINE_RE = re.compile(r'^<a href="https://(?:github\.com|www\.linkedin\.com)[^\n]*$', re.MULTILINE)
HEADER_MARKER = "<!-- profile:active -->"
FOOTER_MARKER = "<!-- refreshed daily -->"


# ---------------------------------------------------------------------------
# Filler tweaks — pure text -> text, each independently unit-tested.
# ---------------------------------------------------------------------------

def rotate_badge_order(text: str, rnd: random.Random) -> str:
    lines = BADGE_LINE_RE.findall(text)
    if len(lines) < 2:
        return text
    shuffled = lines[:]
    while shuffled == lines:  # guarantee a visible change, not a no-op shuffle
        rnd.shuffle(shuffled)
    it = iter(shuffled)
    return BADGE_LINE_RE.sub(lambda _m: next(it), text)


def toggle_header_spacer(text: str) -> str:
    if HEADER_MARKER in text:
        return text.replace("\n" + HEADER_MARKER, "")
    return text.replace("<br>\n\n<div align=\"center\">", f"<br>\n{HEADER_MARKER}\n\n<div align=\"center\">", 1)


def toggle_footer_spacer(text: str) -> str:
    if FOOTER_MARKER in text:
        return text.replace("\n" + FOOTER_MARKER, "")
    marker_point = '<!--SYNCED_AT_START-->'
    return text.replace(marker_point, f"{FOOTER_MARKER}\n{marker_point}", 1)


FILLER_TWEAKS = [
    lambda text, rnd: rotate_badge_order(text, rnd),
    lambda text, rnd: toggle_header_spacer(text),
    lambda text, rnd: toggle_footer_spacer(text),
]


def apply_filler_tweaks(text: str, count: int, rnd: random.Random) -> str:
    """Applies `count` distinct tweaks (capped at how many exist)."""
    order = list(range(len(FILLER_TWEAKS)))
    rnd.shuffle(order)
    for idx in order[:count]:
        text = FILLER_TWEAKS[idx](text, rnd)
    return text


def roll_commit_count(date_seed: str, max_commits: int) -> int:
    if max_commits <= 1:
        return 1
    return random.Random(date_seed).randint(1, max_commits)


# ---------------------------------------------------------------------------
# Git plumbing
# ---------------------------------------------------------------------------

def _git(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def has_changes(cwd: str) -> bool:
    r = _git(["status", "--porcelain"], cwd)
    return bool(r.stdout.strip())


def commit_all(cwd: str, message: str) -> bool:
    _git(["add", "-A"], cwd)
    r = _git(["commit", "-m", message], cwd)
    return r.returncode == 0


REAL_MESSAGES = ["update repo showcase", "sync daily content", "refresh profile data"]
FILLER_MESSAGES = ["tidy up README", "minor layout tweak", "small formatting pass"]


def run(public_repo_dir: str, max_commits: int, dry_run: bool) -> int:
    readme_path = os.path.join(public_repo_dir, "README.md")
    today = dt.date.today()
    rnd = random.Random(today.isoformat())

    if not has_changes(public_repo_dir):
        print("[commit_booster] nothing changed, skipping.")
        return 0

    commit_count = roll_commit_count(today.isoformat(), max_commits)
    print(f"[commit_booster] rolled {commit_count} commit(s) for {today.isoformat()}")

    if dry_run:
        print(f"[commit_booster] DRY RUN — would make {commit_count} commit(s), "
              f"first real ({rnd.choice(REAL_MESSAGES)!r}), "
              f"then {commit_count - 1} filler commit(s).")
        return 0

    # Commit 1: whatever the pipeline actually changed (README + generated assets + data copies).
    commit_all(public_repo_dir, rnd.choice(REAL_MESSAGES))

    # Commits 2..N: one small, distinct, real cosmetic edit *per* commit — applied and
    # committed one at a time, not batched, otherwise everything after the first commit
    # has nothing left to stage and silently becomes a no-op.
    remaining = commit_count - 1
    if remaining > 0 and os.path.exists(readme_path):
        tweak_order = list(range(len(FILLER_TWEAKS)))
        rnd.shuffle(tweak_order)
        for idx in tweak_order[:remaining]:
            with open(readme_path) as f:
                text = f.read()
            tweaked = FILLER_TWEAKS[idx](text, rnd)
            if tweaked == text:
                continue  # this tweak had nothing to change; don't burn a commit on it
            with open(readme_path, "w") as f:
                f.write(tweaked)
            commit_all(public_repo_dir, rnd.choice(FILLER_MESSAGES))

    push = _git(["push"], public_repo_dir)
    if push.returncode != 0:
        print(f"[commit_booster] push failed: {push.stderr}", file=sys.stderr)
        return 1
    print("[commit_booster] pushed.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("public_repo_dir")
    ap.add_argument("--max-commits", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.exit(run(args.public_repo_dir, args.max_commits, args.dry_run))
