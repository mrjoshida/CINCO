#!/usr/bin/env python3

def to_native_565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

def swap16(v):
    return ((v >> 8) | (v << 8)) & 0xFFFF

def decode_565(p):
    r = ((p >> 11) & 31) * 255 // 31
    g = ((p >> 5) & 63) * 255 // 63
    b = (p & 31) * 255 // 31
    return r, g, b

# Let's test skin tone: (230, 160, 140)
true_r, true_g, true_b = 230, 160, 140
native = to_native_565(true_r, true_g, true_b)
print(f"True RGB: ({true_r}, {true_g}, {true_b})")
print(f"Native RGB565: 0x{native:04X}")

# What happens with current code:
# gen_sprites swapped it:
pre_swapped = swap16(native)
# lcd_fill swapped it:
in_fb = swap16(pre_swapped)
# index.html swapped it:
in_browser = swap16(in_fb)
dec_r, dec_g, dec_b = decode_565(in_browser)
print(f"Decoded in browser currently: ({dec_r}, {dec_g}, {dec_b})")

# What happens if we DO NOT pre-swap (native RGB565 everywhere):
no_pre_swap = native
in_fb_correct = swap16(no_pre_swap)
in_browser_correct = swap16(in_fb_correct)
cor_r, cor_g, cor_b = decode_565(in_browser_correct)
print(f"Decoded in browser with native RGB565: ({cor_r}, {cor_g}, {cor_b})")
