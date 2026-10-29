#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Cinco Identity Generator 2.5™ Web Site & Artifact Builder
"""
Build script for Cinco Web Site:
1. Builds the WebAssembly emulator in build/emu/
2. Bundles the Cinco web installer into build/installer/index.html
3. Copies firmware binary to build/firmware/cinco.fwsc (and verifies product ID FM-1_433)
   Also maintains backwards-compatible copies/symlinks (cinco.fwsc, felucca.fwsc)
4. Prepares unified build/site/ staging directory for GitHub Pages CI
"""
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = REPO_ROOT / "build"
WEB_DIR = REPO_ROOT / "web"
EMU_DIR = BUILD_DIR / "emu"
INSTALLER_DIR = BUILD_DIR / "installer"
FIRMWARE_DIR = BUILD_DIR / "firmware"
SITE_DIR = BUILD_DIR / "site"

EXPECTED_PRODUCT_ID = "FM-1_433"
BLOCKS, BLK, KEEP = 20, 0x30, 0x2F


def run_cmd(cmd, cwd=None, env=None, check=True):
    print(f"Running: {' '.join(str(c) for c in cmd)} (cwd: {cwd or '.'})")
    res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"Command failed with code {res.returncode}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")
        sys.exit(res.returncode)
    return res


def decode_product_id(raw_fwsc: bytes) -> str:
    if len(raw_fwsc) < BLOCKS * BLK:
        return ""
    return "".join(
        chr((raw_fwsc[i * BLK + KEEP] - i - 1) & 0xFF)
        for i in range(BLOCKS)
        if raw_fwsc[i * BLK + KEEP] != 0x7D
    )


def build_emulator():
    print("\n--- Step 1: Building WebAssembly Emulator in build/emu/ ---")
    build_sh = WEB_DIR / "emu" / "build.sh"
    run_cmd([str(build_sh)], cwd=REPO_ROOT)

    required = [
        EMU_DIR / "index.html",
        EMU_DIR / "felucca.wasm",
        EMU_DIR / "worklet.js",
        EMU_DIR / "fonts" / "DotGothic16-subset.woff",
        EMU_DIR / "fonts" / "OFL.txt"
    ]
    for f in required:
        if not f.is_file() or f.stat().st_size == 0:
            print(f"ERROR: Emulator build missing file: {f}")
            sys.exit(1)
        print(f"  Verified emulator file: {f.relative_to(REPO_ROOT)} ({f.stat().st_size} bytes)")


def bundle_installer():
    print("\n--- Step 2: Bundling Cinco Web Installer into build/installer/index.html ---")
    INSTALLER_DIR.mkdir(parents=True, exist_ok=True)
    
    # Ensure cinco_installer.html is generated/updated
    gen_script = REPO_ROOT / "scripts" / "generate_cinco_installer.py"
    run_cmd(["python3", str(gen_script)], cwd=REPO_ROOT)

    src_installer = WEB_DIR / "cinco_installer.html"
    if not src_installer.is_file():
        print(f"ERROR: Missing installer source: {src_installer}")
        sys.exit(1)

    dst_installer = INSTALLER_DIR / "index.html"
    shutil.copy2(src_installer, dst_installer)
    print(f"  Bundled: {dst_installer.relative_to(REPO_ROOT)} ({dst_installer.stat().st_size} bytes)")


