#!/usr/bin/env python3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

paths_to_check = [
    REPO_ROOT / "web" / "cinco_installer.html",
    REPO_ROOT / "build" / "installer" / "index.html",
    REPO_ROOT / "build" / "site" / "installer" / "index.html"
]

required_ids = [
    'id="go"',
    'id="bar"',
    'id="status"',
    'id="log"',
    'id="stock-file"',
    'id="stock-go"',
    'id="stock-recovery"',
    'id="lang"',
    'id="emu-link"',
    'id="start-btn"',
    'id="tray-clock"',
    'id="win-close"',
    'id="win-help"',
    'id="cancel-btn"'
]

required_data_t = [
    'data-t="intro"',
    'data-t="warn"',
    'data-t="install"',
    'data-t="emuLink"',
    'data-t="direct"',
    'data-t="brick"',
    'data-t="stockTitle"',
    'data-t="back"',
    'data-t="stockFile"',
    'data-t="stockGo"',
    'data-t="stockBackup"',
    'data-t="stockRecovery"',
    'data-t="license"'
]

win98_checks = [
    "#008080",
    "linear-gradient(90deg, var(--win-blue)",
    "Cinco Identity Generator 2.5 Setup Wizard",
    "M-VAVE FM-1 Synthesizer Terminal Deployment Wizard",
    "Destination Hardware Terminal",
    "4d3d3d3",
    "repeating-linear-gradient",
    "win98-taskbar",
    "win98-start-btn",
    "taskbar-tray"
]

for p in paths_to_check:
    if not p.is_file():
        print(f"FAIL: Missing file {p}")
        sys.exit(1)
    content = p.read_text(encoding="utf-8")
    for req in required_ids:
        if req not in content:
            print(f"FAIL: Missing {req} in {p}")
            sys.exit(1)
    for req in required_data_t:
        if req not in content:
            print(f"FAIL: Missing {req} in {p}")
            sys.exit(1)
    for check in win98_checks:
        if check not in content:
            print(f"FAIL: Missing {check} in {p}")
            sys.exit(1)
    print(f"PASS: Verified {p.relative_to(REPO_ROOT)}")

print("ALL INSTALLER ARTIFACTS VERIFIED SUCCESSFULLY!")
