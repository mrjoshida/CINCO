/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO State and Performance Engine Interface */

#ifndef CINCO_STATE_H
#define CINCO_STATE_H

#include <stdint.h>
#include "cinco_speech_data.h"

/* Sound source / character selection */
enum {
    SRC_CELERY = 0,
    SRC_OYSTER = 1,
    SRC_TAYNE  = 2,
    SRC_TALK   = 3,
    SRC_COUNT  = 4
};

#define CINCO_PRESET_COUNT 16
#define CINCO_ALGO_COUNT 16
#define CINCO_GROOVE_COUNT 8

extern const char *const CINCO_ALGO_NAMES[CINCO_ALGO_COUNT];
extern const char *const CINCO_PRESET_NAMES[CINCO_PRESET_COUNT];
extern const char *const CINCO_GROOVE_NAMES[CINCO_GROOVE_COUNT];

/* Unified performance state: single source of truth for sound + view */
typedef struct {
    uint8_t source;            /* SRC_CELERY, SRC_OYSTER, SRC_TAYNE, SRC_TALK */
    uint8_t variant;           /* patch variant within source (0..3) */
    uint8_t k4d;               /* K1: 4d3d3d3 macro intensity (0..127) */
    uint8_t tone;              /* K2: filter tone / timbre (0..127) */
    uint8_t mosaic;            /* mosaic block size / bitcrush intensity (0..127) */
    uint8_t tempo;             /* K3: groove tempo (80..160 BPM) */
    uint8_t mix;               /* K4: balance between groove and synth (0..127) */

    /* Performance triggers */
    uint8_t wobble;            /* LFO held: hat wobble */
    uint8_t flail;             /* ARP held: flarhgunnstow */
    uint8_t nude;              /* FX: nude Tayne active */
    uint8_t groove;            /* PLAY: groove sequencer running */
    uint8_t rec;               /* REC: loop overdub active */
    uint8_t diag;              /* diagnostic overlay active */
    uint8_t env_mode;          /* 0: Brass, 1: Pad, 2: Pluck, 3: Bass */
    uint8_t scale_mode;        /* 0: Chromatic, 1: Minor, 2: Major, 3: Pentatonic, 4: Blues */
    uint8_t groove_pattern;    /* 0: Eurodance, 1: Rave, 2: House */

    /* Office Suite & After Dark Pack */
    uint8_t boss_mode;         /* 1 = Boss spreadsheet active */
    uint8_t view_mode;         /* 0 = Dancers, 1 = Disk Defragmenter */
    uint8_t screensaver;       /* 1 = Flying celery screensaver active */
    uint32_t last_activity_ms; /* tracks last input time */
    uint8_t coffee_level;      /* 0..100, coffee meter */
    char error_msg[64];        /* error popup text */
    uint8_t error_popup_t;     /* frames remaining for error popup */
    int16_t celery_x[4];       /* flying celery x */
    int16_t celery_y[4];       /* flying celery y */
    int8_t celery_vx[4];       /* flying celery vx */
    int8_t celery_vy[4];       /* flying celery vy */
    int16_t prev_celery_x[4];  /* flying celery prev x */
    int16_t prev_celery_y[4];  /* flying celery prev y */

    /* Disk Defragmenter Sequencer */
    uint16_t seq_grid[6];       /* 6 tracks x 16 steps (bits 0..15). Row 0: Kick, 1: Snare, 2: C.Hat, 3: O.Hat, 4: Bass, 5: Stab */
    uint8_t  seq_row;           /* Active row cursor (0..5) */
    int8_t   seq_pitch_offset;  /* Pitch transposition for Bass/Stab (-12..+12) */

    /* Animation clock */
    uint32_t anim_tick;
    uint8_t  frame_idx;
    uint32_t last_frame_ms;

    /* UI Overlays */
    uint8_t  nsfw_popup_t;     /* frames remaining for NSFW flash alert */
    uint8_t  receipt_t;        /* frames remaining for Oyster smiling receipt */
    char     term_line[3][32]; /* 3 terminal lines */
    char     current_title[48];/* active window title */
    uint32_t current_mosaic;   /* active mosaic factor */
} cinco_perf_t;

extern cinco_perf_t perf;

/* Function prototypes */
void cinco_perf_init(void);
void cinco_term_push(const char *msg);
void cinco_speech_play(uint8_t phrase_id);
void cinco_speech_init(void);
void cinco_speech_process(int32_t *out, uint32_t n);
void cinco_sound_init(void);
void cinco_sound_set_source(uint8_t src);
void cinco_sound_set_preset(uint8_t preset);
void cinco_sound_set_algo(uint8_t algo);
void cinco_sound_apply_env(uint8_t mode);
void cinco_sound_apply_scale(uint8_t mode);
void cinco_groove_init(void);
void cinco_groove_set_pattern(uint8_t pat);
void cinco_groove_load_template(uint8_t pat);
uint8_t cinco_groove_get_step(void);
uint8_t cinco_groove_get_bass_root(uint8_t mode, uint8_t bar);
uint8_t cinco_groove_get_stab_chord(uint8_t mode, uint8_t bar, uint8_t note_idx);
void cinco_groove_process(uint32_t n);
void cinco_audio_block(int32_t *out, uint32_t n);
void cinco_save_state(void);
void cinco_load_state(void);

static const char * const SEQ_ROW_NAMES[6] = {
    "KICK", "SNARE", "C.HAT", "O.HAT", "BASS", "STAB"
};

#define CINCO_SAVE_MAGIC 0x4F434E49 /* "INCO" */
typedef struct __attribute__((packed)) {
    uint32_t magic;
    uint8_t  source;          /* Preset 0..15 */
    uint8_t  variant;         /* Synth Algo 0..15 */
    uint8_t  k4d;
    uint8_t  tone;
    uint8_t  mosaic;
    uint8_t  tempo;
    uint8_t  mix;
    uint8_t  groove;
    int8_t   octave;
    uint8_t  groove_pattern;  /* Groove Style 0..7 */
    uint16_t seq_grid[6];     /* 12 bytes */
    uint8_t  seq_row;         /* 1 byte */
    int8_t   seq_pitch_offset;/* 1 byte */
    uint8_t  reserved[4];     /* 4 bytes (Total: 32 bytes) */
} cinco_save_t;
_Static_assert(sizeof(cinco_save_t) == 32u, "cinco_save_t size");

#endif /* CINCO_STATE_H */
