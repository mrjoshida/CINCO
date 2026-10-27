#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    print("=== Cinco Identity Generator 2.5: Matrix Verification ===")
    wasm_path = "build/emu/felucca.wasm"
    if not os.path.exists(wasm_path):
        print(f"Error: {wasm_path} does not exist. Please run ./web/emu/build.sh first.")
        return 1

    node_script = "scripts/verify_matrix_emu.mjs"
    if not os.path.exists(node_script):
        print(f"Error: {node_script} does not exist.")
        return 1

    print(f"Running WASM matrix tests via Node.js ({wasm_path})...\n")
    proc = subprocess.run(["node", node_script, wasm_path], capture_output=True, text=True)
    
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)

    if proc.returncode != 0:
        print(f"Matrix verification failed with exit code {proc.returncode}.")
        return proc.returncode

    print("Matrix verification completed successfully with 100% pass rate.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
