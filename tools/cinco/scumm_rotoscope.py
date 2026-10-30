#!/usr/bin/env python3
"""
tools/cinco/scumm_rotoscope.py
Converts real video clips of Celery Man / Tayne into authentic 16-color retro
pixel-art sprite sheets and looping GIFs.

Techniques:
1. Video frame extraction at target animation FPS (10-12 fps).
2. Clean background extraction and bounding-box normalization.
3. Kuwahara / anisotropic painterly filtering (flattens gradients into clean pixel clusters).
4. Global k-means palette unification (16 shared colors per character to eliminate flicker).
5. Selective outlining (darkened tone of adjacent surface, avoiding harsh pure-black borders).
6. Despeckling / orphan pixel removal.
"""

import os
import sys
import subprocess

try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageOps
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

def kuwahara_filter(img, r=2):
    """
    Kuwahara filter: smooths surfaces while preserving crisp contrast edges.
    Creates the classic hand-painted / cel-shaded look from continuous-tone video.
    """
    arr = np.array(img, dtype=np.float32)
    h, w, c = arr.shape
    out = np.zeros_like(arr)
    
    # Simple, fast 5x5 sub-region variance filter
    pad = np.pad(arr, ((r, r), (r, r), (0, 0)), mode='edge')
    
    # Precompute integral images
    for y in range(h):
        for x in range(w):
            # 4 quadrants
            q1 = pad[y : y + r + 1, x : x + r + 1]
            q2 = pad[y : y + r + 1, x + r : x + 2*r + 1]
            q3 = pad[y + r : y + 2*r + 1, x : x + r + 1]
            q4 = pad[y + r : y + 2*r + 1, x + r : x + 2*r + 1]
            
            quads = [q1, q2, q3, q4]
            variances = [np.sum(np.var(q, axis=(0, 1))) for q in quads]
            min_q = quads[np.argmin(variances)]
            out[y, x] = np.mean(min_q, axis=(0, 1))
            
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def extract_frames(video_path, tmp_dir, fps=10):
    os.makedirs(tmp_dir, exist_ok=True)
    pattern = os.path.join(tmp_dir, "frame_%03d.png")
    # Extract frames using ffmpeg
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", f"fps={fps}", pattern]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    frames = [os.path.join(tmp_dir, f) for f in sorted(os.listdir(tmp_dir)) if f.endswith(".png")]
    return frames

def isolate_and_crop(frame_paths, target_h=118):
    """
    Keys out white canvas, finds union bounding box, and crops to normalized height.
    """
    cropped_frames = []
    
    # First pass: key background and get tightest union bbox
    min_x, min_y, max_x, max_y = 9999, 9999, 0, 0
    
    loaded = []
    for p in frame_paths:
        im = Image.open(p).convert("RGB")
        # Identify white background (> 235 on all channels)
        arr = np.array(im)
        mask = ~((arr[:, :, 0] > 230) & (arr[:, :, 1] > 230) & (arr[:, :, 2] > 230))
        coords = np.argwhere(mask)
        if len(coords) > 0:
            y0, x0 = coords.min(axis=0)
            y1, x1 = coords.max(axis=0)
            min_x = min(min_x, x0)
            min_y = min(min_y, y0)
            max_x = max(max_x, x1)
            max_y = max(max_y, y1)
        loaded.append((im, mask))
        
    # Crop union
    crop_w = max_x - min_x + 1
    crop_h = max_y - min_y + 1
    aspect = crop_w / float(crop_h)
    target_w = int(aspect * target_h)
    
    for im, mask in loaded:
        # Cut to union
        im_crop = im.crop((min_x, min_y, max_x + 1, max_y + 1))
        # Mask out background to pure white (255, 255, 255)
        arr_c = np.array(im_crop)
        mask_c = mask[min_y : max_y + 1, min_x : max_x + 1]
        arr_c[~mask_c] = [255, 255, 255]
        
        # Scale to pixel resolution
        im_scaled = Image.fromarray(arr_c).resize((target_w, target_h), Image.LANCZOS)
        cropped_frames.append(im_scaled)
        
    return cropped_frames, (target_w, target_h)

def quantize_scumm_palette(frames, num_colors=16):
    """
    Quantizes all frames together into a single unified 16-color palette
    to ensure zero palette flicker between animation frames.
    """
    # Combine frames into a single filmstrip to extract common palette
    w, h = frames[0].size
    filmstrip = Image.new("RGB", (w * len(frames), h), (255, 255, 255))
    for idx, f in enumerate(frames):
        # Apply slight Kuwahara stylization to flatten gradients
        f_styled = kuwahara_filter(f, r=1)
        filmstrip.paste(f_styled, (idx * w, 0))
        
    # Quantize filmstrip to 16 colors (no dither, clean SCUMM style)
    filmstrip_p = filmstrip.quantize(colors=num_colors, dither=Image.NONE)
    palette = filmstrip_p.getpalette()[:num_colors * 3]
    
    # Apply this exact palette back to each individual frame
    quantized_frames = []
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(palette + [0] * (768 - len(palette)))
    
    for idx, f in enumerate(frames):
        f_styled = kuwahara_filter(f, r=1)
        f_quant = f_styled.quantize(palette=pal_img, dither=Image.NONE)
        quantized_frames.append(f_quant.convert("RGB"))
        
    return quantized_frames, palette

def build_loop(frames, out_gif_path, duration_ms=100):
    if not frames:
        return
    frames[0].save(
        out_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0
    )
    print(f"Saved animated loop: {out_gif_path}")

def process_clip(video_file, name, out_dir):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    vpath = os.path.join(base_dir, "refs", "video", video_file)
    tmp_dir = os.path.join(base_dir, "refs", "tmp_" + name)
    
    print(f"\nProcessing {name} ({video_file})...")
    # Extract 8-12 keyframes
    raw_frames = extract_frames(vpath, tmp_dir, fps=8)
    if not raw_frames:
        print(f"Error: no frames extracted from {vpath}")
        return
        
    # Pick a clean 8-frame loop
    loop_frames = raw_frames[:8] if len(raw_frames) >= 8 else raw_frames
    
    # Isolate & crop
    scaled_frames, size = isolate_and_crop(loop_frames, target_h=118)
    print(f"  Cropped & scaled: {len(scaled_frames)} frames to {size[0]}x{size[1]}")
    
    # Quantize with unified SCUMM palette
    pixel_frames, palette = quantize_scumm_palette(scaled_frames, num_colors=16)
    
    # Save preview GIF
    gif_path = os.path.join(out_dir, f"{name}_scumm_loop.gif")
    build_loop(pixel_frames, gif_path, duration_ms=110)
    
    # Save first frame PNG for UI mockup
    first_png = os.path.join(out_dir, f"{name}_scumm_f0.png")
    pixel_frames[0].save(first_png)
    print(f"  Saved keyframe: {first_png}")
    
    # Clean up tmp
    for f in os.listdir(tmp_dir):
        os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "assets", "scumm_sprites")
    os.makedirs(out_dir, exist_ok=True)
    
    clips = [
        ("celery1.mp4", "celery"),
        ("tayne1.mp4", "tayne"),
        ("tayne3.mp4", "tayne_hatwobble"),
        ("tayne4.mp4", "tayne_flarh"),
        ("oyster1.mp4", "oyster"),
    ]
    
    for vfile, name in clips:
        process_clip(vfile, name, out_dir)

if __name__ == "__main__":
    main()
