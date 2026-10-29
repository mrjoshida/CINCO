#!/usr/bin/env python3
import re
import sys

def check_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Check essential DOM IDs required by worklet/audio/UI
    required_ids = [
        "screen", "go", "start", "main-win", "status-main", "status-tempo",
        "status-identity", "systray-clock", "start-btn", "start-menu",
        "about-modal", "sysprop-modal", "volume-popup", "master-vol-slider",
        "sl-macro", "sl-bpm", "sl-tone", "sl-mix",
        "rad-celery", "rad-oyster", "rad-tayne",
        "btn-k4d", "btn-wobble", "btn-flail", "btn-nude", "btn-receipt",
        "btn-degauss", "btn-fullscreen", "btn-reset-crt", "btn-snapshot",
        "btn-oct-dn", "btn-oct-up", "btn-play-stop",
        "pk-0", "pk-26" # first and last piano keys
    ]

    for rid in required_ids:
        if f'id="{rid}"' not in content:
            errors.append(f"Missing required DOM element with id='{rid}'")

    # Check piano keys (0 to 26)
    for i in range(27):
        if f'id="pk-{i}"' not in content:
            errors.append(f"Missing piano key pk-{i}")

    # Check JS module syntax
    m = re.search(r"<script type=\"module\">(.*?)</script>", content, re.DOTALL)
    if not m:
        errors.append("Missing <script type='module'> block")
    else:
        js = m.group(1)
        # Check for matching braces roughly
        open_braces = js.count("{")
        close_braces = js.count("}")
        if open_braces != close_braces:
            errors.append(f"JS curly braces mismatch: {open_braces} open vs {close_braces} close")

    if errors:
        print(f"Validation FAILED with {len(errors)} errors:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("HTML and JavaScript structure verification PASSED! All 27 keys and required elements present.")

if __name__ == "__main__":
    check_html("web/emu/index.html")
