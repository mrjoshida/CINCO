#!/usr/bin/env python3
"""
Hardware Display SPI Budget & Profiling Test Suite

Validates that all interactive visual modes stay within:
- ST7789 240x240 IPS LCD on SPI1 clocked at 12 MHz (1.5 MB/s = 750,000 RGB565 px/s).
- 30 FPS Frame Budget: 33.3 ms max SPI time per frame (<= 25,000 pixels / frame).
- Zero full screen wipes in steady state (Full Clears == 0).
- No draw-call thrashing (Avg Calls / Frame <= 20).
"""

import json
import os
import subprocess
import sys

WASM_PATH = "build/emu/felucca.wasm"
RUNNER_SCRIPT = "scripts/test_display_budget_runner.mjs"


def run_benchmark():
    if not os.path.exists(WASM_PATH):
        print(f"Error: {WASM_PATH} not found. Run ./web/emu/build.sh first.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(RUNNER_SCRIPT):
        print(f"Error: {RUNNER_SCRIPT} not found.", file=sys.stderr)
        sys.exit(1)

    cmd = ["node", RUNNER_SCRIPT, WASM_PATH]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        print(f"Runner failed with exit code {proc.returncode}:", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        print("Failed to parse runner JSON output:", file=sys.stderr)
        print(proc.stdout, file=sys.stderr)
        sys.exit(1)

    return data


def format_table(data):
    results = data.get("results", [])

    header = (
        "+--------------------------------+-----------------+------------------+-----------------+-------------+--------+\n"
        "| Mode                           | Avg SPI Time    | Peak SPI Time    | Avg Calls/Frame | Full Clears | Status |\n"
        "+--------------------------------+-----------------+------------------+-----------------+-------------+--------+"
    )
    footer = (
        "+--------------------------------+-----------------+------------------+-----------------+-------------+--------+"
    )

    rows = []
    for r in results:
        name = r.get("name", "Unknown")[:30]
        avg_spi = f"{r.get('avg_spi_time_ms', 0.0):.2f} ms"
        peak_spi = f"{r.get('peak_spi_time_ms', 0.0):.2f} ms"
        avg_calls = f"{r.get('avg_calls_per_frame', 0.0):.1f}"
        full_clears = str(r.get("full_clears", 0))
        status = "[PASS]" if r.get("pass", False) else "[FAIL]"

        row = (
            f"| {name:<30} "
            f"| {avg_spi:>15} "
            f"| {peak_spi:>16} "
            f"| {avg_calls:>15} "
            f"| {full_clears:>11} "
            f"| {status:<6} |"
        )
        rows.append(row)

    table = "\n".join([header] + rows + [footer])
    return table


def main():
    print("=" * 106)
    print("  CINCO FIRMWARE - HARDWARE DISPLAY SPI BUDGET & PROFILING TEST SUITE")
    print("  Target: ST7789 240x240 IPS LCD @ 12 MHz SPI | Frame Budget: 33.3 ms (25,000 px/frame)")
    print("=" * 106)

    data = run_benchmark()
    table = format_table(data)
    print(table)

    all_passed = data.get("all_passed", False)
    total = data.get("total_modes", 0)
    passed_count = sum(1 for r in data.get("results", []) if r.get("pass", False))

    print(f"\nResult: {passed_count}/{total} modes passed display budget constraints.")
    if all_passed:
        print("SUCCESS: All display modes are within 30 FPS SPI transmission budget, zero tear wipes.\n")
        sys.exit(0)
    else:
        print("FAILURE: One or more display modes exceeded hardware budget or had full clears.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
