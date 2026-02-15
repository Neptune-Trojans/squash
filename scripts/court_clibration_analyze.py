from pathlib import Path

import yaml

if __name__ == '__main__':
    from src.squash.court_calibration.court_calibrator import CourtCalibrator
    from src.squash.visualization.court_visualizer import CourtVisualizer

    # Load court calibration config
    config_path = Path(__file__).resolve().parent.parent / "src" / "squash" / "court_calibration" / "court_calibration.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    calibrator = CourtCalibrator(config=config)
    visualizer = CourtVisualizer()
    visualizer.process_video("../data/videos/vid.mp4", "../data/videos/vid_annotated.mp4", calibrator)