#!/usr/bin/env python3
import os
import sys

try:
    from PIL import Image
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

def main():
    p = "/Users/joshcaldwell/dev/celery-man/docs/cinco/mock/01_idle_celery.png"
    im = Image.open(p)
    print(f"File: {p}")
    print(f"Exact Image Dimensions: width={im.size[0]} px, height={im.size[1]} px")
    print(f"Total Pixel Count: {im.size[0] * im.size[1]} pixels (240x240 = 57,600)")
    
    # Check sprite dimensions inside
    sp_path = "/Users/joshcaldwell/dev/celery-man/assets/scumm_sprites/celery_scumm_f0.png"
    sp = Image.open(sp_path)
    print(f"Celery Sprite Dimensions: width={sp.size[0]} px, height={sp.size[1]} px")

if __name__ == "__main__":
    main()
