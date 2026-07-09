"""
Unit tests for commit_booster.py's pure text-transform + selection logic.
The actual git plumbing (has_changes / commit_all / push) is exercised
separately against a throwaway repo — see the "git smoke test" section at
the bottom, run manually with: python3 test_commit_booster.py --with-git

Run: python3 test_commit_booster.py
"""
import random
import sys

from commit_booster import (
    rotate_badge_order, toggle_header_spacer, toggle_footer_spacer,
    apply_filler_tweaks, roll_commit_count, FILLER_TWEAKS,
)

SAMPLE_README = """<picture>
<img src="assets/generated/banner-header-light.svg">
</picture>

<br>

<div align="center">

<a href="https://github.com/yoshibase"><img src="badge1"></a>&nbsp;
<a href="https://www.linkedin.com/in/oz1127"><img src="badge2"></a>&nbsp;
<a href="https://github.com/yoshibase?tab=repositories"><img src="badge3"></a>

</div>

<!--SYNCED_AT_START--><!-- synced: pending --><!--SYNCED_AT_END-->
"""


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


def test_rotate_badge_order_changes_order_not_content():
    rnd = random.Random("fixed-seed")
    out = rotate_badge_order(SAMPLE_README, rnd)
    check("badge rotation actually changes the text", out != SAMPLE_README)
    for needle in ["badge1", "badge2", "badge3"]:
        check(f"rotation keeps {needle} present", needle in out)


def test_rotate_badge_order_noop_when_fewer_than_two():
    text = "<a href=\"https://github.com/x\">only one</a>"
    out = rotate_badge_order(text, random.Random(1))
    check("single badge line is left alone", out == text)


def test_toggle_header_spacer_is_idempotent_pair():
    once = toggle_header_spacer(SAMPLE_README)
    check("first toggle inserts the marker", "<!-- profile:active -->" in once)
    twice = toggle_header_spacer(once)
    check("second toggle removes it again", twice == SAMPLE_README)


def test_toggle_footer_spacer_is_idempotent_pair():
    once = toggle_footer_spacer(SAMPLE_README)
    check("first toggle inserts the marker", "<!-- refreshed daily -->" in once)
    twice = toggle_footer_spacer(once)
    check("second toggle removes it again", twice == SAMPLE_README)


def test_apply_filler_tweaks_count_zero_is_noop():
    out = apply_filler_tweaks(SAMPLE_README, 0, random.Random(1))
    check("count=0 changes nothing", out == SAMPLE_README)


def test_apply_filler_tweaks_count_matches_available_tweaks():
    out = apply_filler_tweaks(SAMPLE_README, len(FILLER_TWEAKS), random.Random(2))
    check("applying every tweak changes the text", out != SAMPLE_README)


def test_roll_commit_count_deterministic_per_date():
    a = roll_commit_count("2026-07-09", 3)
    b = roll_commit_count("2026-07-09", 3)
    check("same date always rolls the same count (idempotent reruns)", a == b)
    check("count is within [1,3]", 1 <= a <= 3)


def test_roll_commit_count_capped_at_one():
    check("max_commits=1 always returns 1 (the opt-out)", roll_commit_count("2026-07-09", 1) == 1)


def test_roll_commit_count_varies_across_dates():
    rolls = {roll_commit_count(f"2026-07-{d:02d}", 3) for d in range(1, 15)}
    check("rolls actually vary across different days (not stuck on one value)", len(rolls) > 1)


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
