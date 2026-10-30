/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO Sound Engine & Audio DSP Macro Processing */

#ifndef CINCO_SOUND_C
#define CINCO_SOUND_C

#include <stdint.h>
#include "cinco_state.h"

cinco_perf_t perf;

const char *const CINCO_ALGO_NAMES[CINCO_ALGO_COUNT] = {
    "4D Brass [Dual Saw]",
    "Flarh Sync [Hard Sync]",
    "Oyster Sub [Sub Bass]",
    "Cinco CZ [Reso Trapezoid]",
    "Tayne FM4 [Cascade Bell]",
    "Paul Rudd [FM Slap Bass]",
    "Mancierge [Formant Choir]",
    "C-Phone [8-Bit Lofi]",
    "Plucked Celery [Physical]",
    "Flarh Cloud [Granular]",
    "Executive [B3 Organ]",
    "Boardroom [Trio Unison]",
    "Oyster Glass [CZ String]",
    "Solid Bass [DX7 House]",
    "Robo-Vowel [Formant Morph]",
    "D-Pants [Filtered Noise]"
};

const char *const CINCO_PRESET_NAMES[CINCO_PRESET_COUNT] = {
    "Celery Man",
    "Oyster Smiling",
    "Tayne Classic",
    "Computer Voice",
    "Celery 4D Supersaw",
    "Oyster Velvet Chime",
    "Tayne BETA Rave",
    "Nude Tayne Acid 303",
    "Cinco C-Phone",
    "Plucked Celery Harp",
    "Hat Wobble Organ",
    "Paul Rudd Deluxe",
    "Executive Coffee Pad",
    "OSHA Warning Sync",
    "Cinco D-Pants Filter",
    "Identity 2.5 Cyber Choir"
};

const char *const CINCO_GROOVE_NAMES[CINCO_GROOVE_COUNT] = {
    "Eurodance 90s",
    "Rave Breakbeat",
    "Pumping House",
    "Acid Trance 303",
    "Happy Hardcore",
    "Speed Garage",
    "Belgian Techno",
    "Italo Disco"
};

static uint32_t wobble_ph = 0;
static uint32_t mosaic_cnt = 0;
static int32_t mosaic_l = 0;
static int32_t mosaic_r = 0;

/* Track preset and engine setup helpers */
static void apply_preset_to(track_t *t, uint32_t pi)
{
    const engine_t *e = ENGINES[t->eng_req % NENGINES];
    uint32_t i;
    t->preset = (uint8_t)pi;
    if (e->npresets && pi < e->npresets) {
        for (i = 0; i < 8u; i++)
            t->p[P_E0 + i] = (int16_t)e->presets[pi].e[i];
        t->p[P_ATK] = e->presets[pi].env[0];
        t->p[P_DEC] = e->presets[pi].env[1];
        t->p[P_SUS] = e->presets[pi].env[2];
        t->p[P_REL] = e->presets[pi].env[3];
    }
}

static void set_engine_of(track_t *t, uint32_t ei)
{
    const engine_t *e = ENGINES[ei % NENGINES];
    uint32_t i;
    t->eng_req = (uint8_t)(ei % NENGINES);
    for (i = 0; i < 8u; i++)
        t->p[P_E0 + i] = e->edit[i].def;
    apply_preset_to(t, 0);
}

void cinco_term_push(const char *msg)
{
    uint32_t i;
    for (i = 0; i < 32; i++) {
        perf.term_line[0][i] = perf.term_line[1][i];
        perf.term_line[1][i] = perf.term_line[2][i];
    }
    for (i = 0; msg && msg[i] && i < 31; i++) {
        perf.term_line[2][i] = msg[i];
    }
    perf.term_line[2][i] = '\0';
}

static uint8_t perf_inited = 0;

