"""Resolve data/ and repo-root paths independent of shell cwd."""
from __future__ import annotations

import os

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)


def resolve_data_dir(data_dir: str | None) -> str:
    """Absolute path to the data directory (default: <repo>/data)."""
    if not data_dir:
        return os.path.join(REPO_ROOT, "data")
    if os.path.isabs(data_dir):
        return os.path.normpath(data_dir)
    # Relative paths are from repo root (e.g. "data"), not shell cwd.
    return os.path.normpath(os.path.join(REPO_ROOT, data_dir))


def resolve_repo_dir(public_repo_dir: str) -> str:
    """Absolute path to the profile repo root (where README.template.md lives)."""
    if os.path.isabs(public_repo_dir):
        return os.path.normpath(public_repo_dir)
    return os.path.normpath(os.path.join(REPO_ROOT, public_repo_dir))
