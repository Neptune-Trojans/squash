"""Tests for squash.video.loader."""

import pytest

from squash.video.loader import load_video


def test_load_video_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_video("/nonexistent/video.mp4")