void cinco_perf_init(void)
{
    if (perf_inited)
        return;
    perf_inited = 1;

    perf.source = SRC_CELERY;
    perf.variant = 0;
    perf.k4d = 0;
    perf.tone = 64;
    perf.mosaic = 0;
    perf.tempo = 120;
    perf.mix = 64;
    perf.wobble = 0;
    perf.flail = 0;
    perf.nude = 0;
    perf.groove = 0;
    perf.rec = 0;
    perf.diag = 0;
    perf.env_mode = 0;
    perf.scale_mode = 0;
    perf.groove_pattern = 0;
    perf.seq_row = 0;
    perf.seq_pitch_offset = 0;
    for (int sgi = 0; sgi < 6; sgi++) perf.seq_grid[sgi] = 0;
    perf.anim_tick = 0;
    perf.frame_idx = 0;
    perf.last_frame_ms = 0;
    perf.nsfw_popup_t = 0;
    perf.receipt_t = 0;
    perf.boss_mode = 0;
    perf.view_mode = 0;
    perf.screensaver = 0;
    perf.last_activity_ms = 0;
    perf.coffee_level = 80;
    perf.error_popup_t = 0;
    perf.error_msg[0] = '\0';
    perf.celery_x[0] = 30;  perf.celery_y[0] = 40;  perf.celery_vx[0] = 2;  perf.celery_vy[0] = 1;
    perf.celery_x[1] = 180; perf.celery_y[1] = 60;  perf.celery_vx[1] = -2; perf.celery_vy[1] = 2;
    perf.celery_x[2] = 80;  perf.celery_y[2] = 160; perf.celery_vx[2] = 3;  perf.celery_vy[2] = -1;
    perf.celery_x[3] = 160; perf.celery_y[3] = 200; perf.celery_vx[3] = -2; perf.celery_vy[3] = -2;
    for (int ci = 0; ci < 4; ci++) {
        perf.prev_celery_x[ci] = perf.celery_x[ci];
        perf.prev_celery_y[ci] = perf.celery_y[ci];
    }

    perf.current_mosaic = 1;
    perf.current_title[0] = '\0';

    /* Terminal welcome */
    uint32_t i;
    for (i = 0; i < 3; i++) perf.term_line[i][0] = '\0';

    const char *w0 = "CINCO COMPUTER OS 2.5";
    const char *w1 = "SYSTEM READY";
    const char *w2 = "> Celery Man loaded.";

    for (i = 0; w0[i] && i < 31; i++) perf.term_line[0][i] = w0[i]; perf.term_line[0][i] = '\0';
    for (i = 0; w1[i] && i < 31; i++) perf.term_line[1][i] = w1[i]; perf.term_line[1][i] = '\0';
    for (i = 0; w2[i] && i < 31; i++) perf.term_line[2][i] = w2[i]; perf.term_line[2][i] = '\0';
}

#ifndef QN_CHROM
#define QN_CHROM 0
#endif
#ifndef QN_SNAP
#define QN_SNAP 1
#endif

void cinco_sound_apply_env(uint8_t mode)
{
    perf.env_mode = (uint8_t)(mode % 4u);
    switch (perf.env_mode) {
    case 0: /* Snappy Brass */
        trk[0].p[P_ATK] = 2;
        trk[0].p[P_DEC] = 60;
        trk[0].p[P_SUS] = 20;
        trk[0].p[P_REL] = 35;
        trk[0].p[P_ED_FLT] = 55;
        break;
    case 1: /* Sustained Pad */
        trk[0].p[P_ATK] = 75;
        trk[0].p[P_DEC] = 90;
        trk[0].p[P_SUS] = 127;
        trk[0].p[P_REL] = 100;
        trk[0].p[P_ED_FLT] = 10;
        break;
    case 2: /* Staccato Pluck */
        trk[0].p[P_ATK] = 0;
        trk[0].p[P_DEC] = 25;
        trk[0].p[P_SUS] = 0;
        trk[0].p[P_REL] = 15;
        trk[0].p[P_ED_FLT] = 65;
        break;
    case 3: /* Punch Bass */
    default:
        trk[0].p[P_ATK] = 0;
        trk[0].p[P_DEC] = 45;
        trk[0].p[P_SUS] = 40;
        trk[0].p[P_REL] = 25;
        trk[0].p[P_ED_FLT] = 70;
        break;
    }
}

