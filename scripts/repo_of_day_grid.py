"""Build a reverse-chronological 30-day calendar grid for repo-of-day display."""
from __future__ import annotations
import datetime as dt

CALENDAR_DAYS = 30


def profile_today(day: dt.date | None = None) -> dt.date:
    """Calendar day for the profile grid — always UTC to match the nightly workflow."""
    if day is not None:
        return day
    return dt.datetime.now(dt.timezone.utc).date()


def date_label(day: dt.date) -> str:
    """Match fetch_trending.py today_label format (e.g. 'Jul 16')."""
    return day.strftime("%b ") + str(day.day)


def build_repo_of_day_grid(
    history: list[dict],
    days: int = CALENDAR_DAYS,
    today: dt.date | None = None,
) -> list[dict]:
    """Last `days` calendar days, newest first. Missing days get date-only placeholders."""
    today = profile_today(today)
    by_date = {e["date"]: e for e in history if e.get("date")}
    grid: list[dict] = []
    for offset in range(days):
        label = date_label(today - dt.timedelta(days=offset))
        grid.append(by_date.get(label) or {"date": label})
    return grid


def validate_consecutive_grid(grid: list[dict], today: dt.date | None = None) -> None:
    """Fail fast if the grid is not 30 consecutive calendar days (newest first)."""
    today = profile_today(today)
    if len(grid) != CALENDAR_DAYS:
        raise ValueError(f"repo-of-day grid must have {CALENDAR_DAYS} cells, got {len(grid)}")
    for i, cell in enumerate(grid):
        expected = date_label(today - dt.timedelta(days=i))
        if cell.get("date") != expected:
            raise ValueError(
                f"repo-of-day grid slot {i} is {cell.get('date')!r}, expected consecutive {expected!r}"
            )
