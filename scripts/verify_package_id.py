#!/usr/bin/env python3
"""Verify package marker in .fwsc file against expected ID."""

import sys
from pathlib import Path

BLOCKS, BLK, KEEP = 20, 0x30, 0x2F

def verify(fwsc_path, expected_id):
    p = Path(fwsc_path)
    if not p.is_file():
        print(f"Error: file not found: {p}", file=sys.stderr)
        return False
    data = p.read_bytes()
    marker_bytes = []
    for i in range(BLOCKS):
        idx = i * BLK + KEEP
        if idx < len(data):
            marker_bytes.append(data[idx])
    
    # Marker decoding: m = (ord(ch) + i + 1) & 0xFF, if unused marker is 0x7D
    decoded_chars = []
    for i, m in enumerate(marker_bytes):
        if m == 0x7D:
            break
        # ch = (m - (i + 1)) & 0xFF
        ch = chr((m - (i + 1)) & 0xFF)
        decoded_chars.append(ch)
    decoded_id = "".join(decoded_chars)
    print(f"File: {p}")
    print(f"  Decoded identity: '{decoded_id}'")
    print(f"  Expected identity: '{expected_id}'")
    matches = (decoded_id == expected_id)
    print(f"  Matches: {matches}")
    return matches

if __name__ == "__main__":
    expected = sys.argv[1] if len(sys.argv) > 1 else "FM-1_555"
    f1 = verify("build/cinco.fwsc", expected)
    f2 = verify("build/firmware/cinco.fwsc", expected)
    if not (f1 and f2):
        sys.exit(1)
    print("ALL VERIFICATIONS PASSED")
