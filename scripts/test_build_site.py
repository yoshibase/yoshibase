"""Tests for the yoshibase.com build (no network)."""
import datetime as dt
import json
import os
import re
import tempfile

from build_site import build, contribution_bars, page_values


def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    assert cond, label


NOW = dt.datetime(2026, 10, 29, 0, 7, tzinfo=dt.timezone.utc)


def _contrib(tmp, data):
    with open(os.path.join(tmp, "contributions.json"), "w") as f:
        json.dump(data, f)


def test_contribution_values():
    with tempfile.TemporaryDirectory() as tmp:
        _contrib(tmp, {"total": 227, "weeks": [0, 3, 10]})
        v = page_values(tmp, NOW)
        check("total on the badge", v["GH_TOTAL"] == "227")
        check("caption", v["GH_CAPTION"].startswith("227 contributions"))
        check("one bar per week", v["GH_BARS"].count("<rect") == 3)


def test_missing_data_falls_back_quietly():
    with tempfile.TemporaryDirectory() as tmp:
        v = page_values(tmp, NOW)
        check("fallback caption", v["GH_CAPTION"] == "A year of commits")
        check("still draws a waveform", v["GH_BARS"].count("<rect") == 53)


def test_bars_never_exceed_the_frame():
    svg = contribution_bars([0, 1, 50, 2])
    heights = [float(x) for x in re.findall(r'height="([0-9.]+)"', svg)[1:]]
    check("bar heights within 150", all(2 <= hgt <= 150 for hgt in heights))


def test_build_fills_every_placeholder():
    with tempfile.TemporaryDirectory() as data, tempfile.TemporaryDirectory() as out:
        _contrib(data, {"total": 3, "weeks": [3]})
        site = os.path.join(out, "_site")
        build(site, data, NOW)
        for page in ("index.html", "about.html"):
            check(f"no placeholders left in {page}", "{{" not in open(os.path.join(site, page)).read())
        check("CNAME written", open(os.path.join(site, "CNAME")).read().strip() == "yoshibase.com")
        check("player assets copied", all(os.path.exists(os.path.join(site, f)) for f in
              ("player.css", "player.js", "fonts/archivo.woff2", "img/busker.jpg")))


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)} tests passed.")
