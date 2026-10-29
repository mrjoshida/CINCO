/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO Graphics & Display Engine: ST7789 strip-aware 240x240 renderer */

#ifndef CINCO_GFX_C
#define CINCO_GFX_C

#include <stdint.h>
#include "cinco_state.h"
#include "cinco_assets.h"

/* Native RGB565 Palette Constants (lcd_fill/lcd_blit perform ST7789 byte-swapping) */
#define C_DESKTOP     0x6E1Bu   /* #6DC0DB cyan desktop */
#define C_WIN_FACE    0xEF7Du   /* #EDECED light grey window face */
#define C_WHITE       0xFFFFu   /* #FFFFFF */
#define C_BLACK       0x0000u   /* #000000 */
#define C_BORDER_DARK 0x8410u   /* #808080 3D shadow */
#define C_BORDER_MID  0xCE79u   /* #CCCCCC 3D border */
#define C_PROG_BLUE   0x0115u   /* #0420AC title blue */
#define C_PAPER       0xFFFDu   /* #FFFEE8 receipt paper */
#define C_INK         0x2104u   /* #202020 ink */
#define C_GREEN       0x07E0u   /* #00FF00 retro green */
#define C_RED         0xF800u   /* #FF0000 pure red */
#define C_YELLOW      0xFFE0u   /* #FFFF00 yellow */
#define C_AMBER       0xFC00u   /* #FF8000 amber */
#define C_COFFEE      0x6182u   /* #603010 dark coffee brown */

