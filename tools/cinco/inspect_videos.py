#!/usr/bin/env python3
"""
Extract the first frame from each MP4 into refs/frames/ to inspect content.
"""
import os
import subprocess

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    vdir = os.path.join(base_dir, "refs", "video")
    fdir = os.path.join(base_dir, "refs", "frames")
    os.makedirs(fdir, exist_ok=True)

    for v in sorted(os.listdir(vdir)):
        if v.endswith(".mp4"):
            stem = os.path.splitext(v)[0]
            out_img = os.path.join(fdir, f"{stem}_f0.png")
            mp4_path = os.path.join(vdir, v)
            cmd = ["ffmpeg", "-y", "-ss", "00:00:00.5", "-i", mp4_path, "-vframes", "1", out_img]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(out_img):
                print(f"Extracted {stem}: {out_img} ({os.path.getsize(out_img)} B)")

if __name__ == "__main__":
    main()
