#!/usr/bin/env python3
import re
import sys

def test_rle_assets():
    print("=== VALIDATING RLE ANIMATION SPRITES IN CINCO_ASSETS.H ===")
    with open("firmware/src/cinco_assets.h") as f:
        content = f.read()

    # Match:
    # static const cinco_anim_t cinco_anim_<name> = {
    #     .w = ...,
    #     .h = ...,
    #     .nframes = ...,
    #     .fps = ...,
    #     .pal = ...,
    #     .frame_off = ...,
    #     .rle = ...
    # };
    anim_blocks = re.findall(
        r"static const cinco_anim_t (cinco_anim_\w+)\s*=\s*\{([^}]+)\};", content
    )

    print(f"Found {len(anim_blocks)} animations in cinco_assets.h:")
    for anim_name, body in anim_blocks:
        fields = {}
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if line.startswith("."):
                k, v = line.split("=", 1)
                fields[k.strip().lstrip(".")] = v.strip().rstrip("u;")

        w = int(fields["w"])
        h = int(fields["h"])
        nframes = int(fields["nframes"])
        fps = int(fields["fps"])
        off_name = fields["frame_off"]
        rle_name = fields["rle"]

        print(f"\nChecking {anim_name}: {w}x{h}, {nframes} frames, {fps} fps, offsets: {off_name}, rle: {rle_name}")

        # Extract frame_off array
        off_match = re.search(r"static const uint32_t " + off_name + r"\[\d+\]\s*=\s*\{([^}]+)\};", content)
        if not off_match:
            print(f"  ERROR: Could not find offset array {off_name}")
            sys.exit(1)
        offsets = [int(x.strip().rstrip("u")) for x in off_match.group(1).split(",") if x.strip()]
        assert len(offsets) == nframes

        # Extract rle array
        rle_match = re.search(r"static const uint8_t " + rle_name + r"\[(\d+)\]\s*=\s*\{([^}]+)\};", content)
        if not rle_match:
            print(f"  ERROR: Could not find rle array {rle_name}")
            sys.exit(1)
        rle_size = int(rle_match.group(1))
        # Parse hex/dec bytes
        rle_bytes = []
        for token in rle_match.group(2).split(","):
            token = token.strip().rstrip("u")
            if token:
                rle_bytes.append(int(token, 0))
        assert len(rle_bytes) == rle_size

        print(f"  RLE buffer size: {rle_size} bytes, Frame offsets: {offsets}")

        # Simulate unpacking for every frame
        for f_idx in range(nframes):
            rle_pos = offsets[f_idx]
            px = 0
            py = 0
            total_pixels = 0
            while py < h:
                if rle_pos >= len(rle_bytes):
                    print(f"  CRITICAL ERROR: Frame {f_idx} ran past end of RLE buffer at rle_pos {rle_pos} >= {len(rle_bytes)}!")
                    sys.exit(1)
                b = rle_bytes[rle_pos]
                rle_pos += 1
                run = (b >> 4) + 1
                col_idx = b & 0x0F
                
                while run > 0:
                    run -= 1
                    total_pixels += 1
                    px += 1
                    if px >= w:
                        px = 0
                        py += 1
                        if py >= h:
                            break

            assert total_pixels == w * h, f"Frame {f_idx} total pixels {total_pixels} != {w * h}"
            if f_idx + 1 < nframes:
                next_off = offsets[f_idx + 1]
                assert rle_pos <= next_off, f"Frame {f_idx} unpacked past next offset ({rle_pos} > {next_off})"

        print(f"  SUCCESS: All {nframes} frames cleanly unpack exactly {w * h} pixels without overrunning RLE buffer!")

    print("\nALL RLE ANIMATION SPRITES VERIFIED 100% BUFFER SAFE!")

if __name__ == "__main__":
    test_rle_assets()
