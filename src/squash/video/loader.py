"""Loading and reading video files."""

from pathlib import Path

import cv2
import numpy as np


def load_video(path: str | Path) -> cv2.VideoCapture:
    """Open a video file and return a VideoCapture object.

    Raises FileNotFoundError if the path does not exist.
    Raises RuntimeError if OpenCV cannot open the file.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Video not found: {path}")

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {path}")
    return cap


def get_video_info(cap: cv2.VideoCapture) -> dict:
    """Return basic metadata for an opened VideoCapture."""
    return {
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }


def read_frame(cap: cv2.VideoCapture) -> np.ndarray | None:
    """Read the next frame, returning the array or None at end-of-video."""
    ok, frame = cap.read()
    return frame if ok else None
