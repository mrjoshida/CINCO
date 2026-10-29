#!/usr/bin/env python3
"""
tools/cinco/pixelate_frames.py
Converts extracted video frames of Paul into authentic 16-color
retro pixel art sprites fitted for the 240x240 screen window.
"""
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

def pixelate_frame(src_path, dst_path, target_h=116, colors=16, dither=True):
    im = Image.open(src_path).convert("RGBA")
    
    # Isolate subject from white/near-white background
    data = im.getdata()
    new_data = []
    for r, g, b, a in data:
        # If near white
        if r > 240 and g > 240 and b > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, 255))
    im.putdata(new_data)
    
    # Get bounding box of character
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        
    w, h = im.size
    aspect = w / float(h)
    new_h = target_h
    new_w = int(aspect * new_h)
    
    # 1. Downscale to pixel-art resolution
    im_small = im.resize((new_w, new_h), Image.LANCZOS)
    
    # Paste onto clean white background
    canvas = Image.new("RGB", (new_w, new_h), (255, 255, 255))
    canvas.paste(im_small, (0, 0), im_small)
    
    # 2. Quantize to 16 colors (adaptive retro palette)
    dither_flag = Image.FLOYDSTEINBERG if dither else Image.NONE
    im_quant = canvas.quantize(colors=colors, dither=dither_flag)
    
    im_quant.convert("RGB").save(dst_path)
    print(f"Created pixel art: {dst_path} ({new_w}x{new_h}, {colors} colors)")

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    fdir = os.path.join(base_dir, "refs", "frames")
    out_dir = os.path.join(base_dir, "assets", "sprites_pixelated")
    os.makedirs(out_dir, exist_ok=True)
    
    test_frames = [
        ("celery1_f0.png", "celery_real_pixel.png"),
        ("tayne1_f0.png", "tayne_real_pixel.png"),
        ("tayne3_f0.png", "tayne_hatwobble_real_pixel.png"),
        ("tayne4_f0.png", "tayne_flarh_real_pixel.png"),
        ("tayne5_f0.png", "tayne_nude_real_pixel.png"),
        ("oyster2_f0.png", "oyster_real_pixel.png"),
    ]
    
    for src, dst in test_frames:
        src_path = os.path.join(fdir, src)
        dst_path = os.path.join(out_dir, dst)
        if os.path.exists(src_path):
            pixelate_frame(src_path, dst_path, target_h=118, colors=16, dither=True)

if __name__ == "__main__":
    main()
