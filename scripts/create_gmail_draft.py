#!/usr/bin/env python3
"""
Generate and open a Gmail compose window for submitting Cinco Identity Generator 2.5
to Sven Trogus at The Firmware Hub.

Opening the compose window in the user's default browser on macOS automatically
creates and saves a draft in Gmail.
"""

import subprocess
import sys
import urllib.parse

RECIPIENT = "zven@thefirmwarehub.com"
SUBJECT = "The Firmware Hub: Cinco Identity Generator 2.5"

BODY = """Hi Sven,

Dropping the corporate in-universe shtick to send over a genuine firmware submission for the M-VAVE FM-1!

The project is Cinco Identity Generator 2.5, based on the computer interface from the classic Tim and Eric "Celery Man" sketch (Paul Rudd ordering up Celery Man, Tayne, Oyster, 4d3d3d3, Hat Wobble, and Nude Tayne). While the theme is comedic, the firmware itself is a full, serious, and deeply engineered playable instrument.

Here are the submission details formatted per The Firmware Hub requirements:

Name of the firmware: Cinco Identity Generator 2.5
Your name (as it should appear): Josh Caldwell
Repository: https://github.com/mrjoshida/CINCO
Identity (FM-1_...): FM-1_555
Licence: GPL-3.0-only
What it does (two or three sentences): An interactive synthesizer terminal for the M-VAVE FM-1 based on the classic Tim & Eric "Celery Man" sketch. Combines a custom fixed-point FM/DSP audio engine and 27-key capacitive touch input with rotoscoped pixel art dancers (Celery Man, Oyster, Tayne) on the 240x240 LCD, LPC speech synthesis, a 4d3d3d3 cascading macro encoder, Nude Tayne audio bitcrush and mosaic censorship, and a Lotus 1-2-3 boss key screensaver.
Picture (link or attached): https://raw.githubusercontent.com/mrjoshida/CINCO/main/docs/cinco/mock/01_idle_celery.png
Play in the browser / editor / video (optional): https://mrjoshida.github.io/CINCO/
Tested on a real FM-1, leaving it again works: yes

Technical notes:
- Tested on physical FM-1 hardware: boots cleanly from stock V15, contains the required Felucca update loader, and verified rescue boot path back to V15 and other firmwares.
- Identity FM-1_555 was audited against catalog.json and confirmed 100% free with zero regex or range conflicts.
- All real-time audio DSP is strictly fixed-point arithmetic (Q15, Q12, Q24) in render loops with zero floating-point math in the audio interrupt path.
- The web companion at https://mrjoshida.github.io/CINCO/ includes a Windows 98 styled browser emulator and WebAssembly/Web MIDI flasher.
- The repository root includes the required fmhub.json.

Thanks for building and maintaining The Firmware Hub!

Best regards,
Josh Caldwell
"""


def generate_compose_url(recipient: str, subject: str, body: str) -> str:
    params = {
        "view": "cm",
        "fs": "1",
        "to": recipient,
        "su": subject,
        "body": body,
    }
    return f"https://mail.google.com/mail/?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"


def main():
    compose_url = generate_compose_url(RECIPIENT, SUBJECT, BODY)
    print("=" * 70)
    print("GMAIL DRAFT GENERATOR")
    print("=" * 70)
    print(f"To: {RECIPIENT}")
    print(f"Subject: {SUBJECT}")
    print("-" * 70)
    print("Body:")
    print(BODY)
    print("=" * 70)
    print(f"Generated URL length: {len(compose_url)} chars")
    print(f"Compose URL: {compose_url[:120]}...")
    print("\nLaunching browser to open Gmail compose draft...")

    try:
        res = subprocess.run(["open", compose_url], check=True)
        if res.returncode == 0:
            print("[SUCCESS] Browser launched successfully. Gmail will auto-save the draft.")
        else:
            print(f"[ERROR] 'open' command exited with code {res.returncode}", file=sys.stderr)
            sys.exit(res.returncode)
    except Exception as e:
        print(f"[ERROR] Failed to run 'open': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
