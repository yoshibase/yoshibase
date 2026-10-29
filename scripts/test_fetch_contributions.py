"""Unit tests for the contribution summary (no network)."""
import datetime as dt

from fetch_contributions import longest_run, summarize


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


def _calendar(weeks):
    day0 = dt.date(2026, 1, 4)
    out, i = [], 0
    for week in weeks:
        days = []
        for c in week:
            days.append({"date": (day0 + dt.timedelta(days=i)).isoformat(), "contributionCount": c})
            i += 1
        out.append({"contributionDays": days})
    return {"totalContributions": sum(sum(w) for w in weeks), "weeks": out}


def test_longest_run_basic():
    check("empty is 0", longest_run([]) == 0)
    check("no activity is 0", longest_run([0, 0, 0]) == 0)
    check("run spans gaps correctly", longest_run([1, 2, 0, 3, 1, 1, 0, 5]) == 3)


def test_summarize_counts_and_weeks():
    cal = _calendar([[0, 1, 2, 0, 0, 3, 4], [1, 1]])
    s = summarize(cal, dt.datetime(2026, 1, 20, 0, 5, tzinfo=dt.timezone.utc))
    check("total from API", s["total"] == 12)
    check("active days counted", s["active_days"] == 6)
    check("longest run crosses the week boundary", s["longest_run"] == 4)
    check("weekly totals", s["weeks"] == [10, 2])
    check("date range", s["from"] == "2026-01-04" and s["to"] == "2026-01-12")


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
