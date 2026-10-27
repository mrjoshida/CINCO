#!/usr/bin/env python3
import os
import shutil

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src = os.path.join(base_dir, "docs", "cinco", "art", "celery_ai_pixel_118h.png")
    dst = "/Users/joshcaldwell/.gemini/antigravity/brain/f58a7aa3-c697-4814-8977-f1773867c203/mockups/celery_ai_pixel_118h.png"
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print("Copied celery_ai_pixel_118h.png to artifacts")

if __name__ == "__main__":
    main()