void cinco_sound_apply_scale(uint8_t mode)
{
    perf.scale_mode = (uint8_t)(mode % 5u);
    switch (perf.scale_mode) {
    case 0: /* Chromatic */
        trk[0].p[P_QUANT] = QN_CHROM;
        trk[0].p[P_SCALE] = 0;
        break;
    case 1: /* Natural Minor */
        trk[0].p[P_QUANT] = QN_SNAP;
        trk[0].p[P_SCALE] = 2;
        break;
    case 2: /* Major */
        trk[0].p[P_QUANT] = QN_SNAP;
        trk[0].p[P_SCALE] = 1;
        break;
    case 3: /* Minor Pentatonic */
        trk[0].p[P_QUANT] = QN_SNAP;
        trk[0].p[P_SCALE] = 6;
        break;
    case 4: /* Blues / Dorian */
    default:
        trk[0].p[P_QUANT] = QN_SNAP;
        trk[0].p[P_SCALE] = 3;
        break;
    }
}

void cinco_sound_set_algo(uint8_t algo)
{
    perf.variant = algo % CINCO_ALGO_COUNT;
    switch (perf.variant) {
    case 0:
        /* 0: ENG_ANALOG (Saw dual detune, snappy filter) */
        set_engine_of(&trk[0], 0);
        trk[0].p[P_E0] = 0;
        trk[0].p[P_E1] = 16;
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 1:
        /* 1: ENG_ANALOG (AW_SYNC = 5, sync lead) */
        set_engine_of(&trk[0], 0);
        trk[0].p[P_E0] = 5;
        trk[0].p[P_E1] = 28;
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 2:
        /* 2: ENG_ANALOG (AW_SUB = 6, sub bass) */
        set_engine_of(&trk[0], 0);
        trk[0].p[P_E0] = 6;
        trk[0].p[P_E2] = 64;
        trk[0].p[P_VOICE] = V_MONO;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 3:
        /* 3: ENG_PHASE (preset 4, resonant trapezoid) */
        set_engine_of(&trk[0], 2);
        apply_preset_to(&trk[0], 4);
        trk[0].p[P_CHOR] = 60;
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 4:
        /* 4: ENGI_FM6 (preset 1, BELL 4-op cascade) */
        set_engine_of(&trk[0], ENGI_FM6);
        apply_preset_to(&trk[0], 1);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 5:
        /* 5: ENGI_FM6 (preset 2, FM BASS slap) */
        set_engine_of(&trk[0], ENGI_FM6);
        apply_preset_to(&trk[0], 2);
        trk[0].p[P_VOICE] = V_MONO;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 6:
        /* 6: ENG_FORMANT (preset 0, CHOIR AAH) */
        set_engine_of(&trk[0], 5);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 7:
        /* 7: ENG_LOFI (preset 2, 8-bit chip) */
        set_engine_of(&trk[0], 3);
        apply_preset_to(&trk[0], 2);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 8:
        /* 8: ENG_PHYS (preset 0, Karplus physical pluck string) */
        set_engine_of(&trk[0], ENGI_PHYS);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 9:
        /* 9: ENG_GRAIN (preset 0, Granular particle cloud) */
        set_engine_of(&trk[0], 8);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 10:
        /* 10: ENG_WHEEL (preset 0, Tonewheel organ with rotary) */
        set_engine_of(&trk[0], 7);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 11:
        /* 11: ENG_TRIO (preset 0, 3-oscillator unison chord) */
        set_engine_of(&trk[0], 6);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 12:
        /* 12: ENG_PHASE (preset 5, CZ resonant string with chorus) */
        set_engine_of(&trk[0], 2);
        apply_preset_to(&trk[0], 5);
        trk[0].p[P_CHOR] = 85;
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 13:
        /* 13: ENGI_FM6 (preset 3, FM brass / solid lead) */
        set_engine_of(&trk[0], ENGI_FM6);
        apply_preset_to(&trk[0], 3);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 14:
        /* 14: ENG_FORMANT (preset 1, CHOIR OOH vowel morph) */
        set_engine_of(&trk[0], 5);
        apply_preset_to(&trk[0], 1);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    case 15:
        /* 15: ENG_NOISE (preset 0, filtered pink noise sweep) */
        set_engine_of(&trk[0], 11);
        apply_preset_to(&trk[0], 0);
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;
    default:
        break;
    }

    cinco_sound_apply_env(perf.env_mode);
    cinco_sound_apply_scale(perf.scale_mode);
}

