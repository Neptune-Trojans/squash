import argparse

from src.squash.utils.split_video_to_frames import split_video_to_frames


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a video into individual frames")
    parser.add_argument("--video_path", type=str, help="Path to the input video file")
    parser.add_argument("--output_path", type=str, default="data/output", help="Base output folder (default: data/output)")
    parser.add_argument("--format", type=str, default="jpg", choices=["jpg", "png"], help="Image format (default: jpg)")
    args = parser.parse_args()

    split_video_to_frames(args.video_path, args.output_path, args.format)


if __name__ == "__main__":
    main()