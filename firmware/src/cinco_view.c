/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO Performance View: Maps instrument performance state to 240x240 screen */

#ifndef CINCO_VIEW_C
#define CINCO_VIEW_C

#include <stdint.h>
#include "cinco_state.h"
#include "cinco_gfx.c"

static uint8_t view_initialized = 0;

/* Draw 3D beveled window chrome */
static void cinco_draw_window_chrome(int32_t x, int32_t y, int32_t w, int32_t h, const char *title)
{
    /* Outer face */
    lcd_fill(x, y, w, h, C_WIN_FACE);
    /* 3D bevel: light top/left, dark bottom/right */
    lcd_fill(x, y, w, 1, C_WHITE);
    lcd_fill(x, y, 1, h, C_WHITE);
    lcd_fill(x, y + h - 1, w, 1, C_BORDER_DARK);
    lcd_fill(x + w - 1, y, 1, h, C_BORDER_DARK);

    /* Title bar */
    lcd_fill(x + 3, y + 3, w - 6, 16, C_WHITE);
    lcd_fill(x + 3, y + 3, w - 6, 1, C_BLACK);
    lcd_fill(x + 3, y + 18, w - 6, 1, C_BLACK);
    lcd_fill(x + 3, y + 3, 1, 16, C_BLACK);
    lcd_fill(x + w - 4, y + 3, 1, 16, C_BLACK);

    /* Minimize box [-] on left */
    lcd_fill(x + 4, y + 4, 14, 14, C_WIN_FACE);
    lcd_fill(x + 4, y + 4, 14, 1, C_BLACK);
    lcd_fill(x + 4, y + 17, 14, 1, C_BLACK);
    lcd_fill(x + 4, y + 4, 1, 14, C_BLACK);
    lcd_fill(x + 17, y + 4, 1, 14, C_BLACK);
    lcd_fill(x + 7, y + 10, 8, 2, C_BLACK);

    /* Scroll buttons [v][^] on right */
    int32_t rx = x + w - 4 - 30;
    lcd_fill(rx, y + 4, 13, 14, C_WIN_FACE);
    lcd_fill(rx, y + 4, 13, 1, C_BLACK);
    lcd_fill(rx, y + 17, 13, 1, C_BLACK);
    lcd_fill(rx, y + 4, 1, 14, C_BLACK);
    lcd_fill(rx + 12, y + 4, 1, 14, C_BLACK);
    /* v arrow */
    lcd_fill(rx + 4, y + 7, 5, 1, C_BLACK);
    lcd_fill(rx + 5, y + 8, 3, 1, C_BLACK);
    lcd_fill(rx + 6, y + 9, 1, 1, C_BLACK);

    int32_t rx2 = rx + 14;
    lcd_fill(rx2, y + 4, 13, 14, C_WIN_FACE);
    lcd_fill(rx2, y + 4, 13, 1, C_BLACK);
    lcd_fill(rx2, y + 17, 13, 1, C_BLACK);
    lcd_fill(rx2, y + 4, 1, 14, C_BLACK);
    lcd_fill(rx2 + 12, y + 4, 1, 14, C_BLACK);
    /* ^ arrow */
    lcd_fill(rx2 + 6, y + 7, 1, 1, C_BLACK);
    lcd_fill(rx2 + 5, y + 8, 3, 1, C_BLACK);
    lcd_fill(rx2 + 4, y + 9, 5, 1, C_BLACK);

    /* Title string */
    cinco_draw_string(x + 22, y + 8, title, C_BLACK);

    /* White inner canvas */
    lcd_fill(x + 4, y + 21, w - 8, h - 25, C_WHITE);
    lcd_fill(x + 4, y + 21, w - 8, 1, C_BORDER_DARK);
    lcd_fill(x + 4, y + 21, 1, h - 25, C_BORDER_DARK);
    lcd_fill(x + 4, y + h - 5, w - 8, 1, C_WHITE);
    lcd_fill(x + w - 5, y + 21, 1, h - 25, C_WHITE);
}

/* Cinco Office Suite: Lotus 1-2-3 Boss Key spreadsheet */
static void cinco_draw_boss_key(void)
{
    /* Full screen (240x240) retro spreadsheet */
    lcd_fill(0, 0, 240, 240, C_BLACK);

    /* Top bar in dark blue/grey: [Lotus 1-2-3 Release 3.1 - CELERY_CORP_Q3.WK1] */
    lcd_fill(0, 0, 240, 13, C_PROG_BLUE);
    cinco_draw_string(2, 3, "[Lotus 1-2-3 Release 3.1 - CELERY_CORP_Q3.WK1]", C_WHITE);

    /* Column headers band */
    lcd_fill(0, 14, 240, 12, C_BORDER_DARK);
    cinco_draw_string(4, 16, "#", C_WHITE);
    cinco_draw_string(42, 16, "A", C_WHITE);
    cinco_draw_string(140, 16, "B", C_WHITE);
    cinco_draw_string(210, 16, "C", C_WHITE);

    /* Grid vertical dividers */
    lcd_fill(16, 14, 1, 204, C_BORDER_DARK);
    lcd_fill(126, 14, 1, 204, C_BORDER_DARK);
    lcd_fill(196, 14, 1, 204, C_BORDER_DARK);

    /* Row horizontal divider lines & row numbers 1..11 */
    static const char *const row_num[11] = {
        " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", "11"
    };

    for (int r = 0; r < 11; r++) {
        int32_t ry = 26 + r * 17;
        lcd_fill(0, ry + 16, 240, 1, C_BORDER_DARK);
        cinco_draw_string(2, ry + 4, row_num[r], C_BORDER_MID);
    }

    /* Cell data:
     * A1: CELERY REVENUE -> B1: $4,320.00
     * A2: OYSTER LICENSING -> B2: $812.50
     * A3: TAYNE R&D -> B3: ($1,400.00)
     * A4: 4d3d3d3 CONSULT -> B4: $9,999.99
     * A5: WIFE PHONE MIN -> B5: 0.00
     * A6: NET EARNINGS -> B6: $13,732.49
     * A8: FLARH RATIO -> B8: 98.4%
     * A9: COFFEE STATUS -> B9: REFILL
     */
    cinco_draw_string(20, 30, "CELERY REVENUE", C_GREEN);
    cinco_draw_string(130, 30, "$4,320.00", C_GREEN);

    cinco_draw_string(20, 47, "OYSTER LICENSING", C_GREEN);
    cinco_draw_string(130, 47, "$812.50", C_GREEN);

    cinco_draw_string(20, 64, "TAYNE R&D", C_GREEN);
    cinco_draw_string(130, 64, "($1,400.00)", C_RED);

    cinco_draw_string(20, 81, "4d3d3d3 CONSULT", C_GREEN);
    cinco_draw_string(130, 81, "$9,999.99", C_GREEN);

    cinco_draw_string(20, 98, "WIFE PHONE MIN", C_GREEN);
    cinco_draw_string(130, 98, "0.00", C_GREEN);

    /* Highlight Net Earnings */
    lcd_fill(17, 112, 179, 16, C_PROG_BLUE);
    cinco_draw_string(20, 115, "NET EARNINGS", C_WHITE);
    cinco_draw_string(130, 115, "$13,732.49", C_WHITE);

    cinco_draw_string(20, 149, "FLARH RATIO", C_GREEN);
    cinco_draw_string(130, 149, "98.4%", C_GREEN);

    cinco_draw_string(20, 166, "COFFEE STATUS", C_GREEN);
    cinco_draw_string(130, 166, "REFILL", C_YELLOW);

    /* Bottom prompt: READY     [PRESS ANY KEY TO WORK] */
    lcd_fill(0, 222, 240, 18, C_WIN_FACE);
    lcd_fill(0, 222, 240, 1, C_WHITE);
    cinco_draw_string(6, 227, "READY     [PRESS ANY KEY TO WORK]", C_BLACK);
    if ((fm1_ms / 500u) & 1u) {
        lcd_fill(228, 227, 4, 7, C_BLACK);
    }
}

