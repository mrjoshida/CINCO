#!/usr/bin/env python3
"""
tools/cinco/gen_speech.py
Generates compressed speech assets for Celery Man firmware using macOS 'say' (Fred voice)
and standard 4-bit IMA ADPCM (DVI ADPCM) compression.

Outputs:
- WAV caches in assets/speech/
- C header firmware/src/cinco_speech_data.h
"""

import argparse
import math
import os
import shutil
import struct
import subprocess
import sys
import wave

# Standard IMA / DVI ADPCM index and step-size tables
INDEX_TABLE = [
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8
]

STEP_SIZE_TABLE = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
]

# Phrase definitions: (ID, spoken text, is_vowel_loop)
PHRASES = [
    ("BOOT", "Good morning, Paul.", False),
    ("CELERY", "Celery Man.", False),
    ("OYSTER", "Oyster.", False),
    ("TAYNE", "Tayne.", False),
    ("4D3D", "4d3d3d3 engaged.", False),
    ("WOBBLE", "Hat wobble.", False),
    ("FLARH", "Flarhgunnstow.", False),
    ("NSFW", "Warning: this is not suitable for work.", False),
    ("PRINTOUT", "Printout generated.", False),
    ("YES", "Yes, Paul.", False),
    ("BETA", "I have a beta sequence.", False),
    ("ENTER", "Can I entertayne you?", False),
    ("VOWEL_AA", "Aaah.", True),
    ("VOWEL_EE", "Eee.", True),
    ("VOWEL_OH", "Oooh.", True),
]

def ima_adpcm_decode_nibble(nibble: int, valpred: int, index: int):
    """Decodes a single 4-bit ADPCM nibble."""
    step = STEP_SIZE_TABLE[index]
    vpdiff = step >> 3
    if nibble & 4:
        vpdiff += step
    if nibble & 2:
        vpdiff += (step >> 1)
    if nibble & 1:
        vpdiff += (step >> 2)

    if nibble & 8:
        valpred -= vpdiff
    else:
        valpred += vpdiff

    valpred = max(-32768, min(32767, valpred))
    index = max(0, min(88, index + INDEX_TABLE[nibble]))
    return valpred, index

def ima_adpcm_encode(samples):
    """
    Encodes 16-bit linear PCM samples into 4-bit IMA ADPCM bytes.
    Storage format: 2 samples per byte.
    Lower nibble (bits 0-3) = sample 2*i
    Upper nibble (bits 4-7) = sample 2*i + 1
    """
    valpred = 0
    index = 0
    encoded_bytes = bytearray()
    decoded_sim = []

    padded_samples = list(samples)
    if len(padded_samples) % 2 != 0:
        padded_samples.append(padded_samples[-1])

    for i in range(0, len(padded_samples), 2):
        s0 = padded_samples[i]
        s1 = padded_samples[i + 1]

        # Nibble 0
        step = STEP_SIZE_TABLE[index]
        diff = s0 - valpred
        nibble0 = 0
        if diff < 0:
            nibble0 = 8
            diff = -diff
        if diff >= step:
            nibble0 |= 4
            diff -= step
        if diff >= (step >> 1):
            nibble0 |= 2
            diff -= (step >> 1)
        if diff >= (step >> 2):
            nibble0 |= 1
        valpred, index = ima_adpcm_decode_nibble(nibble0, valpred, index)
        decoded_sim.append(valpred)

        # Nibble 1
        step = STEP_SIZE_TABLE[index]
        diff = s1 - valpred
        nibble1 = 0
        if diff < 0:
            nibble1 = 8
            diff = -diff
        if diff >= step:
            nibble1 |= 4
            diff -= step
        if diff >= (step >> 1):
            nibble1 |= 2
            diff -= (step >> 1)
        if diff >= (step >> 2):
            nibble1 |= 1
        valpred, index = ima_adpcm_decode_nibble(nibble1, valpred, index)
        decoded_sim.append(valpred)

        encoded_bytes.append((nibble1 << 4) | (nibble0 & 0x0F))

    return encoded_bytes, decoded_sim[:len(samples)]