/* ------------------------------------------- 5x7 Bitmap Terminal Font --- */
/* Printable ASCII 32 (' ') to 126 ('~') */
static const uint8_t CINCO_FONT5X7[][5] = {
    {0x00, 0x00, 0x00, 0x00, 0x00}, /*   */
    {0x00, 0x00, 0x5F, 0x00, 0x00}, /* ! */
    {0x00, 0x07, 0x00, 0x07, 0x00}, /* " */
    {0x14, 0x7F, 0x14, 0x7F, 0x14}, /* # */
    {0x24, 0x2A, 0x7F, 0x2A, 0x12}, /* $ */
    {0x23, 0x13, 0x08, 0x64, 0x62}, /* % */
    {0x36, 0x49, 0x55, 0x22, 0x50}, /* & */
    {0x00, 0x05, 0x03, 0x00, 0x00}, /* ' */
    {0x00, 0x1C, 0x22, 0x41, 0x00}, /* ( */
    {0x00, 0x41, 0x22, 0x1C, 0x00}, /* ) */
    {0x08, 0x2A, 0x1C, 0x2A, 0x08}, /* * */
    {0x08, 0x08, 0x3E, 0x08, 0x08}, /* + */
    {0x00, 0x50, 0x30, 0x00, 0x00}, /* , */
    {0x08, 0x08, 0x08, 0x08, 0x08}, /* - */
    {0x00, 0x60, 0x60, 0x00, 0x00}, /* . */
    {0x20, 0x10, 0x08, 0x04, 0x02}, /* / */
    {0x3E, 0x51, 0x49, 0x45, 0x3E}, /* 0 */
    {0x00, 0x42, 0x7F, 0x40, 0x00}, /* 1 */
    {0x42, 0x61, 0x51, 0x49, 0x46}, /* 2 */
    {0x21, 0x41, 0x45, 0x4B, 0x31}, /* 3 */
    {0x18, 0x14, 0x12, 0x7F, 0x10}, /* 4 */
    {0x27, 0x45, 0x45, 0x45, 0x39}, /* 5 */
    {0x3C, 0x4A, 0x49, 0x49, 0x30}, /* 6 */
    {0x01, 0x71, 0x09, 0x05, 0x03}, /* 7 */
    {0x36, 0x49, 0x49, 0x49, 0x36}, /* 8 */
    {0x06, 0x49, 0x49, 0x29, 0x1E}, /* 9 */
    {0x00, 0x36, 0x36, 0x00, 0x00}, /* : */
    {0x00, 0x56, 0x36, 0x00, 0x00}, /* ; */
    {0x08, 0x14, 0x22, 0x41, 0x00}, /* < */
    {0x14, 0x14, 0x14, 0x14, 0x14}, /* = */
    {0x00, 0x41, 0x22, 0x14, 0x08}, /* > */
    {0x02, 0x01, 0x51, 0x09, 0x06}, /* ? */
    {0x32, 0x49, 0x79, 0x41, 0x3E}, /* @ */
    {0x7E, 0x11, 0x11, 0x11, 0x7E}, /* A */
    {0x7F, 0x49, 0x49, 0x49, 0x36}, /* B */
    {0x3E, 0x41, 0x41, 0x41, 0x22}, /* C */
    {0x7F, 0x41, 0x41, 0x22, 0x1C}, /* D */
    {0x7F, 0x49, 0x49, 0x49, 0x41}, /* E */
    {0x7F, 0x09, 0x09, 0x09, 0x01}, /* F */
    {0x3E, 0x41, 0x49, 0x49, 0x7A}, /* G */
    {0x7F, 0x08, 0x08, 0x08, 0x7F}, /* H */
    {0x00, 0x41, 0x7F, 0x41, 0x00}, /* I */
    {0x20, 0x40, 0x41, 0x3F, 0x01}, /* J */
    {0x7F, 0x08, 0x14, 0x22, 0x41}, /* K */
    {0x7F, 0x40, 0x40, 0x40, 0x40}, /* L */
    {0x7F, 0x02, 0x0C, 0x02, 0x7F}, /* M */
    {0x7F, 0x04, 0x08, 0x10, 0x7F}, /* N */
    {0x3E, 0x41, 0x41, 0x41, 0x3E}, /* O */
    {0x7F, 0x09, 0x09, 0x09, 0x06}, /* P */
    {0x3E, 0x41, 0x51, 0x21, 0x5E}, /* Q */
    {0x7F, 0x09, 0x19, 0x29, 0x46}, /* R */
    {0x46, 0x49, 0x49, 0x49, 0x31}, /* S */
    {0x01, 0x01, 0x7F, 0x01, 0x01}, /* T */
    {0x3F, 0x40, 0x40, 0x40, 0x3F}, /* U */
    {0x1F, 0x20, 0x40, 0x20, 0x1F}, /* V */
    {0x7F, 0x20, 0x18, 0x20, 0x7F}, /* W */
    {0x63, 0x14, 0x08, 0x14, 0x63}, /* X */
    {0x03, 0x04, 0x78, 0x04, 0x03}, /* Y */
    {0x61, 0x51, 0x49, 0x45, 0x43}, /* Z */
    {0x00, 0x7F, 0x41, 0x41, 0x00}, /* [ */
    {0x02, 0x04, 0x08, 0x10, 0x20}, /* \ */
    {0x00, 0x41, 0x41, 0x7F, 0x00}, /* ] */
    {0x04, 0x02, 0x01, 0x02, 0x04}, /* ^ */
    {0x40, 0x40, 0x40, 0x40, 0x40}, /* _ */
    {0x00, 0x01, 0x02, 0x04, 0x00}, /* ` */
    {0x20, 0x54, 0x54, 0x54, 0x78}, /* a */
    {0x7F, 0x48, 0x44, 0x44, 0x38}, /* b */
    {0x38, 0x44, 0x44, 0x44, 0x20}, /* c */
    {0x38, 0x44, 0x44, 0x48, 0x7F}, /* d */
    {0x38, 0x54, 0x54, 0x54, 0x18}, /* e */
    {0x08, 0x7E, 0x09, 0x01, 0x02}, /* f */
    {0x0C, 0x52, 0x52, 0x52, 0x3E}, /* g */
    {0x7F, 0x08, 0x04, 0x04, 0x78}, /* h */
    {0x00, 0x44, 0x7D, 0x40, 0x00}, /* i */
    {0x20, 0x40, 0x44, 0x3D, 0x00}, /* j */
    {0x7F, 0x10, 0x28, 0x44, 0x00}, /* k */
    {0x00, 0x41, 0x7F, 0x40, 0x00}, /* l */
    {0x7C, 0x04, 0x18, 0x04, 0x78}, /* m */
    {0x7C, 0x08, 0x04, 0x04, 0x78}, /* n */
    {0x38, 0x44, 0x44, 0x44, 0x38}, /* o */
    {0x7C, 0x14, 0x14, 0x14, 0x08}, /* p */
    {0x08, 0x14, 0x14, 0x18, 0x7C}, /* q */
    {0x7C, 0x08, 0x04, 0x04, 0x08}, /* r */
    {0x48, 0x54, 0x54, 0x54, 0x20}, /* s */
    {0x04, 0x3F, 0x44, 0x40, 0x20}, /* t */
    {0x3C, 0x40, 0x40, 0x20, 0x7C}, /* u */
    {0x1C, 0x20, 0x40, 0x20, 0x1C}, /* v */
    {0x3C, 0x40, 0x30, 0x40, 0x3C}, /* w */
    {0x44, 0x28, 0x10, 0x28, 0x44}, /* x */
    {0x0C, 0x50, 0x50, 0x50, 0x3C}, /* y */
    {0x44, 0x64, 0x54, 0x4C, 0x44}, /* z */
    {0x00, 0x08, 0x36, 0x41, 0x00}, /* { */
    {0x00, 0x00, 0x7F, 0x00, 0x00}, /* | */
    {0x00, 0x41, 0x36, 0x08, 0x00}, /* } */
    {0x10, 0x08, 0x08, 0x10, 0x08}, /* ~ */
};

