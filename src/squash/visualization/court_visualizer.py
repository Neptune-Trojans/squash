"""Visualize court calibration detections on video frames."""

from pathlib import Path
from typing import Dict, Optional

import cv2
import numpy as np


# Color per class (BGR)
DEFAULT_COLORS = {
    "tin": (0, 255, 255),           # yellow
    "left-square": (255, 0, 0),     # blue
    "right-square": (0, 255, 0),    # green
    "front-wall-down": (0, 0, 255), # red
}
FALLBACK_COLOR = (255, 255, 255)


class CourtVisualizer:
    """Draw court calibration detections on video and save the result."""

    def __init__(
        self,
        colors: Optional[Dict[str, tuple]] = None,
        line_thickness: int = 2,
        font_scale: float = 0.6,
        corner_radius: int = 5,
    ):
        self.colors = colors or DEFAULT_COLORS
        self.line_thickness = line_thickness
        self.font_scale = font_scale
        self.corner_radius = corner_radius

    def draw_detections(
        self,
        frame: np.ndarray,
        keypoints: Dict[str, np.ndarray],
    ) -> np.ndarray:
        """Draw detected court elements on a single frame.

        Args:
            frame: BGR image (will not be modified in place).
            keypoints: Mapping of class_name -> (4, 2) corner array,
                       as returned by CourtCalibrator.detect_keypoints().

        Returns:
            Annotated copy of the frame.
        """
        annotated = frame.copy()

        for class_name, corners in keypoints.items():
            color = self.colors.get(class_name, FALLBACK_COLOR)
            pts = corners.astype(np.int32)

            # Draw polygon outline
            cv2.polylines(annotated, [pts], isClosed=True, color=color, thickness=self.line_thickness)

            # Draw corner circles
            for pt in pts:
                cv2.circle(annotated, tuple(pt), self.corner_radius, color, -1)

            # Label at top-left corner
            label_pos = (int(pts[0][0]), int(pts[0][1]) - 10)
            cv2.putText(
                annotated, class_name, label_pos,
                cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, color,
                thickness=self.line_thickness,
            )

        return annotated

    def process_video(
        self,
        video_path: str | Path,
        output_path: str | Path,
        calibrator,
        every_n_frames: int = 1,
    ) -> Path:
        """Run calibration on each frame, draw detections, and save the video.

        Args:
            video_path: Input video file.
            output_path: Where to write the annotated video.
            calibrator: A CourtCalibrator instance (must have detect_keypoints).
            every_n_frames: Run detection every N frames (reuse last
                            detection for intermediate frames).

        Returns:
            Path to the saved output video.
        """
        video_path = Path(video_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        last_keypoints: Dict[str, np.ndarray] = {}
        frame_idx = 0

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if frame_idx % every_n_frames == 0:
                try:
                    last_keypoints = calibrator.detect_keypoints(frame)
                except (ValueError, Exception):
                    pass  # keep previous detections if this frame fails

            annotated = self.draw_detections(frame, last_keypoints)
            writer.write(annotated)

            frame_idx += 1
            if frame_idx % 100 == 0:
                print(f"  Processed {frame_idx}/{total} frames")

        cap.release()
        writer.release()
        print(f"Saved annotated video to {output_path}")
        return output_path
