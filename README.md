# Squash

Computer vision tools for squash court detection, calibration, and visualization.

## Notebooks

- **court_lines.ipynb** -- Detects court lines using Hough Transform, filters them by angle into horizontal/vertical groups, and merges fragmented segments.
- **court_segments.ipynb** -- Detects court regions via contour detection and filters out noise by area and aspect ratio.
