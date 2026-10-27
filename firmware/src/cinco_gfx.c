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
/* Unpacks and blits a 4-bit RLE frame directly into the display canvas */
static void cinco_blit_sprite(const cinco_anim_t *a, uint32_t frame_idx,
                             int32_t dst_x, int32_t dst_y, uint32_t mosaic_block)
{
    if (!a || frame_idx >= a->nframes)
        return;

    /* Apply kinetics horizontal displacement */
    if (perf.wobble) {
        if (perf.source == SRC_OYSTER) {
            dst_x += (perf.frame_idx & 1) ? 3 : -3;
        } else if (perf.source == SRC_CELERY || perf.source == SRC_TALK) {
            dst_x += (perf.frame_idx & 1) ? 2 : -2;
        }
    } else if (perf.flail) {
        if (perf.source == SRC_OYSTER || perf.source == SRC_CELERY || perf.source == SRC_TALK) {
            dst_x += ((int32_t)(perf.frame_idx % 3) - 1) * 4;
        }
    }
        
    uint32_t rle_pos = a->frame_off[frame_idx];
    const uint8_t *rle = a->rle;
    const uint16_t *pal = a->pal;
    
    int32_t w = a->w;
    int32_t h = a->h;
    int32_t px = 0;
    int32_t py = 0;
    
    if (mosaic_block <= 1) {
        /* Standard 1:1 pixel rendering */
        while (py < h) {
            uint8_t b = rle[rle_pos++];
            uint32_t run = (b >> 4) + 1u;
            uint32_t col_idx = b & 0x0Fu;
            uint16_t color = pal[col_idx];
            
            /* Color 0 is canvas white */
            while (run--) {
                if (col_idx != 0 && (dst_x + px >= 0 && dst_x + px < 240) &&
                    (dst_y + py >= 0 && dst_y + py < 240)) {
                    lcd_fill(dst_x + px, dst_y + py, 1, 1, color);
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
    } else {
        /* Mosaic / Pixel Censorship Decimation (Nude Tayne mode) */
        uint32_t m = mosaic_block;
        while (py < h) {
            uint8_t b = rle[rle_pos++];
            uint32_t run = (b >> 4) + 1u;
            uint32_t col_idx = b & 0x0Fu;
            uint16_t color = pal[col_idx];
            
            while (run--) {
                /* Quantize to mosaic block grid */
                if (col_idx != 0 && (px % m == 0) && (py % m == 0)) {
                    int32_t bx = dst_x + px;
                    int32_t by = dst_y + py;
                    lcd_fill(bx, by, m, m, color);
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
    }

    /* Small pixel bowler hat on Oyster's head when Hat Wobble is active */
    if (perf.wobble && perf.source == SRC_OYSTER) {
        int32_t hx = dst_x + 71;
        int32_t hy = dst_y + 6;
        if (mosaic_block <= 1) {
            lcd_fill(hx + 5, hy, 12, 1, C_BLACK);
            lcd_fill(hx + 3, hy + 1, 16, 2, C_BLACK);
            lcd_fill(hx + 2, hy + 3, 18, 4, C_BLACK);
            lcd_fill(hx + 2, hy + 7, 18, 1, C_RED);
            lcd_fill(hx, hy + 8, 22, 2, C_BLACK);
            lcd_fill(hx - 1, hy + 7, 1, 1, C_BLACK);
            lcd_fill(hx + 22, hy + 7, 1, 1, C_BLACK);
        } else {
            uint32_t m = mosaic_block;
            int32_t qhx = (hx / (int32_t)m) * (int32_t)m;
            int32_t qhy = (hy / (int32_t)m) * (int32_t)m;
            lcd_fill(qhx, qhy, m * 2, m, C_BLACK);
        }
    }
}

#endif /* CINCO_GFX_C */
