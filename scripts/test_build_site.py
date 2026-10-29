"""Tests for the yoshibase.com build (no network)."""
import datetime as dt
import json
import os
import tempfile

from build_site import barcode, build, page_values


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


NOW = dt.datetime(2026, 10, 29, 0, 7, tzinfo=dt.timezone.utc)


def _data(tmp, history, contrib=None):
    with open(os.path.join(tmp, "repo_of_day.json"), "w") as f:
        json.dump(history, f)
    if contrib:
        with open(os.path.join(tmp, "contributions.json"), "w") as f:
            json.dump(contrib, f)


def test_today_pick_is_escaped_and_linked():
    with tempfile.TemporaryDirectory() as tmp:
        _data(tmp, [{"date": "Oct 29", "repo": "a/b", "desc": "<script>x</script>", "stars_today": "+5"}])
        v = page_values(tmp, NOW)
        check("links the repo", v["TODAY_URL"] == "https://github.com/a/b")
        check("description escaped", "<script>" not in v["TODAY_DESC"] and "&lt;script&gt;" in v["TODAY_DESC"])
        check("momentum line", v["TODAY_DETAIL"] == "+5 stars since yesterday")


def test_missing_data_falls_back_quietly():
    with tempfile.TemporaryDirectory() as tmp:
        v = page_values(tmp, NOW)
        check("falls back to the profile", v["TODAY_URL"] == "https://github.com/yoshibase")
        check("no contribution line", v["CONTRIB_LINE"] == "")


def test_barcode_is_deterministic():
    check("same seed, same bars", barcode("x") == barcode("x"))
    check("different seed, different bars", barcode("x") != barcode("y"))


def test_build_fills_every_placeholder():
    with tempfile.TemporaryDirectory() as data, tempfile.TemporaryDirectory() as out:
        _data(data, [], {"total": 3, "active_days": 1, "longest_run": 1, "weeks": [3]})
        site = os.path.join(out, "_site")
        build(site, data, NOW)
        page = open(os.path.join(site, "index.html")).read()
        check("no placeholders left", "{{" not in page)
        check("CNAME written", open(os.path.join(site, "CNAME")).read().strip() == "yoshibase.com")
        check("fonts copied", os.path.exists(os.path.join(site, "fonts", "barlow-500.woff2")))


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
