#!/usr/bin/env python3
import shutil
import subprocess
import sys

print("Python version:", sys.version)
for tool in ["pi32v2-elf-objdump", "pi32v2-elf-readelf", "pi32v2-elf-nm", "llvm-objdump", "readelf", "objdump"]:
    path = shutil.which(tool)
    print(f"  {tool}: {path}")

# Check python modules
for mod in ["elftools", "pyelftools"]:
    try:
        __import__(mod)
        print(f"  Python module {mod}: Available")
    except ImportError:
        print(f"  Python module {mod}: Not available")

# Look for jieli toolchain anywhere in HOME or PATH
import os
for root, dirs, files in os.walk(os.path.expanduser("~")):
    if "pi32v2-elf-objdump" in files or "download.bat" in files or "isd_download.exe" in files:
        print("Found toolchain candidate:", root)
    # Don't recurse too deep in common huge dirs
    if root.count(os.sep) - os.path.expanduser("~").count(os.sep) >= 4:
        dirs.clear()
