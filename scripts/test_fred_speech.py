#!/usr/bin/env python3
import subprocess
import os
import wave
import sys

def main():
    os.makedirs("assets/speech", exist_ok=True)
    test_wav = "assets/speech/test_fred.wav"
    cmd = ["say", "-v", "Fred", "-o", test_wav, "--data-format=LEI16@8000", "Good morning Paul."]
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        return 1
    
    if os.path.exists(test_wav):
        with wave.open(test_wav, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            size = os.path.getsize(test_wav)
            print(f"Generated {test_wav}: {frames} frames, {rate} Hz, {duration:.2f}s, {size} bytes")
        return 0
    else:
        print("WAV file not created")
        return 1

if __name__ == "__main__":
    sys.exit(main())
