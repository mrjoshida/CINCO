#!/usr/bin/env python3
"""Inspect and prepare animated GIF assets for Tayne Studio 98 in base64 data URI format.
"""
import base64
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ASSETS = {
    "idle": REPO_ROOT / "assets/scumm_sprites/tayne_scumm_loop.gif",
    "wobble": REPO_ROOT / "assets/scumm_sprites/tayne_hatwobble_scumm_loop.gif",
    "flarh": REPO_ROOT / "assets/scumm_sprites/tayne_flarh_scumm_loop.gif",
    "nude": REPO_ROOT / "assets/sprites_pixelated/tayne_nude_real_pixel.png",
    "oyster_receipt": REPO_ROOT / "assets/scumm_sprites/oyster_scumm_f0.png",
}

def main():
    print("Preparing Tayne Studio Assets...")
    out = {}
    total_bytes = 0
    for key, path in ASSETS.items():
        if not path.is_file():
            print(f"Missing: {path}")
            continue
        data = path.read_bytes()
        mime = "image/gif" if path.suffix == ".gif" else "image/png"
        b64 = base64.b64encode(data).decode("ascii")
        data_uri = f"data:{mime};base64,{b64}"
        out[key] = data_uri
        total_bytes += len(data)
        print(f"  {key}: {len(data)} bytes -> {len(data_uri)} chars ({mime})")

    print(f"Total raw asset size: {total_bytes} bytes ({total_bytes / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
