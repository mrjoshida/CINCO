#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Verification test suite for unified Windows 98 OS between emulator and installer
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def verify_file(rel_path, is_installer=False):
    path = REPO_ROOT / rel_path
    if not path.is_file():
        return [f"File missing: {rel_path}"]
    
    html = path.read_text(encoding="utf-8")
    errors = []

    # 1. Zero alert(), confirm(), prompt() calls
    for fn in ["alert(", "confirm(", "prompt("]:
        matches = [m.start() for m in re.finditer(re.escape(fn), html)]
        if matches:
            errors.append(f"{rel_path}: Found {len(matches)} native '{fn}' calls in HTML!")

    # 2. Desktop shortcuts exact list and order
    expected_icons = [
        ("d-mycomp", "My Computer"),
        ("d-app", "Cinco Synth"),
        ("d-tayne", "Tayne Studio 98"),
        ("d-defrag", "Cinco Defrag"),
        ("d-boss", "Lotus 1-2-3"),
        ("d-installer", "Setup Wizard"),
        ("d-manual", "CINCO Manual"),
        ("d-recycle", "Recycle Bin")
    ]
    for icon_id, label in expected_icons:
        if f'id="{icon_id}"' not in html:
            errors.append(f"{rel_path}: Desktop icon id='{icon_id}' missing!")
        if label not in html:
            errors.append(f"{rel_path}: Desktop icon label '{label}' missing!")

    # Old conflicting icons must NOT exist
    for bad in ["WebMIDI Network Neighborhood", "Download Firmware Package", "Paul's PC"]:
        if bad in html:
            errors.append(f"{rel_path}: Obsolete desktop icon text found: '{bad}'")

    # 3. In-universe Windows and dialogs
    windows_checks = [
        ("Recycle Bin", [
            'id="win-recycle"', 'tayne_beta_leaked_v1.raw', 'paul_sandwich_order.txt',
            'corrupted_cluster_4d3d.dat', 'oyster_receipt_unpaid.doc', 'celery_unapproved_moves.avi',
            'id="btn-empty-recycle"', 'id="modal-confirm-recycle"',
            'permanently incinerate these 5 Cinco memory assets'
        ]),
        ("Tayne Studio 98", [
            'id="win-tayne"', 'Tayne Studio 98 (Beta Edition)', 'id="tayne-status-card"',
            'id="btn-tayne-load"', 'id="btn-tayne-wobble"', 'id="btn-tayne-flarh"',
            'id="btn-tayne-nude"', 'id="btn-tayne-receipt"'
        ]),
        ("Cinco Defrag", [
            'id="win-defrag"', 'Defragmenting Drive C:', 'id="defrag-cluster-grid"',
            '■ Allocated', '■ Free', '■ 4d3d3d3 Fragmented', '■ Unmovable'
        ]),
        ("Lotus 1-2-3", [
            'id="win-lotus"', 'Lotus 1-2-3 (Boss Mode)', 'CORPORATE_BUDGET.WK1',
            'Celery Stalk Procurement', '$4,200,000', 'APPROVED',
            'Tayne Beta Research & Development', '$18,500,000', 'CONFIDENTIAL',
            'Oyster Smiling High-Resolution Printing', '$320,000', 'PENDING',
            '4d3d3d3 Macro Overclocking', '$9,800,000', 'ENGAGED',
            'TOTAL CORPORATE ALLOCATION', '$32,820,000', 'SIGNED (PAUL)'
        ]),
        ("System Properties", [
            'id="sysprop-modal"', 'Cinco Business Systems OS 2.5', 'Celery Man Workstation Edition', 'Paul (Managing Director)'
        ]),
        ("CINCO Manual", [
            'id="win-manual"', 'id="toc-welcome"', 'id="toc-controls"', 'id="toc-identities"',
            'id="toc-kinetics"', 'id="toc-boss"', 'id="toc-osha"', 'id="manual-content-view"'
        ]),
        ("Shut Down & Screens", [
            'id="modal-shutdown"', 'id="shutdown-opt-off"', 'id="shutdown-opt-restart"', 'id="shutdown-opt-dos"',
            'id="screen-shutdown"', "It's now safe to turn off", 'id="screen-dos"', 'Cinco Business Systems(R) MS-DOS 7.10'
        ]),
        ("Volume Popup & Systray", [
            'id="volume-popup"', 'id="systray-vol"', 'id="master-vol-slider"'
        ])
    ]
    for win_name, tokens in windows_checks:
        for t in tokens:
            if t not in html:
                errors.append(f"{rel_path}: [{win_name}] missing required token: '{t}'")

    # 4. Taskbar & Start Menu
    taskbar_tokens = [
        'class="win-taskbar"', 'id="start-btn"', 'id="start-menu"',
        'class="start-sidebar">CINCO OS 2.5<'
    ]
    for tok in taskbar_tokens:
        if tok not in html:
            errors.append(f"{rel_path}: Taskbar/Start menu missing token: '{tok}'")

    # 5. Typography and antialiasing
    type_tokens = [
        "-webkit-font-smoothing: subpixel-antialiased;",
        "-moz-osx-font-smoothing: auto;",
        "text-rendering: optimizeLegibility;",
        'Tahoma, "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif'
    ]
    for tok in type_tokens:
        if tok not in html:
            errors.append(f"{rel_path}: Typography token missing: '{tok}'")

    # 6. Specific Installer checks
    if is_installer:
        installer_tokens = [
            'id="modal-exit-setup"',
            'id="modal-confirm-stock"',
            'id="task-pill-main"',
            'Cinco Identity Generator 2.5 Setup Wizard',
            'progress#bar',
            'id="status"',
            'id="log"'
        ]
        for tok in installer_tokens:
            if tok not in html:
                errors.append(f"{rel_path}: Installer-specific token missing: '{tok}'")

    return errors

def main():
    print("==================================================")
    print(" VERIFYING UNIFIED CINCO OS 2.5 ENVIRONMENT       ")
    print("==================================================")
    all_errors = []

    print("\n1. Verifying Workstation Emulator (web/emu/index.html)...")
    emu_errs = verify_file("web/emu/index.html", is_installer=False)
    if emu_errs:
        for e in emu_errs:
            print(f"  ❌ {e}")
        all_errors.extend(emu_errs)
    else:
        print("  ✓ Emulator verified successfully!")

    print("\n2. Verifying Web Installer (web/cinco_installer.html)...")
    inst_errs = verify_file("web/cinco_installer.html", is_installer=True)
    if inst_errs:
        for e in inst_errs:
            print(f"  ❌ {e}")
        all_errors.extend(inst_errs)
    else:
        print("  ✓ Web Installer verified successfully!")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} error(s).")
        sys.exit(1)
    else:
        print("\nSUCCESS: All files verified! 100% Unified Windows 98 OS environment.")
        print("ZERO native alert() / confirm() / prompt() calls in either page.")

if __name__ == "__main__":
    main()
