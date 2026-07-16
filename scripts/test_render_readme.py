"""Unit tests for repo-of-day calendar grid rendering logic."""
import datetime as dt

from repo_of_day_grid import build_repo_of_day_grid, date_label


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


def test_date_label_matches_fetch_trending():
    d = dt.date(2026, 7, 16)
    check("Jul 16 label format", date_label(d) == "Jul 16")
    check("single-digit day has no leading zero", date_label(dt.date(2026, 7, 8)) == "Jul 8")


def test_grid_has_30_days():
    grid = build_repo_of_day_grid([], today=dt.date(2026, 7, 16))
    check("always 30 cells", len(grid) == 30)


def test_grid_newest_first():
    today = dt.date(2026, 7, 16)
    grid = build_repo_of_day_grid([], today=today)
    check("first cell is today", grid[0]["date"] == "Jul 16")
    check("last cell is 29 days ago", grid[-1]["date"] == date_label(today - dt.timedelta(days=29)))


def test_grid_maps_history_by_date():
    history = [
        {"date": "Jul 16", "repo": "new/today"},
        {"date": "Jul 8", "repo": "old/pick"},
    ]
    grid = build_repo_of_day_grid(history, today=dt.date(2026, 7, 16))
    check("today's pick mapped", grid[0]["repo"] == "new/today")
    check("Jul 8 pick in correct slot", grid[8]["repo"] == "old/pick")
    check("gap day is placeholder", "repo" not in grid[1])
    check("placeholder keeps date label", grid[1]["date"] == "Jul 15")


def test_grid_no_sample_data_filler():
    """Sparse history must not invent picks for missing days."""
    history = [{"date": "Jul 8", "repo": "only/one"}]
    grid = build_repo_of_day_grid(history, today=dt.date(2026, 7, 16))
    filled = [e for e in grid if "repo" in e]
    check("only real history entries appear", len(filled) == 1 and filled[0]["repo"] == "only/one")


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