void cinco_sound_set_preset(uint8_t preset)
{
    perf.source = preset % CINCO_PRESET_COUNT;
    switch (perf.source) {
    case 0:
        /* Celery Man (Brass) */
        cinco_sound_set_algo(0);
        break;
    case 1:
        /* Oyster Smiling (CZ Glass Chime) */
        cinco_sound_set_algo(3);
        break;
    case 2:
        /* Tayne Classic (FM Slap Bass) */
        cinco_sound_set_algo(5);
        break;
    case 3:
        /* Computer Voice (Singing Formant) */
        cinco_sound_set_algo(6);
        break;
    case 4:
        /* Celery 4D Supersaw (Cascading Saw) */
        cinco_sound_set_algo(0);
        trk[0].p[P_CHOR] = 90;
        break;
    case 5:
        /* Oyster Velvet Chime (CZ Resonant String) */
        cinco_sound_set_algo(12);
        trk[0].p[P_CHOR] = 85;
        break;
    case 6:
        /* Tayne BETA Rave (Rave FM Lead) */
        cinco_sound_set_algo(4);
        break;
    case 7:
        /* Nude Tayne Acid 303 (Acid 303 Squelch) */
        cinco_sound_set_algo(2);
        trk[0].p[P_E5] = 80;
        break;
    case 8:
        /* Cinco C-Phone (8-Bit Lofi) */
        cinco_sound_set_algo(7);
        break;
    case 9:
        /* Plucked Celery Harp (Karplus Physical Pluck) */
        cinco_sound_set_algo(8);
        trk[0].p[P_CHOR] = 40;
        break;
    case 10:
        /* Hat Wobble Organ (Tonewheel B3 Organ) */
        cinco_sound_set_algo(10);
        break;
    case 11:
        /* Paul Rudd Deluxe (Trio Unison Lead) */
        cinco_sound_set_algo(11);
        trk[0].p[P_CHOR] = 60;
        break;
    case 12:
        /* Executive Coffee Pad (Granular Cloud Pad) */
        cinco_sound_set_algo(9);
        break;
    case 13:
        /* OSHA Warning Sync (Hard Sync Lead) */
        cinco_sound_set_algo(1);
        break;
    case 14:
        /* Cinco D-Pants Filter (Filtered Pink Noise Sweep) */
        cinco_sound_set_algo(15);
        break;
    case 15:
        /* Identity 2.5 Cyber Choir (Formant Morph Choir) */
        cinco_sound_set_algo(14);
        break;
    default:
        break;
    }
}

void cinco_sound_set_source(uint8_t src)
{
    cinco_sound_set_preset(src);
}

void cinco_sound_init(void)
{
    cinco_perf_init();
    cinco_sound_set_preset(perf.source);
}