/* Disk Defragmenter 16x6 cluster grid visualizer rendered into cv_px */
static void cinco_draw_defrag_grid(int32_t ox, int32_t oy, int32_t ww, int32_t wh, uint8_t step)
{
    (void)wh;
    int32_t cw_x = ox + 4;
    int32_t cw_y = oy + 21;
    int32_t cw_w = ww - 8;

    uint8_t kick_hit = ((step & 3u) == 0u);
    uint8_t clap_hit = (step == 4u || step == 12u);

    /* Wait for any pending DMA transfer using cv_px */
    lcd_sync();

    uint16_t bg_sw = swap16(C_WIN_FACE);
    uint16_t white_sw = swap16(C_WHITE);
    uint16_t dark_sw = swap16(C_BORDER_DARK);

    /* Clear the 208x84 buffer to background */
    for (uint32_t i = 0; i < 208u * 84u; i++) {
        cv_px[i] = bg_sw;
    }

    for (int r = 0; r < 6; r++) {
        for (int c = 0; c < 16; c++) {
            uint16_t color;
            /* Amber/Red blocks pulse on active drum & bass hits */
            if (r == 4 && c == step) {
                color = C_AMBER; /* Bass pump */
            } else if (r == 5 && c == step) {
                color = (kick_hit || clap_hit) ? C_RED : C_AMBER; /* Drum hit */
            } else if (r == 3 && c == step && (kick_hit || clap_hit)) {
                color = C_RED;
            } else if (r == 0 || (r == 1 && c < 12) || (r == 2 && c < 6)) {
                color = C_PROG_BLUE; /* System / Celery files */
            } else if ((r == 1 && c >= 12) || (r == 2 && c >= 6 && c < 14) || (r == 3 && c < 10)) {
                color = C_GREEN; /* Synth engine buffers */
            } else {
                color = C_WHITE; /* Free clusters */
            }

            uint16_t col_sw = swap16(color);
            int32_t bx = c * 13;
            int32_t by = r * 14;

            for (int32_t dy = 0; dy < 11; dy++) {
                uint16_t *dst = &cv_px[(by + dy) * 208 + bx];
                for (int32_t dx = 0; dx < 11; dx++) {
                    if (dy == 0 || dx == 0) {
                        dst[dx] = white_sw;
                    } else if (dy == 10 || dx == 10) {
                        dst[dx] = dark_sw;
                    } else {
                        dst[dx] = col_sw;
                    }
                }
            }
        }
    }

    int32_t gx = cw_x + (cw_w - 208) / 2;
    int32_t gy = cw_y + 8;
    lcd_blit((uint32_t)gx, (uint32_t)gy, 208, 84, cv_px);
}

static void cinco_draw_defrag_progress(int32_t ox, int32_t oy, int32_t ww, int32_t wh, uint32_t bpm, uint32_t progress)
{
    (void)wh;
    int32_t cw_x = ox + 4;
    int32_t cw_y = oy + 21;
    int32_t cw_w = ww - 8;
    int32_t bar_w = cw_w - 24;

    /* Status text at cw_y + 98 */
    lcd_fill((uint32_t)(cw_x + 12), (uint32_t)(cw_y + 98), (uint32_t)bar_w, 10, C_WIN_FACE);
    char defrag_buf[40];
    snprintf(defrag_buf, sizeof(defrag_buf), "Defrag: %u BPM [%lu%% Optimized]", (unsigned)bpm, (unsigned long)progress);
    cinco_draw_string(cw_x + 12, cw_y + 98, defrag_buf, C_BLACK);

    /* Visual defrag progress bar at cw_y + 112 */
    lcd_fill((uint32_t)(cw_x + 12), (uint32_t)(cw_y + 112), (uint32_t)bar_w, 10, C_WHITE);
    lcd_fill((uint32_t)(cw_x + 12), (uint32_t)(cw_y + 112), (uint32_t)bar_w, 1, C_BORDER_DARK);
    lcd_fill((uint32_t)(cw_x + 12), (uint32_t)(cw_y + 112), 1, 10, C_BORDER_DARK);
    lcd_fill((uint32_t)(cw_x + 12), (uint32_t)(cw_y + 121), (uint32_t)bar_w, 1, C_WHITE);
    lcd_fill((uint32_t)(cw_x + 12 + bar_w - 1), (uint32_t)(cw_y + 112), 1, 10, C_WHITE);

    int32_t fill_w = (bar_w - 4) * (int32_t)progress / 100;
    if (fill_w > 0) {
        lcd_fill((uint32_t)(cw_x + 14), (uint32_t)(cw_y + 114), (uint32_t)fill_w, 6, C_PROG_BLUE);
    }
}

static uint32_t defrag_start_ms = 0;
static uint8_t defrag_prev_mode = 0;

static uint32_t cinco_get_defrag_progress(uint32_t bpm)
{
    if (defrag_start_ms == 0 || !defrag_prev_mode) {
        defrag_start_ms = fm1_ms;
        defrag_prev_mode = 1;
    }
    uint32_t elapsed = fm1_ms - defrag_start_ms;
    /* Duration: ~8000ms at 120 BPM */
    uint32_t duration_ms = 960000u / (bpm ? bpm : 120u);
    if (duration_ms < 4000u) duration_ms = 4000u;
    uint32_t progress = (elapsed * 100u) / duration_ms;
    if (progress > 100u) progress = 100u;
    return progress;
}

static void cinco_check_defrag_complete(uint32_t progress)
{
    if (progress >= 100u) {
        perf.view_mode = 0;
        defrag_prev_mode = 0;
        defrag_start_ms = 0;
        view_initialized = 0;
        ui.force = 1;
        cinco_term_push("> DEFRAG: 240 clusters optimized. 0 errors.");
        cinco_speech_play(CINCO_PHRASE_YES);
    }
}

