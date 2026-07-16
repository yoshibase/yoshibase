"""Build a reverse-chronological 30-day calendar grid for repo-of-day display."""
from __future__ import annotations
import datetime as dt

CALENDAR_DAYS = 30


def date_label(day: dt.date) -> str:
    """Match fetch_trending.py today_label format (e.g. 'Jul 16')."""
    return day.strftime("%b ") + str(day.day)


def build_repo_of_day_grid(
    history: list[dict],
    days: int = CALENDAR_DAYS,
    today: dt.date | None = None,
) -> list[dict]:
    """Last `days` calendar days, newest first. Missing days get date-only placeholders."""
    today = today or dt.date.today()
    by_date = {e["date"]: e for e in history if e.get("date")}
    grid: list[dict] = []
    for offset in range(days):
        label = date_label(today - dt.timedelta(days=offset))
        grid.append(by_date.get(label) or {"date": label})
    return grid