void cinco_audio_block(int32_t *out, uint32_t n)
{
    /* 1. Macro updates on Track 0 */
    /* When NSFW mode is OFF, Knob 2 (perf.tone) sweeps filter cutoff/timbre across full musical spectrum */
    if (!perf.nude) {
        switch (trk[0].eng_req) {
        case 0: /* ENG_ANALOG */
        case 3: /* ENG_LOFI */ {
            int32_t cut = 10 + ((int32_t)perf.tone * 117) / 127;
            if (cut > 127) cut = 127;
            if (cut < 0) cut = 0;
            trk[0].p[P_E4] = (int16_t)cut;
            break;
        }
        case 2: /* ENG_PHASE */ {
            int32_t dcw = 5 + ((int32_t)perf.tone * 122) / 127;
            if (dcw > 127) dcw = 127;
            if (dcw < 0) dcw = 0;
            trk[0].p[P_E2] = (int16_t)dcw;
            break;
        }
        case 12: /* ENGI_FM6 */ {
            int32_t mlvl = -64 + ((int32_t)perf.tone * 127) / 127;
            if (mlvl > 63) mlvl = 63;
            if (mlvl < -64) mlvl = -64;
            trk[0].p[P_E2] = (int16_t)mlvl;
            break;
        }
        case 5: /* ENG_FORMANT */ {
            int32_t vowel = ((int32_t)perf.tone * 127) / 127;
            if (vowel > 127) vowel = 127;
            if (vowel < 0) vowel = 0;
            trk[0].p[P_E0] = (int16_t)vowel;
            break;
        }
        case 6: /* ENG_TRIO */ {
            int32_t cut = 10 + ((int32_t)perf.tone * 117) / 127;
            if (cut > 127) cut = 127;
            if (cut < 0) cut = 0;
            trk[0].p[P_E5] = (int16_t)cut;
            break;
        }
        case 7: /* ENG_WHEEL */ {
            int32_t reg = ((int32_t)perf.tone * 15) / 127;
            trk[0].p[P_E0] = (int16_t)reg;
            break;
        }
        case 8: /* ENG_GRAIN */ {
            int32_t tone = 10 + ((int32_t)perf.tone * 117) / 127;
            if (tone > 127) tone = 127;
            if (tone < 0) tone = 0;
            trk[0].p[P_E7] = (int16_t)tone;
            break;
        }
        case 9: /* ENGI_PHYS */ {
            int32_t brit = 10 + ((int32_t)perf.tone * 117) / 127;
            if (brit > 127) brit = 127;
            if (brit < 0) brit = 0;
            trk[0].p[P_E2] = (int16_t)brit;
            break;
        }
        case 11: /* ENG_NOISE */ {
            int32_t freq = 10 + ((int32_t)perf.tone * 117) / 127;
            if (freq > 127) freq = 127;
            if (freq < 0) freq = 0;
            trk[0].p[P_E2] = (int16_t)freq;
            break;
        }
        default:
            break;
        }
    }

    /* 4d3d3d3: Analog drive & delay send on Track 0 */
    trk[0].p[P_DIST] = (perf.k4d > 100) ? (int16_t)(((perf.k4d - 100) * 12) / 27) : 0;
    trk[0].p[P_DLY] = (int16_t)(((int32_t)perf.k4d * 50) / 127);
    trk[0].p[P_E5] = (int16_t)(24 + ((int32_t)perf.k4d * 68) / 127);
    trk[0].p[P_LEVEL] = (int16_t)(100 - (((int32_t)perf.k4d * 22) / 127));

    /* 4d3d3d3: Chorus, detune, and engine-specific macro modulation */
    switch (trk[0].eng_req) {
    case 0: /* ENG_ANALOG */ {
        if (trk[0].p[P_E0] == 0) {
            trk[0].p[P_E1] = (int16_t)(16 + ((int32_t)perf.k4d * 90) / 127);
        }
        trk[0].p[P_CHOR] = (int16_t)(((int32_t)perf.k4d * 115) / 127);
        break;
    }
    case 2: /* ENG_PHASE */ {
        int32_t chor = 60 + ((int32_t)perf.k4d * 56) / 127;
        if (chor > 127) chor = 127;
        trk[0].p[P_CHOR] = (int16_t)chor;
        break;
    }
    case 12: /* ENGI_FM6 */ {
        int32_t chor = ((int32_t)perf.k4d * 115) / 127;
        trk[0].p[P_CHOR] = (int16_t)chor;
        break;
    }
    case 5: /* ENG_FORMANT */ {
        int32_t buzz = 30 + ((int32_t)perf.k4d * 80) / 127;
        if (buzz > 127) buzz = 127;
        trk[0].p[P_E4] = (int16_t)buzz;
        trk[0].p[P_CHOR] = (int16_t)(((int32_t)perf.k4d * 115) / 127);
        break;
    }
    default: {
        trk[0].p[P_CHOR] = (int16_t)(((int32_t)perf.k4d * 115) / 127);
        break;
    }
    }

    /* 2. Pitch LFO wobble (6 Hz tempo-synced vibrato on trk[0] active voices) */
    uint32_t tempo = perf.tempo;
    if (tempo < 80) tempo = 80;
    if (tempo > 160) tempo = 160;
    uint32_t freq_hz = (tempo * 6u) / 120u;
    wobble_ph += (((freq_hz * 97390u) >> 8) * n) >> 8;

    int32_t vib = 0;
    if (perf.wobble) {
        vib = (sine_i(wobble_ph) * 160) >> 15;
    }
    for (uint32_t i = 0; i < NVOICE; i++) {
        trk[0].v[i].fine = (int16_t)vib;
    }

    /* 3. Flail trigger (rapid 16th-note arp or slicer on trk[0]) */
    if (perf.flail) {
        trk[0].p[P_SLCR] = 1;     /* SL_GATE */
        trk[0].p[P_SLRATE] = 1;   /* 16th note */
        trk[0].p[P_SLPAT] = 0;    /* 0x5555: alternating 16th */
        trk[0].p[P_SLDEPTH] = 127;
        trk[0].p[P_AMODE] = 1;    /* Arp UP */
        trk[0].p[P_ARATE] = 1;    /* 16th note arp */
        trk[0].p[P_AOCT] = 2;
    } else {
        trk[0].p[P_SLCR] = 0;     /* SL_OFF */
        trk[0].p[P_AMODE] = 0;    /* Arp OFF */
    }

    /* 4. Eurodance Groove Sequencer */
    cinco_groove_process(n);

    /* 5. ADPCM Speech Processing */
    cinco_speech_process(out, n);

    /* 6. Audio Mosaic: sample-and-hold downsampler + bit reduction */
    if (perf.nude) {
        uint32_t hold = 2u + ((uint32_t)perf.mosaic >> 2); /* 2..33 */
        uint32_t shift = 2u + ((uint32_t)perf.mosaic >> 3);       /* 2..17 */
        if (shift > 14u) shift = 14u;
        int32_t mask = ~((1 << shift) - 1);

        for (uint32_t i = 0; i < n; i++) {
            if (++mosaic_cnt >= hold) {
                mosaic_cnt = 0;
                mosaic_l = out[2u * i];
                mosaic_r = out[2u * i + 1u];
            }
            int32_t l = mosaic_l;
            int32_t r = mosaic_r;
            l &= mask;
            r &= mask;
            out[2u * i] = l;
            out[2u * i + 1u] = r;
        }
    } else {
        mosaic_cnt = 0;
    }

    /* 7. Master headroom backoff, softclip, and clamping to [-32767, 32767] */
    for (uint32_t i = 0; i < n; i++) {
        int32_t l = (out[2u * i] * 7) >> 3;
        int32_t r = (out[2u * i + 1u] * 7) >> 3;
        l = softclip(l);
        r = softclip(r);
        if (l > 32767) l = 32767;
        else if (l < -32767) l = -32767;
        if (r > 32767) r = 32767;
        else if (r < -32767) r = -32767;
        out[2u * i] = l;
        out[2u * i + 1u] = r;
    }
}

#endif /* CINCO_SOUND_C */
