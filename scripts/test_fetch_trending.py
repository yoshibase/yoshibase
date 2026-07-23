"""
Unit tests for the pure logic in fetch_trending.py — the parts that don't
need network access. api.github.com wasn't reachable from the dev sandbox
this was built in, so the HTTP calls themselves (search_candidates,
fetch_owner_location) are only exercised live once this runs inside GitHub
Actions; everything else — dedup, delta math, flag/category resolution,
selection, card building — is verified here with no network involved.

Run: python3 test_fetch_trending.py
"""
from fetch_trending import (
    compute_deltas, pick_repo_of_day, update_repo_of_day_history,
    build_card, resolve_flag_icon, pick_category_icon, _human,
)


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


def test_human():
    check("1_234 -> 1.2k", _human(1234) == "1.2k")
    check("999 -> 999", _human(999) == "999")
    check("2_500_000 -> 2.5m", _human(2_500_000) == "2.5m")


def test_compute_deltas_new_repo_gets_zero():
    candidates = [{"full_name": "a/b", "stargazers_count": 500}]
    out = compute_deltas(candidates, prev_snapshot={})
    check("unseen repo has delta 0 (not a false spike)", out[0]["delta"] == 0)


def test_compute_deltas_growth():
    candidates = [{"full_name": "a/b", "stargazers_count": 1500}]
    out = compute_deltas(candidates, prev_snapshot={"a/b": 1000})
    check("delta computed correctly", out[0]["delta"] == 500)


def test_pick_repo_of_day_skips_already_featured():
    ranked = [{"full_name": f"popular/{i}"} for i in range(6)]
    # only "popular/0" is used; with pool_size=5 the picker must choose
    # from the next 5, so run it many times and confirm 0 never comes back.
    seen = set()
    for day in range(30):
        pick = pick_repo_of_day(ranked, already_featured={"popular/0"}, date_seed=f"day-{day}")
        seen.add(pick["full_name"])
    check("never re-picks an already-featured repo", "popular/0" not in seen)
    check("does pick from the remaining candidates", len(seen) > 0)


def test_pick_repo_of_day_falls_back_when_all_featured():
    ranked = [{"full_name": "popular/one"}]
    pick = pick_repo_of_day(ranked, already_featured={"popular/one"}, date_seed="2026-07-08")
    check("falls back to #1 rather than returning nothing", pick["full_name"] == "popular/one")


def test_pick_repo_of_day_deterministic_per_date():
    ranked = [{"full_name": f"repo/{i}"} for i in range(5)]
    a = pick_repo_of_day(ranked, already_featured=set(), date_seed="2026-07-08")
    b = pick_repo_of_day(ranked, already_featured=set(), date_seed="2026-07-08")
    check("same date always picks the same repo (idempotent reruns)", a["full_name"] == b["full_name"])


def test_pick_repo_of_day_varies_across_dates():
    ranked = [{"full_name": f"repo/{i}"} for i in range(5)]
    picks = {pick_repo_of_day(ranked, set(), date_seed=f"2026-07-{d:02d}")["full_name"] for d in range(1, 15)}
    check("doesn't robotically always pick #1 (varies across days)", len(picks) > 1)


def test_history_window_stays_at_30():
    history = [{"date": f"day{i}", "repo": f"r{i}"} for i in range(30)]
    new_entry = {"date": "today", "repo": "new/repo"}
    updated = update_repo_of_day_history(history, new_entry, "today")
    check("window capped at 30", len(updated) == 30)
    check("newest entry is first (reverse-chronological)", updated[0]["repo"] == "new/repo")
    check("oldest entry dropped", "r29" not in [e["repo"] for e in updated])


def test_history_rerun_same_day_replaces_not_duplicates():
    history = [{"date": "today", "repo": "old/pick"}]
    new_entry = {"date": "today", "repo": "new/pick"}
    updated = update_repo_of_day_history(history, new_entry, "today")
    check("re-running the same day replaces, doesn't duplicate", len(updated) == 1 and updated[0]["repo"] == "new/pick")


def test_resolve_flag_icon_matches_keyword():
    check("'San Francisco, USA' -> flag-us", resolve_flag_icon("San Francisco, USA") == "flag-us")
    check("'Singapore' -> flag-sg", resolve_flag_icon("Singapore") == "flag-sg")
    check("case-insensitive match", resolve_flag_icon("BERLIN, GERMANY") == "flag-de")


def test_resolve_flag_icon_defaults_to_intl():
    check("blank location -> flag-intl", resolve_flag_icon(None) == "flag-intl")
    check("unrecognized location -> flag-intl", resolve_flag_icon("Somewhere over the rainbow") == "flag-intl")


def test_pick_category_icon_matches_keyword():
    check("'agent' in description -> brain", pick_category_icon("foo/bar", "a multi agent framework") == "brain")
    check("'rust' in repo name -> crab", pick_category_icon("foo/rust-tool", None) == "crab")
    check("'python' -> snake", pick_category_icon("foo/python-utils", None) == "snake")


def test_pick_category_icon_defaults_to_package():
    check("no keyword match -> package", pick_category_icon("foo/bar", "just a thing") == "package")


def test_pick_category_icon_word_boundary_not_substring():
    # regression test: the original daily_profile_boost.py used plain
    # substring matching, which meant "go" matched inside "google" and
    # "algorithm" — word-boundary matching must not repeat that.
    check("'go' doesn't false-match inside 'google'", pick_category_icon("foo/google-clone", None) != "blue-circle")
    check("'go' doesn't false-match inside 'algorithm'", pick_category_icon("foo/bar", "sorting algorithm") != "blue-circle")
    check("'go' does match standalone", pick_category_icon("foo/go-server", None) == "blue-circle")


def test_resolve_flag_icon_word_boundary_not_substring():
    check("'uk' doesn't false-match inside 'Ukraine'", resolve_flag_icon("Ukraine") != "flag-uk")
    check("'uk' does match standalone", resolve_flag_icon("London, UK") == "flag-uk")


def test_build_card_shape():
    repo = {"full_name": "owner/repo", "description": "an autonomous agent thing", "language": "Python",
            "stargazers_count": 12345, "forks_count": 678}
    card = build_card(repo, location="Tokyo, Japan", date_label="Jul 8")
    check("build_card includes date when given one", card["date"] == "Jul 8")
    check("build_card humanizes stars", card["stars"] == "12.3k")
    check("build_card tags agent-flavored descriptions as robot/brain category", card["cat"] in ("robot", "brain"))
    check("build_card resolves the passed-in location to a flag", card["flag"] == "flag-jp")


def test_build_card_no_location():
    repo = {"full_name": "owner/repo", "description": "a thing", "language": None,
            "stargazers_count": 10, "forks_count": 2}
    card = build_card(repo, location=None)
    check("build_card falls back to flag-intl when location is None", card["flag"] == "flag-intl")
    check("build_card has no 'date' key when date_label isn't passed", "date" not in card)


def test_build_card_includes_stars_today_delta():
    repo = {"full_name": "owner/repo", "description": "a thing", "language": "Python",
            "stargazers_count": 50_000, "forks_count": 100, "delta": 2100}
    card = build_card(repo, location=None)
    check("stars_today formatted", card["stars_today"] == "+2.1k")


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
