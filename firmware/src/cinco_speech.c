/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO IMA-ADPCM Speech Streaming Voice (8 kHz -> 44.1 kHz fixed-point) */

#ifndef CINCO_SPEECH_C
#define CINCO_SPEECH_C

#include <stdint.h>
#include "cinco_state.h"
#include "cinco_speech_data.h"

#define SPEECH_PHASE_INC ((8000u << 16) / 44100u)  /* Fixed-point phase increment: 11888 */

/* Standard IMA / DVI ADPCM index and step tables */
static const int8_t ima_index_table[16] = {
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8
};

static const int16_t ima_step_size_table[89] = {
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
};

/* Speech voice engine state */
typedef struct {
    uint8_t active;
    uint8_t phrase_id;
    const uint8_t *data;
    uint32_t num_samples;
    uint32_t sample_idx;       /* Current 8 kHz sample index */
    uint32_t phase;            /* Q16 phase accumulator */
    int32_t valpred;           /* ADPCM predictor */
    int32_t index;             /* ADPCM step index */
    int32_t curr_sample;       /* Current 16-bit decoded PCM sample */
    int32_t prev_sample;       /* Previous 16-bit decoded PCM sample */
} cinco_speech_voice_t;

static cinco_speech_voice_t speech_voice;
static volatile uint8_t speech_play_req = 0xFF;

static inline void ima_adpcm_decode_nibble(uint8_t nibble, int32_t *valpred, int32_t *index)
{
    int32_t step = ima_step_size_table[*index];
    int32_t diff = step >> 3;
    if (nibble & 4u) diff += step;
    if (nibble & 2u) diff += (step >> 1);
    if (nibble & 1u) diff += (step >> 2);

    if (nibble & 8u)
        *valpred -= diff;
    else
        *valpred += diff;

    if (*valpred > 32767) *valpred = 32767;
    else if (*valpred < -32768) *valpred = -32768;

    *index += ima_index_table[nibble & 0x0Fu];
    if (*index < 0) *index = 0;
    else if (*index > 88) *index = 88;
}

static inline int32_t speech_decode_next(cinco_speech_voice_t *v)
{
    if (v->sample_idx >= v->num_samples) {
        return 0;
    }
    uint32_t byte_idx = v->sample_idx >> 1;
    uint8_t byte = v->data[byte_idx];
    uint8_t nibble = (v->sample_idx & 1u) ? (byte >> 4) : (byte & 0x0Fu);
    ima_adpcm_decode_nibble(nibble, &v->valpred, &v->index);
    v->sample_idx++;
    return v->valpred;
}

void cinco_speech_init(void)
{
    speech_voice.active = 0;
    speech_voice.phrase_id = 0;
    speech_voice.data = 0;
    speech_voice.num_samples = 0;
    speech_voice.sample_idx = 0;
    speech_voice.phase = 0;
    speech_voice.valpred = 0;
    speech_voice.index = 0;
    speech_voice.curr_sample = 0;
    speech_voice.prev_sample = 0;
    speech_play_req = 0xFF;
}

void cinco_speech_play(uint8_t phrase_id)
{
    if (phrase_id < CINCO_PHRASE_COUNT) {
        speech_play_req = phrase_id;
    }
}

void cinco_speech_process(int32_t *out, uint32_t n)
{
    if (speech_play_req != 0xFF) {
        uint8_t pid = speech_play_req;
        speech_play_req = 0xFF;
        if (pid < CINCO_PHRASE_COUNT) {
            speech_voice.phrase_id = pid;
            speech_voice.data = cinco_phrases[pid].data;
            speech_voice.num_samples = cinco_phrases[pid].num_samples;
            speech_voice.sample_idx = 0;
            speech_voice.phase = 0;
            speech_voice.valpred = 0;
            speech_voice.index = 0;
            speech_voice.prev_sample = 0;
            speech_voice.curr_sample = speech_decode_next(&speech_voice);
            speech_voice.active = 1;
        }
    }

    if (!speech_voice.active)
        return;

    for (uint32_t i = 0; i < n; i++) {
        if (!speech_voice.active)
            break;

        int32_t s = speech_voice.prev_sample +
            (((speech_voice.curr_sample - speech_voice.prev_sample) * (int32_t)speech_voice.phase) >> 16);

        out[2u * i] = ((out[2u * i] * 7) >> 3) + s;
        out[2u * i + 1u] = ((out[2u * i + 1u] * 7) >> 3) + s;

        speech_voice.phase += SPEECH_PHASE_INC;
        while (speech_voice.phase >= 65536u) {
            speech_voice.phase -= 65536u;
            speech_voice.prev_sample = speech_voice.curr_sample;
            if (speech_voice.sample_idx < speech_voice.num_samples) {
                speech_voice.curr_sample = speech_decode_next(&speech_voice);
            } else {
                speech_voice.active = 0;
                break;
            }
        }
    }
}

#endif /* CINCO_SPEECH_C */
