#!/usr/bin/env python3
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
if os.path.exists(venv_py) and sys.executable != venv_py:
    os.execv(venv_py, [venv_py] + sys.argv)

from PIL import Image

im = Image.open("docs/cinco/screenshots/01_boot_celery.png")
colors = im.getcolors(maxcolors=256)
print(f"Total unique colors in 01_boot_celery.png: {len(colors)}")
# Sort by count descending
colors.sort(key=lambda x: x[0], reverse=True)
for count, (r, g, b) in colors[:10]:
    hex_str = f"#{r:02X}{g:02X}{b:02X}"
    print(f"  {count:5d} pixels: {hex_str}  RGB({r:3d}, {g:3d}, {b:3d})")

# Check desktop background at (2, 2)
bg = im.getpixel((2, 2))
print(f"Desktop at (2, 2): RGB{bg}  Hex: #{bg[0]:02X}{bg[1]:02X}{bg[2]:02X}")

# Check dancer region center at (120, 90)
dancer_pixel = im.getpixel((120, 90))
print(f"Dancer at (120, 90): RGB{dancer_pixel}  Hex: #{dancer_pixel[0]:02X}{dancer_pixel[1]:02X}{dancer_pixel[2]:02X}")
