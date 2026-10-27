#!/usr/bin/env python3
import re
import sys

def test_speech_assets():
    print("=== VALIDATING ADPCM SPEECH ASSETS IN CINCO_SPEECH_DATA.H ===")
    with open("firmware/src/cinco_speech_data.h") as f:
        content = f.read()

    # Find all phrase arrays: static const uint8_t cinco_phrase_<name>[<size>] = { ... };
    arr_re = re.compile(r"static const uint8_t (cinco_phrase_\w+)\[(\d+)\]\s*=\s*\{")
    arrays = dict(arr_re.findall(content))
    print(f"Found {len(arrays)} phrase arrays.")

    # Match each [CINCO_PHRASE_<ID>] = { .data = <arr>, .num_samples = <n>, ... }
    entry_re = re.compile(
        r"\[(CINCO_PHRASE_\w+)\]\s*=\s*\{([^}]+)\}", re.MULTILINE
    )
    entries = entry_re.findall(content)
    print(f"Found {len(entries)} phrase entries in table:")

    for enum_id, body in entries:
        fields = {}
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if line.startswith("."):
                k, v = line.split("=", 1)
                fields[k.strip().lstrip(".")] = v.strip().rstrip("u;")

        arr_name = fields[".data" if ".data" in fields else "data"]
        num_samples = int(fields[".num_samples" if ".num_samples" in fields else "num_samples"])
        arr_size = int(arrays[arr_name])
        req_size = (num_samples + 1) // 2
        print(f"  {enum_id:25s} -> {arr_name:25s}: {num_samples:6d} samples, requires {req_size:5d} B, array has {arr_size:5d} B -> {'SAFE' if arr_size >= req_size else 'OVERRUN'}")
        assert arr_size >= req_size

    print("\nALL SPEECH ASSETS VERIFIED 100% BUFFER SAFE!")

if __name__ == "__main__":
    test_speech_assets()
