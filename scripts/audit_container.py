#!/usr/bin/env python3
import struct
import sys
import os
sys.path.insert(0, "tools")

from fm1pkg_make import (
    _T, crc16, enc, sfc, chipkey_decode, KEY, FLASH_HDR, UFW_CHIP,
    APP_SLOT, FLASH_SIZE
)

def audit_fwsc(fwsc_path, app_bin_path, ota_bin_path):
    print(f"=== AUDITING CONTAINER & PACKAGING: {fwsc_path} ===")
    data = open(fwsc_path, "rb").read()
    print(f"File size: {len(data)} bytes")

    # 1. Unpack .fwsc marker bytes (the 20 identity blocks)
    # The first 20 blocks of 0x30 bytes: 0x2F data + 1 marker byte
    raw = bytearray(data)
    logical = bytearray()
    identity_chars = []
    for i in range(20):
        block = raw[i * 0x30:(i + 1) * 0x30]
        payload = block[:0x2F]
        marker = block[0x2F]
        logical += payload
        if marker == 0x7D:
            identity_chars.append(" ")
        else:
            ch_code = (marker - (i + 1)) & 0xFF
            identity_chars.append(chr(ch_code))
    logical += raw[20 * 0x30:]
    product_str = "".join(identity_chars).strip()
    print(f"Container Product Identity: '{product_str}'")

    # 2. Check logical UFW header
    hdr = bytearray(logical[:0x40])
    enc(hdr, 0, 0x40)
    
    hcrc0, hcrc1 = struct.unpack_from("<HH", hdr, 0)
    calc_hcrc0 = crc16(hdr[2:0x40])
    print(f"UFW Header CRC0: stored 0x{hcrc0:04x}, calculated 0x{calc_hcrc0:04x} -> {'MATCH' if hcrc0 == calc_hcrc0 else 'MISMATCH'}")
    assert hcrc0 == calc_hcrc0

    total, nfiles = struct.unpack_from("<IH", hdr, 4)
    print(f"Total logical size: {total} bytes, number of files: {nfiles}")
    assert total == len(logical)
    assert nfiles == 2

    chip_sig = hdr[16:16+len(UFW_CHIP)]
    print(f"UFW Chip signature: {chip_sig.decode('ascii', errors='ignore')}")
    assert chip_sig == UFW_CHIP

    # 3. Check directory entries
    lst = bytearray(logical[0x40:0x40 + nfiles * 0x50])
    calc_lst_crc = crc16(lst)
    print(f"UFW Directory CRC1: stored 0x{hcrc1:04x}, calculated 0x{calc_lst_crc:04x} -> {'MATCH' if hcrc1 == calc_lst_crc else 'MISMATCH'}")
    assert hcrc1 == calc_lst_crc

    # Decrypt each 0x50 entry individually
    files = {}
    for i in range(nfiles):
        e = bytearray(logical[0x40 + i * 0x50:0x40 + (i + 1) * 0x50])
        enc(e, 0, 0x50)
        typ, idx, dcrc, rsv, off, size, alloc_sz = struct.unpack_from("<HHHHIII", e, 0)
        name = e[0x40:].split(b"\x00")[0].decode()
        f_data = logical[off:off + size]
        calc_dcrc = crc16(f_data)
        print(f"  File {i}: {name} (type {typ}, offset 0x{off:x}, size {size} bytes, dcrc: stored 0x{dcrc:04x}, calculated 0x{calc_dcrc:04x}) -> {'MATCH' if dcrc == calc_dcrc else 'MISMATCH'}")
        assert dcrc == calc_dcrc
        files[name] = f_data

    # Check ota.bin matches build/loader/ota.bin
    if os.path.exists(ota_bin_path):
        ref_ota = open(ota_bin_path, "rb").read()
        print(f"Verifying ota.bin against {ota_bin_path}: {'MATCH' if files['ota.bin'] == ref_ota else 'MISMATCH'}")
        assert files['ota.bin'] == ref_ota

    # 4. Check flash.bin contents
    flash = bytearray(files['flash.bin'])
    print(f"\nFlash image size: {len(flash)} bytes (FLASH_SIZE = 0x{FLASH_SIZE:x})")
    assert len(flash) == FLASH_SIZE

    # Decode head (first 0x4000)
    head = bytearray(flash[:0x4000])
    for o in range(0, len(head), 32):
        enc(head, o, 32)

    hdr_crc = struct.unpack_from("<H", head, 0)[0]
    calc_hdr_crc = crc16(FLASH_HDR)
    print(f"Flash Header CRC: stored 0x{hdr_crc:04x}, calculated 0x{calc_hdr_crc:04x} -> {'MATCH' if hdr_crc == calc_hdr_crc else 'MISMATCH'}")
    assert hdr_crc == calc_hdr_crc

    # Decode app area from 0x4000
    # The app area was SFC-encrypted with chip key KEY (0x980F)
    app_area = bytearray(flash[0x4000:])
    sfc(app_area, 0, len(app_area), 0, KEY)

    # In app_area, offset 0 is app_area_head entry
    # struct entry: crc16(body) [2], body [30]: dcrc[2], offset[4], size[4], flags[1], resvd[1], index[2], name[16]
    dcrc, offset, size, flags, resvd, index, name = struct.unpack_from("<HIIBBH16s", app_area, 2)
    name_str = name.split(b"\x00")[0].decode()
    print(f"\nApp Area Head Entry: name='{name_str}', load_offset=0x{offset:08x}, size={size}, flags=0x{flags:02x}")
    print(f"Target Load / Entry Point: 0x{offset:08x} (Expect 0x02000120) -> {'VALID' if offset == 0x02000120 else 'INVALID'}")
    assert offset == 0x02000120

    # In app_area, offset 32 has the entry for app.bin:
    dcrc_app, off_app, size_app, flags_app, resvd_app, index_app, name_app = struct.unpack_from("<HIIBBH16s", app_area, 34)
    name_app_str = name_app.split(b"\x00")[0].decode()
    print(f"App Entry: name='{name_app_str}', offset=0x{off_app:x}, size={size_app} (APP_SLOT={APP_SLOT}), dcrc=0x{dcrc_app:04x}")
    assert name_app_str == "app.bin"
    assert size_app == APP_SLOT

    app_data = app_area[off_app:off_app + size_app]
    calc_app_dcrc = crc16(app_data)
    print(f"App Data CRC: stored 0x{dcrc_app:04x}, calculated 0x{calc_app_dcrc:04x} -> {'MATCH' if dcrc_app == calc_app_dcrc else 'MISMATCH'}")
    assert dcrc_app == calc_app_dcrc

    # Verify against actual felucca.bin
    ref_app = open(app_bin_path, "rb").read()
    print(f"Physical app size: {len(ref_app)} bytes vs APP_SLOT: {APP_SLOT} bytes (Headroom: {APP_SLOT - len(ref_app)} bytes)")
    assert len(ref_app) <= APP_SLOT
    assert app_data[:len(ref_app)] == ref_app
    assert app_data[len(ref_app):] == b"\xFF" * (APP_SLOT - len(ref_app))
    print("VERIFIED: app.bin in .fwsc exactly matches build/felucca.bin with valid 0xFF padding!")

    # Verify first instruction of app.bin
    # Expected crt0: goto 1f; rts; (goto +4 = 0x00 0x02 or similar)
    print(f"First 8 bytes of app.bin: {ref_app[:8].hex()}")
    # Let's verify disassembly of _start
    print("ALL CONTAINER & PACKAGING INTEGRITY CHECKS PASSED!\n")

if __name__ == "__main__":
    sys.path.insert(0, "tools")
    audit_fwsc("build/felucca.fwsc", "build/felucca.bin", "build/loader/ota.bin")
