#!/usr/bin/env python3
"""
Fetch actual isolated MP4 clips from skluck/celery-man into refs/video/
"""
import os
import sys
import urllib.request

VIDEOS = [
    "celery1.mp4",
    "celery2.mp4",
    "celery3.mp4",
    "celery4.mp4",
    "oyster1.mp4",
    "oyster2.mp4",
    "tayne1.mp4",
    "tayne2.mp4",
    "tayne3.mp4",
    "tayne4.mp4",
    "tayne5.mp4",
]

BASE_URL = "https://raw.githubusercontent.com/skluck/celery-man/master/video/"

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "refs", "video")
    os.makedirs(out_dir, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0"}
    for v in VIDEOS:
        dst = os.path.join(out_dir, v)
        if os.path.exists(dst):
            print(f"  [cached] {v}")
            continue
        url = BASE_URL + v
        print(f"  [downloading] {v} <- {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp, open(dst, "wb") as f:
                f.write(resp.read())
            print(f"  [saved] {v} ({os.path.getsize(dst)} bytes)")
        except Exception as e:
            print(f"  [error] {v}: {e}")

if __name__ == "__main__":
    main()
