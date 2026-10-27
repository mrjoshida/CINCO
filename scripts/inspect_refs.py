#!/usr/bin/env python3
"""
Inspect reference files in refs/
"""
import os
import sys

# Auto-trampoline into .venv if PIL not available
try:
    from PIL import Image
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    refs_dir = os.path.join(base_dir, "refs")
    for f in sorted(os.listdir(refs_dir)):
        p = os.path.join(refs_dir, f)
        if os.path.isfile(p):
            try:
                im = Image.open(p)
                nframes = getattr(im, "n_frames", 1)
                print(f"{f:25s}: size={im.size}, mode={im.mode}, frames={nframes}, {os.path.getsize(p)} bytes")
            except Exception as e:
                print(f"{f:25s}: not an image ({e}), {os.path.getsize(p)} bytes")

if __name__ == "__main__":
    main()
