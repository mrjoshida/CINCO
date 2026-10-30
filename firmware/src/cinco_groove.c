/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO 90s Eurodance Groove Sequencer Engine */

#ifndef CINCO_GROOVE_C
#define CINCO_GROOVE_C

#include <stdint.h>
#include "cinco_state.h"

static void set_engine_of(track_t *t, uint32_t ei);
static void apply_preset_to(track_t *t, uint32_t pi);

static uint8_t groove_running = 0;
static uint8_t step_idx = 0;
static uint8_t bar_idx = 0;
static uint32_t sample_acc = 0;
static uint8_t prev_bass_note = 0;
static uint8_t prev_stab_notes[3] = {0, 0, 0};

/* Eurodance chord roots: C2 (36), Ab1 (32), Bb1 (34), G1 (31) */
static const uint8_t bass_roots[4] = {36, 32, 34, 31};

/* Offbeat rave synth chords:
 * Bar 0: C minor (C4=60, Eb4=63, G4=67)
 * Bar 1: Ab major (Ab3=56, C4=60, Eb4=63)
 * Bar 2: Bb major (Bb3=58, D4=62, F4=65)
 * Bar 3: G minor (G3=55, Bb3=58, D4=62) */
static const uint8_t stab_chords[4][3] = {
    {60, 63, 67},
    {56, 60, 63},
    {58, 62, 65},
    {55, 58, 62}
};

/* 8 styles x 6 tracks defragmenter pattern templates */
static const uint16_t GROOVE_TEMPLATES[8][6] = {
    /* 0: Eurodance 90s */
    { 0x1111, 0x1010, 0xAAAA, 0x4444, 0xFFFF, 0x4444 },
    /* 1: Rave Breakbeat */
    { 0x0481, 0x1010, 0xAAAA, 0x4144, 0x1489, 0x0041 },
    /* 2: Pumping House */
    { 0x1111, 0x1010, 0xFFFF, 0x4444, 0x4144, 0x4444 },
    /* 3: Acid Trance 303 */
    { 0x1111, 0x1010, 0xAAAA, 0x4444, 0xFFFF, 0x0101 },
    /* 4: Happy Hardcore */
    { 0x1111, 0x5410, 0xFFFF, 0x4444, 0xAAAA, 0x4924 },
    /* 5: Speed Garage */
    { 0x0441, 0x1010, 0xFFFF, 0x4040, 0x4441, 0x2124 },
    /* 6: Belgian Techno */
    { 0x1111, 0x1010, 0xFFFF, 0x4444, 0x4D4D, 0x8888 },
    /* 7: Italo Disco */
    { 0x0101, 0x1010, 0xFFFF, 0x4444, 0xFFFF, 0x1111 }
};

void cinco_groove_load_template(uint8_t pat)
{
    uint8_t p = pat % CINCO_GROOVE_COUNT;
    for (uint32_t r = 0; r < 6u; r++) {
        perf.seq_grid[r] = GROOVE_TEMPLATES[p][r];
    }
}

static void cinco_groove_step(uint8_t step, uint8_t bar)
{
    uint16_t mask = (uint16_t)(1u << (step & 15u));

    /* Row 0 (Kick) */
    if (perf.seq_grid[0] & mask) {
        trk_note_on(&trk[3], 36, 120);
    }

    /* Row 1 (Snare) */
    if (perf.seq_grid[1] & mask) {
        trk_note_on(&trk[3], (step == 4u || step == 12u) ? 39 : 38, 115);
    }

    /* Row 2 (C.Hat) */
    if (perf.seq_grid[2] & mask) {
        trk_note_on(&trk[3], 42, 95);
    }

    /* Row 3 (O.Hat) */
    if (perf.seq_grid[3] & mask) {
        trk_note_on(&trk[3], 46, 105);
    }

    /* Row 4 (Bass) */
    if (perf.seq_grid[4] & mask) {
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        int32_t r = (int32_t)bass_roots[bar & 3u] + perf.seq_pitch_offset;
        if (r < 12) r = 12;
        if (r > 108) r = 108;
        uint8_t root = (uint8_t)r;
        uint8_t b_note = (step & 1u) ? (root + 12u) : root;
        prev_bass_note = b_note;
        trk_note_on(&trk[1], b_note, 110);
    }

    /* Row 5 (Stabs) */
    if (perf.seq_grid[5] & mask) {
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        for (uint32_t i = 0; i < 3; i++) {
            int32_t sn = (int32_t)stab_chords[bar & 3u][i] + perf.seq_pitch_offset;
            if (sn < 12) sn = 12;
            if (sn > 120) sn = 120;
            prev_stab_notes[i] = (uint8_t)sn;
            trk_note_on(&trk[2], prev_stab_notes[i], 102);
        }
    }
}

