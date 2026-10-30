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

static void cinco_groove_step(uint8_t step, uint8_t bar)
{
    uint8_t pat = perf.groove_pattern % CINCO_GROOVE_COUNT;
    uint8_t root = bass_roots[bar & 3u];

    switch (pat) {
    case 0: {
        /* 0: Eurodance 90s */
        /* Kick: Steps 0, 4, 8, 12 */
        if ((step & 3u) == 0u) {
            trk_note_on(&trk[3], 36, 120);
        }
        /* Clap: Steps 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 39, 115);
        }
        /* Open Hat: Steps 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 46, 105);
        }
        /* Closed Hat: Offbeat 16th notes (1, 3, 5, 7, 9, 11, 13, 15) */
        if (step & 1u) {
            trk_note_on(&trk[3], 42, 95);
        }

        /* Bassline on Track 1 (ENG_ANALOG) */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
        }
        /* 16th-note octave pump: even steps = low root, odd steps = high root */
        uint8_t b_note = (step & 1u) ? (root + 12u) : root;
        prev_bass_note = b_note;
        trk_note_on(&trk[1], b_note, 110);

        /* Rave stabs on Track 2 (ENGI_FM6) */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        /* Offbeat minor chords on steps 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 102);
            }
        }
        break;
    }

    case 1: {
        /* 1: Rave Breakbeat */
        /* Syncopated Kick: 0, 7, 10 */
        if (step == 0u || step == 7u || step == 10u) {
            trk_note_on(&trk[3], 36, 120);
        }
        /* Snare: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 38, 118);
        }
        /* Hat: 2, 6, 8, 14 */
        if (step == 2u || step == 6u || step == 8u || step == 14u) {
            trk_note_on(&trk[3], 46, 100);
        }

        /* Bassline */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        if (step == 0u || step == 3u || step == 7u || step == 10u || step == 12u) {
            prev_bass_note = root;
            trk_note_on(&trk[1], root, 115);
        }

        /* Rave Stabs */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if (step == 0u || step == 6u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 105);
            }
        }
        break;
    }

    case 2: {
        /* 2: Pumping House */
        /* 4 on the floor kick */
        if ((step & 3u) == 0u) {
            trk_note_on(&trk[3], 36, 122);
        }
        /* Clap: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 39, 110);
        }
        /* Open Hat on offbeats: 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 46, 110);
        }
        /* Shaker on all 16ths */
        trk_note_on(&trk[3], 42, (step & 1u) ? 80 : 60);

        /* House bass on 2, 6, 8, 14 */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        if ((step & 3u) == 2u || step == 8u) {
            uint8_t b_note = root + 12u;
            prev_bass_note = b_note;
            trk_note_on(&trk[1], b_note, 108);
        }

        /* Chords */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if ((step & 3u) == 2u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 100);
            }
        }
        break;
    }

    case 3: {
        /* 3: Acid Trance 303 (16th bassline, driving 909 kick, trance chords) */
        /* Driving 909 Kick: 0, 4, 8, 12 */
        if ((step & 3u) == 0u) {
            trk_note_on(&trk[3], 36, 125);
        }
        /* Clap: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 39, 110);
        }
        /* Open Hat: 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 46, 110);
        }
        /* Closed Hat on 16ths */
        if (step & 1u) {
            trk_note_on(&trk[3], 42, 95);
        }

        /* 16th acid bassline on Track 1 */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        static const uint8_t acid_pattern[16] = {0, 12, 0, 3, 0, 7, 12, 10, 0, 12, 3, 5, 0, 7, 12, 10};
        uint8_t b_note = root + acid_pattern[step];
        prev_bass_note = b_note;
        trk_note_on(&trk[1], b_note, (step % 4 == 0) ? 122 : 105);

        /* Trance chords on steps 0, 8 */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if (step == 0u || step == 8u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 95);
            }
        }
        break;
    }

    case 4: {
        /* 4: Happy Hardcore (fast 16th breaks, bouncy octave bass, euphoric rave chords) */
        /* Kick: 0, 4, 8, 12 */
        if ((step & 3u) == 0u) {
            trk_note_on(&trk[3], 36, 127);
        }
        /* Break snare: 4, 10, 12, 14 */
        if (step == 4u || step == 10u || step == 12u || step == 14u) {
            trk_note_on(&trk[3], 38, 115);
        }
        /* Open Hat: 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 46, 105);
        }
        /* Rapid 16th closed hats */
        trk_note_on(&trk[3], 42, 90);

        /* Bouncy octave bass on offbeats */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        if (step & 1u) {
            uint8_t b_note = (step & 2u) ? (root + 12u) : root;
            prev_bass_note = b_note;
            trk_note_on(&trk[1], b_note, 120);
        }

        /* Euphoric rave chords: 2, 5, 8, 11, 14 */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if (step == 2u || step == 5u || step == 8u || step == 11u || step == 14u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 108);
            }
        }
        break;
    }

    case 5: {
        /* 5: Speed Garage (syncopated kick 0/6/10, snare 4/12, Reese bass, organ stabs) */
        /* Syncopated kick: 0, 6, 10 */
        if (step == 0u || step == 6u || step == 10u) {
            trk_note_on(&trk[3], 36, 125);
        }
        /* Snare: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 38, 118);
        }
        /* Hats */
        if (step == 2u || step == 4u || step == 6u || step == 8u || step == 10u || step == 12u || step == 14u) {
            trk_note_on(&trk[3], 42, 100);
        } else {
            trk_note_on(&trk[3], 42, 70);
        }
        if (step == 6u || step == 14u) {
            trk_note_on(&trk[3], 46, 105);
        }

        /* Reese bass */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        if (step == 0u || step == 6u || step == 10u || step == 14u) {
            prev_bass_note = root;
            trk_note_on(&trk[1], root, 120);
        }

        /* Organ stabs: 2, 5, 8, 13 */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if (step == 2u || step == 5u || step == 8u || step == 13u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 108);
            }
        }
        break;
    }

    case 6: {
        /* 6: Belgian Techno (industrial 4-on-the-floor, dark driving bass, metallic clang) */
        /* Industrial 4-on-the-floor kick */
        if ((step & 3u) == 0u) {
            trk_note_on(&trk[3], 36, 127);
        }
        /* Clap: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 39, 110);
        }
        /* Metallic clang (Rim / Bell) on 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 37, 115);
        }
        if (step == 14u) {
            trk_note_on(&trk[3], 56, 110);
        }
        /* Closed hat: every 16th */
        trk_note_on(&trk[3], 42, (step & 1u) ? 90 : 75);

        /* Dark driving bass on 0, 2, 3, 6, 8, 10, 11, 14 */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        if (step == 0u || step == 2u || step == 3u || step == 6u ||
            step == 8u || step == 10u || step == 11u || step == 14u) {
            prev_bass_note = root;
            trk_note_on(&trk[1], root, 115);
        }

        /* Industrial stabs on 3, 7, 11, 15 */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if ((step & 3u) == 3u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 100);
            }
        }
        break;
    }

    case 7:
    default: {
        /* 7: Italo Disco (Moroder 16th octave bass, electro kick 0/8, 80s chords) */
        /* Electro kick: 0, 8 */
        if (step == 0u || step == 8u) {
            trk_note_on(&trk[3], 36, 124);
        }
        /* Snare: 4, 12 */
        if (step == 4u || step == 12u) {
            trk_note_on(&trk[3], 38, 115);
        }
        /* Open Hat: 2, 6, 10, 14 */
        if ((step & 3u) == 2u) {
            trk_note_on(&trk[3], 46, 105);
        }
        /* Closed hat: every 16th */
        trk_note_on(&trk[3], 42, 80);

        /* Moroder 16th octave bass */
        if (prev_bass_note) {
            trk_note_off(&trk[1], prev_bass_note);
            prev_bass_note = 0;
        }
        static const uint8_t moroder_oct[4] = {0, 0, 12, 0};
        uint8_t b_note = root + moroder_oct[step & 3u];
        prev_bass_note = b_note;
        trk_note_on(&trk[1], b_note, 112);

        /* 80s synth chords on 0, 4, 8, 12 */
        for (uint32_t i = 0; i < 3; i++) {
            if (prev_stab_notes[i]) {
                trk_note_off(&trk[2], prev_stab_notes[i]);
                prev_stab_notes[i] = 0;
            }
        }
        if ((step & 3u) == 0u) {
            for (uint32_t i = 0; i < 3; i++) {
                prev_stab_notes[i] = stab_chords[bar & 3u][i];
                trk_note_on(&trk[2], prev_stab_notes[i], 100);
            }
        }
        break;
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
