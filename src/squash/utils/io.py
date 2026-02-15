"""File I/O helpers."""

from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    """Create a directory (and parents) if it doesn't exist, return the Path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