static void cinco_draw_defrag_content(int32_t ox, int32_t oy, int32_t ww, int32_t wh)
{
    uint32_t bpm = perf.tempo ? perf.tempo : 120u;
    uint32_t ms_per_step = 15000u / bpm;
    if (ms_per_step == 0) ms_per_step = 1;
    uint8_t step = perf.groove ? cinco_groove_get_step() : (uint8_t)((fm1_ms / ms_per_step) & 15u);
    uint32_t progress = cinco_get_defrag_progress(bpm);

    cinco_draw_defrag_grid(ox, oy, ww, wh, step);
    cinco_draw_defrag_progress(ox, oy, ww, wh, bpm, progress);
    cinco_check_defrag_complete(progress);
}

static void cinco_draw_defrag(void)
{
    int32_t ox = 4;
    int32_t oy = 4;
    int32_t ww = 232;
    int32_t wh = 160;
    char title_buf[40];
    snprintf(title_buf, sizeof(title_buf), "Disk Defragmenter - %u BPM", (unsigned)(perf.tempo ? perf.tempo : 120u));
    cinco_draw_window_chrome(ox, oy, ww, wh, title_buf);
    int32_t cw_x = ox + 4;
    int32_t cw_y = oy + 21;
    int32_t cw_w = ww - 8;
    int32_t cw_h = wh - 25;
    lcd_fill((uint32_t)cw_x, (uint32_t)cw_y, (uint32_t)cw_w, (uint32_t)cw_h, C_WIN_FACE);
    cinco_draw_defrag_content(ox, oy, ww, wh);
}

