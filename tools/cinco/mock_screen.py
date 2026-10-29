#!/usr/bin/env python3
"""
tools/cinco/mock_screen.py
Renders high-fidelity, authentic 240x240 CINCO 2.5 screens using real rotoscoped
and pixelated character sprites from the Cinco Identity Generator 2.5 suite.
"""

import os
import sys
import argparse

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    if os.path.exists(venv_py) and sys.executable != venv_py:
        os.execv(venv_py, [venv_py] + sys.argv)
    raise

# 24-bit Colors from style.md
C_DESKTOP = (109, 192, 219)       # #6DC0DB cyan
C_WIN_FACE = (237, 236, 237)      # #EDECED
C_WIN_WHITE = (255, 255, 255)
C_BORDER_LIGHT = (255, 255, 255)  # 3D highlight
C_BORDER_DARK = (128, 128, 128)   # 3D shadow
C_BORDER_MID = (204, 204, 204)    # Outer border
C_BLACK = (0, 0, 0)
C_TERM_BG = (0, 0, 0)
C_TERM_TEXT = (255, 255, 255)
C_TERM_DIM = (136, 136, 136)
C_PROG_BLUE = (4, 32, 172)        # #0420AC
C_PAPER = (255, 254, 232)
C_INK = (32, 32, 32)

def draw_bevel_rect(draw, x, y, w, h, fill=C_WIN_FACE, sunken=False):
    c_tl = C_BORDER_DARK if sunken else C_BORDER_LIGHT
    c_br = C_BORDER_LIGHT if sunken else C_BORDER_DARK
    
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=C_BORDER_MID)
    draw.line([x + 1, y + 1, x + w - 2, y + 1], fill=c_tl)
    draw.line([x + 1, y + 1, x + 1, y + h - 2], fill=c_tl)
    draw.line([x + 1, y + h - 2, x + w - 2, y + h - 2], fill=c_br)
    draw.line([x + w - 2, y + 1, x + w - 2, y + h - 2], fill=c_br)

def draw_window(draw, x, y, w, h, title="Celery Man", active=True):
    draw_bevel_rect(draw, x, y, w, h, fill=C_WIN_FACE)
    # Titlebar
    tb_h = 16
    draw.rectangle([x + 3, y + 3, x + w - 4, y + 3 + tb_h], fill=C_WIN_WHITE, outline=C_BLACK)
    
    # Minimize box [-] on left
    draw.rectangle([x + 4, y + 4, x + 4 + 14, y + 4 + 14], fill=C_WIN_FACE, outline=C_BLACK)
    draw.line([x + 7, y + 11, x + 15, y + 11], fill=C_BLACK, width=2)
    
    # Scroll buttons [v][^] on right
    rx = x + w - 4 - 30
    draw.rectangle([rx, y + 4, rx + 13, y + 4 + 14], fill=C_WIN_FACE, outline=C_BLACK)
    draw.polygon([(rx + 4, y + 8), (rx + 10, y + 8), (rx + 7, y + 13)], fill=C_BLACK) # v
    
    rx2 = rx + 14
    draw.rectangle([rx2, y + 4, rx2 + 13, y + 4 + 14], fill=C_WIN_FACE, outline=C_BLACK)
    draw.polygon([(rx2 + 4, y + 13), (rx2 + 10, y + 13), (rx2 + 7, y + 8)], fill=C_BLACK) # ^
    
    # Title text
    tx = x + 24
    draw.text((tx, y + 5), title, fill=C_BLACK)

    # Inner Canvas
    cx = x + 4
    cy = y + 21
    cw = w - 8
    ch = h - 25
    draw_bevel_rect(draw, cx, cy, cw, ch, fill=C_WIN_WHITE, sunken=True)
    return (cx + 2, cy + 2, cw - 4, ch - 4)

def draw_terminal(draw, x, y, w, h, lines=None):
    draw_bevel_rect(draw, x, y, w, h, fill=C_TERM_BG, sunken=True)
    draw.rectangle([x + 2, y + 2, x + w - 3, y + 13], fill=C_BORDER_DARK)
    draw.text((x + 6, y + 3), "Paul's COMPUTER", fill=C_WIN_WHITE)
    
    if not lines:
        lines = ["> Good morning Paul.", "> What will your first sequence be?"]
    
    ly = y + 16
    for line in lines:
        draw.text((x + 6, ly), line, fill=C_TERM_TEXT)
        ly += 11
    # Blinking cursor
    draw.line([x + 6 + len(lines[-1]) * 6, ly - 2, x + 6 + len(lines[-1]) * 6 + 5, ly - 2], fill=C_TERM_TEXT, width=1)

