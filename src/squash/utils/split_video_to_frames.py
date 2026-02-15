import os
import cv2


def split_video_to_frames(
    video_path: str,
    output_path: str = "data/output",
    fmt: str = "jpg",
) -> str:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(output_path, "images", video_name)
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_idx = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        filename = os.path.join(output_dir, f"frame_{frame_idx:06d}.{fmt}")
        cv2.imwrite(filename, frame)
        frame_idx += 1

        if frame_idx % 100 == 0:
            print(f"  Saved {frame_idx}/{total} frames")

    cap.release()
    print(f"Done — saved {frame_idx} frames to {output_dir}")
    return output_dir