def ima_adpcm_decode(encoded_bytes: bytearray, num_samples: int):
    """Decodes packed 4-bit IMA ADPCM byte stream into 16-bit linear PCM samples."""
    valpred = 0
    index = 0
    decoded = []
    for b in encoded_bytes:
        n0 = b & 0x0F
        valpred, index = ima_adpcm_decode_nibble(n0, valpred, index)
        decoded.append(valpred)
        if len(decoded) == num_samples:
            break

        n1 = (b >> 4) & 0x0F
        valpred, index = ima_adpcm_decode_nibble(n1, valpred, index)
        decoded.append(valpred)
        if len(decoded) == num_samples:
            break
    return decoded

def compute_snr(orig, dec):
    """Computes signal-to-noise ratio in decibels (dB)."""
    signal_pwr = sum(s * s for s in orig)
    noise_pwr = sum((s - d) ** 2 for s, d in zip(orig, dec))
    if noise_pwr == 0:
        return 999.0
    if signal_pwr == 0:
        return 0.0
    return 10.0 * math.log10(signal_pwr / noise_pwr)

def find_vowel_loop(samples, sample_rate=8000, target_duration=0.10):
    """
    Finds seamless, byte-aligned loop points in sustained vowel samples.
    Returns (loop_start, loop_len) where both are even numbers.
    """
    n = len(samples)
    s_min = int(n * 0.30)
    s_max = int(n * 0.75)

    # Estimate fundamental pitch period via autocorrelation
    center = (s_min + s_max) // 2
    sub = samples[center : center + 500]
    best_corr = -1.0
    pitch_period = 65
    for lag in range(40, 100):
        corr = sum(sub[i] * sub[i + lag] for i in range(250))
        norm = math.sqrt(sum(sub[i]**2 for i in range(250)) * sum(sub[i+lag]**2 for i in range(250)))
        coeff = corr / (norm + 1e-9)
        if coeff > best_corr:
            best_corr = coeff
            pitch_period = lag

    target_k = max(2, round(target_duration * sample_rate / pitch_period))

    # Detect positive zero crossings
    zcs = []
    for i in range(s_min, s_max):
        if samples[i-1] <= 0 and samples[i] > 0:
            zcs.append(i)

    best_score = float('inf')
    best_loop = (0, 0)

    for i, z1 in enumerate(zcs):
        s1 = z1 if z1 % 2 == 0 else z1 + 1
        for z2 in zcs[i+1:]:
            length = z2 - s1
            if length % 2 != 0:
                length += 1
            if s1 + length >= len(samples):
                break

            k = length / pitch_period
            if k < 2 or k > target_k + 4:
                continue

            jump = abs(samples[s1 + length - 1] - samples[s1])
            slope1 = samples[s1 + 1] - samples[s1]
            slope2 = samples[s1 + length - 1] - samples[s1 + length - 2]
            slope_err = abs(slope1 - slope2)
            k_err = abs(round(k) - k) * 500
            dur_bias = abs(k - target_k) * 50

            score = jump * 10 + slope_err * 2 + k_err + dur_bias

            if score < best_score:
                best_score = score
                best_loop = (s1, length)

    return best_loop

def synthesize_or_load(phrase_id: str, text: str, cache_dir: str, force_synth: bool = False):
    """
    Synthesizes speech using macOS 'say' or loads existing cached WAV.
    Returns (samples, sample_rate).
    """
    os.makedirs(cache_dir, exist_ok=True)
    wav_path = os.path.join(cache_dir, f"{phrase_id.lower()}.wav")

    needs_synth = force_synth or not os.path.exists(wav_path)
    if needs_synth:
        if not shutil.which("say"):
            raise RuntimeError(f"macOS 'say' command not available and cached file '{wav_path}' does not exist.")

        cmd = [
            "say",
            "-v", "Fred",
            "--data-format=LEI16@8000",
            "-o", wav_path,
            text
        ]
        subprocess.run(cmd, check=True)

    with wave.open(wav_path, "rb") as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)

    if nchannels != 1 or sampwidth != 2 or framerate != 8000:
        raise ValueError(f"Unexpected audio format in {wav_path}: {nchannels}ch, {sampwidth*8}bit, {framerate}Hz")

    samples = list(struct.unpack(f"<{nframes}h", raw))
    return samples, framerate

