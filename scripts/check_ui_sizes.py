#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    ui_files = [
        "ui.c", "ui_draw.c", "ui_input.c", "ui_events.c", "ui_graph.c",
        "ui_layer.c", "ui_menu.c", "ui_name.c", "ui_slice.c", "ui_fm6op.c",
        "ui_tools.c", "ui_help.c", "menu_items.c", "favorites.c", "category.c"
    ]
    total_lines = 0
    total_bytes = 0
    for f in ui_files:
        p = os.path.join(src_dir, f)
        if os.path.exists(p):
            with open(p, "r", encoding="latin-1") as fp:
                lines = len(fp.readlines())
            size = os.path.getsize(p)
            print(f"{f:15s}: {lines:5d} lines, {size:7d} bytes")
            total_lines += lines
            total_bytes += size
    print("-" * 35)
    print(f"Total UI files : {total_lines:5d} lines, {total_bytes:7d} bytes")

if __name__ == "__main__":
    main()
