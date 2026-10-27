#!/usr/bin/env python3
import os
import sys
import subprocess
import glob

# Trampoline to venv if needed
venv_py = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".venv", "bin", "python3"))
if os.path.exists(venv_py) and sys.executable != venv_py:
    os.execv(venv_py, [venv_py] + sys.argv)

from PIL import Image

def main():
    print("=== Running Celery Man Emulator Verification ===")
    
    # 1. Run Node.js emulator driver
    node_cmd = ["node", "scripts/verify_cinco_emu.mjs", "build/emu/felucca.wasm"]
    res = subprocess.run(node_cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("Error from verify_cinco_emu.mjs:")
        print(res.stderr)
        return 1

    # 2. Output directories
    doc_dir = "docs/cinco/screenshots"
    art_dir = "/Users/joshcaldwell/.gemini/antigravity/brain/f58a7aa3-c697-4814-8977-f1773867c203/screenshots"
    sub_art_dir = "/Users/joshcaldwell/.gemini/antigravity/brain/12a7daa9-aa98-48e3-8f94-7bdaa9f28d95/screenshots"
    os.makedirs(doc_dir, exist_ok=True)
    os.makedirs(art_dir, exist_ok=True)
    os.makedirs(sub_art_dir, exist_ok=True)

    ppms = sorted(glob.glob("scratch/cinco_frames/*.ppm"))
    if not ppms:
        print("Error: No PPM screenshots found!")
        return 1

    required_screens = ["10_boss_key", "11_disk_defrag", "12_screensaver", "13_cinco_error"]
    found_screens = set()

    print(f"Converting {len(ppms)} PPM screenshots to PNG...")
    for ppm_path in ppms:
        base = os.path.splitext(os.path.basename(ppm_path))[0]
        im = Image.open(ppm_path)
        
        # Verify resolution
        assert im.size == (240, 240), f"Invalid size {im.size}"
        
        # Check non-blank
        colors = len(im.getcolors(maxcolors=65536))
        assert colors > 1, f"Frame {base} is blank!"
        print(f"  Frame '{base}': size={im.size}, colors={colors}")
        found_screens.add(base)
        
        # Save to doc_dir and art_dirs
        png_doc = os.path.join(doc_dir, f"{base}.png")
        png_art = os.path.join(art_dir, f"{base}.png")
        png_sub = os.path.join(sub_art_dir, f"{base}.png")
        im.save(png_doc)
        im.save(png_art)
        im.save(png_sub)
        print(f"    Saved -> {png_doc}")

    for req in required_screens:
        assert req in found_screens, f"Required screen '{req}' was not captured!"

    print("\nALL EMULATOR VERIFICATION CHECKS PASSED!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
