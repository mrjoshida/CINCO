#!/usr/bin/env python3
"""
CINCO IDENTITY GENERATOR 2.5: DISK DEFRAGMENTER VIEW TOGGLE VERIFICATION

Verifies that:
1. Pressing B_SEQ toggles perf.view_mode between 0 (Dancers) and 1 (Disk Defrag).
2. When perf.view_mode == 1 (Disk Defrag):
   - Pressing B_FX sets perf.view_mode = 0.
   - Pressing B_LFO sets perf.view_mode = 0.
   - Pressing B_ARP sets perf.view_mode = 0.
   - Pressing B_HOME sets perf.view_mode = 0.
   - Pressing B_SAVE sets perf.view_mode = 0.
   - Turning the character preset encoder (EN_PRESET CW or CCW) sets perf.view_mode = 0.
"""

import json
import os
import subprocess
import sys
import unittest

WASM_PATH = "build/emu/felucca.wasm"
RUNNER_SCRIPT = "scripts/test_defrag_toggle_runner.mjs"

def run_defrag_suite():
    if not os.path.exists(WASM_PATH):
        raise FileNotFoundError(f"{WASM_PATH} not found. Please build with web/emu/build.sh.")
    if not os.path.exists(RUNNER_SCRIPT):
        raise FileNotFoundError(f"{RUNNER_SCRIPT} not found.")

    proc = subprocess.run(
        ["node", RUNNER_SCRIPT, WASM_PATH],
        capture_output=True,
        text=True
    )
    if proc.returncode != 0 and not proc.stdout.strip().startswith("{"):
        raise RuntimeError(f"Runner failed (exit code {proc.returncode}):\n{proc.stderr}")

    return json.loads(proc.stdout)


class TestDefragToggle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = run_defrag_suite()
        cls.results = {r["name"]: r for r in cls.data.get("results", [])}

    def test_b_seq_toggle(self):
        res = self.results.get("B_SEQ Toggle")
        self.assertIsNotNone(res, "B_SEQ Toggle result not found")
        self.assertEqual(res.get("initialView"), 0, "Initial view should be 0 (Dancers)")
        self.assertEqual(res.get("activeView"), 1, "View after B_SEQ should be 1 (Disk Defrag)")
        self.assertEqual(res.get("finalView"), 0, "View after second B_SEQ should be 0 (Dancers)")
        self.assertEqual(res.get("titleOn"), "Disk Defragmenter - C:")
        self.assertTrue(res.get("pass"))

    def test_b_fx_exit_defrag(self):
        res = self.results.get("B_FX Exit")
        self.assertIsNotNone(res, "B_FX Exit result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_b_lfo_exit_defrag(self):
        res = self.results.get("B_LFO Exit")
        self.assertIsNotNone(res, "B_LFO Exit result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_b_arp_exit_defrag(self):
        res = self.results.get("B_ARP Exit")
        self.assertIsNotNone(res, "B_ARP Exit result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_b_home_exit_defrag(self):
        res = self.results.get("B_HOME Exit")
        self.assertIsNotNone(res, "B_HOME Exit result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_b_save_exit_defrag(self):
        res = self.results.get("B_SAVE Exit")
        self.assertIsNotNone(res, "B_SAVE Exit result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_preset_enc_cw_exit_defrag(self):
        res = self.results.get("Preset Enc CW")
        self.assertIsNotNone(res, "Preset Enc CW result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))

    def test_preset_enc_ccw_exit_defrag(self):
        res = self.results.get("Preset Enc CCW")
        self.assertIsNotNone(res, "Preset Enc CCW result not found")
        self.assertEqual(res.get("viewBefore"), 1)
        self.assertEqual(res.get("viewAfter"), 0)
        self.assertTrue(res.get("pass"))


def main():
    print("=" * 80)
    print("  CINCO IDENTITY GENERATOR 2.5: DISK DEFRAG TOGGLE VERIFICATION")
    print("=" * 80)

    try:
        data = run_defrag_suite()
    except Exception as e:
        print(f"Error running defrag suite: {e}")
        return 1

    results = data.get("results", [])
    print(f"\n{'Test Case':<18} | {'Trigger Action':<35} | {'Before':<6} | {'After':<6} | {'Status'}")
    print("-" * 80)

    all_pass = True
    for r in results:
        st = "[PASS]" if r.get("pass") else "[FAIL]"
        if not r.get("pass"):
            all_pass = False
        v_before = str(r.get("viewBefore", r.get("initialView", "-")))
        v_after = str(r.get("viewAfter", r.get("finalView", "-")))
        print(f"{r['name']:<18} | {r['action']:<35} | {v_before:<6} | {v_after:<6} | {st}")

    print("-" * 80)
    print(f"Defrag Toggle Suite: {sum(1 for r in results if r.get('pass'))} / {len(results)} tests passed.")
    print("=" * 80)

    # Also run unittest runner for standard test assertion reporting
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDefragToggle)
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)

    return 0 if (all_pass and test_result.wasSuccessful()) else 1


if __name__ == "__main__":
    sys.exit(main())
