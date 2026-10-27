#!/usr/bin/env python3
import json
import os
import subprocess
import sys

def main():
    print("=" * 80)
    print("  CINCO IDENTITY GENERATOR 2.5: 24-STATE INTERSECTION MATRIX VERIFICATION")
    print("=" * 80)

    wasm_path = "build/emu/felucca.wasm"
    runner_script = "scripts/test_full_matrix_runner.mjs"

    if not os.path.exists(wasm_path):
        print(f"Error: {wasm_path} not found. Please build with web/emu/build.sh.")
        return 1

    if not os.path.exists(runner_script):
        print(f"Error: {runner_script} not found.")
        return 1

    proc = subprocess.run(["node", runner_script, wasm_path], capture_output=True, text=True)
    if proc.returncode != 0 and not proc.stdout.strip().startswith("{"):
        print("Runner execution failed with stderr:")
        print(proc.stderr)
        return 1

    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        print("Failed to parse runner JSON output:", e)
        print("STDOUT:", proc.stdout[:500])
        print("STDERR:", proc.stderr[:500])
        return 1

    matrix = data.get("matrixResults", [])
    print(f"\n--- 1. 24-STATE COMBINATORIAL MATRIX (Character x Kinetics x NSFW) ---")
    print(f"{'#':<3} | {'Character':<8} | {'Kinetics':<8} | {'Mode':<5} | {'Mosaic':<6} | {'Audio Peak':<10} | {'Screen Px':<9} | {'Title':<30} | {'Status'}")
    print("-" * 105)

    all_matrix_pass = True
    for item in matrix:
        st = "[PASS]" if item["pass"] else "[FAIL]"
        if not item["pass"]:
            all_matrix_pass = False
        print(f"{item['id']:<3} | {item['source']:<8} | {item['kinetics']:<8} | {item['nsfw']:<5} | {item['mosaic']:<6} | {item['audioPeak']:<10.4f} | {item['screenPixels']:<9} | {item['actualTitle']:<30} | {st}")

    print("-" * 105)
    print(f"Combinatorial Matrix: {sum(1 for m in matrix if m['pass'])} / {len(matrix)} states PASS.")

    # Envelope modes
    env_list = data.get("envResults", [])
    print(f"\n--- 2. ENVELOPE MODES (B_ENV: 4 Profiles) ---")
    print(f"{'Mode':<5} | {'Profile Name':<16} | {'ATK':<4} | {'DEC':<4} | {'SUS':<4} | {'REL':<4} | {'FLT':<4} | {'Status'}")
    print("-" * 65)
    all_env_pass = True
    for e in env_list:
        st = "[PASS]" if e["pass"] else "[FAIL]"
        if not e["pass"]:
            all_env_pass = False
        print(f"{e['mode']:<5} | {e['name']:<16} | {e['atk']:<4} | {e['dec']:<4} | {e['sus']:<4} | {e['rel']:<4} | {e['flt']:<4} | {st}")

    # Scale modes
    scale_list = data.get("scaleResults", [])
    print(f"\n--- 3. SCALE MODES (B_SCL: 5 Modes) ---")
    print(f"{'Mode':<5} | {'Scale Name':<18} | {'Quant':<6} | {'Scale':<6} | {'Status'}")
    print("-" * 55)
    all_scale_pass = True
    for s in scale_list:
        st = "[PASS]" if s["pass"] else "[FAIL]"
        if not s["pass"]:
            all_scale_pass = False
        print(f"{s['mode']:<5} | {s['name']:<18} | {s['quant']:<6} | {s['scale']:<6} | {st}")

    # Source persistence
    persist_list = data.get("persistResults", [])
    print(f"\n--- 4. ENVELOPE & SCALE PRESET PERSISTENCE ACROSS SOURCES ---")
    print(f"{'Character':<12} | {'Active Env Mode':<16} | {'Active Scale Mode':<18} | {'Status'}")
    print("-" * 65)
    all_persist_pass = True
    for p in persist_list:
        st = "[PASS]" if p["pass"] else "[FAIL]"
        if not p["pass"]:
            all_persist_pass = False
        print(f"{p['source']:<12} | Mode {p['curEnv']} (Pad)       | Mode {p['curScale']} (Blues)        | {st}")

    print("\n" + "=" * 80)
    total_tests = len(matrix) + len(env_list) + len(scale_list) + len(persist_list)
    passed_tests = (
        sum(1 for m in matrix if m["pass"]) +
        sum(1 for e in env_list if e["pass"]) +
        sum(1 for s in scale_list if s["pass"]) +
        sum(1 for p in persist_list if p["pass"])
    )

    if data.get("allPassed"):
        print(f"  ALL {total_tests} EXHAUSTIVE INTEGRATION TESTS PASSED (100.0% SUCCESS)")
        print("=" * 80)
        return 0
    else:
        print(f"  VERIFICATION FAILED: {passed_tests} / {total_tests} passed.")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
