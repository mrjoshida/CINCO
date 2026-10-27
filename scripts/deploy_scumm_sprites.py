#!/usr/bin/env python3
import os
import shutil

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "assets", "scumm_sprites")
    art_dir = "/Users/joshcaldwell/.gemini/antigravity/brain/f58a7aa3-c697-4814-8977-f1773867c203/scumm"
    os.makedirs(art_dir, exist_ok=True)
    
    for f in os.listdir(src_dir):
        if f.endswith(".gif") or f.endswith(".png"):
            shutil.copyfile(os.path.join(src_dir, f), os.path.join(art_dir, f))
            print(f"Copied {f} to {art_dir}")

if __name__ == "__main__":
    main()
