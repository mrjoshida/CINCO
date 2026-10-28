/* SPDX-License-Identifier: GPL-3.0-only
 * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */
/* CINCO UI Layer: replaces stock Felucca UI with the Cinco 2.5 retro desktop interface. */

#ifndef CINCO_UI_C
#define CINCO_UI_C

#include <stdint.h>
#include "cinco_state.h"

static void cinco_str_copy(char *dst, const char *src, uint32_t max)
{
    uint32_t i = 0;
    while (src && src[i] && i + 1u < max) {
        dst[i] = src[i];
        i++;
    }
    dst[i] = '\0';
}

/* Screen state machine and sleep management */
enum { SCR_ON, SCR_OFF, SCR_WAKE, SCR_SLPOUT, SCR_SHOW };

static struct {
    uint32_t idle;
    uint8_t st;
    uint8_t eat;
    uint32_t t;
    uint32_t eat_t;
} scrn;

static void scr_wake_now(void)
{
    scrn.idle = fm1_ms;
    if (scrn.st == SCR_OFF)
        scrn.st = SCR_WAKE;
    scrn.eat = 1;
}

/* UI global state struct (compatible with main.c, ota, midi, and storage) */
static struct {
    uint8_t home;
    uint8_t page;
    uint8_t bank;
    uint8_t cursor;
    uint8_t lane;
    uint8_t force;
    uint8_t uboot;               /* seconds remaining before entering UBoot */
    uint8_t msg_t;
    char msg[24];
    struct {
        uint8_t on;
        uint8_t pick, trk, id;
        volatile uint8_t io[2];
    } ml;
    volatile uint8_t mpc[NTRK];
} ui;

/* System preferences flags */
#define PREF_ANIM_OFF 2u
#define PREF_CPU2_ON  (1u << 16)

static uint8_t ui_prefs = 0;
static uint8_t ui_prefs2 = 0;
static int32_t undo_depth = 0;
static uint32_t pat_sig[NTRK];
static uint8_t pat_last[NTRK];

#if !FELUCCA_FLASH
#ifndef OBJ_SETTINGS
#define OBJ_SETTINGS 0
#endif
static int st_load(uint32_t obj, void *dst, uint32_t max) { (void)obj; (void)dst; (void)max; return -1; }
static int st_save(uint32_t obj, const void *src, uint32_t len) { (void)obj; (void)src; (void)len; return -1; }
#endif

void cinco_save_state(void)
{
#if FELUCCA_FLASH
    if (!flash_ok)
        return;
#endif
    cinco_save_t save;
    memset(&save, 0, sizeof(save));
    save.magic = CINCO_SAVE_MAGIC;
    save.source = perf.source;
    save.variant = perf.variant;
    save.k4d = perf.k4d;
    save.tone = perf.tone;
    save.mosaic = perf.mosaic;
    save.tempo = perf.tempo;
    save.mix = perf.mix;
    save.groove = perf.groove;
    save.octave = song.octave;
    st_save(OBJ_SETTINGS, &save, sizeof(save));
}

void cinco_load_state(void)
{
#if FELUCCA_FLASH
    if (!flash_ok)
        return;
#endif
    cinco_save_t save;
    int n = st_load(OBJ_SETTINGS, &save, sizeof(save));
    if (n == (int)sizeof(save) && save.magic == CINCO_SAVE_MAGIC) {
        perf.source = save.source;
        perf.variant = save.variant;
        perf.k4d = save.k4d;
        perf.tone = save.tone;
        perf.mosaic = save.mosaic;
        perf.tempo = save.tempo;
        perf.mix = save.mix;
        perf.groove = save.groove;
        song.octave = save.octave;
        song.g[G_BPM] = (int16_t)save.tempo;
        song.playing = save.groove;
        cinco_sound_set_source(perf.source);
        cinco_term_push("> Saved state restored.");
    }
}

static void persist_boot(void)
{
    cinco_perf_init();
#if FELUCCA_FLASH
    uint32_t f = irq_save();
    flash_ok = FL_FAR(fl_jedec_ram)() == 0x856014u;
    irq_restore(f);
    if (!flash_ok)
        return;
    fl_plain_window_init();
#endif
    cinco_load_state();
}

