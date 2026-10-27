#!/usr/bin/env python3
import os
import sys

try:
    from PIL import Image
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    fdir = os.path.join(base_dir, "refs", "frames")
    for f in sorted(os.listdir(fdir)):
        if f.endswith(".png"):
            p = os.path.join(fdir, f)
            im = Image.open(p)
            print(f"{f:15s}: size={im.size}, mode={im.mode}")

if __name__ == "__main__":
    main()
