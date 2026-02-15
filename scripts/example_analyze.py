#!/usr/bin/env python3
"""Run court calibration on a squash video."""

import argparse
from pathlib import Path

import cv2
import yaml

from src.squash.court_calibration.court_calibrator import CourtCalibrator
from src.squash.video.loader import load_video, get_video_info


def main() -> None:

    video_path = '../data/videos/vid.mp4'
    # Load video info
    cap = load_video(video_path)
    info = get_video_info(cap)
    print(f"Video: {video_path}")
    print(f"  Resolution: {info['width']}x{info['height']}")
    print(f"  FPS: {info['fps']}")
    print(f"  Frames: {info['frame_count']}")

    # Read first frame
    ok, frame = cap.read()
    if not ok:
        print("Error: Failed to read first frame")
        cap.release()
        return

    # Load court calibration config
    config_path = Path(__file__).resolve().parent.parent / "src" / "squash" / "court_calibration" / "court_calibration.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Run court calibration
    calibrator = CourtCalibrator(config=config)
    keypoints = calibrator.detect_keypoints(frame)

    print("\nDetected court elements:")
    for class_name, corners in keypoints.items():
        print(f"  {class_name}: {corners.tolist()}")

    cap.release()


if __name__ == "__main__":
    main()
