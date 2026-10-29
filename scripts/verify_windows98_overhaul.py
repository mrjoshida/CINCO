#!/usr/bin/env python3
"""
Comprehensive verification test suite for Windows 98 desktop overhaul.
Verifies all 9 requirements, DOM IDs, text content, taskbar integration,
and ensures zero alert() / confirm() / prompt() calls exist.
"""

import sys
import re

def test_overhaul():
    with open("web/emu/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    errors = []

    # 1. Check for absolute zero native browser dialogs
    for fn in ["alert(", "confirm(", "prompt("]:
        matches = [m.start() for m in re.finditer(re.escape(fn), html)]
        if matches:
            errors.append(f"Found {len(matches)} native '{fn}' calls in HTML!")

    # 2. Check Recycle Bin Window (#win-recycle)
    required_recycle = [
        'id="win-recycle"', 'Recycle Bin', 'id="btn-empty-recycle"',
        'tayne_beta_leaked_v1.raw', '4,210 KB',
        'paul_sandwich_order.txt', '1 KB',
        'corrupted_cluster_4d3d.dat', '64 KB',
        'oyster_receipt_unpaid.doc', '12 KB',
        'celery_unapproved_moves.avi', '8,900 KB',
        'id="recycle-status-count"', '5 object(s)',
        'id="recycle-status-size"', '13.1 MB',
        'id="modal-confirm-recycle"',
        'Are you sure you want to permanently incinerate these 5 Cinco memory assets?',
        'id="btn-confirm-recycle-yes"', 'id="btn-confirm-recycle-no"'
    ]
    for item in required_recycle:
        if item not in html:
            errors.append(f"Recycle Bin missing: {item}")

    # 3. Check Tayne Studio 98 Window (#win-tayne)
    required_tayne = [
        'id="win-tayne"', 'Tayne Studio 98 (Beta Edition)',
        'id="tayne-status-card"', 'Dancer Sequence Loaded',
        'id="btn-tayne-load"', 'Load Tayne into Terminal',
        'id="btn-tayne-wobble"', 'Hat Wobble',
        'id="btn-tayne-flarh"', 'Flarhgunnstow',
        'id="btn-tayne-nude"', 'Nude Tayne (NSFW)',
        'id="btn-tayne-receipt"', 'Print Oyster Receipt'
    ]
    for item in required_tayne:
        if item not in html:
            errors.append(f"Tayne Studio missing: {item}")

    # 4. Check Disk Defragmenter Window (#win-defrag)
    required_defrag = [
        'id="win-defrag"', 'Defragmenting Drive C:',
        'Drive C: (Cinco 4D3D3D3 Partition)',
        '■ Allocated', '■ Free', '■ 4d3d3d3 Fragmented', '■ Unmovable',
        'id="defrag-progress-text"', '42% Complete',
        'id="defrag-cluster-grid"',
        'id="btn-defrag-pause"', 'id="btn-defrag-stop"', 'id="btn-defrag-details"'
    ]
    for item in required_defrag:
        if item not in html:
            errors.append(f"Disk Defragmenter missing: {item}")

    # 5. Check Lotus 1-2-3 Window (#win-lotus)
    required_lotus = [
        'id="win-lotus"',
        'Lotus 1-2-3 (Boss Mode) — [CORPORATE_BUDGET.WK1]',
        'Q3 Cinco Business Systems Enterprise Forecast',
        'Celery Stalk Procurement', '$4,200,000', 'APPROVED',
        'Tayne Beta Research & Development', '$18,500,000', 'CONFIDENTIAL',
        'Oyster Smiling High-Resolution Printing', '$320,000', 'PENDING',
        '4d3d3d3 Macro Overclocking', '$9,800,000', 'ENGAGED',
        'TOTAL CORPORATE ALLOCATION', '$32,820,000', 'SIGNED (PAUL)',
        'READY | A1 | CALC'
    ]
    for item in required_lotus:
        if item not in html:
            errors.append(f"Lotus 1-2-3 missing: {item}")

    # 6. Check CINCO Manual Window (#win-manual)
    required_manual = [
        'id="win-manual"', 'Cinco Business Systems Help — User Reference Guide',
        'id="toc-welcome"', 'id="toc-controls"', 'id="toc-identities"',
        'id="toc-kinetics"', 'id="toc-boss"', 'id="toc-osha"',
        'id="manual-content-view"', 'id="manual-status-panel"'
    ]
    for item in required_manual:
        if item not in html:
            errors.append(f"CINCO Manual missing: {item}")

    # 7. Check Setup Wizard Launcher (#win-setup-launcher)
    required_setup = [
        'id="win-setup-launcher"', 'Cinco Setup & Hardware Flasher',
        'FM-1_555', 'id="btn-launch-installer"', 'Launch Setup Wizard ▶',
        'id="btn-cancel-installer"'
    ]
    for item in required_setup:
        if item not in html:
            errors.append(f"Setup Wizard Launcher missing: {item}")

    # 8. Check Shut Down Dialog & Screens (#modal-shutdown)
    required_shutdown = [
        'id="modal-shutdown"', 'Shut Down Windows',
        'id="shutdown-opt-off"', 'Shut down the computer',
        'id="shutdown-opt-restart"', 'Restart the computer',
        'id="shutdown-opt-dos"', 'Restart the computer in',
        'id="btn-shutdown-ok"', 'id="btn-shutdown-cancel"', 'id="btn-shutdown-help"',
        'id="screen-shutdown"', "It's now safe to turn off", "your computer.",
        'id="btn-turn-on"',
        'id="screen-dos"', 'Cinco Business Systems(R) MS-DOS 7.10',
        'id="btn-dos-exit"', 'id="dos-input"'
    ]
    for item in required_shutdown:
        if item not in html:
            errors.append(f"Shut Down Dialog missing: {item}")

    # 9. Check Coffee Dialog (#modal-coffee)
    required_coffee = [
        'id="modal-coffee"', 'Cinco Executive Coffee Service',
        'Managing Director Paul has taken a 15-minute executive espresso recess. OSHA vigilance level restored to 100%.',
        'id="btn-coffee-ok"'
    ]
    for item in required_coffee:
        if item not in html:
            errors.append(f"Coffee Dialog missing: {item}")

    # 10. Check Taskbar Pills
    required_pills = [
        'id="task-pill-main"',
        'id="task-pill-recycle"',
        'id="task-pill-tayne"',
        'id="task-pill-defrag"',
        'id="task-pill-lotus"',
        'id="task-pill-manual"',
        'id="task-pill-setup"'
    ]
    for item in required_pills:
        if item not in html:
            errors.append(f"Taskbar pill missing: {item}")

    # 11. Check Desktop Icons
    required_desktop = [
        'id="d-mycomp"', 'id="d-app"', 'id="d-tayne"', 'id="d-defrag"',
        'id="d-boss"', 'id="d-installer"', 'id="d-manual"', 'id="d-recycle"'
    ]
    for item in required_desktop:
        if item not in html:
            errors.append(f"Desktop icon missing: {item}")

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"  ❌ {e}")
        sys.exit(1)
    else:
        print("All 9 Application Windows and Windows 98 Dialogs VERIFIED successfully!")
        print("ZERO native alert() / confirm() / prompt() calls confirmed.")

if __name__ == "__main__":
    test_overhaul()