void cinco_groove_init(void)
{
    groove_running = 0;
    step_idx = 0;
    bar_idx = 0;
    sample_acc = 0;
    prev_bass_note = 0;
    prev_stab_notes[0] = 0;
    prev_stab_notes[1] = 0;
    prev_stab_notes[2] = 0;

    cinco_groove_load_template(perf.groove_pattern);

    /* Configure Track 3: DRUM */
    set_engine_of(&trk[3], ENGI_DRUM);
    trk[3].p[P_LEVEL] = perf.mix;

    /* Configure Track 1: Eurodance pumping bass (ENG_ANALOG) */
    set_engine_of(&trk[1], 0);
    trk[1].p[P_VOICE] = V_MONO;
    trk[1].p[P_E0] = 0;          /* SAW */
    trk[1].p[P_E4] = 55;         /* Filter CUT */
    trk[1].p[P_E5] = 45;         /* Filter RES */
    trk[1].p[P_ED_FLT] = 50;     /* Filter Env depth */
    trk[1].p[P_ATK] = 0;         /* Snappy attack */
    trk[1].p[P_DEC] = 45;        /* Snappy decay ~200ms */
    trk[1].p[P_SUS] = 15;        /* Low sustain */
    trk[1].p[P_REL] = 25;
    trk[1].p[P_LEVEL] = perf.mix;

    /* Configure Track 2: Rave synth stabs (ENGI_FM6) */
    set_engine_of(&trk[2], ENGI_FM6);
    apply_preset_to(&trk[2], 3); /* FM BRASS preset */
    trk[2].p[P_VOICE] = V_POLY;
    trk[2].p[P_ATK] = 0;
    trk[2].p[P_DEC] = 50;
    trk[2].p[P_SUS] = 0;
    trk[2].p[P_REL] = 30;
    trk[2].p[P_CHOR] = 50;
    trk[2].p[P_REV] = 40;
    trk[2].p[P_LEVEL] = perf.mix;
}

void cinco_groove_process(uint32_t n)
{
    /* Scale groove track mix levels from perf.mix (K4) */
    int16_t lvl = (int16_t)(perf.mix <= 127 ? perf.mix : 127);
    trk[1].p[P_LEVEL] = lvl;
    trk[2].p[P_LEVEL] = lvl;
    trk[3].p[P_LEVEL] = lvl;

    if (!perf.groove) {
        if (groove_running) {
            groove_running = 0;
            if (prev_bass_note) {
                trk_note_off(&trk[1], prev_bass_note);
                prev_bass_note = 0;
            }
            for (uint32_t i = 0; i < 3; i++) {
                if (prev_stab_notes[i]) {
                    trk_note_off(&trk[2], prev_stab_notes[i]);
                    prev_stab_notes[i] = 0;
                }
            }
            step_idx = 0;
            bar_idx = 0;
            sample_acc = 0;
        }
        return;
    }

    groove_running = 1;

    /* BPM calculation: 44100 * 15 / tempo */
    uint32_t tempo = perf.tempo;
    if (tempo < 80) tempo = 80;
    if (tempo > 160) tempo = 160;
    uint32_t step_samples = 661500u / tempo;

    sample_acc += n;
    while (sample_acc >= step_samples) {
        sample_acc -= step_samples;
        cinco_groove_step(step_idx, bar_idx);
        step_idx = (step_idx + 1u) & 15u;
        if (step_idx == 0u) {
            bar_idx = (bar_idx + 1u) & 3u;
        }
    }
}

void cinco_groove_set_pattern(uint8_t pat)
{
    perf.groove_pattern = pat % CINCO_GROOVE_COUNT;
    cinco_groove_load_template(perf.groove_pattern);
    if (prev_bass_note) {
        trk_note_off(&trk[1], prev_bass_note);
        prev_bass_note = 0;
    }
    for (uint32_t i = 0; i < 3; i++) {
        if (prev_stab_notes[i]) {
            trk_note_off(&trk[2], prev_stab_notes[i]);
            prev_stab_notes[i] = 0;
        }
    }
}

uint8_t cinco_groove_get_step(void)
{
    return step_idx;
}

#endif /* CINCO_GROOVE_C */