/* Cinco After Dark: Flying Celery screensaver */
static void cinco_init_screensaver_sprites(void)
{
    uint16_t *ss_stalk_up = cv_px;
    uint16_t *ss_stalk_down = cv_px + 480;
    uint16_t *ss_title = cv_px + 960;

    uint16_t black_sw = swap16(C_BLACK);
    uint16_t green_sw = swap16(C_GREEN);
    uint16_t dgreen_sw = swap16(0xE003u);
    uint16_t white_sw = swap16(C_WHITE);
    uint16_t paper_sw = swap16(C_PAPER);
    uint16_t border_sw = swap16(C_BORDER_MID);
    uint16_t title_color_sw = swap16(C_BORDER_DARK);

    for (int i = 0; i < 480; i++) {
        ss_stalk_up[i] = black_sw;
        ss_stalk_down[i] = black_sw;
    }

    for (int flap = 0; flap < 2; flap++) {
        uint16_t *buf = flap ? ss_stalk_down : ss_stalk_up;
        for (int r = 0; r < 4; r++)
            for (int c = 0; c < 5; c++)
                buf[(7 + r) * 24 + (0 + c)] = dgreen_sw;
        for (int r = 0; r < 2; r++)
            for (int c = 0; c < 4; c++)
                buf[(6 + r) * 24 + (2 + c)] = green_sw;
        for (int r = 0; r < 4; r++)
            for (int c = 0; c < 10; c++)
                buf[(9 + r) * 24 + (4 + c)] = green_sw;
        for (int c = 0; c < 7; c++)
            buf[8 * 24 + (6 + c)] = white_sw;
        for (int c = 0; c < 8; c++)
            buf[11 * 24 + (5 + c)] = dgreen_sw;
        for (int r = 0; r < 4; r++)
            for (int c = 0; c < 3; c++)
                buf[(9 + r) * 24 + (14 + c)] = paper_sw;

        if (flap == 0) {
            /* Wings UP */
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(6 + r) * 24 + (6 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(4 + r) * 24 + (5 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(2 + r) * 24 + (4 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 2; c++) buf[(0 + r) * 24 + (3 + c)] = border_sw;

            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(6 + r) * 24 + (10 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(4 + r) * 24 + (11 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(2 + r) * 24 + (12 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 2; c++) buf[(0 + r) * 24 + (13 + c)] = border_sw;
        } else {
            /* Wings DOWN */
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(11 + r) * 24 + (6 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(13 + r) * 24 + (5 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(15 + r) * 24 + (4 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 2; c++) buf[(17 + r) * 24 + (3 + c)] = border_sw;

            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(11 + r) * 24 + (10 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(13 + r) * 24 + (11 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 3; c++) buf[(15 + r) * 24 + (12 + c)] = white_sw;
            for (int r = 0; r < 2; r++) for (int c = 0; c < 2; c++) buf[(17 + r) * 24 + (13 + c)] = border_sw;
        }
    }

    for (int i = 0; i < 156 * 8; i++) {
        ss_title[i] = black_sw;
    }
    const char *str = "Cinco After Dark (c) 1991";
    int cur_x = 0;
    while (*str) {
        char ch = *str++;
        if (ch >= 32 && ch <= 126) {
            const uint8_t *glyph = CINCO_FONT5X7[(uint8_t)(ch - 32)];
            for (int col = 0; col < 5; col++) {
                uint8_t line = glyph[col];
                for (int row = 0; row < 7; row++) {
                    if (line & (1u << row)) {
                        ss_title[row * 156 + (cur_x + col)] = title_color_sw;
                    }
                }
            }
        }
        cur_x += 6;
    }
}

static void cinco_draw_celery_stalk(int32_t x, int32_t y, uint8_t flap)
{
    int32_t bx = x;
    int32_t by = y - 6;
    if (bx >= 0 && bx + 24 <= 240 && by >= 0 && by + 20 <= 240) {
        const uint16_t *buf = flap ? (cv_px + 480) : cv_px;
        lcd_blit((uint32_t)bx, (uint32_t)by, 24, 20, buf);
    }
}

static void cinco_erase_stalk_bbox(int32_t px, int32_t py)
{
    int32_t bx = px;
    int32_t by = py - 6;
    int32_t bw = 24;
    int32_t bh = 20;

    if (bx < 0) { bw += bx; bx = 0; }
    if (by < 0) { bh += by; by = 0; }
    if (bw > 0 && bh > 0 && bx < 240 && by < 240) {
        lcd_fill((uint32_t)bx, (uint32_t)by, (uint32_t)bw, (uint32_t)bh, C_BLACK);
        /* If bounding box overlapped center text, restore text */
        if (bx < 198 && bx + bw > 42 && by < 124 && by + bh > 116) {
            lcd_blit(42, 116, 156, 8, cv_px + 960);
        }
    }
}

static void cinco_draw_screensaver(void)
{
    static uint32_t last_ss_ms = 0;
    uint32_t now = fm1_ms;
    if (now - last_ss_ms < 50u) {
        return;
    }
    last_ss_ms = now;

    uint8_t flap_tick = (uint8_t)(now / 150u);

    for (int i = 0; i < 4; i++) {
        /* Erase previous stalk bounding box */
        cinco_erase_stalk_bbox(perf.prev_celery_x[i], perf.prev_celery_y[i]);

        perf.celery_x[i] += perf.celery_vx[i];
        perf.celery_y[i] += perf.celery_vy[i];

        /* Wrap around screen edges */
        if (perf.celery_x[i] < -24) perf.celery_x[i] = 240;
        if (perf.celery_x[i] > 240) perf.celery_x[i] = -24;
        if (perf.celery_y[i] < -24) perf.celery_y[i] = 240;
        if (perf.celery_y[i] > 240) perf.celery_y[i] = -24;

        int32_t x = perf.celery_x[i];
        int32_t y = perf.celery_y[i];
        uint8_t flap = (flap_tick + (uint8_t)i) & 1u;

        cinco_draw_celery_stalk(x, y, flap);

        perf.prev_celery_x[i] = perf.celery_x[i];
        perf.prev_celery_y[i] = perf.celery_y[i];
    }
}

/* Centered beveled error dialog popup (20, 48, 200, 80) */
static void cinco_draw_error_popup(void)
{
    int32_t dx = 20, dy = 48, dw = 200, dh = 80;
    lcd_fill(dx, dy, dw, dh, C_WIN_FACE);
    lcd_fill(dx, dy, dw, 1, C_WHITE);
    lcd_fill(dx, dy, 1, dh, C_WHITE);
    lcd_fill(dx, dy + dh - 1, dw, 1, C_BORDER_DARK);
    lcd_fill(dx + dw - 1, dy, 1, dh, C_BORDER_DARK);

    /* Title bar: "CINCO SYSTEM ALERT" */
    lcd_fill(dx + 3, dy + 3, dw - 6, 14, C_RED);
    cinco_draw_string(dx + 6, dy + 6, "CINCO SYSTEM ALERT", C_WHITE);

    /* Yellow warning icon: [ ! ] */
    lcd_fill(dx + 8, dy + 22, 16, 16, C_YELLOW);
    lcd_fill(dx + 8, dy + 22, 16, 1, C_BLACK);
    lcd_fill(dx + 8, dy + 37, 16, 1, C_BLACK);
    lcd_fill(dx + 8, dy + 22, 1, 16, C_BLACK);
    lcd_fill(dx + 23, dy + 22, 1, 16, C_BLACK);
    lcd_fill(dx + 15, dy + 25, 2, 7, C_BLACK);
    lcd_fill(dx + 15, dy + 34, 2, 2, C_BLACK);

    /* Text from perf.error_msg word-wrapped */
    const char *msg = perf.error_msg;
    char l1[32];
    char l2[32];
    l1[0] = '\0';
    l2[0] = '\0';
    uint32_t len = 0;
    while (msg[len]) len++;
    if (len <= 26) {
        uint32_t k;
        for (k = 0; k < len && k < 31; k++) l1[k] = msg[k];
        l1[k] = '\0';
    } else {
        int split = 26;
        while (split > 12 && msg[split] != ' ') split--;
        int k;
        for (k = 0; k < split && k < 31; k++) l1[k] = msg[k];
        l1[k] = '\0';
        while (msg[split] == ' ') split++;
        int m = 0;
        while (msg[split] && m < 27) l2[m++] = msg[split++];
        l2[m] = '\0';
    }
    cinco_draw_string(dx + 28, dy + 24, l1, C_BLACK);
    if (l2[0]) {
        cinco_draw_string(dx + 28, dy + 36, l2, C_BLACK);
    }

    /* [ OK ] button at bottom */
    int32_t bx = dx + (dw - 48) / 2;
    int32_t by = dy + dh - 22;
    lcd_fill(bx, by, 48, 16, C_WIN_FACE);
    lcd_fill(bx, by, 48, 1, C_WHITE);
    lcd_fill(bx, by, 1, 16, C_WHITE);
    lcd_fill(bx, by + 15, 48, 1, C_BORDER_DARK);
    lcd_fill(bx + 47, by, 1, 16, C_BORDER_DARK);
    cinco_draw_string(bx + 10, by + 4, "[ OK ]", C_BLACK);
}

/* Coffee mug indicator on desktop taskbar next to terminal at (216, 222, 18, 14) */
static void cinco_draw_coffee_mug(int32_t x, int32_t y, uint8_t level)
{
    /* Steam curling above mug if level > 0 */
    if (level > 0) {
        uint32_t phase = (fm1_ms / 150u) & 7u;
        int32_t s1_x = x + 5 + ((phase & 1u) ? 1 : -1);
        int32_t s1_y = y + 2 - ((int32_t)phase >> 1);
        int32_t s2_x = x + 9 + (((phase + 2u) & 1u) ? 1 : -1);
        int32_t s2_y = y + 2 - (((int32_t)phase + 1) >> 1);
        if (s1_y >= 0 && s1_y < 240) lcd_fill(s1_x, s1_y, 1, 1, C_WHITE);
        if (s2_y >= 0 && s2_y < 240) lcd_fill(s2_x, s2_y, 1, 1, C_WHITE);
    }

    /* Mug body outer (10x9) */
    int32_t mx = x + 2;
    int32_t my = y + 4;
    int32_t mw = 10;
    int32_t mh = 9;

    lcd_fill(mx, my, mw, mh, C_WHITE);
    lcd_fill(mx, my, mw, 1, C_BORDER_MID);
    lcd_fill(mx, my + mh - 1, mw, 1, C_BORDER_DARK);
    lcd_fill(mx, my, 1, mh, C_BORDER_MID);
    lcd_fill(mx + mw - 1, my, 1, mh, C_BORDER_DARK);

    /* Ceramic handle on right side */
    int32_t hx = mx + mw;
    lcd_fill(hx, my + 2, 3, 1, C_WHITE);
    lcd_fill(hx + 2, my + 2, 1, 4, C_WHITE);
    lcd_fill(hx, my + 5, 3, 1, C_WHITE);
    lcd_fill(hx + 2, my + 2, 1, 4, C_BORDER_DARK);

    /* Mug interior with coffee */
    int32_t ix = mx + 1;
    int32_t iy = my + 1;
    int32_t iw = mw - 2;
    int32_t ih = mh - 2;

    lcd_fill(ix, iy, iw, ih, C_PAPER);

    /* Dark brown coffee liquid proportional to level */
    int32_t lh = ((int32_t)level * ih) / 100;
    if (lh > ih) lh = ih;
    if (lh > 0) {
        lcd_fill(ix, iy + ih - lh, iw, lh, C_COFFEE);
    }

    /* When level == 0, draw small red "!" next to it */
    if (level == 0) {
        lcd_fill(x - 4, y + 4, 2, 5, C_RED);
        lcd_fill(x - 4, y + 10, 2, 2, C_RED);
    }
}

/* ----------------------------------------------- Dirty State Tracking --- */
static uint8_t last_rendered_frame = 255;
static uint8_t last_rendered_cursor = 255;
static uint32_t last_rendered_state = 0xFFFFFFFFu;
static char last_rendered_term[3][32];
static uint32_t last_rendered_taskbar = 0xFFFFFFFFu;
static uint8_t last_rendered_coffee = 0xFF;
static uint8_t last_rendered_defrag_step = 255;
static uint32_t last_rendered_defrag_prog = 0xFFFFFFFFu;
static uint32_t last_rendered_defrag_ms = 0;
static uint8_t overlay_active = 0;

static inline uint32_t cinco_get_layout_state(int32_t nwindows)
{
    uint32_t s = 0;
    s |= (uint32_t)(perf.screensaver & 1u);
    s |= (uint32_t)(perf.boss_mode & 1u) << 1;
    s |= (uint32_t)(perf.view_mode & 1u) << 2;
    s |= (uint32_t)((nwindows - 1) & 0x0Fu) << 3;
    s |= (uint32_t)(perf.source & 0x03u) << 7;
    s |= (uint32_t)(perf.nude & 1u) << 9;
    s |= (uint32_t)(perf.wobble & 1u) << 10;
    s |= (uint32_t)(perf.flail & 1u) << 11;
    s |= (uint32_t)(perf.nsfw_popup_t > 0 ? 1u : 0u) << 12;
    s |= (uint32_t)(perf.receipt_t > 0 ? 1u : 0u) << 13;
    s |= (uint32_t)(perf.diag > 0 ? 1u : 0u) << 14;
    s |= (uint32_t)(perf.error_popup_t > 0 ? 1u : 0u) << 15;
    s |= (uint32_t)(perf.mosaic & 0x7Fu) << 16;
    return s;
}

static inline uint32_t cinco_get_taskbar_state(void)
{
    uint32_t s = 0;
    s |= (uint32_t)(song.octave & 0x0Fu);
    s |= (uint32_t)(perf.env_mode & 0x03u) << 4;
    s |= (uint32_t)(perf.scale_mode & 0x07u) << 6;
    s |= (uint32_t)(perf.tempo & 0x01FFu) << 9;
    s |= (uint32_t)(perf.groove & 1u) << 18;
    s |= (uint32_t)(perf.rec & 1u) << 19;
    s |= (uint32_t)(perf.nude & 1u) << 20;
    s |= (uint32_t)(perf.wobble & 1u) << 21;
    s |= (uint32_t)(perf.flail & 1u) << 22;
    return s;
}

static void cinco_draw_terminal_chrome(int32_t tx, int32_t ty, int32_t tw, int32_t th)
{
    lcd_fill((uint32_t)tx, (uint32_t)ty, (uint32_t)tw, (uint32_t)th, C_BLACK);
    /* 3D Sunken border */
    lcd_fill((uint32_t)tx, (uint32_t)ty, (uint32_t)tw, 1, C_BORDER_DARK);
    lcd_fill((uint32_t)tx, (uint32_t)ty, 1, (uint32_t)th, C_BORDER_DARK);
    lcd_fill((uint32_t)tx, (uint32_t)(ty + th - 1), (uint32_t)tw, 1, C_WHITE);
    lcd_fill((uint32_t)(tx + tw - 1), (uint32_t)ty, 1, (uint32_t)th, C_WHITE);

    /* Terminal title bar */
    lcd_fill((uint32_t)(tx + 2), (uint32_t)(ty + 2), (uint32_t)(tw - 4), 12, C_BORDER_DARK);
    cinco_draw_string(tx + 6, ty + 4, "CINCO OS 2.5", C_WHITE);
}

static void cinco_draw_terminal_text(int32_t tx, int32_t ty, int32_t tw, uint8_t cursor_on)
{
    /* Clear text lines area */
    lcd_fill((uint32_t)(tx + 2), (uint32_t)(ty + 16), (uint32_t)(tw - 4), 38, C_BLACK);
    cinco_draw_string(tx + 6, ty + 17, perf.term_line[0], C_WHITE);
    cinco_draw_string(tx + 6, ty + 29, perf.term_line[1], C_WHITE);
    cinco_draw_string(tx + 6, ty + 41, perf.term_line[2], C_WHITE);

    if (cursor_on) {
        uint32_t len = 0;
        while (perf.term_line[2][len]) len++;
        cinco_draw_char(tx + 6 + (int32_t)len * 6, ty + 41, '_', C_WHITE);
    }
}

static void cinco_draw_taskbar(void)
{
    /* 4. Desktop Status Indicators Taskbar */
    lcd_fill(0, 227, 240, 13, C_WIN_FACE);
    lcd_fill(0, 227, 240, 1, C_WHITE);
    lcd_fill(0, 239, 240, 1, C_BORDER_DARK);

    int32_t bx = 2;

    /* Active Octave indicator: [OCT: +0] (or -1, +1, etc.) */
    char oct_buf[10];
    oct_buf[0] = '['; oct_buf[1] = 'O'; oct_buf[2] = 'C'; oct_buf[3] = 'T'; oct_buf[4] = ':'; oct_buf[5] = ' ';
    if (song.octave < 0) {
        oct_buf[6] = '-';
        oct_buf[7] = (char)('0' - song.octave);
    } else {
        oct_buf[6] = '+';
        oct_buf[7] = (char)('0' + song.octave);
    }
    oct_buf[8] = ']';
    oct_buf[9] = '\0';
    cinco_draw_string(bx, 230, oct_buf, C_BLACK);
    bx += 56;

    /* Active Envelope: [BRASS], [PAD], [PLUCK], [BASS] */
    static const char *const env_badges[4] = { "[BRASS]", "[PAD]", "[PLUCK]", "[BASS]" };
    const char *env_str = env_badges[perf.env_mode % 4u];
    cinco_draw_string(bx, 230, env_str, C_BLACK);
    uint32_t elen = 0; while (env_str[elen]) elen++;
    bx += (int32_t)(elen * 6u) + 2;

    /* Active Scale: [CHR], [MIN], [MAJ], [PNT], [BLU] */
    static const char *const scl_badges[5] = { "[CHR]", "[MIN]", "[MAJ]", "[PNT]", "[BLU]" };
    const char *scl_str = scl_badges[perf.scale_mode % 5u];
    cinco_draw_string(bx, 230, scl_str, C_BLACK);
    uint32_t slen = 0; while (scl_str[slen]) slen++;
    bx += (int32_t)(slen * 6u) + 2;

    /* Active Tempo: [XXXBPM] */
    char bpm_badge[12];
    snprintf(bpm_badge, sizeof(bpm_badge), "[%uBPM]", (unsigned)perf.tempo);
    cinco_draw_string(bx, 230, bpm_badge, C_PROG_BLUE);
    uint32_t blen = 0; while (bpm_badge[blen]) blen++;
    bx += (int32_t)(blen * 6u) + 2;

    /* Active Modifiers */
    if (perf.nude && bx + 36 <= 240) {
        cinco_draw_string(bx, 230, "[NSFW]", C_RED);
        bx += 38;
    }
    if (perf.wobble && bx + 30 <= 240) {
        cinco_draw_string(bx, 230, "[WOB]", C_GREEN);
        bx += 32;
    }
    if (perf.flail && bx + 42 <= 240) {
        cinco_draw_string(bx, 230, "[FLARH]", C_AMBER);
        bx += 44;
    }
    if (perf.groove && bx + 36 <= 240) {
        cinco_draw_string(bx, 230, "[PLAY]", C_GREEN);
        bx += 38;
    }
    if (perf.rec && bx + 30 <= 240) {
        cinco_draw_string(bx, 230, "[REC]", C_RED);
        bx += 32;
    }

    /* Coffee mug indicator on desktop taskbar next to terminal at (216, 222, 18, 14) */
    if (bx <= 214) {
        cinco_draw_coffee_mug(216, 222, perf.coffee_level);
    }
}

static void cinco_draw_overlays(void)
{
    /* 5. Overlays: NSFW Protocol Warning Dialog */
    if (perf.nsfw_popup_t > 0) {
        int32_t dx = 20, dy = 48, dw = 200, dh = 76;
        lcd_fill((uint32_t)dx, (uint32_t)dy, (uint32_t)dw, (uint32_t)dh, C_WIN_FACE);
        lcd_fill((uint32_t)dx, (uint32_t)dy, (uint32_t)dw, 1, C_WHITE);
        lcd_fill((uint32_t)dx, (uint32_t)dy, 1, (uint32_t)dh, C_WHITE);
        lcd_fill((uint32_t)dx, (uint32_t)(dy + dh - 1), (uint32_t)dw, 1, C_BORDER_DARK);
        lcd_fill((uint32_t)(dx + dw - 1), (uint32_t)dy, 1, (uint32_t)dh, C_BORDER_DARK);

        /* Dialog blue title banner */
        lcd_fill((uint32_t)(dx + 3), (uint32_t)(dy + 3), (uint32_t)(dw - 6), 14, C_PROG_BLUE);
        cinco_draw_string(dx + 6, dy + 6, "SECURITY PROTOCOL", C_WHITE);

        cinco_draw_string(dx + 8, dy + 24, "THIS IS NOT SUITABLE", C_BLACK);
        cinco_draw_string(dx + 8, dy + 36, "FOR WORK. ARE YOU SURE?", C_BLACK);

        /* [YES] button */
        lcd_fill((uint32_t)(dx + dw - 60), (uint32_t)(dy + 48), 50, 18, C_WIN_FACE);
        lcd_fill((uint32_t)(dx + dw - 60), (uint32_t)(dy + 48), 50, 1, C_WHITE);
        lcd_fill((uint32_t)(dx + dw - 60), (uint32_t)(dy + 48), 1, 18, C_WHITE);
        lcd_fill((uint32_t)(dx + dw - 60), (uint32_t)(dy + 48 + 17), 50, 1, C_BORDER_DARK);
        lcd_fill((uint32_t)(dx + dw - 60 + 49), (uint32_t)(dy + 48), 1, 18, C_BORDER_DARK);
        cinco_draw_string(dx + dw - 48, dy + 53, "[YES]", C_BLACK);
    }

    /* 6. Overlays: Oyster Smiling Receipt */
    if (perf.receipt_t > 0) {
        int32_t rx = 30, ry = 24, rw = 180, rh = 116;
        lcd_fill((uint32_t)rx, (uint32_t)ry, (uint32_t)rw, (uint32_t)rh, C_WHITE);
        /* 3D bevel */
        lcd_fill((uint32_t)(rx + 1), (uint32_t)(ry + 1), (uint32_t)(rw - 2), 1, C_BORDER_MID);
        lcd_fill((uint32_t)(rx + 1), (uint32_t)(ry + 1), 1, (uint32_t)(rh - 2), C_BORDER_MID);
        lcd_fill((uint32_t)(rx + 1), (uint32_t)(ry + rh - 2), (uint32_t)(rw - 2), 1, C_BORDER_DARK);
        lcd_fill((uint32_t)(rx + rw - 2), (uint32_t)(ry + 1), 1, (uint32_t)(rh - 2), C_BORDER_DARK);
        /* 1px black border: left, right, bottom */
        lcd_fill((uint32_t)rx, (uint32_t)ry, 1, (uint32_t)rh, C_BLACK);
        lcd_fill((uint32_t)(rx + rw - 1), (uint32_t)ry, 1, (uint32_t)rh, C_BLACK);
        lcd_fill((uint32_t)rx, (uint32_t)(ry + rh - 1), (uint32_t)rw, 1, C_BLACK);
        /* Perforated top border: 2px dashed segments */
        for (int32_t px = rx; px < rx + rw; px += 4) {
            lcd_fill((uint32_t)px, (uint32_t)ry, 2, 1, C_BLACK);
        }
        /* Receipt printout text */
        cinco_draw_string(40, 32, "*** CINCO PRINTOUT ***", C_BLACK);
        cinco_draw_string(40, 44, "OYSTER SMILING ( ^ _ ^ )", C_BLACK);
        cinco_draw_string(40, 60, "CODE: 4d3d3d3", C_BLACK);
        cinco_draw_string(40, 72, "STATUS: VERIFIED & SAVED", C_BLACK);
        cinco_draw_string(40, 84, "FLASH: 0xFC000 COMMITTED", C_BLACK);
        cinco_draw_string(40, 100, "[ OK ]  CINCO OS 2.5", C_BLACK);
    }

    /* 7. Overlays: Diagnostic Overlay */
    if (perf.diag > 0) {
        int32_t dx = 16, dy = 20, dw = 208, dh = 120;
        /* Green-on-black retro diagnostic HUD box with 3D bevel */
        lcd_fill((uint32_t)dx, (uint32_t)dy, (uint32_t)dw, (uint32_t)dh, C_BLACK);
        lcd_fill((uint32_t)dx, (uint32_t)dy, (uint32_t)dw, 1, C_WHITE);
        lcd_fill((uint32_t)dx, (uint32_t)dy, 1, (uint32_t)dh, C_WHITE);
        lcd_fill((uint32_t)dx, (uint32_t)(dy + dh - 1), (uint32_t)dw, 1, C_BORDER_DARK);
        lcd_fill((uint32_t)(dx + dw - 1), (uint32_t)dy, 1, (uint32_t)dh, C_BORDER_DARK);
        lcd_fill((uint32_t)(dx + 1), (uint32_t)(dy + 1), (uint32_t)(dw - 2), 1, C_BORDER_MID);
        lcd_fill((uint32_t)(dx + 1), (uint32_t)(dy + 1), 1, (uint32_t)(dh - 2), C_BORDER_MID);

        /* HUD Title & line */
        cinco_draw_string(dx + 26, dy + 10, "=== SYSTEM DIAGNOSTICS ===", C_GREEN);
        lcd_fill((uint32_t)(dx + 6), (uint32_t)(dy + 22), (uint32_t)(dw - 12), 1, C_GREEN);

        /* Retro diagnostic lines */
        cinco_draw_string(dx + 12, dy + 28, "CPU: JieLi AC7916 120MHz", C_GREEN);
        cinco_draw_string(dx + 12, dy + 44, "RAM: 56.8KB / 73.7KB (23% Free)", C_GREEN);
        cinco_draw_string(dx + 12, dy + 60, "AUDIO: 44.1kHz 32-bit Q15", C_GREEN);
        cinco_draw_string(dx + 12, dy + 76, "DANCER: 118px 4-bit RLE OK", C_GREEN);
        cinco_draw_string(dx + 12, dy + 92, "GROOVE: 16-Step Sequencer", C_GREEN);
    }

    /* 8. Overlays: Cinco System Alert Dialog */
    if (perf.error_popup_t > 0) {
        cinco_draw_error_popup();
    }
}

/* Compose the complete Cinco screen frame */
static void cinco_view_render(void)
{
    static uint8_t screensaver_init = 0;
    static uint8_t boss_rendered = 0;
    static uint8_t last_boss_cursor = 255;

    /* Master View Router:
     * If screensaver active, render screensaver and return */
    if (perf.screensaver) {
        if (!screensaver_init) {
            cinco_init_screensaver_sprites();
            lcd_fill(0, 0, 240, 240, C_BLACK);
            lcd_blit(42, 116, 156, 8, cv_px + 960);
            uint8_t flap_tick = (uint8_t)(fm1_ms / 150u);
            for (int i = 0; i < 4; i++) {
                perf.prev_celery_x[i] = perf.celery_x[i];
                perf.prev_celery_y[i] = perf.celery_y[i];
                uint8_t flap = (flap_tick + (uint8_t)i) & 1u;
                cinco_draw_celery_stalk(perf.celery_x[i], perf.celery_y[i], flap);
            }
            screensaver_init = 1;
        } else {
            cinco_draw_screensaver();
        }
        return;
    }
    if (screensaver_init) {
        screensaver_init = 0;
        view_initialized = 0;
        ui.force = 1;
    }

    /* If boss mode spreadsheet active, render spreadsheet and return */
    if (perf.boss_mode) {
        if (!boss_rendered) {
            cinco_draw_boss_key();
            boss_rendered = 1;
            last_boss_cursor = (uint8_t)((fm1_ms / 500u) & 1u);
        } else {
            uint8_t cur_cursor = (uint8_t)((fm1_ms / 500u) & 1u);
            if (cur_cursor != last_boss_cursor) {
                lcd_fill(228, 227, 4, 7, cur_cursor ? C_BLACK : C_WIN_FACE);
                last_boss_cursor = cur_cursor;
            }
        }
        return;
    }
    if (boss_rendered) {
        boss_rendered = 0;
        view_initialized = 0;
        ui.force = 1;
    }

    /* Determine active animation and window title */
    const cinco_anim_t *anim = &cinco_anim_celery;
    char title_buf[48] = "Celery Man";
    const char *title = title_buf;
    uint32_t mosaic = 1;

    if (perf.view_mode == 1) {
        title = "Disk Defragmenter - C:";
    } else {
        /* Check motion overrides */
        if (perf.flail) {
            switch (perf.source) {
            case SRC_TAYNE:
                anim = &cinco_anim_tayne_flarh;
                title = perf.nude ? "NUDE TAYNE - FLARHGUNNSTOW" : "Tayne - FLARHGUNNSTOW!";
                break;
            case SRC_OYSTER:
                anim = &cinco_anim_oyster;
                title = perf.nude ? "NUDE OYSTER - FLARHGUNNSTOW" : "Oyster - FLARHGUNNSTOW!";
                break;
            case SRC_CELERY:
            case SRC_TALK:
            default:
                anim = &cinco_anim_celery;
                title = perf.nude ? "NUDE CELERY - FLARHGUNNSTOW" : "Celery Man - FLARHGUNNSTOW!";
                break;
            }
        } else if (perf.wobble) {
            switch (perf.source) {
            case SRC_TAYNE:
                anim = &cinco_anim_tayne_hatwobble;
                title = perf.nude ? "NUDE TAYNE - Hat Wobble" : "Tayne - Hat Wobble";
                break;
            case SRC_OYSTER:
                anim = &cinco_anim_oyster;
                title = perf.nude ? "NUDE OYSTER - Hat Wobble" : "Oyster - Hat Wobble";
                break;
            case SRC_CELERY:
            case SRC_TALK:
            default:
                anim = &cinco_anim_celery;
                title = perf.nude ? "NUDE CELERY - Hat Wobble" : "Celery Man - Hat Wobble";
                break;
            }
        } else {
            switch (perf.source) {
            case SRC_CELERY:
                anim = &cinco_anim_celery;
                title = perf.nude ? "NUDE CELERY MAN" : "Celery Man";
                break;
            case SRC_OYSTER:
                anim = &cinco_anim_oyster;
                title = perf.nude ? "NUDE OYSTER" : "Oyster Smiling";
                break;
            case SRC_TAYNE:
                anim = &cinco_anim_tayne;
                title = perf.nude ? "NUDE TAYNE" : "Tayne (BETA)";
                break;
            case SRC_TALK:
                anim = &cinco_anim_celery;
                title = perf.nude ? "NUDE SPEECH SYNTH" : "Speech Synthesizer";
                break;
            default:
                anim = &cinco_anim_celery;
                title = "Celery Man";
                break;
            }
        }

        /* Orthogonal mosaic filter applied to WHATEVER is dancing when nude is active */
        if (perf.nude) {
            mosaic = 8 + (perf.mosaic * 10) / 127; /* 8..18 px blocks */
        }
    }

    perf.current_mosaic = mosaic;
    uint32_t ti = 0;
    while (title && title[ti] && ti + 1u < sizeof(perf.current_title)) {
        perf.current_title[ti] = title[ti];
        ti++;
    }
    perf.current_title[ti] = '\0';

    /* Update animation frame index */
    uint32_t now = fm1_ms;
    uint32_t fps = anim->fps ? anim->fps : 8u;
    if (perf.flail && (perf.source == SRC_OYSTER || perf.source == SRC_CELERY || perf.source == SRC_TALK)) {
        fps *= 2u;
    }
    uint32_t frame_duration = 1000u / fps;
    if (now - perf.last_frame_ms >= frame_duration) {
        perf.last_frame_ms = now;
        perf.frame_idx = (uint8_t)((perf.frame_idx + 1u) % anim->nframes);
    } else if (perf.frame_idx >= anim->nframes) {
        perf.frame_idx = 0;
    }

    /* 4d3d3d3 Window Cascades */
    int32_t nwindows = 1 + ((int32_t)perf.k4d * 15) / 120;
    if (nwindows > 16) nwindows = 16;

    int32_t tx = 4;
    int32_t ty = 168;
    int32_t tw = 232;
    int32_t th = 57;

    uint8_t cursor_on = (uint8_t)((fm1_ms / 500u) & 1u);
    uint32_t current_state = cinco_get_layout_state(nwindows);
    uint32_t cur_taskbar = cinco_get_taskbar_state();

    uint8_t force_full_redraw = (!view_initialized || ui.force || current_state != last_rendered_state);

    if (force_full_redraw) {
        last_rendered_state = current_state;
        view_initialized = 1;
        ui.force = 0;

        /* 1. Desktop background */
        lcd_fill(0, 0, 240, 240, C_DESKTOP);

        /* 2. 4d3d3d3 Window Cascades */
        for (int32_t i = 0; i < nwindows; i++) {
            int32_t ox = 4 + i * 3;
            int32_t oy = 4 + i * 3;
            int32_t ww = 232 - (nwindows - 1) * 3;
            int32_t wh = 160 - (nwindows - 1) * 3;
            if (ww < 175) ww = 175;
            if (wh < 115) wh = 115;

            cinco_draw_window_chrome(ox, oy, ww, wh, title);

            /* Only draw content on topmost window */
            if (i == nwindows - 1) {
                if (perf.view_mode == 1) {
                    int32_t cw_x = ox + 4;
                    int32_t cw_y = oy + 21;
                    int32_t cw_w = ww - 8;
                    int32_t cw_h = wh - 25;
                    lcd_fill((uint32_t)cw_x, (uint32_t)cw_y, (uint32_t)cw_w, (uint32_t)cw_h, C_WIN_FACE);
                    cinco_draw_defrag_content(ox, oy, ww, wh);
                    uint32_t bpm = perf.tempo ? perf.tempo : 120u;
                    uint32_t ms_per_step = 15000u / bpm;
                    if (ms_per_step == 0) ms_per_step = 1;
                    last_rendered_defrag_step = perf.groove ? cinco_groove_get_step() : (uint8_t)((fm1_ms / ms_per_step) & 15u);
                    last_rendered_defrag_prog = 50u + ((fm1_ms * bpm / 1200u) % 49u);
                    last_rendered_defrag_ms = fm1_ms;
                } else {
                    int32_t cx = ox + 4 + (ww - 8 - anim->w) / 2;
                    int32_t cy = oy + 21 + (wh - 25 - anim->h) / 2;
                    cinco_blit_sprite(anim, perf.frame_idx, cx, cy, mosaic);
                    last_rendered_frame = perf.frame_idx;
                }
            }
        }

        /* 3. CINCO OS 2.5 Terminal */
        cinco_draw_terminal_chrome(tx, ty, tw, th);
        cinco_draw_terminal_text(tx, ty, tw, cursor_on);
        memcpy(last_rendered_term, perf.term_line, sizeof(last_rendered_term));
        last_rendered_cursor = cursor_on;

        /* 4. Desktop Status Indicators Taskbar */
        cinco_draw_taskbar();
        last_rendered_taskbar = cur_taskbar;
        last_rendered_coffee = perf.coffee_level;

        /* 5..8 Overlays */
        cinco_draw_overlays();
        overlay_active = (perf.nsfw_popup_t > 0 || perf.error_popup_t > 0 || perf.receipt_t > 0 || perf.diag > 0);
        return;
    }

    /* Incremental / Dirty-Rect Rendering Path (0 ms overhead when static) */
    int32_t ox = 4 + (nwindows - 1) * 3;
    int32_t oy = 4 + (nwindows - 1) * 3;
    int32_t ww = 232 - (nwindows - 1) * 3;
    int32_t wh = 160 - (nwindows - 1) * 3;
    if (ww < 175) ww = 175;
    if (wh < 115) wh = 115;

    uint8_t any_overlay = (perf.nsfw_popup_t > 0 || perf.error_popup_t > 0 || perf.receipt_t > 0 || perf.diag > 0);

    /* A. Window Content Update */
    if (any_overlay) {
        if (!overlay_active) {
            cinco_draw_overlays();
            overlay_active = 1;
        }
        /* While popup is active: PAUSE background updates (dancer, defrag, terminal, taskbar) */
        return;
    } else {
        if (overlay_active) {
            overlay_active = 0;
            view_initialized = 0;
            ui.force = 1;
        } else if (perf.view_mode == 1) {
            uint32_t bpm = perf.tempo ? perf.tempo : 120u;
            uint32_t ms_per_step = 15000u / bpm;
            if (ms_per_step == 0) ms_per_step = 1;
            uint8_t step = perf.groove ? cinco_groove_get_step() : (uint8_t)((fm1_ms / ms_per_step) & 15u);
            uint8_t step_changed = (step != last_rendered_defrag_step);
            uint8_t time_up = (fm1_ms - last_rendered_defrag_ms >= 500u);

            if (step_changed) {
                cinco_draw_defrag_grid(ox, oy, ww, wh, step);
                last_rendered_defrag_step = step;
            }
            if (time_up) {
                uint32_t progress = cinco_get_defrag_progress(bpm);
                if (progress != last_rendered_defrag_prog) {
                    cinco_draw_defrag_progress(ox, oy, ww, wh, bpm, progress);
                    last_rendered_defrag_prog = progress;
                    last_rendered_defrag_ms = fm1_ms;
                    cinco_check_defrag_complete(progress);
                }
            }
        } else {
            defrag_prev_mode = 0;
            defrag_start_ms = 0;
            if (perf.frame_idx != last_rendered_frame) {
                int32_t cx = ox + 4 + (ww - 8 - anim->w) / 2;
                int32_t cy = oy + 21 + (wh - 25 - anim->h) / 2;
                cinco_blit_sprite(anim, perf.frame_idx, cx, cy, mosaic);
                last_rendered_frame = perf.frame_idx;
            }
        }
    }

    /* B. Terminal text update */
    uint8_t term_dirty = (memcmp(last_rendered_term, perf.term_line, sizeof(last_rendered_term)) != 0);
    if (term_dirty) {
        cinco_draw_terminal_text(tx, ty, tw, cursor_on);
        memcpy(last_rendered_term, perf.term_line, sizeof(last_rendered_term));
        last_rendered_cursor = cursor_on;
    } else if (cursor_on != last_rendered_cursor) {
        /* C. Blinking cursor toggle: ONLY fill the 6x8 cursor rectangle */
        uint32_t len = 0;
        while (perf.term_line[2][len]) len++;
        int32_t cur_x = tx + 6 + (int32_t)len * 6;
        int32_t cur_y = ty + 41;
        lcd_fill((uint32_t)cur_x, (uint32_t)cur_y, 6, 8, C_BLACK);
        if (cursor_on) {
            cinco_draw_char(cur_x, cur_y, '_', C_WHITE);
        }
        last_rendered_cursor = cursor_on;
    }

    /* D. Taskbar badges update */
    if (cur_taskbar != last_rendered_taskbar) {
        cinco_draw_taskbar();
        last_rendered_taskbar = cur_taskbar;
        last_rendered_coffee = perf.coffee_level;
    } else if (perf.coffee_level != last_rendered_coffee) {
        lcd_fill(214, 222, 26, 17, C_WIN_FACE);
        cinco_draw_coffee_mug(216, 222, perf.coffee_level);
        last_rendered_coffee = perf.coffee_level;
    }
}

#endif /* CINCO_VIEW_C */