def prepare_firmware():
    print("\n--- Step 3: Verifying and Preparing Firmware Binaries in build/firmware/ ---")
    FIRMWARE_DIR.mkdir(parents=True, exist_ok=True)

    src_fwsc = None
    candidates = [
        BUILD_DIR / "cinco.fwsc",
        BUILD_DIR / "felucca.fwsc",
        FIRMWARE_DIR / "cinco.fwsc",
        FIRMWARE_DIR / "felucca.fwsc",
    ]
    for c in candidates:
        if c.is_file() and c.stat().st_size > 0:
            src_fwsc = c
            break

    if src_fwsc is None:
        print("Firmware not found locally in build/; attempting download from GitHub Pages...")
        fallback_urls = [
            "https://raw.githubusercontent.com/mrjoshida/CINCO/gh-pages/firmware/cinco.fwsc",
            "https://raw.githubusercontent.com/mrjoshida/CINCO/gh-pages/firmware/felucca.fwsc",
            "https://mrjoshida.github.io/CINCO/firmware/cinco.fwsc"
        ]
        for url in fallback_urls:
            try:
                print(f"  Attempting download from {url}...")
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                    if len(data) > 100000 and decode_product_id(data) == EXPECTED_PRODUCT_ID:
                        src_fwsc = BUILD_DIR / "cinco.fwsc"
                        src_fwsc.write_bytes(data)
                        print(f"  Successfully downloaded {len(data)} bytes from {url}")
                        break
            except Exception as e:
                print(f"  Fetch failed: {e}")

    if src_fwsc is None:
        print("ERROR: Neither build/cinco.fwsc nor build/felucca.fwsc found and remote fetch failed!")
        sys.exit(1)

    raw = src_fwsc.read_bytes()
    product_id = decode_product_id(raw)
    print(f"  Decoded Product ID from {src_fwsc.name}: '{product_id}'")
    if product_id != EXPECTED_PRODUCT_ID:
        print(f"ERROR: Product ID mismatch! Expected '{EXPECTED_PRODUCT_ID}', got '{product_id}'")
        sys.exit(1)

    # Ensure build/cinco.fwsc exists
    cinco_build_fwsc = BUILD_DIR / "cinco.fwsc"
    if not cinco_build_fwsc.is_file() or cinco_build_fwsc.stat().st_size != len(raw):
        shutil.copy2(src_fwsc, cinco_build_fwsc)
        print(f"  Created {cinco_build_fwsc.relative_to(REPO_ROOT)}")

    # Ensure build/cinco.bin exists if felucca.bin is present
    felucca_bin = BUILD_DIR / "felucca.bin"
    if felucca_bin.is_file():
        shutil.copy2(felucca_bin, BUILD_DIR / "cinco.bin")
        print(f"  Created {BUILD_DIR / 'cinco.bin'}")

    # Copy to build/firmware/cinco.fwsc and build/firmware/felucca.fwsc
    dst_cinco_fwsc = FIRMWARE_DIR / "cinco.fwsc"
    shutil.copy2(src_fwsc, dst_cinco_fwsc)
    print(f"  Deployed to firmware dir: {dst_cinco_fwsc.relative_to(REPO_ROOT)} ({dst_cinco_fwsc.stat().st_size} bytes)")

    dst_felucca_fwsc = FIRMWARE_DIR / "felucca.fwsc"
    shutil.copy2(src_fwsc, dst_felucca_fwsc)
    print(f"  Backwards compat copy: {dst_felucca_fwsc.relative_to(REPO_ROOT)}")

    # Copy licenses if present
    lic_dir = REPO_ROOT / "LICENSES"
    if lic_dir.is_dir():
        dst_lic = FIRMWARE_DIR / "LICENSES"
        dst_lic.mkdir(exist_ok=True)
        for lf in lic_dir.glob("*.txt"):
            shutil.copy2(lf, dst_lic / lf.name)
    for doc in ["LICENSE", "LICENSING.md"]:
        doc_p = REPO_ROOT / doc
        if doc_p.is_file():
            shutil.copy2(doc_p, FIRMWARE_DIR / doc)


def assemble_unified_site():
    print("\n--- Step 4: Assembling Unified Site Directory in build/site/ ---")
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy emulator to root of site
    for item in EMU_DIR.iterdir():
        if item.is_dir():
            shutil.copytree(item, SITE_DIR / item.name)
        else:
            shutil.copy2(item, SITE_DIR / item.name)
    
    # 2. Copy installer to site/installer/
    shutil.copytree(INSTALLER_DIR, SITE_DIR / "installer")

    # 3. Copy firmware to site/firmware/
    shutil.copytree(FIRMWARE_DIR, SITE_DIR / "firmware")

    # 4. Create .nojekyll
    (SITE_DIR / ".nojekyll").write_text("")
    print(f"  Unified site assembled at {SITE_DIR.relative_to(REPO_ROOT)}")


def main():
    print("==================================================")
    print(" CINCO IDENTITY GENERATOR 2.5™ — WEB SITE BUILDER ")
    print("==================================================")
    build_emulator()
    bundle_installer()
    prepare_firmware()
    assemble_unified_site()
    print("\nSUCCESS: All web components built and verified successfully!")


if __name__ == "__main__":
    main()