static void usb_serial_apply(void) { }

/* Track sound initialization helpers */
static void track_defaults(track_t *t)
{
    uint32_t i;
    for (i = 0; i < P_COUNT; i++)
        t->p[i] = TP[i].def;
    t->p[P_LEVEL] = 100;
}

static void track_defaults_steps(track_t *t)
{
    uint32_t i;
    for (i = 0; i < NSTEP; i++) {
        t->step[i].note[0] = 0;
        t->step[i].note[1] = 0;
        t->step[i].note[2] = 0;
        t->step[i].note[3] = 0;
        t->step[i].n = 0;
        t->step[i].flags = 0;
        t->step[i].time = 0;
    }
}

static void load_pat16(track_t *t, const uint8_t *note, const uint8_t *flags)
{
    uint32_t i;
    for (i = 0; i < 16; i++) {
        t->step[i].note[0] = note[i];
        t->step[i].n = note[i] ? 1 : 0;
        t->step[i].flags = flags[i];
    }
}

static uint32_t steps_sig(const track_t *t)
{
    (void)t;
    return 1u;
}



/* Service and storage stubs */
static void palette_apply(void)
{
    /* Cinco 2.5 palette initialization */
}

static void panel_setup(void)
{
    /* Calibration hook for OCT- + OCT+ power-on */
}

static void settings_save(void)
{
    cinco_save_state();
}
static void settings_poll(void) { }
static void settings_later(void) { }
static void autosave_boot(uint32_t clean)
{
    (void)clean;
    cinco_sound_set_source(perf.source);
}
static void autosave_poll(void) { }

/* Notification banner hook */
static void ui_message(const char *msg)
{
    uint32_t i = 0;
    while (msg && msg[i] && i < sizeof(ui.msg) - 1u) {
        ui.msg[i] = msg[i];
        i++;
    }
    ui.msg[i] = '\0';
    ui.msg_t = 60; /* display for ~60 frames */
}

#include "cinco_view.c"

/* Initial splash screen */
static void draw_splash(void)
{
    cinco_sound_init();
    cinco_groove_init();
    cinco_speech_init();
    cinco_sound_set_source(perf.source);
    cinco_speech_play(CINCO_PHRASE_BOOT);
    cinco_view_render();
}

/* Core UI frame compositor */
static void ui_draw(void)
{
    if (perf.nsfw_popup_t > 0)
        perf.nsfw_popup_t--;
    if (perf.receipt_t > 0)
        perf.receipt_t--;
    if (perf.error_popup_t > 0)
        perf.error_popup_t--;
    cinco_view_render();
}

