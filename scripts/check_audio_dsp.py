#!/usr/bin/env python3
import os
import subprocess
import re

tc_dir = os.path.expanduser("~/.jieli/toolchain")

def run_in_docker(args):
    cmd = [
        "docker", "run", "--rm", "--platform", "linux/amd64",
        "-v", f"{os.getcwd()}:/work",
        "-v", f"{tc_dir}:/opt/jieli:ro",
        "-w", "/work",
        "debian:bookworm-slim",
    ] + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return r.stdout

print("=== CHECKING FLOATING POINT CALLS IN AUDIO ISR PATH ===")
# Disassemble all functions in .text
dis = run_in_docker(["/opt/jieli/pi32v2/bin/objdump", "-d", "build/felucca.elf"])

# Extract symbols
functions = {}
cur_fn = None
cur_lines = []

for line in dis.splitlines():
    m = re.match(r"^([a-zA-Z0-9_\.\$]+):$", line)
    if m:
        if cur_fn:
            functions[cur_fn] = cur_lines
        cur_fn = m.group(1)
        cur_lines = []
    elif cur_fn:
        cur_lines.append(line)

if cur_fn:
    functions[cur_fn] = cur_lines

print(f"Total disassembled functions: {len(functions)}")

# List of soft-float libcall patterns
fp_patterns = [
    "__addsf3", "__mulsf3", "__divsf3", "__subsf3", "__fixsfsi", "__floatsisf",
    "__extendsfdf2", "__truncdfsf2", "__adddf3", "__muldf3", "__divdf3", "__subdf3"
]

audio_fns = [
    "fm1_alnk0_irq", "audio_block", "cinco_audio_block",
    "cinco_groove_process", "cinco_groove_step",
    "cinco_speech_process", "speech_decode_next", "ima_adpcm_decode_nibble"
]

for fn_name in audio_fns:
    if fn_name in functions:
        lines = functions[fn_name]
        print(f"\nAnalyzing {fn_name} ({len(lines)} assembly instructions):")
        # Check stack frame allocation
        # Usually [--sp] = ... or sp += -N at start
        frame_size = 0
        for l in lines[:5]:
            m_sp = re.search(r"sp\s*\+=\s*(-?\d+)", l)
            if m_sp:
                frame_size += abs(int(m_sp.group(1)))
        print(f"  Estimated stack frame allocation: {frame_size} bytes")
        
        # Check for any calls
        calls = []
        fp_calls = []
        for l in lines:
            for pat in fp_patterns:
                if pat in l:
                    fp_calls.append((pat, l.strip()))
            if re.search(r"\bcall\b|\bcalla\b", l):
                calls.append(l.strip())
        print(f"  Function calls ({len(calls)}):")
        for c in calls:
            print(f"    {c}")
        if fp_calls:
            print(f"  CRITICAL HAZARD: Found {len(fp_calls)} floating point calls in {fn_name}:")
            for pat, l in fp_calls:
                print(f"    {pat}: {l}")
        else:
            print(f"  ZERO floating-point libcalls in {fn_name}!")
    else:
        print(f"Function {fn_name} inlined or not found in symbol table")
