#!/usr/bin/env python3
import os
import shutil
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
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    art_dir = os.path.join(base_dir, "docs", "cinco", "art")
    os.makedirs(art_dir, exist_ok=True)
    
    # 1. Copy image-generator asset
    gen_img_src = "/Users/joshcaldwell/.gemini/antigravity/brain/f58a7aa3-c697-4814-8977-f1773867c203/celery_man_pixel_1793120745000.jpg"
    gen_img_dst = os.path.join(art_dir, "celery_man_ai_generated.jpg")
    if os.path.exists(gen_img_src):
        shutil.copyfile(gen_img_src, gen_img_dst)
        print(f"Copied AI generated image to {gen_img_dst}")
        
        # Make a pixelated version of the AI image fitting 118px height
        ai_im = Image.open(gen_img_dst).convert("RGBA")
        bbox = ai_im.getbbox()
        if bbox:
            ai_im = ai_im.crop(bbox)
        aspect = ai_im.size[0] / float(ai_im.size[1])
        new_h = 118
        new_w = int(aspect * new_h)
        ai_small = ai_im.resize((new_w, new_h), Image.LANCZOS)
        ai_small.convert("RGB").quantize(colors=16).convert("RGB").save(os.path.join(art_dir, "celery_ai_pixel_118h.png"))
        print("Generated celery_ai_pixel_118h.png")

if __name__ == "__main__":
    main()
