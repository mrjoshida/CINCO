#!/usr/bin/env python3
"""
Find all references to symbols defined in the UI layer across non-UI files.
"""
import os
import re

UI_FILES = {
    "ui.c", "ui_draw.c", "ui_input.c", "ui_events.c", "ui_graph.c",
    "ui_layer.c", "ui_menu.c", "ui_name.c", "ui_slice.c", "ui_fm6op.c",
    "ui_tools.c", "ui_help.c", "menu_items.c", "favorites.c", "category.c"
}

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    # Check main.c, editor.c, console.c, project.c, seq.c, audio.c, etc.
    non_ui = [f for f in os.listdir(src_dir) if f.endswith(".c") and f not in UI_FILES and f != "felucca.c"]
    
    print(f"Checking non-UI files: {non_ui}")
    ui_syms = ["ui.", "ui_", "scrn.", "AF_", "T_THEME", "T_BG", "draw_text", "boot_leds", "panel_setup", "ui_prefs", "settings_save", "settings_poll", "autosave_boot", "autosave_poll"]
    
    for f in sorted(non_ui):
        p = os.path.join(src_dir, f)
        with open(p, "r", encoding="latin-1") as fp:
            content = fp.read()
        found = []
        for s in ui_syms:
            if s in content:
                found.append(s)
        if found:
            print(f"  {f:15s}: references {found}")

if __name__ == "__main__":
    main()
