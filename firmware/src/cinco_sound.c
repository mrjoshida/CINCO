/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO Sound Engine & Audio DSP Macro Processing */

#ifndef CINCO_SOUND_C
#define CINCO_SOUND_C

#include <stdint.h>
#include "cinco_state.h"

cinco_perf_t perf;

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

void cinco_sound_set_source(uint8_t src)
{
    if (src >= SRC_COUNT)
        src = SRC_CELERY;

    perf.source = src;

    switch (src) {
    case SRC_CELERY:
        /* Dual saw/pulse brass, snappy 24dB ladder filter envelope, decay ~350ms, sustain 20% */
        set_engine_of(&trk[0], 0); /* ENG_ANALOG */
        trk[0].p[P_E0] = 0;        /* WAVE: SAW */
        trk[0].p[P_E1] = 16;       /* DTN: 16 cents */
        trk[0].p[P_E2] = 64;       /* MIX: 50% */
        trk[0].p[P_E4] = 48;       /* CUT */
        trk[0].p[P_E5] = 36;       /* RES */
        trk[0].p[P_ED_FLT] = 52;   /* Snappy ladder filter envelope */
        trk[0].p[P_ATK] = 8;       /* Fast attack */
        trk[0].p[P_DEC] = 68;      /* Decay ~350ms */
        trk[0].p[P_SUS] = 25;      /* Sustain 20% of 127 */
        trk[0].p[P_REL] = 45;
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;

    case SRC_OYSTER:
        /* Glassy bell/chorus CZ patch, chorus send 60% */
        set_engine_of(&trk[0], 2); /* ENG_PHASE */
        apply_preset_to(&trk[0], 4); /* BELL preset */
        trk[0].p[P_CHOR] = 76;     /* Chorus send 60% (76 / 127) */
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;

    case SRC_TAYNE:
        /* 90s FM brass/slap bass */
        set_engine_of(&trk[0], ENGI_FM6); /* ENGI_FM6 = 12 */
        apply_preset_to(&trk[0], 2);      /* FM BASS preset */
        trk[0].p[P_VOICE] = V_MONO;
        trk[0].p[P_ATK] = 0;
        trk[0].p[P_DEC] = 55;
        trk[0].p[P_SUS] = 20;
        trk[0].p[P_REL] = 30;
        trk[0].p[P_LEVEL] = 100;
        break;

    case SRC_TALK:
        /* ENG_FORMANT ("VOICE") */
        set_engine_of(&trk[0], 5); /* ENG_FORMANT */
        apply_preset_to(&trk[0], 0); /* CHOIR AAH */
        trk[0].p[P_VOICE] = V_POLY;
        trk[0].p[P_LEVEL] = 100;
        break;

    default:
        break;
    }

    cinco_sound_apply_env(perf.env_mode);
    cinco_sound_apply_scale(perf.scale_mode);
}

void cinco_sound_init(void)
{
    cinco_perf_init();
    cinco_sound_set_source(perf.source);
}

void cinco_audio_block(int32_t *out, uint32_t n)
{
    /* 1. Macro updates on Track 0 */
    switch (perf.source) {
    case SRC_CELERY: {
        /* K1 (4d3d3d3) modulates filter cutoff, resonance, chorus upwards */
        /* K2 (Tone) modulates filter cutoff */
        int32_t cut = 25 + ((int32_t)perf.tone * 55) / 127 + ((int32_t)perf.k4d * 45) / 127;
        if (cut > 127) cut = 127;
        int32_t res = 25 + ((int32_t)perf.k4d * 85) / 127;
        if (res > 127) res = 127;
        int32_t chor = ((int32_t)perf.k4d * 85) / 127;
        trk[0].p[P_E4] = (int16_t)cut;
        trk[0].p[P_E5] = (int16_t)res;
        trk[0].p[P_CHOR] = (int16_t)chor;
        break;
    }
    case SRC_OYSTER: {
        int32_t dcw = 20 + ((int32_t)perf.tone * 70) / 127 + ((int32_t)perf.k4d * 37) / 127;
        if (dcw > 127) dcw = 127;
        int32_t chor = 76 + ((int32_t)perf.k4d * 40) / 127;
        if (chor > 127) chor = 127;
        trk[0].p[P_E2] = (int16_t)dcw;
        trk[0].p[P_CHOR] = (int16_t)chor;
        break;
    }
    case SRC_TAYNE: {
        int32_t mlvl = -40 + ((int32_t)perf.tone * 70) / 127 + ((int32_t)perf.k4d * 30) / 127;
        if (mlvl > 63) mlvl = 63;
        if (mlvl < -64) mlvl = -64;
        int32_t chor = ((int32_t)perf.k4d * 80) / 127;
        trk[0].p[P_E2] = (int16_t)mlvl;
        trk[0].p[P_CHOR] = (int16_t)chor;
        break;
    }
    case SRC_TALK: {
        trk[0].p[P_E0] = (int16_t)perf.tone;
        int32_t buzz = 30 + ((int32_t)perf.k4d * 80) / 127;
        if (buzz > 127) buzz = 127;
        trk[0].p[P_E4] = (int16_t)buzz;
        trk[0].p[P_CHOR] = (int16_t)(((int32_t)perf.k4d * 60) / 127);
        break;
    }
    default:
        break;
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

    /* 7. Clamping to [-32767, 32767] */
    for (uint32_t i = 0; i < n; i++) {
        int32_t l = out[2u * i];
        int32_t r = out[2u * i + 1u];
        if (l > 32767) l = 32767;
        else if (l < -32767) l = -32767;
        if (r > 32767) r = 32767;
        else if (r < -32767) r = -32767;
        out[2u * i] = l;
        out[2u * i + 1u] = r;
    }
}

#endif /* CINCO_SOUND_C */