/* Plot a single character using the 5x7 bitmap font */
static void cinco_draw_char(int32_t x, int32_t y, char c, uint16_t color)
{
    if (c < 32 || c > 126)
        c = ' ';
    const uint8_t *glyph = CINCO_FONT5X7[(uint8_t)(c - 32)];
    int col, row;
    for (col = 0; col < 5; col++) {
        uint8_t line = glyph[col];
        for (row = 0; row < 7; row++) {
            if (line & (1u << row))
                lcd_fill(x + col, y + row, 1, 1, color);
        }
    }
}

/* Print string using 5x7 font */
static void cinco_draw_string(int32_t x, int32_t y, const char *s, uint16_t color)
{
    int32_t cur_x = x;
    while (s && *s) {
        cinco_draw_char(cur_x, y, *s, color);
        cur_x += 6;
        s++;
    }
}

/* ----------------------------------------------- RLE Sprite Blitting --- */
/* Unpacks and blits a 4-bit RLE frame directly into the off-screen RAM buffer cv_px,
 * then sends the entire sprite bounding box to the ST7789 display with ONE single lcd_blit DMA burst. */
static void cinco_blit_sprite(const cinco_anim_t *a, uint32_t frame_idx,
                             int32_t dst_x, int32_t dst_y, uint32_t mosaic_block)
{
    if (!a || frame_idx >= a->nframes)
        return;

    /* Apply kinetics horizontal displacement */
    int32_t shift_x = 0;
    if (perf.wobble) {
        if (perf.source == SRC_OYSTER) {
            shift_x = (perf.frame_idx & 1) ? 3 : -3;
        } else if (perf.source == SRC_CELERY || perf.source == SRC_TALK) {
            shift_x = (perf.frame_idx & 1) ? 2 : -2;
        }
    } else if (perf.flail) {
        if (perf.source == SRC_OYSTER || perf.source == SRC_CELERY || perf.source == SRC_TALK) {
            shift_x = ((int32_t)(perf.frame_idx % 3) - 1) * 4;
        }
    }
    dst_x += shift_x;

    int32_t w = a->w;
    int32_t h = a->h;

    /* Clamp dst coordinates to display boundaries */
    if (dst_x < 0) dst_x = 0;
    if (dst_y < 0) dst_y = 0;
    if (dst_x + w > 240) dst_x = 240 - w;
    if (dst_y + h > 240) dst_y = 240 - h;

    uint32_t total_px = (uint32_t)w * (uint32_t)h;
    if (total_px > CV_MAX)
        return;

    /* Wait for any previous DMA transfer using cv_px to finish */
    lcd_sync();

    /* Clear the sprite bounding box in cv_px to byte-swapped C_WHITE */
    uint16_t white_swapped = swap16(C_WHITE);
    for (uint32_t i = 0; i < total_px; i++) {
        cv_px[i] = white_swapped;
    }

    /* Pre-swap palette to ST7789 byte order */
    uint16_t pal_swapped[16];
    for (uint32_t i = 0; i < 16; i++) {
        pal_swapped[i] = swap16(a->pal[i]);
    }

    uint32_t rle_pos = a->frame_off[frame_idx];
    const uint8_t *rle = a->rle;

    /* Unpack RLE runs into cv_px in RAM (< 0.1 ms in CPU) */
    int32_t px = 0;
    int32_t py = 0;
    while (py < h) {
        uint8_t b = rle[rle_pos++];
        uint32_t run = (b >> 4) + 1u;
        uint32_t col_idx = b & 0x0Fu;
        uint16_t color = pal_swapped[col_idx];

        while (run--) {
            if (col_idx != 0) {
                cv_px[py * w + px] = color;
            }
            px++;
            if (px >= w) {
                px = 0;
                py++;
                if (py >= h)
                    break;
            }
        }
    }

    /* Small pixel bowler hat on Oyster's head when Hat Wobble is active */
    if (perf.wobble && perf.source == SRC_OYSTER) {
        int32_t rx = 71;
        int32_t ry = 6;
        uint16_t black_sw = swap16(C_BLACK);
        uint16_t red_sw = swap16(C_RED);

        for (int32_t c = 0; c < 12; c++) cv_px[(ry) * w + (rx + 5 + c)] = black_sw;
        for (int32_t r = 0; r < 2; r++)
            for (int32_t c = 0; c < 16; c++) cv_px[(ry + 1 + r) * w + (rx + 3 + c)] = black_sw;
        for (int32_t r = 0; r < 4; r++)
            for (int32_t c = 0; c < 18; c++) cv_px[(ry + 3 + r) * w + (rx + 2 + c)] = black_sw;
        for (int32_t c = 0; c < 18; c++) cv_px[(ry + 7) * w + (rx + 2 + c)] = red_sw;
        for (int32_t r = 0; r < 2; r++)
            for (int32_t c = 0; c < 22; c++) cv_px[(ry + 8 + r) * w + (rx + c)] = black_sw;
        cv_px[(ry + 7) * w + (rx - 1)] = black_sw;
        cv_px[(ry + 7) * w + (rx + 22)] = black_sw;
    }

    /* Mosaic decimation in cv_px (Nude Tayne / NSFW modes) */
    if (mosaic_block > 1) {
        uint32_t m = mosaic_block;
        for (int32_t by = 0; by < h; by += (int32_t)m) {
            int32_t bh = ((by + (int32_t)m) <= h) ? (int32_t)m : (h - by);
            for (int32_t bx = 0; bx < w; bx += (int32_t)m) {
                int32_t bw = ((bx + (int32_t)m) <= w) ? (int32_t)m : (w - bx);
                /* Sample block color from top-left or center */
                uint16_t block_color = cv_px[by * w + bx];
                if (block_color == white_swapped) {
                    int32_t cx = bx + bw / 2;
                    int32_t cy = by + bh / 2;
                    if (cv_px[cy * w + cx] != white_swapped) {
                        block_color = cv_px[cy * w + cx];
                    }
                }
                for (int32_t r = 0; r < bh; r++) {
                    uint16_t *row = &cv_px[(by + r) * w + bx];
                    for (int32_t c = 0; c < bw; c++) {
                        row[c] = block_color;
                    }
                }
            }
        }
    }

    /* Clear margins if displaced to prevent kinetics trails on white canvas */
    if (shift_x != 0) {
        if (dst_x >= 6) {
            lcd_fill((uint32_t)(dst_x - 6), (uint32_t)dst_y, 6, (uint32_t)h, C_WHITE);
        }
        if (dst_x + w + 6 <= 240) {
            lcd_fill((uint32_t)(dst_x + w), (uint32_t)dst_y, 6, (uint32_t)h, C_WHITE);
        }
    }

    /* Send the entire sprite frame to the ST7789 display with ONE single DMA burst */
    lcd_blit((uint32_t)dst_x, (uint32_t)dst_y, (uint32_t)w, (uint32_t)h, cv_px);
}

#endif /* CINCO_GFX_C */
