# CINCO 2.5 — Visual Style Guide & Screen Specification

This document defines the exact dimensions, color palettes, typography, and layout rules for rendering the Cinco Identity Generator 2.5 interface on the M-VAVE FM-1's 240×240 ST7789 display.

---

## 1. Color Palette & RGB565 Tokens

The ST7789 display uses big-endian swapped 16-bit RGB565 (`swap16((r<<11)|(g<<5)|b)`).

| Element | 24-bit Hex | RGB888 | RGB565 (native) | RGB565 (swapped) |
|---|---|---|---|---|
| **Desktop Background** | `#6DC0DB` | `(109, 192, 219)` | `0x6E1B` | `0x1B6E` |
| **Window Face** | `#EDECED` | `(237, 236, 237)` | `0xEF7D` | `0x7DEF` |
| **Window Border Light (3D Highlight)** | `#FFFFFF` | `(255, 255, 255)` | `0xFFFF` | `0xFFFF` |
| **Window Border Dark (3D Shadow)** | `#808080` | `(128, 128, 128)` | `0x8410` | `0x1084` |
| **Window Border Mid (3D Outer)** | `#CCCCCC` | `(204, 204, 204)` | `0xCE79` | `0x79CE` |
| **Titlebar Background** | `#FFFFFF` | `(255, 255, 255)` | `0xFFFF` | `0xFFFF` |
| **Titlebar Text / Outline** | `#000000` | `(0, 0, 0)` | `0x0000` | `0x0000` |
| **Terminal Background** | `#000000` | `(0, 0, 0)` | `0x0000` | `0x0000` |
| **Terminal Text / Prompt** | `#FFFFFF` | `(255, 255, 255)` | `0xFFFF` | `0xFFFF` |
| **Terminal Text (Dim/Sub)** | `#888888` | `(136, 136, 136)` | `0x8C71` | `0x718C` |
| **Progress Bar Fill** | `#0420AC` | `(4, 32, 172)` | `0x0115` | `0x1501` |
| **Dialog Alert Border** | `#000000` | `(0, 0, 0)` | `0x0000` | `0x0000` |
| **Oyster Printout Paper** | `#FFFEE8` | `(255, 254, 232)` | `0xFFFD` | `0xFDFF` |
| **Oyster Printout Ink** | `#202020` | `(32, 32, 32)` | `0x2104` | `0x0421` |

---

## 2. 240×240 Screen Layout Geometry

To accommodate ST7789 SPI DMA strip rendering without a full 115 KB frame buffer, the screen is laid out into coordinate regions:

```
0,0 ----------------------------------------------------------------- 240,0
|  DESKTOP MARGIN (top 4px)                                         |
|  +-------------------------------------------------------------+  |
|  | DANCER WINDOW (x: 4, y: 4, w: 232, h: 164)                  |  |
|  | +---------------------------------------------------------+ |  |
|  | | Titlebar (h: 18px): [-] Celery Man             [v][^] | |  |
|  | +---------------------------------------------------------+ |  |
|  | | White Canvas (x: 8, y: 24, w: 224, h: 140)             | |  |
|  | |                                                         | |  |
|  | |           [ DANCER SPRITE: ~96 x 128 px ]               | |  |
|  | |                                                         | |  |
|  | +---------------------------------------------------------+ |  |
|  +-------------------------------------------------------------+  |
|  DESKTOP GAP (y: 168 to 172: 4px)                                  |
|  +-------------------------------------------------------------+  |
|  | "CINCO OS 2.5" TERMINAL (x: 4, y: 172, w: 232, h: 64)        |  |
|  | Title: CINCO OS 2.5 (h: 14px)                               |  |
|  | Black Screen: lines 1-3 (8px font, 10px pitch)             |  |
|  | > 4d3d3d3 engaged._                                         |  |
|  +-------------------------------------------------------------+  |
|  DESKTOP MARGIN (bottom 4px)                                      |
0,240 ------------------------------------------------------------- 240,240
```

### 4d3d3d3 Window Cascading Multipliers
When `K1` (4d3d3d3 intensity) increases from 0 to 127:
- **0–31 (Normal)**: 1 primary window at `(4, 4)`.
- **32–63 (2×)**: 2 windows cascaded at offset `(+10, +10)`.
- **64–95 (4×)**: 4 windows cascaded at offsets `(+8, +8)`, `(+16, +16)`, `(+24, +24)`.
- **96–127 (8× Overdrive)**: 8 windows cascading across the desktop; dancer face swaps to distorted manic grin.

### Modal Overlays (Non-Blocking)
- **NSFW Flash Warning**: Centered box `(x: 20, y: 60, w: 200, h: 80)` with thick black border and white background:
  `WARNING: THIS IS NOT SUITABLE FOR WORK.`
  `ARE YOU SURE?  [YES]`
- **Loading Dialog**: Centered box `(x: 30, y: 80, w: 180, h: 60)` with blue segmented bar `(w: 140, h: 12)`.
- **Oyster Smiling Printout**: Receipt paper slip extending from bottom right `(x: 120, y: 40, w: 100, h: 140)` with dithering dot-matrix render of Oyster.

---

## 3. Typography Specs

1. **Titlebar Font**: Clean proportional 10px sans (Inter Tight or Fukiai) in pure black on white titlebar.
2. **Terminal Monospace Font**: 5×7 or 6×8 classic retro computer monospace font with glowing cursor `_`.
3. **Buttons / Controls Chrome**:
   - Minimize box: 14×14 px with 6×2 px center horizontal black bar.
   - Scroll arrows: 14×14 px with 5×3 px triangular glyphs (`▼`, `▲`).

---

## 4. Dancer Animation Specifications

Dancers are centered on the white window canvas.

| Character | Costume & Features | Primary Animation | Loop Frames | Frame Rate |
|---|---|---|---|---|
| **Celery Man** | Silver metallic suit, dark shirt | Stiff mechanical 2-step leg kick and arm pump | 8 frames | 12 fps |
| **Oyster** | Striped red/orange flame ski toque, dark fleece | Slight shoulder bounce with fixed wide grin | 6 frames | 8 fps |
| **Tayne (BETA)** | Beige trench coat, fedora, thin mustache | Smooth arm swing and hip sway | 8 frames | 12 fps |
| **Hat Wobble** | Tayne with fedora | Tayne rhythmically tilting fedora left/right | 6 frames | 12 fps |
| **Flarhgunnstow**| Any character (Tayne default) | Chaotic flailing arms and rubbery leg kicks | 8 frames | 16 fps |
| **Nude Tayne** | Heavily mosaiced pixelated body | Suggestive pelvic swivel dance | 8 frames | 12 fps |