def generate_header(results, output_path: str):
    """Generates the C header file firmware/src/cinco_speech_data.h."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    lines = [
        "/* SPDX-License-Identifier: GPL-3.0-only",
        " * Copyright (C) 2026 Cinco Identity Generator 2.5 / Celery Man Firmware */",
        "/* Generated by tools/cinco/gen_speech.py - DO NOT EDIT MANUALLY */",
        "/* Compressed 4-bit IMA ADPCM Speech Assets (8000 Hz mono, 2 samples per byte) */",
        "",
        "#ifndef CINCO_SPEECH_DATA_H",
        "#define CINCO_SPEECH_DATA_H",
        "",
        "#include <stdint.h>",
        "",
        "/* Phrase Identifiers */",
        "typedef enum {"
    ]

    for p in results:
        lines.append(f"    CINCO_PHRASE_{p['id']} = {p['index']},")
    lines.append("    CINCO_PHRASE_COUNT")
    lines.append("} cinco_phrase_id_t;")
    lines.append("")

    lines.extend([
        "/* Phrase Descriptor */",
        "typedef struct {",
        "    const uint8_t *data;",
        "    uint32_t num_samples;   /* Total audio samples */",
        "    uint32_t sample_rate;   /* 8000 Hz */",
        "    uint32_t loop_start;    /* Loop start sample index (0 if one-shot) */",
        "    uint32_t loop_len;      /* Loop length in samples (0 if one-shot) */",
        "} cinco_phrase_desc_t;",
        ""
    ])

    # ADPCM byte arrays
    lines.append("/* 4-bit IMA ADPCM Data Arrays */")
    lines.append("/* Byte format: bits 0-3 = sample 2*i, bits 4-7 = sample 2*i + 1 */")
    lines.append("")

    for p in results:
        arr_name = f"cinco_phrase_{p['id'].lower()}"
        enc_bytes = p["encoded_bytes"]
        lines.append(f"/* Phrase: {p['id']} - \"{p['text']}\" ({p['num_samples']} samples, {p['duration_s']:.3f}s, SNR: {p['snr_db']:.2f} dB) */")
        lines.append(f"static const uint8_t {arr_name}[{len(enc_bytes)}] = {{")

        # 16 bytes per line
        for offset in range(0, len(enc_bytes), 16):
            chunk = enc_bytes[offset : offset + 16]
            chunk_hex = ", ".join(f"0x{b:02X}u" for b in chunk)
            lines.append(f"    {chunk_hex},")

        lines.append("};")
        lines.append("")

    # Descriptor table
    lines.extend([
        "/* Phrase Descriptor Table */",
        "static const cinco_phrase_desc_t cinco_phrases[CINCO_PHRASE_COUNT] = {"
    ])

    for p in results:
        arr_name = f"cinco_phrase_{p['id'].lower()}"
        lines.extend([
            f"    [CINCO_PHRASE_{p['id']}] = {{",
            f"        .data = {arr_name},",
            f"        .num_samples = {p['num_samples']}u,",
            f"        .sample_rate = {p['sample_rate']}u,",
            f"        .loop_start = {p['loop_start']}u,",
            f"        .loop_len = {p['loop_len']}u,",
            "    },"
        ])

    lines.extend([
        "};",
        "",
        "#endif /* CINCO_SPEECH_DATA_H */",
        ""
    ])

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Generate compressed IMA ADPCM speech assets for Celery Man.")
    parser.add_argument("--output", default="firmware/src/cinco_speech_data.h", help="Path to output C header")
    parser.add_argument("--cache-dir", default="assets/speech", help="Cache directory for synthesized WAV files")
    parser.add_argument("--force-synth", action="store_true", help="Force re-synthesis with macOS say")
    parser.add_argument("--min-snr", type=float, default=20.0, help="Minimum allowable round-trip SNR in dB")
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_path = os.path.join(project_root, args.output) if not os.path.isabs(args.output) else args.output
    cache_path = os.path.join(project_root, args.cache_dir) if not os.path.isabs(args.cache_dir) else args.cache_dir

    print("================================================================================")
    print(" CELERY MAN CINCO SPEECH ASSET GENERATOR (IMA ADPCM)")
    print("================================================================================")
    print(f"Output header:   {out_path}")
    print(f"Cache directory: {cache_path}")
    print(f"Min target SNR:  {args.min_snr} dB")
    print("--------------------------------------------------------------------------------")

    results = []
    total_samples = 0
    total_pcm_bytes = 0
    total_adpcm_bytes = 0

    for idx, (phrase_id, text, is_vowel_loop) in enumerate(PHRASES):
        samples, sr = synthesize_or_load(phrase_id, text, cache_path, force_synth=args.force_synth)
        num_samples = len(samples)
        duration_s = num_samples / sr

        # Find loop points if vowel loop
        if is_vowel_loop:
            loop_start, loop_len = find_vowel_loop(samples, sample_rate=sr)
        else:
            loop_start, loop_len = 0, 0

        # ADPCM encode
        enc_bytes, sim_dec = ima_adpcm_encode(samples)

        # ADPCM decode verification
        dec_samples = ima_adpcm_decode(enc_bytes, num_samples)
        if dec_samples != sim_dec:
            raise RuntimeError(f"Decoder simulation mismatch on phrase '{phrase_id}'")

        snr = compute_snr(samples, dec_samples)
        if snr < args.min_snr:
            raise RuntimeError(f"Phrase '{phrase_id}' SNR {snr:.2f} dB is below threshold {args.min_snr} dB")

        pcm_bytes = num_samples * 2
        adpcm_bytes = len(enc_bytes)

        total_samples += num_samples
        total_pcm_bytes += pcm_bytes
        total_adpcm_bytes += adpcm_bytes

        results.append({
            "index": idx,
            "id": phrase_id,
            "text": text,
            "samples": samples,
            "num_samples": num_samples,
            "sample_rate": sr,
            "duration_s": duration_s,
            "loop_start": loop_start,
            "loop_len": loop_len,
            "encoded_bytes": enc_bytes,
            "snr_db": snr
        })

        loop_str = f"L[{loop_start}:{loop_start+loop_len}]" if loop_len > 0 else "-"
        print(f"[{idx:2d}] {phrase_id:10s} | {duration_s:5.2f}s | {num_samples:5d} smp | {adpcm_bytes:5d} B | SNR: {snr:5.2f} dB | Loop: {loop_str:18s} | \"{text}\"")

    print("--------------------------------------------------------------------------------")
    print(f"Total phrases:    {len(results)}")
    print(f"Total samples:    {total_samples} ({total_samples / 8000.0:.2f}s of 8 kHz speech)")
    print(f"Original 16-bit:  {total_pcm_bytes} bytes ({total_pcm_bytes / 1024.0:.1f} KB)")
    print(f"Compressed ADPCM: {total_adpcm_bytes} bytes ({total_adpcm_bytes / 1024.0:.1f} KB)")
    print(f"Compression:      {total_pcm_bytes / total_adpcm_bytes:.2f}x (4 bits/sample)")
    print("--------------------------------------------------------------------------------")

    generate_header(results, out_path)
    header_size = os.path.getsize(out_path)
    print(f"Successfully generated header: {out_path} ({header_size} bytes)")
    print("================================================================================")

if __name__ == "__main__":
    main()