/* Input scanner */
static void ui_input(void)
{
    /* Encoders */
    int32_t d_src = panel_enc(EN_PRESET);
    int32_t d_var = panel_enc(EN_ALGO);
    int32_t d_k1 = panel_enc(EN_K1);
    int32_t d_k2 = panel_enc(EN_K2);
    int32_t d_k3 = panel_enc(EN_K3);
    int32_t d_k4 = panel_enc(EN_K4);

    /* Buttons using fm1_input_edges(&rel) */
    uint32_t rel = 0;
    uint32_t press = fm1_input_edges(&rel);
    uint32_t note_press = fm1_input_note_edges();

    int enc_moved = (d_src != 0 || d_var != 0 || d_k1 != 0 || d_k2 != 0 || d_k3 != 0 || d_k4 != 0);
    int btn_pressed = (press != 0);
    int key_pressed = (note_press != 0 || fm1_in.notes != 0);
    int activity = (enc_moved || btn_pressed || key_pressed);

    if (activity) {
        /* If screensaver active, wake up on any activity */
        if (perf.screensaver) {
            perf.screensaver = 0;
            perf.last_activity_ms = fm1_ms;
            return;
        }

        /* If error popup active, dismiss on press */
        if (perf.error_popup_t > 0 && (btn_pressed || key_pressed)) {
            perf.error_popup_t = 0;
            perf.last_activity_ms = fm1_ms;
            return;
        }

        /* If boss mode active and not B_EDIT, wake to desktop on key or encoder turn */
        if (perf.boss_mode) {
            int is_b_edit = 0;
            for (uint32_t bi = 0; bi < 14; bi++) {
                if (panel_btn_of(bi) == B_EDIT && ((press >> bi) & 1u)) {
                    is_b_edit = 1;
                    break;
                }
            }
            if (!is_b_edit) {
                perf.boss_mode = 0;
                cinco_term_push("> Resuming work.");
                perf.last_activity_ms = fm1_ms;
                if (perf.coffee_level > 0)
                    perf.coffee_level--;
                return;
            }
        }

        perf.last_activity_ms = fm1_ms;
        if (perf.coffee_level > 0)
            perf.coffee_level--;
    } else {
        /* Idle check: 20 seconds of inactivity triggers screensaver */
        if (fm1_ms - perf.last_activity_ms > 20000u) {
            perf.screensaver = 1;
        }
        /* In idle, slowly refill coffee */
        static uint32_t last_coffee_refill_ms = 0;
        if (perf.coffee_level < 100 && (fm1_ms - last_coffee_refill_ms >= 200u)) {
            last_coffee_refill_ms = fm1_ms;
            perf.coffee_level++;
        }
    }

    if (d_src) {
        perf.view_mode = 0; /* Auto-exit Disk Defrag to show dancer */
        int32_t s = (int32_t)perf.source + d_src;
        while (s < 0) s += SRC_COUNT;
        s %= SRC_COUNT;
        if (s != (int32_t)perf.source) {
            perf.source = (uint8_t)s;
            perf.frame_idx = 0;
            cinco_sound_set_source(perf.source);
            switch (perf.source) {
            case SRC_CELERY:
                cinco_term_push("> Celery Man loaded.");
                cinco_speech_play(CINCO_PHRASE_CELERY);
                break;
            case SRC_OYSTER:
                cinco_term_push("> Oyster loaded.");
                cinco_speech_play(CINCO_PHRASE_OYSTER);
                break;
            case SRC_TAYNE:
                cinco_term_push("> Tayne loaded.");
                cinco_speech_play(CINCO_PHRASE_TAYNE);
                break;
            case SRC_TALK:
                cinco_term_push("> Voice synth ready.");
                cinco_speech_play(CINCO_PHRASE_ENTER);
                break;
            default: break;
            }
        }
    }

    if (d_var) {
        int32_t v = (int32_t)perf.variant + d_var;
        while (v < 0) v += 4;
        v %= 4;
        if (v != (int32_t)perf.variant) {
            perf.view_mode = 0; /* Auto-exit Disk Defrag */
            perf.variant = (uint8_t)v;
            switch (perf.variant) {
            case 0: cinco_term_push("> Variant: 0"); break;
            case 1: cinco_term_push("> Variant: 1"); break;
            case 2: cinco_term_push("> Variant: 2"); break;
            default: cinco_term_push("> Variant: 3"); break;
            }
        }
    }

    if (d_k1) {
        uint8_t old_k4d = perf.k4d;
        int32_t v = (int32_t)perf.k4d + d_k1;
        if (v < 0) v = 0;
        if (v > 127) v = 127;
        perf.k4d = (uint8_t)v;
        if (old_k4d <= 32 && perf.k4d > 32) {
            cinco_term_push("> 4d3d3d3 engaged.");
            cinco_speech_play(CINCO_PHRASE_4D3D);
        }
        if (perf.k4d == 127 && old_k4d != 127) {
            perf.error_popup_t = 120;
            cinco_str_copy(perf.error_msg, "WARNING: 4d3d3d3 exceeded recommended OSHA flarh levels.", sizeof(perf.error_msg));
        }
    }

    if (d_k2) {
        if (perf.nude) {
            int32_t v = (int32_t)perf.mosaic + d_k2;
            if (v < 0) v = 0;
            if (v > 127) v = 127;
            perf.mosaic = (uint8_t)v;
        } else {
            int32_t v = (int32_t)perf.tone + d_k2;
            if (v < 0) v = 0;
            if (v > 127) v = 127;
            perf.tone = (uint8_t)v;
        }
    }

    if (d_k3) {
        uint8_t old_tempo = perf.tempo;
        int32_t v = (int32_t)perf.tempo + d_k3;
        if (v < 80) v = 80;
        if (v > 160) v = 160;
        perf.tempo = (uint8_t)v;
        song.g[G_BPM] = (int16_t)v;
        if (perf.tempo != old_tempo) {
            char tmsg[32];
            snprintf(tmsg, sizeof(tmsg), "> Tempo: %u BPM.", (unsigned)perf.tempo);
            cinco_term_push(tmsg);
        }
        if (perf.tempo >= 145 && old_tempo < 145) {
            perf.error_popup_t = 120;
            cinco_str_copy(perf.error_msg, "FATAL: Oyster too wide for current clock speed.", sizeof(perf.error_msg));
        }
    }

    if (d_k4) {
        int32_t v = (int32_t)perf.mix + d_k4;
        if (v < 0) v = 0;
        if (v > 127) v = 127;
        perf.mix = (uint8_t)v;
    }

    /* Buttons using fm1_input_edges(&rel) */
    uint32_t i;
    for (i = 0; i < 14; i++) {
        uint32_t btn = panel_btn_of(i);
        if (btn >= NB)
            continue;

        int p = (press >> i) & 1;
        (void)rel;

        if (btn == B_FX) {
            if (p) {
                perf.view_mode = 0; /* Auto-exit Disk Defrag to show dancer */
                perf.nude = !perf.nude;
                if (perf.nude) {
                    perf.nsfw_popup_t = 60;
                    cinco_term_push("> WARNING: NOT SUITABLE FOR WORK");
                    cinco_speech_play(CINCO_PHRASE_NSFW);
                } else {
                    cinco_term_push("> Routine restored.");
                }
            }
        } else if (btn == B_LFO) {
            if (p) {
                perf.view_mode = 0; /* Auto-exit Disk Defrag to show dancer */
                perf.wobble = !perf.wobble;
                if (perf.wobble) {
                    perf.flail = 0;
                    cinco_speech_play(CINCO_PHRASE_WOBBLE);
                    cinco_term_push("> Hat wobble active.");
                } else {
                    cinco_term_push("> Hat wobble off.");
                }
            }
        } else if (btn == B_ARP) {
            if (p) {
                perf.view_mode = 0; /* Auto-exit Disk Defrag to show dancer */
                perf.flail = !perf.flail;
                if (perf.flail) {
                    perf.wobble = 0;
                    cinco_speech_play(CINCO_PHRASE_FLARH);
                    cinco_term_push("> Flarhgunnstow active.");
                } else {
                    cinco_term_push("> Flarhgunnstow off.");
                }
            }
        } else if (btn == B_PLAY) {
            if (p) {
                perf.groove = !perf.groove;
                song.playing = perf.groove;
                if (perf.groove) {
                    char msg[32] = "> Groove running ";
                    uint32_t b = perf.tempo;
                    int idx = 17;
                    msg[idx++] = (char)('0' + (b / 100u));
                    msg[idx++] = (char)('0' + ((b / 10u) % 10u));
                    msg[idx++] = (char)('0' + (b % 10u));
                    msg[idx++] = ' ';
                    msg[idx++] = 'B';
                    msg[idx++] = 'P';
                    msg[idx++] = 'M';
                    msg[idx++] = '.';
                    msg[idx++] = '\0';
                    cinco_term_push(msg);
                } else {
                    cinco_term_push("> Groove stopped.");
                }
            }
        } else if (btn == B_HOME) {
            if (p) {
                perf.view_mode = 0; /* Auto-exit Disk Defrag */
                perf.wobble = 0;
                perf.flail = 0;
                perf.nude = 0;
                perf.k4d = 0;
                perf.diag = 0;
                perf.source = 0;
                cinco_sound_set_source(SRC_CELERY);
                cinco_term_push("> System reset.");
                cinco_speech_play(CINCO_PHRASE_YES);
            }
        } else if (btn == B_SAVE) {
            if (p) {
                perf.view_mode = 0; /* Auto-exit Disk Defrag to show receipt */
                perf.receipt_t = 80;
                perf.nsfw_popup_t = 0;
                cinco_save_state();
                cinco_speech_play(CINCO_PHRASE_PRINTOUT);
                cinco_term_push("> Printout generated.");
            }
        } else if (btn == B_OCTDN) {
            if (p) {
                if (song.octave > -3)
                    song.octave--;
                char msg[32] = "> Key Octave: ";
                int idx = 14;
                if (song.octave < 0) {
                    msg[idx++] = '-';
                    msg[idx++] = (char)('0' - song.octave);
                } else {
                    msg[idx++] = (char)('0' + song.octave);
                }
                msg[idx] = '\0';
                cinco_term_push(msg);
            }
        } else if (btn == B_OCTUP) {
            if (p) {
                if (song.octave < 3)
                    song.octave++;
                char msg[32] = "> Key Octave: ";
                int idx = 14;
                if (song.octave < 0) {
                    msg[idx++] = '-';
                    msg[idx++] = (char)('0' - song.octave);
                } else {
                    msg[idx++] = (char)('0' + song.octave);
                }
                msg[idx] = '\0';
                cinco_term_push(msg);
            }
        } else if (btn == B_SCL) {
            if (p) {
                perf.scale_mode = (uint8_t)((perf.scale_mode + 1u) % 5u);
                cinco_sound_apply_scale(perf.scale_mode);
                switch (perf.scale_mode) {
                case 0: cinco_term_push("> Scale: Chromatic"); break;
                case 1: cinco_term_push("> Scale: Natural Minor"); break;
                case 2: cinco_term_push("> Scale: Major"); break;
                case 3: cinco_term_push("> Scale: Minor Pentatonic"); break;
                default: cinco_term_push("> Scale: Blues"); break;
                }
            }
        } else if (btn == B_ENV) {
            if (p) {
                perf.env_mode = (uint8_t)((perf.env_mode + 1u) % 4u);
                cinco_sound_apply_env(perf.env_mode);
                switch (perf.env_mode) {
                case 0: cinco_term_push("> Env: Snappy Brass"); break;
                case 1: cinco_term_push("> Env: Sustained Pad"); break;
                case 2: cinco_term_push("> Env: Staccato Pluck"); break;
                default: cinco_term_push("> Env: Punch Bass"); break;
                }
            }
        } else if (btn == B_EDIT) {
            if (p) {
                perf.boss_mode = !perf.boss_mode;
                if (perf.boss_mode) {
                    cinco_term_push("> Boss mode active.");
                } else {
                    cinco_term_push("> Resuming work.");
                }
            }
        } else if (btn == B_GLO) {
            if (p) {
                static uint8_t glo_idx = 0;
                static const uint8_t GLO_PHRASES[3] = {CINCO_PHRASE_BETA, CINCO_PHRASE_ENTER, CINCO_PHRASE_YES};
                cinco_speech_play(GLO_PHRASES[glo_idx]);
                glo_idx = (uint8_t)((glo_idx + 1u) % 3u);
                cinco_term_push("> Voice: Speech quote.");
                perf.error_popup_t = 120;
                cinco_str_copy(perf.error_msg, "CINCO ALERT: Celery stalk detected in floppy drive.", sizeof(perf.error_msg));
            }
        } else if (btn == B_SEQ) {
            if (p) {
                perf.view_mode = !perf.view_mode;
                if (perf.view_mode) {
                    cinco_term_push("> View: Disk Defrag");
                } else {
                    cinco_term_push("> View: Dancers");
                }
            }
        } else if (btn == B_REC) {
            if (p) {
                perf.rec = !perf.rec;
                if (perf.rec) {
                    cinco_term_push("> Recording: Armed [REC]");
                } else {
                    cinco_term_push("> Recording: Standby");
                }
            }
        }
    }
}

/* LED drivers */
static void ui_leds(void)
{
    /* Map performance state to LEDs:
     * LED 0 (Play): light if perf.groove
     * LED 1 (LFO): light if perf.wobble
     * LED 2 (Arp): light if perf.flail
     * LED 3 (FX): light if perf.nude */
    fm1_led[0] = perf.groove ? 1u : 0u;
    fm1_led[1] = perf.wobble ? 1u : 0u;
    fm1_led[2] = perf.flail  ? 1u : 0u;
    fm1_led[3] = perf.nude   ? 1u : 0u;
}

#endif /* CINCO_UI_C */