def paste_sprite(canvas_img, sprite_img_path, canvas_box, offset_y=0, mosaic_block=1):
    if not os.path.exists(sprite_img_path):
        return
    sp = Image.open(sprite_img_path).convert("RGBA")
    
    # Apply mosaic if requested
    if mosaic_block > 1:
        sw, sh = sp.size
        bw = max(1, sw // mosaic_block)
        bh = max(1, sh // mosaic_block)
        sp = sp.resize((bw, bh), Image.NEAREST).resize((sw, sh), Image.NEAREST)
        
    cx, cy, cw, ch = canvas_box
    # Center sprite on canvas
    sw, sh = sp.size
    px = cx + (cw - sw) // 2
    py = cy + (ch - sh) // 2 + offset_y
    
    canvas_img.paste(sp, (px, py), sp if sp.mode == "RGBA" else None)

def apply_rect_mosaic(img, rect, block_size=12):
    x0, y0, x1, y1 = rect
    box = (x0, y0, x1, y1)
    sub = img.crop(box)
    bw = max(1, (x1 - x0) // block_size)
    bh = max(1, (y1 - y0) // block_size)
    sub = sub.resize((bw, bh), Image.NEAREST).resize((x1 - x0, y1 - y0), Image.NEAREST)
    img.paste(sub, box)

def render_state(state_name, out_dir, sprites_dir, art_dir):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    img = Image.new("RGB", (240, 240), C_DESKTOP)
    draw = ImageDraw.Draw(img)
    
    # Prefer scumm_sprites (clean 16-color Kuwahara clusters without black outlines)
    scumm_dir = os.path.join(base_dir, "assets", "scumm_sprites")
    celery_sp = os.path.join(scumm_dir, "celery_scumm_f0.png")
    tayne_sp = os.path.join(scumm_dir, "tayne_scumm_f0.png")
    tayne_wobble_sp = os.path.join(scumm_dir, "tayne_hatwobble_scumm_f0.png")
    tayne_flarh_sp = os.path.join(scumm_dir, "tayne_flarh_scumm_f0.png")
    tayne_nude_sp = os.path.join(scumm_dir, "tayne_scumm_f0.png") # will be mosaic censored
    oyster_sp = os.path.join(scumm_dir, "oyster_scumm_f0.png")
    
    if state_name == "01_idle_celery":
        canvas = draw_window(draw, 4, 4, 232, 160, title="Celery Man")
        paste_sprite(img, celery_sp, canvas)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> Good morning Paul.",
            "> What will your first sequence be?",
            "> Celery Man loaded."
        ])
        
    elif state_name == "02_4d3d3d3_engaged":
        offsets = [(4, 4), (16, 12), (28, 20), (40, 28)]
        for i, (ox, oy) in enumerate(offsets):
            is_top = (i == len(offsets) - 1)
            canvas = draw_window(draw, ox, oy, 192, 136, title="Celery Man", active=is_top)
            if is_top:
                paste_sprite(img, celery_sp, canvas)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> Kick up the 4d3d3d3.",
            "> 4d3d3d3 engaged.",
            "> K1 Macro: 84 / 127"
        ])
        
    elif state_name == "03_tayne_beta":
        canvas = draw_window(draw, 4, 4, 232, 160, title="Tayne (BETA)")
        paste_sprite(img, tayne_sp, canvas)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> I have a BETA sequence.",
            "> Tayne: Hi, I'm Tayne.",
            "> Now Tayne I can get into."
        ])
        
    elif state_name == "04_hat_wobble":
        canvas = draw_window(draw, 4, 4, 232, 160, title="Tayne - Hat Wobble")
        paste_sprite(img, tayne_wobble_sp, canvas)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> Can I see a hat wobble?",
            "> Hat wobble: LFO SYNC ON",
            "> Vibrato: 6.2 Hz (1/8th note)"
        ])
        
    elif state_name == "05_flarhgunnstow":
        canvas = draw_window(draw, 10, 8, 226, 154, title="Tayne - FLARHGUNNSTOW!")
        paste_sprite(img, tayne_flarh_sp, canvas)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> And a flarhgunnstow?",
            "> ARP: CHAOS RATCHET ON",
            "> Slicer stutter active"
        ])
        
    elif state_name == "06_nsfw_warning":
        canvas = draw_window(draw, 4, 4, 232, 160, title="Tayne (BETA)")
        paste_sprite(img, tayne_sp, canvas)
        # Warning Modal Dialog
        draw_bevel_rect(draw, 20, 48, 200, 76, fill=C_WIN_FACE)
        draw.rectangle([23, 51, 216, 65], fill=C_PROG_BLUE)
        draw.text((26, 52), "SECURITY PROTOCOL", fill=C_WIN_WHITE)
        draw.text((28, 70), "THIS IS NOT SUITABLE", fill=C_BLACK)
        draw.text((28, 80), "FOR WORK. ARE YOU SURE?", fill=C_BLACK)
        draw_bevel_rect(draw, 140, 96, 50, 18, fill=C_WIN_FACE)
        draw.text((152, 99), "[YES]", fill=C_BLACK)
        
        draw_terminal(draw, 4, 168, 232, 68, [
            "> FX: Nude Tayne request",
            "> Warning: NSFW protocol",
            "> Press FX to confirm (Mm-hmm)"
        ])

    elif state_name == "07_nude_mosaic":
        canvas = draw_window(draw, 4, 4, 232, 160, title="NUDE TAYNE")
        paste_sprite(img, tayne_nude_sp, canvas)
        # Apply authentic heavy pixel censorship mosaic over pelvis/torso
        apply_rect_mosaic(img, (canvas[0] + 70, canvas[1] + 35, canvas[0] + 150, canvas[1] + 110), block_size=10)
        draw_terminal(draw, 4, 168, 232, 68, [
            "> NUDE TAYNE ENGAGED",
            "> Audio Mosaic: 4-bit / 8kHz",
            "> Oh shit... I'm okay."
        ])
        
    elif state_name == "08_oyster_printout":
        canvas = draw_window(draw, 4, 4, 232, 160, title="OYSTER")
        paste_sprite(img, oyster_sp, canvas)
        # Receipt paper slip sliding out
        px, py, pw, ph = 126, 42, 102, 126
        draw.rectangle([px, py, px + pw, py + ph], fill=C_PAPER, outline=C_INK)
        draw.text((px + 6, py + 6), "CINCO PRINT", fill=C_INK)
        draw.line([px + 6, py + 18, px + pw - 6, py + 18], fill=C_INK)
        draw.text((px + 6, py + 22), "OYSTER SMILING", fill=C_INK)
        # Miniature dithered oyster on receipt
        if os.path.exists(oyster_sp):
            oy = Image.open(oyster_sp).convert("L")
            oy_thumb = oy.resize((84, 58), Image.LANCZOS).convert("1")
            img.paste(oy_thumb, (px + 9, py + 36))
        draw.text((px + 6, py + 104), "PATCH SAVED #3", fill=C_INK)
        
        draw_terminal(draw, 4, 168, 232, 68, [
            "> Printout of Oyster smiling",
            "> Printing receipt...",
            "> Patch saved to Flash Slot 3"
        ])

    elif state_name == "09_talk_soundboard":
        canvas = draw_window(draw, 4, 4, 232, 160, title="Cinco Voice Synthesizer")
        draw_terminal(draw, 4, 24, 232, 212, [
            "CINCO SPEECH INTERFACE",
            "-------------------------",
            "> MODE: SOUNDBOARD",
            "> KEY F3: 'Good morning Paul'",
            "> KEY G3: 'Yes, Paul'",
            "> KEY A3: '4d3d3d3 engaged'",
            "> KEY B3: 'Hat wobble'",
            "> KEY C4: 'Flarhgunnstow'",
            "> KEY D4: 'Nude Tayne'",
            "> KEY E4: 'Not computing'",
            "-------------------------",
            "Pitch: 44.1kHz TMS5220 LPC",
            "Singing Mode: Play key to tune"
        ])

    dst = os.path.join(out_dir, f"{state_name}.png")
    img.save(dst)
    print(f"Rendered: {dst}")

def main():
    parser = argparse.ArgumentParser(description="Render CINCO 2.5 screen mockups")
    parser.add_argument("--all", action="store_true", help="Render all screen states")
    parser.add_argument("--out", default="docs/cinco/mock", help="Output directory")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, args.out)
    sprites_dir = os.path.join(base_dir, "assets", "sprites_pixelated")
    art_dir = os.path.join(base_dir, "docs", "cinco", "art")
    os.makedirs(out_dir, exist_ok=True)

    states = [
        "01_idle_celery",
        "02_4d3d3d3_engaged",
        "03_tayne_beta",
        "04_hat_wobble",
        "05_flarhgunnstow",
        "06_nsfw_warning",
        "07_nude_mosaic",
        "08_oyster_printout",
        "09_talk_soundboard"
    ]
    for s in states:
        render_state(s, out_dir, sprites_dir, art_dir)

if __name__ == "__main__":
    main()
