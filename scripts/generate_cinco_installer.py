import base64
import json
#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Cinco Identity Generator 2.5™ Web Installer Generator
# Cinco Business Systems, Inc. [v2.5] (Celery Man Edition)
# Generates web/cinco_installer.html with authentic Windows 98 Setup Wizard UI
# and unified CINCO OS 2.5 desktop environment
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
web_dir = REPO_ROOT / "web"

def strip_module(src):
    src = re.sub(r"^export\s+", "", src, flags=re.M)
    return re.sub(r"^import .*?;\n", "", src, flags=re.M)

lib_pkg = strip_module((web_dir / "fm1pkg.js").read_text(encoding="utf-8"))
lib_ota = strip_module((web_dir / "fm1ota.js").read_text(encoding="utf-8"))
lib_backup = strip_module((web_dir / "fm1backup.js").read_text(encoding="utf-8"))

combined_lib = f"""// --- INLINED FM1 PKG / OTA / BACKUP LIBRARIES ---
{lib_pkg}

{lib_ota}

{lib_backup}
"""

def get_tayne_assets_js():
    asset_map = {
        "idle": ("image/gif", "assets/scumm_sprites/tayne_scumm_loop.gif"),
        "wobble": ("image/gif", "assets/scumm_sprites/tayne_hatwobble_scumm_loop.gif"),
        "flarh": ("image/gif", "assets/scumm_sprites/tayne_flarh_scumm_loop.gif"),
        "nude": ("image/png", "assets/sprites_pixelated/tayne_nude_real_pixel.png"),
        "oyster": ("image/png", "assets/scumm_sprites/oyster_scumm_f0.png"),
        "snd_tayne": ("audio/wav", "assets/speech/tayne.wav"),
        "snd_wobble": ("audio/wav", "assets/speech/wobble.wav"),
        "snd_flarh": ("audio/wav", "assets/speech/flarh.wav"),
        "snd_yes": ("audio/wav", "assets/speech/yes.wav"),
        "snd_4d3d": ("audio/wav", "assets/speech/4d3d.wav"),
        "snd_nsfw": ("audio/wav", "assets/speech/nsfw.wav"),
        "snd_printout": ("audio/wav", "assets/speech/printout.wav"),
    }
    b64_dict = {}
    for k, (mime, rel_p) in asset_map.items():
        p = REPO_ROOT / rel_p
        data = p.read_bytes()
        b64_dict[k] = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
    return "const TAYNE_ASSETS = " + json.dumps(b64_dict) + ";\n"


template = r"""<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-only
     Cinco Identity Generator 2.5™ Web Installer
     Cinco Business Systems, Inc. [v2.5] (Celery Man Edition)
     Portions derived from Felucca by Leo Kuroshita (@kurogedelic), Hügelton Instruments (GPL-3.0) -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cinco Identity Generator 2.5 Setup Wizard</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 fill=%22%23000080%22/%3E%3Crect x=%223%22 y=%222%22 width=%2210%22 height=%224%22 fill=%22%23fff%22/%3E%3Crect x=%223%22 y=%228%22 width=%2210%22 height=%226%22 fill=%22%23c0c0c0%22/%3E%3Ctext x=%224%22 y=%2213%22 font-family=%22monospace%22 font-size=%226%22 font-weight=%22bold%22 fill=%22%23000080%22%3E5%3C/text%3E%3C/svg%3E">
<meta name="description" content="Cinco Identity Generator 2.5 Setup Wizard for M-VAVE FM-1. Installs Celery Man Edition firmware directly over WebMIDI SysEx.">
<style>
  :root {
    --win-bg: #008080;
    --win-gray: #c0c0c0;
    --win-light: #ffffff;
    --win-lighter: #dfdfdf;
    --win-dark: #808080;
    --win-darker: #000000;
    --win-blue: #000080;
    --win-blue-light: #1084d0;
    --win-selection: #000080;
    --win-text: #000000;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 10px 10px 40px;
    background-color: var(--win-bg);
    color: var(--win-text);
    font-family: Tahoma, "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 12px;
    line-height: 1.4;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    -webkit-font-smoothing: subpixel-antialiased;
    -moz-osx-font-smoothing: auto;
    text-rendering: optimizeLegibility;
    overflow-x: hidden;
    user-select: none;
  }

  button, input, select, textarea {
    font-family: inherit;
    -webkit-font-smoothing: subpixel-antialiased;
    -moz-osx-font-smoothing: auto;
    text-rendering: optimizeLegibility;
  }

  a { color: inherit; text-decoration: none; }
  a:hover { text-decoration: underline; }

  /* 3D Bevel Utilities */
  .bevel-raised {
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  }

  .bevel-sunken {
    border-top: 2px solid var(--win-dark);
    border-left: 2px solid var(--win-dark);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker), inset -1px -1px 0 var(--win-lighter);
  }

  .bevel-thin-raised {
    border-top: 1px solid var(--win-light);
    border-left: 1px solid var(--win-light);
    border-right: 1px solid var(--win-darker);
    border-bottom: 1px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  }

  .bevel-thin-sunken {
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker);
  }

  /* Desktop Icons on Teal Background */
  .desktop-icons {
    position: fixed;
    top: 14px;
    left: 14px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 5;
  }
  .desktop-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 72px;
    text-align: center;
    cursor: pointer;
    text-decoration: none;
    color: #ffffff;
    padding: 4px 2px;
  }
  .desktop-icon:focus, .desktop-icon.active {
    outline: 1px dotted #ffffff;
  }
  .desktop-icon:focus .icon-lbl, .desktop-icon.active .icon-lbl {
    background: var(--win-selection);
    color: #ffffff;
  }
  .desktop-icon .icon-img {
    width: 32px;
    height: 32px;
    margin-bottom: 3px;
    filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.6));
  }
  .desktop-icon .icon-lbl {
    font-size: 11px;
    padding: 1px 3px;
    border-radius: 1px;
    word-break: break-word;
    line-height: 1.2;
    text-shadow: 1px 1px 1px #000000;
  }

  /* Windows 98 Base Window Styles */
  .win-window {
    background: var(--win-gray);
    color: var(--win-text);
    display: flex;
    flex-direction: column;
    position: absolute;
    user-select: none;
  }

  #main-win {
    position: relative;
    width: 580px;
    max-width: 96vw;
    margin: 14px auto 36px auto;
    z-index: 10;
  }

  /* Titlebars */
  .win-titlebar {
    height: 20px;
    background: linear-gradient(90deg, var(--win-blue), var(--win-blue-light));
    color: #ffffff;
    padding: 2px 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: bold;
    font-size: 12px;
    cursor: default;
  }
  .win-titlebar.inactive {
    background: linear-gradient(90deg, #808080, #b0b0b0);
    color: #c0c0c0;
  }
  .win-titlebar-left {
    display: flex;
    align-items: center;
    gap: 6px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .win-title-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }
  .win-controls {
    display: flex;
    gap: 2px;
    flex-shrink: 0;
  }
  .win-btn {
    width: 16px;
    height: 14px;
    background: var(--win-gray);
    border-top: 1px solid var(--win-light);
    border-left: 1px solid var(--win-light);
    border-right: 1px solid var(--win-darker);
    border-bottom: 1px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0;
    font-family: inherit;
    font-size: 11px;
    font-weight: bold;
    color: #000000;
    line-height: 1;
  }
  .win-btn:active {
    border-top: 1px solid var(--win-darker);
    border-left: 1px solid var(--win-darker);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    box-shadow: none;
    padding-top: 1px;
    padding-left: 1px;
  }

  /* Wizard Banner Header */
  .win98-banner {
    background: #ffffff;
    border-bottom: 1px solid var(--win-dark);
    box-shadow: 0 1px 0 var(--win-light);
    padding: 10px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
  }
  .banner-left {
    flex: 1;
    padding-right: 12px;
  }
  .banner-title {
    font-size: 13px;
    font-weight: bold;
    color: #000000;
    margin: 0 0 3px 0;
  }
  .banner-subtitle {
    font-size: 11px;
    color: #333333;
    line-height: 1.3;
    margin: 0;
  }
  .banner-corp {
    font-size: 9.5px;
    color: #666666;
    margin-top: 4px;
    font-family: monospace;
    letter-spacing: 0.05em;
  }
  .banner-right {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }
  .banner-pc-art {
    width: 54px;
    height: 46px;
  }

  /* Setup Dialog Body Area */
  .win98-body {
    padding: 12px 14px 10px;
    background: var(--win-gray);
  }
  .setup-intro {
    font-size: 11px;
    line-height: 1.45;
    margin-bottom: 8px;
    color: #000000;
  }
  .warn-text {
    color: #b00000;
    font-weight: bold;
    font-size: 11px;
    margin: 4px 0 8px;
  }

  /* Fieldsets & Group Boxes */
  fieldset.win-group {
    border: 2px groove #ffffff;
    margin: 8px 0 10px;
    padding: 8px 12px;
    background: transparent;
  }
  fieldset.win-group legend {
    font-size: 11px;
    font-weight: bold;
    color: #000000;
    padding: 0 4px;
  }

  /* Hardware Specifications Grid */
  .hw-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 14px;
    font-size: 11px;
  }
  .hw-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker);
    padding: 2px 6px;
    font-family: "Courier New", monospace;
    font-size: 10.5px;
  }
  .hw-lbl {
    color: #444444;
    font-weight: normal;
  }
  .hw-val {
    color: #000080;
    font-weight: bold;
  }

  /* Section Labels */
  .section-label {
    font-size: 11px;
    font-weight: bold;
    color: #000000;
    margin: 6px 0 3px;
  }

  /* Classic Windows 98 Segmented Progress Bar */
  .progress-frame {
    background: #ffffff;
    border-top: 2px solid var(--win-dark);
    border-left: 2px solid var(--win-dark);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker), inset -1px -1px 0 var(--win-lighter);
    padding: 2px;
    margin: 4px 0 8px;
  }
  progress#bar {
    display: block;
    width: 100%;
    height: 20px;
    appearance: none;
    -webkit-appearance: none;
    border: none;
    background: #ffffff;
  }
  progress#bar::-webkit-progress-bar { background: #ffffff; }
  progress#bar::-webkit-progress-value {
    background-color: var(--win-blue);
    background-image: repeating-linear-gradient(
      90deg,
      var(--win-blue) 0px,
      var(--win-blue) 8px,
      #ffffff 8px,
      #ffffff 10px
    );
  }
  progress#bar::-moz-progress-bar {
    background-color: var(--win-blue);
    background-image: repeating-linear-gradient(
      90deg,
      var(--win-blue) 0px,
      var(--win-blue) 8px,
      #ffffff 8px,
      #ffffff 10px
    );
  }

  /* Status Line Box (Sunken 3D) */
  #status {
    background: #ffffff;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker);
    padding: 3px 6px;
    font-family: "Courier New", Courier, monospace;
    font-size: 11px;
    color: var(--win-blue);
    font-weight: bold;
    min-height: 22px;
    box-sizing: border-box;
    word-break: break-all;
    margin: 2px 0 6px;
    display: flex;
    align-items: center;
  }

  /* Log Terminal Box */
  #log {
    background: #000000;
    color: #00ff66;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker);
    padding: 6px 8px;
    font-family: "Courier New", Courier, monospace;
    font-size: 10.5px;
    line-height: 1.35;
    height: 95px;
    max-height: 95px;
    overflow-y: scroll;
    white-space: pre-wrap;
    margin: 0 0 8px 0;
    box-sizing: border-box;
  }

  /* Stock / Recovery Collapsible */
  details.stock-box {
    border: 2px groove #ffffff;
    padding: 6px 10px;
    margin: 8px 0 4px;
    background: transparent;
  }
  details.stock-box summary {
    font-size: 11px;
    font-weight: bold;
    cursor: pointer;
    color: #000000;
    user-select: none;
    outline: none;
  }
  .stock-content {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--win-dark);
    box-shadow: 0 -1px var(--win-light);
  }

  /* Bottom Command Button Bar (Sunken Divider) */
  .win98-command-bar {
    border-top: 1px solid var(--win-dark);
    box-shadow: 0 1px 0 var(--win-light);
    margin-top: 10px;
    padding-top: 10px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }

  .win98-btn-default {
    font-weight: bold;
    outline: 1px solid #000000;
  }

  /* Sunken Status Bar */
  .win-statusbar {
    display: flex;
    background: var(--win-gray);
    padding: 2px 4px;
    gap: 4px;
    border-top: 1px solid var(--win-dark);
    font-size: 11px;
    line-height: 1.3;
  }
  .status-panel {
    padding: 2px 6px;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .status-panel.main-panel { flex: 1; }

  /* External Links Footer below dialog */
  .footer-links {
    margin-top: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    font-size: 11px;
  }
  .footer-links a {
    color: #ffffff;
    text-decoration: underline;
    text-shadow: 1px 1px 1px #000000;
  }
  .footer-links a:hover { color: #ffff80; }

  /* Bottom Taskbar */
  .win-taskbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 28px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px 3px;
    z-index: 9999;
    box-shadow: inset 0 1px 0 var(--win-lighter);
  }
  .taskbar-left {
    display: flex;
    align-items: center;
    gap: 4px;
    overflow-x: auto;
    height: 100%;
  }
  .start-btn {
    height: 22px;
    padding: 2px 6px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: bold;
    font-size: 11px;
    cursor: pointer;
  }
  .start-btn:active, .start-btn.pressed {
    border-top: 2px solid var(--win-darker);
    border-left: 2px solid var(--win-darker);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    box-shadow: none;
    padding-top: 3px;
    padding-left: 7px;
  }
  .start-logo {
    width: 14px;
    height: 14px;
  }
  .taskbar-divider {
    width: 2px;
    height: 20px;
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    margin: 0 2px;
  }
  .task-pill {
    height: 22px;
    padding: 2px 8px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-darker);
    border-left: 2px solid var(--win-darker);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: bold;
    cursor: pointer;
    max-width: 260px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .task-pill.inactive {
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
    font-weight: normal;
  }
  .taskbar-right {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 4px;
  }
  .systray {
    height: 22px;
    padding: 2px 6px;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
  }
  .systray-icon {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }

  /* Start Menu */
  .start-menu {
    display: none;
    position: fixed;
    bottom: 28px;
    left: 2px;
    width: 200px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    z-index: 10000;
  }
  .start-menu.open { display: flex; }
  .start-sidebar {
    width: 24px;
    background: linear-gradient(180deg, var(--win-blue), #000040);
    color: #ffffff;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 8px 2px;
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 2px;
  }
  .start-items {
    flex: 1;
    padding: 3px 0;
    display: flex;
    flex-direction: column;
  }
  .start-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 12px;
    cursor: pointer;
    color: #000000;
    font-size: 12px;
    text-decoration: none;
  }
  .start-item:hover {
    background: var(--win-blue);
    color: #ffffff;
  }
  .start-item-icon {
    width: 16px;
    height: 16px;
  }
  .start-divider {
    height: 1px;
    background: var(--win-dark);
    border-bottom: 1px solid var(--win-light);
    margin: 3px 2px;
  }

  /* Generic Dialog & Modal Styling */
  .modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: 10001;
    align-items: center;
    justify-content: center;
  }
  .modal-overlay.open { display: flex; }
  .win-dialog {
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: 3px 3px 10px rgba(0,0,0,0.6);
    min-width: 320px;
    display: flex;
    flex-direction: column;
  }
  .dialog-body {
    padding: 12px 14px;
    font-size: 12px;
    line-height: 1.5;
  }
  .dialog-btn {
    font-family: inherit;
    font-size: 12px;
    min-width: 68px;
    padding: 3px 12px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    border-left: 2px solid var(--win-light);
    border-right: 2px solid var(--win-darker);
    border-bottom: 2px solid var(--win-darker);
    box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
    cursor: pointer;
  }
  .dialog-btn:active {
    border-top: 2px solid var(--win-darker);
    border-left: 2px solid var(--win-darker);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    box-shadow: none;
    padding-top: 4px;
    padding-left: 13px;
  }
  .dialog-btn:disabled {
    color: var(--win-dark);
    text-shadow: 1px 1px 0 var(--win-light);
    cursor: default;
  }

  /* Systray Volume Popup */
  .volume-popup {
    display: none;
    position: fixed;
    bottom: 30px;
    right: 10px;
    background: var(--win-gray);
    padding: 10px 14px;
    z-index: 10000;
    width: 90px;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 11px;
  }
  .volume-popup.open { display: flex; }
  .vol-slider {
    writing-mode: vertical-lr;
    direction: rtl;
    height: 80px;
  }

  /* App Windows: Floating Window Layouts */
  .app-window {
    display: none;
    position: absolute;
    top: 40px;
    left: 60px;
    z-index: 20;
  }
  .app-window.open { display: flex; }

  /* Recycle Bin Window */
  #win-recycle { width: 560px; height: 340px; }
  .explorer-toolbar {
    display: flex;
    gap: 4px;
    padding: 3px 6px;
    border-bottom: 1px solid var(--win-dark);
    background: var(--win-gray);
  }
  .explorer-table {
    flex: 1;
    background: #ffffff;
    border-top: 1px solid var(--win-dark);
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    border-bottom: 1px solid var(--win-light);
    overflow-y: auto;
    margin: 4px;
  }
  .file-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    line-height: 1.4;
  }
  .file-table th {
    background: var(--win-gray);
    border-right: 1px solid var(--win-dark);
    border-bottom: 1px solid var(--win-dark);
    padding: 2px 6px;
    text-align: left;
    font-weight: normal;
  }
  .file-table td {
    padding: 2px 6px;
    cursor: pointer;
  }
  .file-table tr.selected {
    background: var(--win-blue);
    color: #ffffff;
  }

  /* Tayne Studio 98 */
  #win-tayne { width: 420px; }
  .tayne-card {
    background: #000000;
    color: #5fe08a;
    font-family: monospace;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #5fe08a;
    font-size: 12px;
    line-height: 1.5;
  }
  .tayne-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  /* Cinco Defrag */
  #win-defrag { width: 440px; }
  .defrag-grid {
    display: grid;
    grid-template-columns: repeat(20, 1fr);
    gap: 2px;
    background: #ffffff;
    padding: 6px;
    height: 120px;
    border: 2px solid var(--win-dark);
    margin: 8px 0;
  }
  .cluster-box {
    width: 100%;
    height: 100%;
    background: #ffffff;
  }
  .cluster-alloc { background: #000080; }
  .cluster-free { background: #ffffff; border: 1px solid #c0c0c0; }
  .cluster-frag { background: #ff0000; }
  .cluster-unmov { background: #008000; }

  /* Lotus 1-2-3 */
  #win-lotus { width: 620px; }
  .lotus-table {
    width: 100%;
    border-collapse: collapse;
    font-family: monospace;
    font-size: 12px;
    line-height: 1.4;
    background: #ffffff;
  }
  .lotus-table th, .lotus-table td {
    border: 1px solid #808080;
    padding: 3px 6px;
  }
  .lotus-table th { background: var(--win-gray); font-weight: bold; }

  /* CINCO Manual */
  #win-manual { width: 560px; height: 380px; }
  .manual-split {
    display: flex;
    flex: 1;
    gap: 6px;
    padding: 6px;
    overflow: hidden;
  }
  .manual-toc {
    width: 160px;
    background: #ffffff;
    border: 1px solid var(--win-dark);
    padding: 4px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .manual-toc-item {
    padding: 3px 6px;
    cursor: pointer;
    font-size: 12px;
  }
  .manual-toc-item.selected {
    background: var(--win-blue);
    color: #ffffff;
  }
  .manual-view {
    flex: 1;
    background: #ffffff;
    border: 1px solid var(--win-dark);
    padding: 8px;
    overflow-y: auto;
    font-size: 12px;
    line-height: 1.5;
  }

  /* Shut Down & Fullscreen DOS / Power Screens */
  #screen-shutdown {
    display: none;
    position: fixed;
    inset: 0;
    background: #000000;
    color: #ff6600;
    font-family: Tahoma, "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 26px;
    font-weight: bold;
    text-align: center;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 20px;
    z-index: 20000;
  }
  #screen-shutdown.open { display: flex; }

  #screen-dos {
    display: none;
    position: fixed;
    inset: 0;
    background: #000000;
    color: #ffffff;
    font-family: monospace;
    font-size: 14px;
    padding: 20px;
    flex-direction: column;
    z-index: 20000;
  }
  #screen-dos.open { display: flex; }
  .dos-input-line { display: flex; gap: 8px; }
  .dos-input {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: monospace;
    font-size: 14px;
    outline: none;
    flex: 1;
  }

  @media (max-width: 768px) {
    .desktop-icons { display: none; }
    #main-win { width: 100%; max-width: 100%; margin: 0 0 16px; }
    .hw-grid { grid-template-columns: 1fr; }
    .banner-pc-art { display: none; }
  }

  /* Tayne Studio 98 Stage & Receipt */
  #win-tayne { width: 440px; }
  .tayne-stage {
    height: 220px;
    background: #000000;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 6px;
    border-top: 2px solid var(--win-dark);
    border-left: 2px solid var(--win-dark);
    border-right: 2px solid var(--win-light);
    border-bottom: 2px solid var(--win-light);
    box-shadow: inset 1px 1px 0 var(--win-darker), inset -1px -1px 0 var(--win-lighter);
  }
  #tayne-stage-img {
    max-height: 200px;
    max-width: 100%;
    object-fit: contain;
    image-rendering: pixelated;
    image-rendering: -moz-crisp-edges;
    image-rendering: crisp-edges;
    transition: transform 0.1s ease;
  }
  .tayne-stage.pulse-4d3d {
    animation: taynePulse 0.14s infinite alternate;
    filter: drop-shadow(0 0 10px #00ffff) contrast(1.15);
  }
  @keyframes taynePulse {
    0% { transform: scale(1.0); }
    100% { transform: scale(1.05) rotate(0.5deg); }
  }

  .tayne-receipt-box {
    position: absolute;
    inset: 10px 20px;
    background: #ffffea;
    color: #111111;
    font-family: monospace;
    font-size: 11px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    text-align: center;
    border-top: 3px dashed #666;
    border-bottom: 3px dashed #666;
    animation: receiptSlideUp 0.35s ease-out;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    z-index: 10;
  }
  @keyframes receiptSlideUp {
    from { transform: translateY(100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  .receipt-pic {
    max-height: 85px;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    border: 1px solid #888;
    margin: 4px 0;
  }

  /* Maximized Window & Inactive Titlebars */
  .win-window.maximized {
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    width: 100vw !important;
    height: calc(100vh - 28px) !important;
    max-width: none !important;
    max-height: none !important;
    margin: 0 !important;
    z-index: 1000 !important;
  }

  .win-titlebar.inactive {
    background: linear-gradient(90deg, #808080, #b0b0b0) !important;
    color: #c0c0c0 !important;
  }

  /* MS-DOS 7.10 Interactive Terminal */
  #screen-dos {
    display: none;
    position: fixed;
    inset: 0;
    background: #000000;
    color: #ffffff;
    font-family: monospace;
    font-size: 14px;
    padding: 20px;
    flex-direction: column;
    z-index: 20000;
    overflow-y: auto;
    box-sizing: border-box;
  }
  #screen-dos.open { display: flex; }
  #dos-terminal-content { flex: 1; }
  .dos-input-line { display: flex; gap: 8px; align-items: center; }
  .dos-input {
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: monospace;
    font-size: 14px;
    outline: none;
    flex: 1;
    padding: 0;
    margin: 0;
  }
  .dos-line {
    white-space: pre-wrap;
    word-break: break-all;
    line-height: 1.35;
  }

</style>
</head>
<body>

<!-- Windows 98 Desktop Icons (Identical to Cinco Workstation) -->
<div class="desktop-icons" aria-label="Desktop Shortcuts">
  <div class="desktop-icon" id="d-mycomp" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="3" y="3" width="26" height="19" rx="1" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <rect x="5" y="5" width="22" height="15" fill="#008080"/>
      <path d="M12 22 L8 28 L24 28 L20 22 Z" fill="#808080" stroke="#000" stroke-width="1.5"/>
      <rect x="7" y="27" width="18" height="2" fill="#dfdfdf"/>
    </svg>
    <span class="icon-lbl">My Computer</span>
  </div>

  <div class="desktop-icon" id="d-app" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="2" y="4" width="28" height="24" rx="2" fill="#141415" stroke="#3a3a3e" stroke-width="1.5"/>
      <rect x="8" y="7" width="16" height="10" fill="#000000"/>
      <circle cx="6" cy="10" r="2" fill="#5fe08a"/>
      <circle cx="26" cy="10" r="2" fill="#ff453a"/>
      <rect x="5" y="20" width="22" height="5" rx="1" fill="#2a2a2d"/>
    </svg>
    <span class="icon-lbl">Cinco Synth</span>
  </div>

  <div class="desktop-icon" id="d-tayne" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <ellipse cx="16" cy="22" rx="12" ry="5" fill="#808080" stroke="#000" stroke-width="1.5"/>
      <rect x="9" y="8" width="14" height="14" rx="2" fill="#000080" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="18" x2="23" y2="18" stroke="#ff0000" stroke-width="2"/>
    </svg>
    <span class="icon-lbl">Tayne Studio 98</span>
  </div>

  <div class="desktop-icon" id="d-defrag" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="3" y="4" width="26" height="24" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <rect x="6" y="7" width="5" height="5" fill="#000080"/>
      <rect x="13" y="7" width="5" height="5" fill="#000080"/>
      <rect x="20" y="7" width="5" height="5" fill="#ffffff"/>
      <rect x="6" y="14" width="5" height="5" fill="#008000"/>
      <rect x="13" y="14" width="5" height="5" fill="#ff0000"/>
      <rect x="20" y="14" width="5" height="5" fill="#008000"/>
      <rect x="6" y="21" width="5" height="5" fill="#ffffff"/>
      <rect x="13" y="21" width="5" height="5" fill="#000080"/>
      <rect x="20" y="21" width="5" height="5" fill="#000080"/>
    </svg>
    <span class="icon-lbl">Cinco Defrag</span>
  </div>

  <div class="desktop-icon" id="d-boss" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="3" y="3" width="26" height="26" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <rect x="3" y="3" width="26" height="6" fill="#008000"/>
      <line x1="3" y1="15" x2="29" y2="15" stroke="#808080" stroke-width="1"/>
      <line x1="3" y1="21" x2="29" y2="21" stroke="#808080" stroke-width="1"/>
      <line x1="12" y1="9" x2="12" y2="29" stroke="#808080" stroke-width="1"/>
      <line x1="20" y1="9" x2="20" y2="29" stroke="#808080" stroke-width="1"/>
    </svg>
    <span class="icon-lbl">Lotus 1-2-3</span>
  </div>

  <div class="desktop-icon" id="d-installer" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="4" y="2" width="24" height="28" rx="2" fill="#000080" stroke="#000" stroke-width="1.5"/>
      <rect x="8" y="4" width="16" height="8" fill="#ffffff"/>
      <rect x="18" y="6" width="4" height="5" fill="#808080"/>
      <rect x="8" y="16" width="16" height="10" fill="#c0c0c0" stroke="#000" stroke-width="1"/>
      <text x="11" y="24" font-family="monospace" font-size="9" font-weight="bold" fill="#000080">5</text>
    </svg>
    <span class="icon-lbl">Setup Wizard</span>
  </div>

  <div class="desktop-icon" id="d-manual" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <path d="M6 3 L22 3 L27 8 L27 29 L6 29 Z" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <path d="M22 3 L22 8 L27 8 Z" fill="#c0c0c0" stroke="#000" stroke-width="1"/>
      <line x1="9" y1="12" x2="23" y2="12" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="16" x2="23" y2="16" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="20" x2="23" y2="20" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="24" x2="18" y2="24" stroke="#000" stroke-width="1.5"/>
    </svg>
    <span class="icon-lbl">CINCO Manual</span>
  </div>

  <div class="desktop-icon" id="d-recycle" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <path d="M7 8 L25 8 L23 28 L9 28 Z" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <line x1="5" y1="8" x2="27" y2="8" stroke="#000" stroke-width="2"/>
      <rect x="12" y="5" width="8" height="3" fill="#808080" stroke="#000" stroke-width="1"/>
      <line x1="12" y1="12" x2="12" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="16" y1="12" x2="16" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="20" y1="12" x2="20" y2="24" stroke="#808080" stroke-width="1.5"/>
    </svg>
    <span class="icon-lbl">Recycle Bin</span>
  </div>
</div>

<!-- Main Application Window: Cinco Identity Generator 2.5 Setup Wizard -->
<main class="win-window bevel-raised" id="main-win" role="dialog" aria-labelledby="win98-title">
  <!-- Title Bar -->
  <div class="win-titlebar" id="win-drag-bar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect x="1" y="1" width="14" height="14" rx="1" fill="#000080"/>
        <rect x="3" y="2" width="10" height="4" fill="#ffffff"/>
        <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
        <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
      </svg>
      <span id="win98-title">Cinco Identity Generator 2.5 Setup Wizard</span>
    </div>
    <div class="win-controls">
      <button class="win-btn" id="btn-win-help" title="Setup Help">?</button>
      <button class="win-btn win-min-btn" id="btn-win-min" data-target="main-win" title="Minimize">_</button>
      <button class="win-btn win-max-btn" id="btn-win-max" data-target="main-win" title="Maximize">口</button>
      <button class="win-btn win-close-btn" id="btn-win-close" data-target="main-win" title="Exit Setup">×</button>
    </div>
  </div>

  <!-- Wizard Top Banner Header -->
  <div class="win98-banner">
    <div class="banner-left">
      <div class="banner-title">Cinco Identity Generator 2.5 Setup</div>
      <div class="banner-subtitle">M-VAVE FM-1 Synthesizer Terminal Deployment Wizard</div>
      <div class="banner-corp">CINCO BUSINESS SYSTEMS, INC. &bull; CELERY MAN EDITION [v2.5]</div>
    </div>
    <div class="banner-right">
      <button class="dialog-btn" id="lang" title="Toggle Language (English / 日本語)" style="min-width: 54px; height: 21px; font-size: 11px; padding: 1px 6px;">English</button>
      <svg class="banner-pc-art" viewBox="0 0 54 46" fill="none" aria-label="4d3d3d3 Retro Terminal">
        <!-- CRT Monitor -->
        <rect x="4" y="2" width="44" height="30" rx="2" fill="#d4d0c8" stroke="#808080" stroke-width="1.5"/>
        <rect x="8" y="5" width="36" height="23" rx="1" fill="#000000"/>
        <rect x="10" y="7" width="32" height="19" fill="#001808"/>
        <!-- Screen Graphics & 4d3d3d3 -->
        <text x="12" y="16" fill="#00ff66" font-family="'Courier New', monospace" font-size="6.5" font-weight="bold">4d3d3d3</text>
        <rect x="12" y="19" width="14" height="2" fill="#00ff66"/>
        <rect x="28" y="19" width="10" height="2" fill="#00aa44"/>
        <circle cx="34" cy="14" r="2" fill="#00ff66"/>
        <!-- Monitor Stand -->
        <rect x="21" y="32" width="10" height="3" fill="#999999"/>
        <rect x="14" y="35" width="24" height="3" rx="1" fill="#d4d0c8" stroke="#808080" stroke-width="1"/>
        <!-- 3.5 Floppy disk leaning -->
        <rect x="42" y="24" width="10" height="15" rx="1" fill="#000080" stroke="#000"/>
        <rect x="44" y="25" width="6" height="5" fill="#ffffff"/>
        <rect x="45" y="33" width="4" height="4" fill="#c0c0c0"/>
      </svg>
    </div>
  </div>

  <!-- Wizard Body Content -->
  <div class="win98-body">
    <div class="setup-intro">
      <p data-t="intro" style="margin: 0 0 4px;"></p>
      <p class="warn-text" data-t="warn"></p>
    </div>

    <!-- Fieldset Group Box: Destination Hardware Terminal -->
    <fieldset class="win-group">
      <legend>Destination Hardware Terminal</legend>
      <div class="hw-grid">
        <div class="hw-item">
          <span class="hw-lbl">Target Device:</span>
          <span class="hw-val">M-VAVE FM-1 (AC7916A)</span>
        </div>
        <div class="hw-item">
          <span class="hw-lbl">Binary Package:</span>
          <span class="hw-val">cinco.fwsc (610 KB, FM-1_555)</span>
        </div>
        <div class="hw-item">
          <span class="hw-lbl">OS Environment:</span>
          <span class="hw-val">CINCO OS 2.5</span>
        </div>
        <div class="hw-item">
          <span class="hw-lbl">Protocol Engine:</span>
          <span class="hw-val">WebMIDI SysEx (Direct)</span>
        </div>
      </div>
    </fieldset>

    <!-- Progress Bar -->
    <div class="section-label">Installation Progress:</div>
    <div class="progress-frame">
      <progress id="bar" max="100" value="0"></progress>
    </div>

    <!-- Status Line and Terminal Log -->
    <div class="section-label">Terminal Output &amp; Device Status:</div>
    <div id="status" class="status-line"></div>
    <pre id="log" aria-label="Console log output"></pre>

    <!-- Cable note & brick warnings -->
    <p style="font-size: 11px; color: #222222; margin: 4px 0 2px;">
      <span data-t="direct"></span>
    </p>
    <p style="font-size: 11px; color: #444444; margin: 0 0 6px;">
      <span data-t="brick"></span>
      <a href="https://github.com/kurogedelic/FM-1-transporter" target="_blank" rel="noopener" style="color: var(--win-blue);">FM-1-transporter</a>
    </p>

    <!-- Disaster Recovery Group Box -->
    <details class="stock-box">
      <summary data-t="stockTitle">Disaster Recovery: Restore Factory M-VAVE Firmware (Stock V15)</summary>
      <div class="stock-content">
        <p style="font-size: 11px; color: #222222; margin: 2px 0 6px;" data-t="back"></p>
        <p style="margin: 4px 0;"><a href="https://www.m-vave.com/download" target="_blank" rel="noopener" style="color: var(--win-blue); font-weight: bold;">[↗ M-VAVE Official Firmware Downloads]</a></p>
        <p style="margin: 6px 0;"><label style="font-size: 11px; font-weight: bold; color: #000000;"><span data-t="stockFile">Official FM-1.fwsc:</span><br>
           <input id="stock-file" type="file" accept=".fwsc" style="font-size: 11px; margin-top: 4px;"></label></p>
        <p style="margin: 6px 0;"><button id="stock-go" class="dialog-btn" disabled data-t="stockGo">Back up and return to official V15</button></p>
        <p style="font-size: 11px; color: #444444; margin: 4px 0;" data-t="stockBackup"></p>
        <p style="font-size: 11px; color: #444444; margin: 4px 0;">
          <label><input id="stock-recovery" type="checkbox"> <span data-t="stockRecovery">Resume an interrupted update: I already saved a complete backup to this computer</span></label>
        </p>
      </div>
    </details>

    <!-- Bottom Command Button Bar -->
    <div class="win98-command-bar">
      <a href="../" class="dialog-btn" id="emu-link" style="margin-right: auto; text-decoration: none;">
        ⚡ <span data-t="emuLink">Cinco Synth Workstation</span>
      </a>
      <button class="dialog-btn" disabled>&lt; Back</button>
      <button id="go" class="dialog-btn win98-btn-default" disabled>
        <span data-t="install">Install &gt;</span>
      </button>
      <button class="dialog-btn" id="cancel-btn">Cancel</button>
    </div>
  </div>

  <!-- Sunken Status Bar -->
  <footer class="win-statusbar">
    <div class="status-panel main-panel">
      <span data-t="license"></span>
      <a href="https://github.com/mrjoshida/CINCO" target="_blank" rel="noopener" style="color: var(--win-blue);">github.com/mrjoshida/CINCO</a>
    </div>
    <div class="status-panel">Target: FM-1</div>
    <div class="status-panel">WebMIDI SysEx</div>
  </footer>
</main>

<!-- External Links Footer -->
<footer class="footer-links">
  <a href="../">⚡ Cinco Synth Workstation</a>
  <a href="https://github.com/mrjoshida/CINCO" target="_blank" rel="noopener">GitHub Repository</a>
  <a href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank" rel="noopener">Cinco Manual</a>
  <a href="../firmware/cinco.fwsc" download>Download Firmware (cinco.fwsc)</a>
</footer>

<!-- Windows 98 Application: Recycle Bin Window -->
<div class="win-window bevel-raised app-window" id="win-recycle">
  <div class="win-titlebar" id="drag-recycle">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16"><path d="M3 4 L13 4 L12 14 L4 14 Z" fill="#c0c0c0" stroke="#000"/><line x1="2" y1="4" x2="14" y2="4" stroke="#000"/></svg>
      <span>Recycle Bin</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-min-btn" data-target="win-recycle" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="win-recycle" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="win-recycle" title="Close">×</button>
    </div>
  </div>
  <div class="explorer-toolbar">
    <button class="dialog-btn" id="btn-empty-recycle">Empty Recycle Bin</button>
  </div>
  <div class="explorer-table">
    <table class="file-table" id="recycle-table">
      <thead>
        <tr><th>Name</th><th>Original Location</th><th>Date Deleted</th><th>Type</th><th>Size</th></tr>
      </thead>
      <tbody id="recycle-tbody">
        <tr tabindex="0"><td>tayne_beta_leaked_v1.raw</td><td>C:\CINCO\ASSETS</td><td>10/24/98 4:18 PM</td><td>RAW File</td><td>4,210 KB</td></tr>
        <tr tabindex="0"><td>paul_sandwich_order.txt</td><td>C:\CINCO\EXECUTIVE</td><td>10/25/98 12:04 PM</td><td>Text Document</td><td>1 KB</td></tr>
        <tr tabindex="0"><td>corrupted_cluster_4d3d.dat</td><td>C:\CINCO\SYSTEM</td><td>10/26/98 9:30 AM</td><td>DAT File</td><td>64 KB</td></tr>
        <tr tabindex="0"><td>oyster_receipt_unpaid.doc</td><td>C:\CINCO\RECEIPTS</td><td>10/27/98 2:15 PM</td><td>WordPad Document</td><td>12 KB</td></tr>
        <tr tabindex="0"><td>celery_unapproved_moves.avi</td><td>C:\CINCO\VAULT</td><td>10/28/98 11:42 AM</td><td>Video Clip</td><td>8,900 KB</td></tr>
      </tbody>
    </table>
  </div>
  <footer class="win-statusbar">
    <div class="status-panel" id="recycle-status-count">5 object(s)</div>
    <div class="status-panel" id="recycle-status-size">13.1 MB</div>
  </footer>
</div>

<!-- Modal Dialog: Confirm Nude Tayne (NSFW) -->
<div class="modal-overlay" id="modal-confirm-nude">
  <div class="win-window bevel-raised" style="width: 320px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Cinco Security Alert - NSFW</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="modal-confirm-nude">×</button></div>
    </div>
    <div class="dialog-body" style="padding:15px; display:flex; gap:12px; align-items:center;">
      <div style="font-size:32px; line-height:1;">⚠️</div>
      <div>
        <div style="font-weight:bold; margin-bottom:4px; color:#aa0000;">WARNING: Not suitable for work.</div>
        <div>Are you sure?</div>
      </div>
    </div>
    <div style="display:flex; justify-content:flex-end; gap:8px; padding:10px; background:var(--win-gray); border-top:1px solid var(--win-light);">
      <button class="dialog-btn" id="btn-nude-cancel" style="width:70px;">Cancel</button>
      <button class="dialog-btn" id="btn-nude-ok" style="width:70px; font-weight:bold;">OK</button>
    </div>
  </div>
</div>

<!-- Modal Dialog: Confirm Empty Recycle Bin -->
<div class="modal-overlay" id="modal-confirm-recycle">
  <div class="win-dialog bevel-raised" style="max-width:380px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Confirm File Delete</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="modal-confirm-recycle">×</button></div>
    </div>
    <div class="dialog-body" style="display:flex;gap:12px;align-items:center;">
      <svg viewBox="0 0 32 32" style="width:32px;height:32px;flex-shrink:0;"><circle cx="16" cy="16" r="14" fill="#ffcc00" stroke="#000"/><text x="13" y="24" font-weight="bold" font-size="20">?</text></svg>
      <div>Are you sure you want to permanently incinerate these 5 Cinco memory assets?</div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;padding:8px 12px;background:var(--win-gray);border-top:1px solid var(--win-dark);">
      <button class="dialog-btn" id="btn-confirm-recycle-yes">Yes</button>
      <button class="dialog-btn" id="btn-confirm-recycle-no">No</button>
    </div>
  </div>
</div>

<!-- Windows 98 Application: Tayne Studio 98 -->
<div class="win-window bevel-raised app-window" id="win-tayne">
  <div class="win-titlebar" id="drag-tayne">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="#000080"/></svg>
      <span>Tayne Studio 98 (Beta Edition)</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-min-btn" data-target="win-tayne" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="win-tayne" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="win-tayne" title="Close">×</button>
    </div>
  </div>
  <div class="dialog-body" style="padding: 8px;">
    <!-- Live animated stage viewport (220px high, dark sunken 3D bezel) -->
    <div class="tayne-stage bevel-sunken" id="tayne-stage">
      <img id="tayne-stage-img" alt="Tayne Routine Stage">
      <div id="tayne-receipt-box" class="tayne-receipt-box bevel-raised" style="display:none;">
        <div style="font-weight:bold; font-size:11px;">CINCO BUSINESS SYSTEMS CORP.</div>
        <div style="font-size:9px; color:#555;">VERIFIED ASSET PRINTOUT</div>
        <img id="tayne-receipt-img" alt="Oyster Smiling" class="receipt-pic">
        <div style="font-size:10px; line-height:1.3;">
          <div>ASSET: OYSTER (SMILING)</div>
          <div>MEM: 4d3d3d3 KINETIC</div>
          <div>STATUS: APPROVED (PAUL)</div>
        </div>
        <button class="dialog-btn" id="btn-close-receipt" style="padding:2px 8px; margin-top:4px;">Tear Receipt ✄</button>
      </div>
    </div>
    <div class="tayne-card" id="tayne-status-card">Dancer Sequence Loaded</div>
    <p style="margin:4px 0 6px; font-size:11px;">Select an automated routine or macro trigger for the active dancer sequence:</p>
    <div class="tayne-buttons">
      <button class="dialog-btn" id="btn-tayne-load" style="grid-column: span 2;">Load Tayne into Terminal</button>
      <button class="dialog-btn" id="btn-tayne-wobble">Hat Wobble</button>
      <button class="dialog-btn" id="btn-tayne-flarh">Flarhgunnstow</button>
      <button class="dialog-btn" id="btn-tayne-speed">4d3d3d3 Speed ⚡</button>
      <button class="dialog-btn" id="btn-tayne-nude" style="color:#aa0000; font-weight:bold;">Nude Tayne (NSFW)</button>
      <button class="dialog-btn" id="btn-tayne-receipt" style="grid-column: span 2;">Print Oyster Receipt</button>
    </div>
    <div style="margin-top:8px;">
      <div style="font-size:10px; font-weight:bold; margin-bottom:4px; color:#222;">CINCO LPC-10 SPEECH SOUNDBOARD:</div>
      <div style="display:flex; gap:4px; flex-wrap:wrap;">
        <button class="dialog-btn tayne-snd-btn" data-sound="snd_tayne">"Tayne"</button>
        <button class="dialog-btn tayne-snd-btn" data-sound="snd_wobble">"Wobble"</button>
        <button class="dialog-btn tayne-snd-btn" data-sound="snd_flarh">"Flarh"</button>
        <button class="dialog-btn tayne-snd-btn" data-sound="snd_yes">"Yes Paul"</button>
        <button class="dialog-btn tayne-snd-btn" data-sound="snd_4d3d">"4d3d3d3"</button>
      </div>
    </div>
    <div style="margin-top:8px;">
      <button class="dialog-btn" id="btn-tayne-sync" style="width:100%; font-weight:bold; background:#e0e0e0;">Sync to FM-1 Hardware ▶</button>
    </div>
  </div>
</div>

<!-- Windows 98 Application: Cinco Defrag -->
<div class="win-window bevel-raised app-window" id="win-defrag">
  <div class="win-titlebar" id="drag-defrag">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#c0c0c0"/><rect x="2" y="2" width="6" height="6" fill="#000080"/></svg>
      <span>Defragmenting Drive C:</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-min-btn" data-target="win-defrag" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="win-defrag" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="win-defrag" title="Close">×</button>
    </div>
  </div>
  <div class="dialog-body">
    <div style="font-weight:bold;margin-bottom:4px;">Drive C: (Cinco 4D3D3D3 Partition)</div>
    <div id="defrag-cluster-grid" class="defrag-grid"></div>
    <div style="display:flex;justify-content:space-between;margin:4px 0;font-size:11px;">
      <span>■ Allocated</span><span>■ Free</span><span>■ 4d3d3d3 Fragmented</span><span>■ Unmovable</span>
    </div>
    <div style="margin:6px 0;display:flex;justify-content:space-between;align-items:center;">
      <span id="defrag-progress-text">42% Complete</span>
      <div style="display:flex;gap:4px;">
        <button class="dialog-btn" id="btn-defrag-pause">Pause</button>
        <button class="dialog-btn" id="btn-defrag-stop">Stop</button>
        <button class="dialog-btn" id="btn-defrag-details">Show Details</button>
      </div>
    </div>
  </div>
</div>

<!-- Windows 98 Application: Lotus 1-2-3 (Boss Mode) -->
<div class="win-window bevel-raised app-window" id="win-lotus">
  <div class="win-titlebar" id="drag-lotus">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#008000"/></svg>
      <span>Lotus 1-2-3 (Boss Mode) — [CORPORATE_BUDGET.WK1]</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-min-btn" data-target="win-lotus" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="win-lotus" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="win-lotus" title="Close">×</button>
    </div>
  </div>
  <div style="padding:6px;overflow-x:auto;">
    <div style="font-weight:bold;color:#000080;margin-bottom:6px;">Q3 Cinco Business Systems Enterprise Forecast</div>
    <table class="lotus-table">
      <thead>
        <tr><th>Account / Division</th><th>Budget (USD)</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr><td>Celery Stalk Procurement</td><td>$4,200,000</td><td>APPROVED</td></tr>
        <tr><td>Tayne Beta Research & Development</td><td>$18,500,000</td><td>CONFIDENTIAL</td></tr>
        <tr><td>Oyster Smiling High-Resolution Printing</td><td>$320,000</td><td>PENDING</td></tr>
        <tr><td>4d3d3d3 Macro Overclocking</td><td>$9,800,000</td><td>ENGAGED</td></tr>
        <tr style="font-weight:bold;background:#e0e0e0;"><td>TOTAL CORPORATE ALLOCATION</td><td>$32,820,000</td><td>SIGNED (PAUL)</td></tr>
      </tbody>
    </table>
  </div>
  <footer class="win-statusbar">
    <div class="status-panel">READY | A1 | CALC</div>
  </footer>
</div>

<!-- Windows 98 Application: CINCO Manual Window -->
<div class="win-window bevel-raised app-window" id="win-manual">
  <div class="win-titlebar" id="drag-manual">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16"><path d="M3 2 L11 2 L13 4 L13 14 L3 14 Z" fill="#fff" stroke="#000"/></svg>
      <span>Cinco Business Systems Help — User Reference Guide</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-min-btn" data-target="win-manual" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="win-manual" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="win-manual" title="Close">×</button>
    </div>
  </div>
  <div class="manual-split">
    <div class="manual-toc">
      <div class="manual-toc-item selected" id="toc-welcome">1. Overview</div>
      <div class="manual-toc-item" id="toc-controls">2. Controls</div>
      <div class="manual-toc-item" id="toc-identities">3. Identities</div>
      <div class="manual-toc-item" id="toc-kinetics">4. Kinetics</div>
      <div class="manual-toc-item" id="toc-boss">5. Boss Key</div>
      <div class="manual-toc-item" id="toc-osha">6. OSHA Guidelines</div>
    </div>
    <div class="manual-view" id="manual-content-view">
      <h3>Welcome to Cinco Identity Generator 2.5™</h3>
      <p>This workstation runs custom Cinco OS 2.5 firmware for the M-VAVE FM-1 Synthesizer Terminal, featuring 4d3d3d3 window cascading, rotoscoped SCUMM dancers, and LPC speech synthesis.</p>
    </div>
  </div>
  <footer class="win-statusbar">
    <div class="status-panel" id="manual-status-panel">Cinco Reference Library v2.5</div>
  </footer>
</div>

<!-- Modal: Exit Setup Confirmation -->
<div class="modal-overlay" id="modal-exit-setup">
  <div class="win-dialog bevel-raised" style="max-width:380px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Exit Setup</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="modal-exit-setup">×</button></div>
    </div>
    <div class="dialog-body" style="display:flex;gap:12px;align-items:center;">
      <svg viewBox="0 0 32 32" style="width:32px;height:32px;flex-shrink:0;">
        <circle cx="16" cy="16" r="14" fill="#ffcc00" stroke="#000"/>
        <text x="13" y="24" font-weight="bold" font-size="20">?</text>
      </svg>
      <div>Are you sure you want to cancel Cinco Identity Generator 2.5 Setup and return to the Cinco Workstation?</div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;padding:8px 12px;background:var(--win-gray);border-top:1px solid var(--win-dark);">
      <button class="dialog-btn" id="btn-exit-setup-yes">Yes</button>
      <button class="dialog-btn" id="btn-exit-setup-no">No</button>
    </div>
  </div>
</div>

<!-- Modal: Confirm Factory Stock Restore -->
<div class="modal-overlay" id="modal-confirm-stock">
  <div class="win-dialog bevel-raised" style="max-width:400px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Confirm Factory Restore</span></div>
      <div class="win-controls"><button class="win-btn" id="btn-confirm-stock-x">×</button></div>
    </div>
    <div class="dialog-body" style="display:flex;gap:12px;align-items:center;">
      <svg viewBox="0 0 32 32" style="width:32px;height:32px;flex-shrink:0;">
        <path d="M16 2 L30 28 L2 28 Z" fill="#ffcc00" stroke="#000" stroke-width="1.5"/>
        <text x="14" y="24" font-weight="bold" font-size="18">!</text>
      </svg>
      <div id="confirm-stock-msg">Has the complete backup file been saved to this computer? Continue to return to official V15. Official V15 cannot open Cinco projects.</div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;padding:8px 12px;background:var(--win-gray);border-top:1px solid var(--win-dark);">
      <button class="dialog-btn" id="btn-confirm-stock-yes">Yes</button>
      <button class="dialog-btn" id="btn-confirm-stock-no">No</button>
    </div>
  </div>
</div>

<!-- Modal: Shut Down Windows -->
<div class="modal-overlay" id="modal-shutdown">
  <div class="win-dialog bevel-raised" style="max-width:350px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Shut Down Windows</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="modal-shutdown">×</button></div>
    </div>
    <div class="dialog-body">
      <div style="display:flex;gap:12px;align-items:flex-start;">
        <svg viewBox="0 0 32 32" style="width:32px;height:32px;flex-shrink:0;"><rect width="32" height="32" fill="#000080"/><circle cx="16" cy="16" r="10" fill="#c0c0c0"/></svg>
        <div>
          <div style="margin-bottom:8px;">What do you want the computer to do?</div>
          <div style="display:flex;flex-direction:column;gap:6px;">
            <label><input type="radio" name="shutdown-opt" id="shutdown-opt-off" checked> Shut down the computer</label>
            <label><input type="radio" name="shutdown-opt" id="shutdown-opt-restart"> Restart the computer</label>
            <label><input type="radio" name="shutdown-opt" id="shutdown-opt-dos"> Restart the computer in MS-DOS mode</label>
          </div>
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:6px;margin-top:16px;">
        <button class="dialog-btn" id="btn-shutdown-ok">OK</button>
        <button class="dialog-btn" id="btn-shutdown-cancel">Cancel</button>
        <button class="dialog-btn" id="btn-shutdown-help">Help</button>
      </div>
    </div>
  </div>
</div>

<!-- Screen: It's now safe to turn off your computer -->
<div id="screen-shutdown">
  <div>It's now safe to turn off<br>your computer.</div>
  <button class="dialog-btn" id="btn-turn-on" style="font-size:14px;padding:6px 16px;">Turn On</button>
</div>

<!-- Screen: MS-DOS 7.10 Mode -->
<!-- Fullscreen MS-DOS 7.10 Screen -->
<div id="screen-dos">
  <div id="dos-terminal-content">
    <div id="dos-banner">
      <div>Cinco Business Systems(R) MS-DOS 7.10</div>
      <div>(C)Copyright Cinco Business Systems Corp 1981-1998.</div>
      <div style="color:#aaa;margin-top:4px;">Type HELP for available commands, or WIN to return to Windows 98.</div>
      <br>
    </div>
    <div id="dos-history"></div>
    <div class="dos-input-line" id="dos-prompt-line">
      <span id="dos-prompt">C:\CINCO&gt;</span>
      <input type="text" class="dos-input" id="dos-input" autocomplete="off" spellcheck="false" autofocus>
    </div>
  </div>
  <div style="margin-top:auto; padding-top:10px;">
    <button class="dialog-btn" id="btn-dos-exit" style="background:#333;color:#fff;border-color:#666;">Exit to Windows 98 (WIN)</button>
  </div>
</div>

<!-- Modal: Coffee Dialog -->
<div class="modal-overlay" id="modal-coffee">
  <div class="win-dialog bevel-raised" style="max-width:380px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>Cinco Executive Coffee Service</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="modal-coffee">×</button></div>
    </div>
    <div class="dialog-body">
      <p>Managing Director Paul has taken a 15-minute executive espresso recess. OSHA vigilance level restored to 100%.</p>
      <div style="display:flex;justify-content:flex-end;margin-top:12px;">
        <button class="dialog-btn" id="btn-coffee-ok">OK</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal: System Properties -->
<div class="modal-overlay" id="sysprop-modal">
  <div class="win-dialog bevel-raised" style="max-width:380px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>System Properties</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="sysprop-modal">×</button></div>
    </div>
    <div class="dialog-body">
      <p><b>Cinco Business Systems OS 2.5</b><br>Celery Man Workstation Edition</p>
      <p>Computer:<br>M-VAVE FM-1 Synthesizer Terminal<br>WebMIDI SysEx Flasher Engine<br>Registered to: Paul (Managing Director)</p>
      <div style="display:flex;justify-content:flex-end;margin-top:12px;">
        <button class="dialog-btn" id="sysprop-ok">OK</button>
      </div>
    </div>
  </div>
</div>

<!-- Modal: About Dialog -->
<div class="modal-overlay" id="about-modal">
  <div class="win-dialog bevel-raised" style="max-width:360px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left"><span>About Cinco 2.5</span></div>
      <div class="win-controls"><button class="win-btn win-close-btn" data-target="about-modal">×</button></div>
    </div>
    <div class="dialog-body">
      <p><b>CINCO OS 2.5 (Celery Man Edition)</b></p>
      <p>Copyright © 2026 Cinco Business Systems, Inc.<br>Portions derived from Felucca by Leo Kuroshita (@kurogedelic), Hügelton Instruments.</p>
      <div style="display:flex;justify-content:flex-end;margin-top:12px;">
        <button class="dialog-btn" id="modal-ok">OK</button>
      </div>
    </div>
  </div>
</div>

<!-- Systray Volume Popup -->
<div class="win-window bevel-raised volume-popup" id="volume-popup">
  <div style="font-size:11px;font-weight:bold;">Volume</div>
  <input type="range" class="vol-slider" id="master-vol-slider" min="0" max="1023" value="700">
  <button class="win-btn" id="vol-popup-close" style="width:100%;height:18px;">Close</button>
</div>

<!-- Bottom Windows 98 Taskbar -->
<footer class="win-taskbar">
  <div class="taskbar-left">
    <button class="start-btn" id="start-btn" aria-haspopup="true" aria-expanded="false">
      <svg class="start-logo" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <rect x="3" y="2" width="10" height="4" fill="#fff"/>
        <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
        <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
      </svg>
      <span>Start</span>
    </button>
    <div class="taskbar-divider"></div>
    <div class="task-pill" id="task-pill-main">
      <svg viewBox="0 0 16 16" style="width:12px;height:12px;"><rect width="16" height="16" fill="#000080"/></svg>
      <span>Cinco Identity Generator 2.5 Setup Wizard</span>
    </div>
    <div class="task-pill inactive" id="task-pill-tayne" style="display:none;">
      <span>Tayne Studio 98</span>
    </div>
    <div class="task-pill inactive" id="task-pill-defrag" style="display:none;">
      <span>Cinco Defrag</span>
    </div>
    <div class="task-pill inactive" id="task-pill-lotus" style="display:none;">
      <span>Lotus 1-2-3</span>
    </div>
    <div class="task-pill inactive" id="task-pill-manual" style="display:none;">
      <span>CINCO Manual</span>
    </div>
    <div class="task-pill inactive" id="task-pill-recycle" style="display:none;">
      <span>Recycle Bin</span>
    </div>
  </div>

  <div class="taskbar-right">
    <div class="systray">
      <svg class="systray-icon" id="systray-vol" viewBox="0 0 16 16" title="Volume Control">
        <path d="M2 5 L5 5 L9 2 L9 14 L5 11 L2 11 Z" fill="#000000"/>
        <path d="M11 5 C12 7 12 9 11 11" stroke="#000000" fill="none" stroke-width="1.5"/>
      </svg>
      <span id="systray-clock">12:00 PM</span>
    </div>
  </div>
</footer>

<!-- Windows 98 Start Menu Popup -->
<div class="start-menu" id="start-menu" role="menu">
  <div class="start-sidebar">CINCO OS 2.5</div>
  <div class="start-items">
    <a class="start-item" id="sm-app" href="../">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#000080"/></svg>
      <span>Cinco Synth</span>
    </a>
    <div class="start-item" id="sm-setup">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#000080"/></svg>
      <span>Setup Wizard</span>
    </div>
    <div class="start-item" id="sm-tayne">
      <svg class="start-item-icon" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="#808080"/></svg>
      <span>Tayne Studio 98</span>
    </div>
    <div class="start-item" id="sm-defrag">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#008000"/></svg>
      <span>Cinco Defrag</span>
    </div>
    <div class="start-item" id="sm-boss">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#008000"/></svg>
      <span>Lotus 1-2-3</span>
    </div>
    <div class="start-item" id="sm-manual">
      <svg class="start-item-icon" viewBox="0 0 16 16"><path d="M3 2 L13 2 L13 14 L3 14 Z" fill="#fff" stroke="#000"/></svg>
      <span>CINCO Manual</span>
    </div>
    <div class="start-divider"></div>
    <div class="start-item" id="sm-sysprop">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#808080"/></svg>
      <span>Control Panel</span>
    </div>
    <div class="start-item" id="sm-about">
      <svg class="start-item-icon" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="#000080"/></svg>
      <span>About Cinco 2.5</span>
    </div>
    <div class="start-divider"></div>
    <div class="start-item" id="sm-shutdown">
      <svg class="start-item-icon" viewBox="0 0 16 16"><rect width="16" height="16" fill="#ff0000"/></svg>
      <span>Shut Down...</span>
    </div>
  </div>
</div>

<script type="module">
/*COMBINED_LIB_PLACEHOLDER*/

const $ = (id) => document.getElementById(id);

const TEXT = {
  en: {
    intro: "Connect your M-VAVE FM-1 via USB-C in Chrome or Edge. Installs Cinco Identity Generator 2.5 (Celery Man Edition) directly over WebMIDI SysEx.",
    warn: "Do not unplug the USB-C cable while writing.",
    install: "Install >",
    emuLink: "Cinco Synth Workstation",
    other: "日本語",
    direct: "Connect the USB cable directly to your computer. No probe or Transporter hardware is required.",
    brick: "If an install fails and the FM-1 no longer starts, recovery requires a Transporter or hardware UBoot:",
    beta: "Cinco Identity Generator 2.5 is custom firmware for M-VAVE FM-1. Provided as-is without warranty under GPL-3.0.",
    back: "Get official FM-1 V15 from M-VAVE and select the unmodified FM-1.fwsc. The browser validates it locally; it is never uploaded to any server.",
    stockTitle: "Disaster Recovery: Restore Factory M-VAVE Firmware (Stock V15)",
    stockFile: "Official FM-1.fwsc:",
    stockGo: "Back up and return to official V15",
    stockBackup: "Current music, saved music, sound banks, samples and settings are saved first. To restore an archive later, reinstall Cinco/Felucca.",
    stockRecovery: "Resume an interrupted update: I already saved a complete backup to this computer",
    stockValid: "Official V15 verified",
    stockConfirm: "Has the complete backup file been saved to this computer? Continue to return to official V15. Official V15 cannot open Cinco projects.",
    stockNeedBackup: "An update loader cannot export a backup. Only select resume if you already saved a complete backup.",
    stockUnsupported: "This firmware version does not support complete backups. Reinstall current firmware first.",
    backup: "Saving complete backup ",
    stockError: "Cannot validate official firmware: ",
    nomidi: "WebMIDI is not supported in this browser. Please open this page in Google Chrome or Microsoft Edge.",
    loadfail: "Could not load firmware package: ",
    start: "Starting...",
    verify: "Verifying package...",
    loader: "Switching to update mode...",
    write: "Writing firmware...",
    reboot: "Restarting device...",
    done: "Installation complete! Cinco Identity Generator 2.5 is running.",
    stopped: "Stopped. Replug the USB cable and press Install again.",
    error: "Error: ",
    denied: "MIDI (SysEx) access was not allowed. Allow MIDI permissions in your browser's site settings and retry.",
    notfound: "FM-1 not found. Ensure USB-C cable supports data transfer, close other MIDI software, and press Install again.",
    model: "The connected device is not an FM-1.",
    lost: "USB connection was lost. Replug and press Install again.",
    noloader: "FM-1 in update mode was not found. Replug the USB cable and press Install again.",
    noreturn: "FM-1 did not return after restart. Please power-cycle the unit.",
    mismatch: "Firmware written, but the FM-1 reported unexpected identity: ",
    badpkg: "The firmware package is damaged or invalid. Please reload the page.",
    leave: "Firmware writing in progress. Do not navigate away or close this page.",
    license: "GPL-3.0, no warranty. Source:",
  },
  ja: {
    intro: "FM-1 を USB-C で接続してください（Chrome または Edge 対応）。Cinco Identity Generator 2.5 (Celery Man Edition) を WebMIDI SysEx 経由で直接インストールします。",
    warn: "書き込み中は USB ケーブルを抜かないでください。",
    install: "インストール >",
    emuLink: "Cinco Synth ワークステーション",
    other: "English",
    direct: "USB ケーブルはパソコンに直接つないでください。Transporter 等の追加機材は不要です。",
    brick: "万一インストールに失敗して起動しなくなった場合の復旧には Transporter が必要です:",
    beta: "Cinco Identity Generator 2.5 は M-VAVE FM-1 向けカスタムファームウェアです。自己責任でお使いください。",
    back: "M-VAVEから公式FM-1 V15を取得し、未変更のFM-1.fwscを選んでください。ファイルはこのブラウザ内で検証し、サーバーへ送りません。",
    stockTitle: "非常時復旧：公式V15に戻す（工場出荷時ファームウェア）",
    stockFile: "公式FM-1.fwsc:",
    stockGo: "バックアップして公式V15へ戻す",
    stockBackup: "現在の曲・保存曲・音色バンク・サンプル・設定を先に保存します。復元はCincoを再インストールして行います。",
    stockRecovery: "更新中断の再開：全体バックアップはすでにパソコンへ保存済み",
    stockValid: "公式V15を確認しました",
    stockConfirm: "全体バックアップファイルをパソコンに保存できましたか？ 続けると公式V15へ戻します。公式V15ではCincoの曲は開けません。",
    stockNeedBackup: "書き込みモードからはバックアップできません。保存済みバックアップがある場合だけ、更新中断の再開にチェックしてください。",
    stockUnsupported: "このバージョンは全体バックアップに未対応です。",
    backup: "全体バックアップ保存中 ",
    stockError: "公式ファイルを確認できません: ",
    nomidi: "このブラウザでは使えません。Chrome か Edge で開いてください。",
    loadfail: "ファームウェアを読み込めませんでした: ",
    start: "開始します...",
    verify: "確認中...",
    loader: "書き込みモードに切り替え中...",
    write: "書き込み中...",
    reboot: "再起動中...",
    done: "完了しました！ Cinco 2.5 が起動します。",
    stopped: "途中で止まりました。USB を挿し直してもう一度押してください。",
    error: "エラー: ",
    denied: "MIDI（SysEx）の使用が許可されませんでした。アドレスバーのサイト設定で MIDI を許可して、もう一度押してください。",
    notfound: "FM-1 が見つかりません。USB ケーブル（データ通信用か）を確かめ、MIDI を使う他のアプリを閉じてから、もう一度押してください。",
    model: "接続されている機器は FM-1 ではありません。",
    lost: "USB の接続が切れました。挿し直してもう一度押してください。",
    noloader: "書き込みモードの FM-1 が見つかりません。USB を挿し直してもう一度押してください。",
    noreturn: "FM-1 が戻ってきません。電源を入れ直してください。",
    mismatch: "書き込みは終わりましたが、FM-1 が別のバージョンを報告しています: ",
    badpkg: "インストールするファイルが壊れています。ページを再読み込みしてください。",
    leave: "書き込み中です。ページを閉じないでください。",
    license: "GPL-3.0、無保証。ソース:",
  }
};

let lang = (navigator.language || "en").toLowerCase().startsWith("ja") ? "ja" : "en";
const t = (k) => TEXT[lang][k] || TEXT["en"][k] || "";
let lastKey = null, lastArg = "";

function applyLang() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-t]").forEach((e) => {
    const val = t(e.dataset.t);
    if (val) e.textContent = val;
  });
  $("lang").textContent = t("other");
  if (lastKey) $("status").textContent = t(lastKey) + lastArg;
}

$("lang").addEventListener("click", () => {
  lang = lang === "ja" ? "en" : "ja";
  applyLang();
});
applyLang();

// ------------------------------------------------------------------ Windows 98 UI System
function updateClock() {
  const now = new Date();
  let h = now.getHours();
  const m = String(now.getMinutes()).padStart(2, "0");
  const ampm = h >= 12 ? "PM" : "AM";
  h = h % 12 || 12;
  const clockEl = $("systray-clock");
  if (clockEl) clockEl.textContent = `${h}:${m} ${ampm}`;
}
setInterval(updateClock, 1000);
updateClock();

// Start menu toggle
const startBtn = $("start-btn");
const startMenu = $("start-menu");
if (startBtn && startMenu) {
  startBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = startMenu.classList.toggle("open");
    startBtn.classList.toggle("pressed", isOpen);
    startBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

document.addEventListener("click", () => {
  if (startMenu) startMenu.classList.remove("open");
  if (startBtn) {
    startBtn.classList.remove("pressed");
    startBtn.setAttribute("aria-expanded", "false");
  }
});

// Window Management
let topZ = 40;
const windowPillMap = {
  "main-win": "task-pill-main",
  "win-recycle": "task-pill-recycle",
  "win-tayne": "task-pill-tayne",
  "win-defrag": "task-pill-defrag",
  "win-lotus": "task-pill-lotus",
  "win-manual": "task-pill-manual",
  "win-setup-launcher": "task-pill-setup"
};

function focusWindow(win, pillId) {
  if (!win) return;
  topZ++;
  win.style.zIndex = topZ;
  
  // Demote all windows to inactive titlebars
  document.querySelectorAll(".win-window").forEach((w) => {
    w.classList.remove("active-win");
    const tb = w.querySelector(".win-titlebar");
    if (tb) tb.classList.add("inactive");
  });
  
  // Activate this window
  win.classList.add("active-win");
  const myTb = win.querySelector(".win-titlebar");
  if (myTb) myTb.classList.remove("inactive");
  
  // Update taskbar pills
  const myPillId = pillId || windowPillMap[win.id];
  document.querySelectorAll(".task-pill").forEach((p) => p.classList.add("inactive"));
  if (myPillId) {
    const p = document.getElementById(myPillId);
    if (p) {
      p.style.display = "flex";
      p.classList.remove("inactive");
    }
  }
}

function openWindow(winId, pillId) {
  const win = document.getElementById(winId);
  if (!win) return;
  win.style.display = "flex";
  focusWindow(win, pillId);
}

function closeWindow(winId, pillId) {
  const win = document.getElementById(winId);
  if (!win) return;
  win.style.display = "none";
  const myPillId = pillId || windowPillMap[winId];
  if (myPillId) {
    const pill = document.getElementById(myPillId);
    if (pill) pill.style.display = "none";
  }
}

function minimizeWindow(win) {
  if (!win) return;
  win.style.display = "none";
  win.classList.remove("active-win");
  const pillId = windowPillMap[win.id];
  if (pillId) {
    const pill = document.getElementById(pillId);
    if (pill) pill.classList.add("inactive");
  }
}

function toggleMaximize(win) {
  if (!win) return;
  const isMax = win.classList.toggle("maximized");
  const maxBtn = win.querySelector(".win-max-btn") || (win.id === "main-win" ? document.getElementById("btn-win-max") : null);
  if (isMax) {
    win.dataset.origLeft = win.style.left || "";
    win.dataset.origTop = win.style.top || "";
    win.dataset.origWidth = win.style.width || "";
    win.dataset.origHeight = win.style.height || "";
    win.dataset.origMaxWidth = win.style.maxWidth || "";
    win.dataset.origMargin = win.style.margin || "";
    win.dataset.origPosition = win.style.position || "";
    if (maxBtn) {
      maxBtn.textContent = "❐";
      maxBtn.title = "Restore";
    }
  } else {
    win.style.left = win.dataset.origLeft || "";
    win.style.top = win.dataset.origTop || "";
    win.style.width = win.dataset.origWidth || "";
    win.style.height = win.dataset.origHeight || "";
    win.style.maxWidth = win.dataset.origMaxWidth || "";
    win.style.margin = win.dataset.origMargin || "";
    win.style.position = win.dataset.origPosition || "";
    if (maxBtn) {
      maxBtn.textContent = "口";
      maxBtn.title = "Maximize";
    }
  }
  focusWindow(win);
}

// Window Dragging
function makeDraggable(win, handle) {
  if (!win || !handle) return;
  let ox = 0, oy = 0, dragging = false;
  handle.addEventListener("pointerdown", (e) => {
    if (e.target.closest("button") || e.target.closest("input")) return;
    if (win.classList.contains("maximized")) return;
    dragging = true;
    focusWindow(win);
    const rect = win.getBoundingClientRect();
    if (win.style.position !== "absolute") {
      win.style.position = "absolute";
      win.style.margin = "0";
      win.style.left = rect.left + "px";
      win.style.top = rect.top + "px";
      win.style.width = rect.width + "px";
    }
    ox = e.clientX - win.offsetLeft;
    oy = e.clientY - win.offsetTop;
    handle.setPointerCapture(e.pointerId);
  });
  handle.addEventListener("pointermove", (e) => {
    if (!dragging || win.classList.contains("maximized")) return;
    win.style.left = Math.max(0, e.clientX - ox) + "px";
    win.style.top = Math.max(0, e.clientY - oy) + "px";
  });
  const stop = () => { dragging = false; };
  handle.addEventListener("pointerup", stop);
  handle.addEventListener("pointercancel", stop);
}

// Draggable windows
[
  ["main-win", "win-drag-bar"],
  ["win-recycle", "drag-recycle"],
  ["win-tayne", "drag-tayne"],
  ["win-defrag", "drag-defrag"],
  ["win-lotus", "drag-lotus"],
  ["win-manual", "drag-manual"]
].forEach(([wId, hId]) => {
  const w = document.getElementById(wId);
  const h = document.getElementById(hId);
  if (w && h) makeDraggable(w, h);
});

// Click anywhere on a window to focus
document.querySelectorAll(".win-window").forEach((w) => {
  w.addEventListener("pointerdown", () => focusWindow(w));
});

// Window controls: min, max, close
document.querySelectorAll(".win-min-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const targetId = btn.dataset.target || btn.closest(".win-window")?.id;
    if (targetId) minimizeWindow(document.getElementById(targetId));
  });
});

document.querySelectorAll(".win-max-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const targetId = btn.dataset.target || btn.closest(".win-window")?.id;
    if (targetId) toggleMaximize(document.getElementById(targetId));
  });
});

document.querySelectorAll(".win-close-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const target = btn.dataset.target;
    if (target) {
      const elTarget = document.getElementById(target);
      if (elTarget) {
        if (elTarget.classList.contains("modal-overlay")) elTarget.classList.remove("open");
        else elTarget.style.display = "none";
      }
      const pill = document.getElementById(windowPillMap[target] || ("task-pill-" + target.replace("win-", "")));
      if (pill) pill.style.display = "none";
    }
  });
});

// Taskbar Pill Toggles
function setupTaskPill(pillId, winId) {
  const pill = document.getElementById(pillId);
  const win = document.getElementById(winId);
  if (!pill || !win) return;
  pill.addEventListener("click", () => {
    const isHidden = (win.style.display === "none" || getComputedStyle(win).display === "none");
    const isTop = (win.classList.contains("active-win") && !pill.classList.contains("inactive"));
    if (isHidden) {
      win.style.display = "flex";
      focusWindow(win, pillId);
    } else if (!isTop) {
      focusWindow(win, pillId);
    } else {
      minimizeWindow(win);
    }
  });
}

Object.entries(windowPillMap).forEach(([wId, pId]) => setupTaskPill(pId, wId));


// Setup Wizard Window Controls
$("btn-win-min")?.addEventListener("click", () => {
  const win = $("main-win");
  const pill = $("task-pill-main");
  if (win && pill) {
    win.style.display = "none";
    pill.classList.add("inactive");
  }
});

$("btn-win-close")?.addEventListener("click", () => {
  $("modal-exit-setup")?.classList.add("open");
});

$("cancel-btn")?.addEventListener("click", () => {
  $("modal-exit-setup")?.classList.add("open");
});

$("btn-win-help")?.addEventListener("click", () => {
  openWindow("win-manual", "task-pill-manual");
});

$("btn-exit-setup-yes")?.addEventListener("click", () => {
  window.location.href = "../";
});

$("btn-exit-setup-no")?.addEventListener("click", () => {
  $("modal-exit-setup")?.classList.remove("open");
});

// Desktop Icons
function setupDesktopIcon(id, winId, pillId, action) {
  const el = $(id);
  if (!el) return;
  el.addEventListener("click", () => {
    document.querySelectorAll(".desktop-icon").forEach((d) => d.classList.remove("active"));
    el.classList.add("active");
  });
  el.addEventListener("dblclick", () => {
    if (action) action();
    else if (winId) openWindow(winId, pillId);
  });
}

setupDesktopIcon("d-mycomp", "sysprop-modal", null, () => $("sysprop-modal")?.classList.add("open"));
setupDesktopIcon("d-app", null, null, () => { window.location.href = "../"; });
setupDesktopIcon("d-tayne", "win-tayne", "task-pill-tayne");
setupDesktopIcon("d-defrag", "win-defrag", "task-pill-defrag");
setupDesktopIcon("d-boss", "win-lotus", "task-pill-lotus");
setupDesktopIcon("d-installer", "main-win", "task-pill-main", () => {
  const win = $("main-win");
  if (win) {
    win.style.display = "flex";
    focusWindow(win, "task-pill-main");
  }
});
setupDesktopIcon("d-manual", "win-manual", "task-pill-manual");
setupDesktopIcon("d-recycle", "win-recycle", "task-pill-recycle");

// Start Menu Items
$("sm-app")?.addEventListener("click", () => { window.location.href = "../"; });
$("sm-setup")?.addEventListener("click", () => {
  const win = $("main-win");
  if (win) {
    win.style.display = "flex";
    focusWindow(win, "task-pill-main");
  }
});
$("sm-tayne")?.addEventListener("click", () => openWindow("win-tayne", "task-pill-tayne"));
$("sm-defrag")?.addEventListener("click", () => openWindow("win-defrag", "task-pill-defrag"));
$("sm-boss")?.addEventListener("click", () => openWindow("win-lotus", "task-pill-lotus"));
$("sm-manual")?.addEventListener("click", () => openWindow("win-manual", "task-pill-manual"));
$("sm-sysprop")?.addEventListener("click", () => $("sysprop-modal")?.classList.add("open"));
$("sm-about")?.addEventListener("click", () => $("about-modal")?.classList.add("open"));
$("sm-shutdown")?.addEventListener("click", () => $("modal-shutdown")?.classList.add("open"));

// Dialog Buttons
$("modal-ok")?.addEventListener("click", () => $("about-modal")?.classList.remove("open"));
$("sysprop-ok")?.addEventListener("click", () => $("sysprop-modal")?.classList.remove("open"));
$("btn-coffee-ok")?.addEventListener("click", () => $("modal-coffee")?.classList.remove("open"));

// Tayne Studio 98 Actions
let tayneHardwareSync = false;
let tayneSpeedBoosted = false;

function playTayneSound(key) {
  try {
    const src = TAYNE_ASSETS[key];
    if (src) {
      const a = new Audio(src);
      a.volume = 0.8;
      a.play().catch(() => {});
    }
  } catch (e) {}
}

function setTayneStage(imgKey, badgeText, soundKey, synthAction) {
  const stageImg = document.getElementById("tayne-stage-img");
  const receiptBox = document.getElementById("tayne-receipt-box");
  const badge = document.getElementById("tayne-status-card");
  
  if (receiptBox) receiptBox.style.display = "none";
  if (stageImg && TAYNE_ASSETS[imgKey]) {
    stageImg.src = TAYNE_ASSETS[imgKey];
  }
  if (badge && badgeText) badge.textContent = badgeText;
  if (soundKey) playTayneSound(soundKey);
  
  if (tayneHardwareSync && typeof synthAction === "function") {
    synthAction();
  }
}

// Initialize stage images
const initialStageImg = document.getElementById("tayne-stage-img");
if (initialStageImg && TAYNE_ASSETS.idle) {
  initialStageImg.src = TAYNE_ASSETS.idle;
}
const receiptImg = document.getElementById("tayne-receipt-img");
if (receiptImg && TAYNE_ASSETS.oyster) {
  receiptImg.src = TAYNE_ASSETS.oyster;
}

// Routine buttons
document.getElementById("btn-tayne-load")?.addEventListener("click", () => {
  const stage = document.getElementById("tayne-stage");
  if (stage) stage.classList.remove("pulse-4d3d");
  tayneSpeedBoosted = false;
  setTayneStage("idle", "Dancer Sequence Loaded", "snd_tayne", () => {
    if (typeof turnKnob === "function") turnKnob("PRESETS", 1);
  });
});

document.getElementById("btn-tayne-wobble")?.addEventListener("click", () => {
  setTayneStage("wobble", "HAT WOBBLE", "snd_wobble", () => {
    if (typeof pressBtn === "function") pressBtn("LFO");
  });
});

document.getElementById("btn-tayne-flarh")?.addEventListener("click", () => {
  setTayneStage("flarh", "FLARHGUNNSTOW", "snd_flarh", () => {
    if (typeof pressBtn === "function") pressBtn("ARP");
  });
});

document.getElementById("btn-tayne-speed")?.addEventListener("click", () => {
  const stage = document.getElementById("tayne-stage");
  const badge = document.getElementById("tayne-status-card");
  tayneSpeedBoosted = !tayneSpeedBoosted;
  if (stage) stage.classList.toggle("pulse-4d3d", tayneSpeedBoosted);
  if (badge) badge.textContent = tayneSpeedBoosted ? "4D3D3D3 ENGAGED ⚡" : "4d3d3d3 Speed Standard";
  playTayneSound("snd_4d3d");
  if (tayneHardwareSync && typeof turnKnob === "function") {
    turnKnob("KNOB 1", 10);
  }
});

// Nude Tayne with confirmation modal
document.getElementById("btn-tayne-nude")?.addEventListener("click", () => {
  document.getElementById("modal-confirm-nude")?.classList.add("open");
});

document.getElementById("btn-nude-cancel")?.addEventListener("click", () => {
  document.getElementById("modal-confirm-nude")?.classList.remove("open");
});

document.getElementById("btn-nude-ok")?.addEventListener("click", () => {
  document.getElementById("modal-confirm-nude")?.classList.remove("open");
  setTayneStage("nude", "NUDE TAYNE (NSFW)", "snd_nsfw", () => {
    if (typeof pressBtn === "function") pressBtn("FX");
  });
});

// Print Oyster receipt
document.getElementById("btn-tayne-receipt")?.addEventListener("click", () => {
  const receiptBox = document.getElementById("tayne-receipt-box");
  const badge = document.getElementById("tayne-status-card");
  if (receiptBox) receiptBox.style.display = "flex";
  if (badge) badge.textContent = "OYSTER RECEIPT";
  playTayneSound("snd_printout");
  if (tayneHardwareSync && typeof pressBtn === "function") {
    pressBtn("SAVE");
  }
});

document.getElementById("btn-close-receipt")?.addEventListener("click", () => {
  const receiptBox = document.getElementById("tayne-receipt-box");
  if (receiptBox) receiptBox.style.display = "none";
  const badge = document.getElementById("tayne-status-card");
  if (badge) badge.textContent = "Dancer Sequence Loaded";
});

// Soundboard buttons
document.querySelectorAll(".tayne-snd-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const snd = btn.dataset.sound;
    if (snd) playTayneSound(snd);
  });
});

// Sync to FM-1 Hardware toggle
const syncBtn = document.getElementById("btn-tayne-sync");
if (syncBtn) {
  syncBtn.addEventListener("click", () => {
    tayneHardwareSync = !tayneHardwareSync;
    syncBtn.textContent = tayneHardwareSync ? "Sync to FM-1 Hardware [ACTIVE ●]" : "Sync to FM-1 Hardware ▶";
    syncBtn.style.background = tayneHardwareSync ? "#000080" : "#e0e0e0";
    syncBtn.style.color = tayneHardwareSync ? "#ffffff" : "#000000";
    if (tayneHardwareSync) {
      const badge = document.getElementById("tayne-status-card");
      if (badge && badge.textContent.includes("WOBBLE") && typeof pressBtn === "function") pressBtn("LFO");
      else if (badge && badge.textContent.includes("FLARH") && typeof pressBtn === "function") pressBtn("ARP");
      else if (typeof turnKnob === "function") turnKnob("PRESETS", 1);
    }
  });
}


// Recycle Bin Incineration
$("btn-empty-recycle")?.addEventListener("click", () => {
  $("modal-confirm-recycle")?.classList.add("open");
});
$("btn-confirm-recycle-no")?.addEventListener("click", () => {
  $("modal-confirm-recycle")?.classList.remove("open");
});
$("btn-confirm-recycle-yes")?.addEventListener("click", () => {
  const tbody = $("recycle-tbody");
  if (tbody) tbody.innerHTML = "";
  const count = $("recycle-status-count");
  const size = $("recycle-status-size");
  if (count) count.textContent = "0 object(s)";
  if (size) size.textContent = "0 KB";
  $("modal-confirm-recycle")?.classList.remove("open");
});

// Cinco Defrag Cluster Grid Simulation
const defragGrid = $("defrag-cluster-grid");
if (defragGrid) {
  defragGrid.innerHTML = "";
  for (let i = 0; i < 160; i++) {
    const box = document.createElement("div");
    box.className = "cluster-box " + (i % 7 === 0 ? "cluster-frag" : i % 5 === 0 ? "cluster-unmov" : i % 2 === 0 ? "cluster-alloc" : "cluster-free");
    defragGrid.appendChild(box);
  }
}

// Shut Down Routine
$("btn-shutdown-cancel")?.addEventListener("click", () => $("modal-shutdown")?.classList.remove("open"));
$("btn-shutdown-help")?.addEventListener("click", () => openWindow("win-manual", "task-pill-manual"));
$("btn-shutdown-ok")?.addEventListener("click", () => {
  $("modal-shutdown")?.classList.remove("open");
  const off = $("shutdown-opt-off");
  const restart = $("shutdown-opt-restart");
  const dos = $("shutdown-opt-dos");
  if (off && off.checked) {
    $("screen-shutdown")?.classList.add("open");
  } else if (restart && restart.checked) {
    window.location.reload();
  } else if (dos && dos.checked) {
    $("screen-dos")?.classList.add("open");
    $("dos-input")?.focus();
  }
});

$("btn-turn-on")?.addEventListener("click", () => {
  $("screen-shutdown")?.classList.remove("open");
});

// MS-DOS 7.10 Interactive CLI
let dosFormatPrompt = false;

function scrollToDosBottom() {
  const dosScreen = document.getElementById("screen-dos");
  if (dosScreen) dosScreen.scrollTop = dosScreen.scrollHeight;
}

function appendDosLine(text, color) {
  const hist = document.getElementById("dos-history");
  if (!hist) return;
  const div = document.createElement("div");
  div.className = "dos-line";
  div.textContent = text;
  if (color) div.style.color = color;
  hist.appendChild(div);
}

function appendDosBlock(lines) {
  lines.forEach((l) => appendDosLine(l));
}

const dosInput = document.getElementById("dos-input");
const dosScreen = document.getElementById("screen-dos");
if (dosScreen && dosInput) {
  dosScreen.addEventListener("click", () => dosInput.focus());
}

if (dosInput) {
  dosInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const raw = dosInput.value;
      const trimmed = raw.trim();
      dosInput.value = "";

      if (dosFormatPrompt) {
        appendDosLine("C:\\CINCO> " + raw);
        if (trimmed.toLowerCase() === "y") {
          appendDosBlock([
            "Formatting 4d3d3d3.00 MB...",
            "Format complete.",
            "",
            "Error writing partition table: Volume is locked by Managing Director Paul.",
            "Cinco Business Systems Protection: \"Now Tayne I can get into.\""
          ]);
        } else {
          appendDosLine("Format aborted.");
        }
        dosFormatPrompt = false;
        scrollToDosBottom();
        return;
      }

      appendDosLine("C:\\CINCO> " + raw);
      if (!trimmed) {
        scrollToDosBottom();
        return;
      }

      const parts = trimmed.split(/\s+/);
      const cmd = parts[0].toLowerCase();
      const arg = parts.slice(1).join(" ").toLowerCase();

      switch (cmd) {
        case "cls":
          const hist = document.getElementById("dos-history");
          if (hist) hist.innerHTML = "";
          break;

        case "ver":
          appendDosLine("MS-DOS Version 7.10 (Cinco Business Systems Corp. 1981-1998)");
          break;

        case "help":
          appendDosBlock([
            "Cinco MS-DOS 7.10 Commands:",
            "  HELP          Display list of commands",
            "  DIR           Display files in C:\\CINCO",
            "  TYPE [file]   Display file contents (e.g. TYPE PAUL.TXT)",
            "  MEM           Show system memory report",
            "  VER           Display MS-DOS version",
            "  CLS           Clear screen",
            "  CELERY        Launch Celery Man routine",
            "  TAYNE         Launch Tayne routine",
            "  4D3D3D3       Engage 4d3d3d3 kinetic acceleration",
            "  OYSTER        Print Oyster receipt",
            "  NUDE          Access restricted dancer asset (NSFW)",
            "  FORMAT C:     Format fixed disk drive",
            "  WIN or EXIT   Return to Windows 98 desktop"
          ]);
          break;

        case "dir":
          appendDosBlock([
            " Volume in drive C is CINCO_OS",
            " Volume Serial Number is 4D3D-3D3D",
            " Directory of C:\\CINCO",
            "",
            ".              <DIR>        04-20-98   4:20p",
            "..             <DIR>        04-20-98   4:20p",
            "CELERY   EXE        57,344  05-12-98   9:15a",
            "TAYNE    COM        18,432  06-01-98   2:30p",
            "4D3D3D3  EXE        98,304  07-14-98  11:45a",
            "OYSTER   PRN        12,288  08-22-98   3:12p",
            "AUTOEXEC BAT           186  09-01-98   8:00a",
            "CONFIG   SYS           162  09-01-98   8:00a",
            "NUDE     DAT        69,420  09-15-98  12:00a",
            "PAUL     TXT           348  10-02-98   1:15p",
            "         8 file(s)        256,484 bytes",
            "         2 dir(s)      14,336,000 bytes free"
          ]);
          break;

        case "type":
          if (arg === "paul.txt") {
            appendDosBlock([
              "--- C:\\CINCO\\PAUL.TXT ---",
              "FROM: Paul (Managing Director, Cinco Business Systems)",
              "TO: Workstation Operator #555",
              "DATE: October 2, 1998",
              "SUBJECT: 4d3d3d3 Expansion & Tayne Beta Deployment",
              "",
              "Please ensure the Celery Man sequences are initialized before 5:00 PM.",
              "Under NO circumstances should Nude Tayne be displayed in the executive suite.",
              "Could I see a hat wobble? And a flarhgunnstow?",
              "",
              "Computer, load up Celery Man."
            ]);
          } else if (arg === "autoexec.bat") {
            appendDosBlock([
              "--- C:\\AUTOEXEC.BAT ---",
              "@ECHO OFF",
              "PROMPT $P$G",
              "PATH C:\\CINCO;C:\\DOS;C:\\WINDOWS",
              "SET SOUND=C:\\CINCO\\LPC10",
              "LH C:\\CINCO\\4D3D3D3.EXE /HIGH",
              "C:\\CINCO\\TAYNE.COM /AUTORUN"
            ]);
          } else if (arg === "config.sys") {
            appendDosBlock([
              "--- C:\\CONFIG.SYS ---",
              "DEVICE=C:\\DOS\\HIMEM.SYS",
              "DEVICE=C:\\DOS\\EMM386.EXE NOEMS",
              "DOS=HIGH,UMB",
              "FILES=40",
              "BUFFERS=40",
              "DEVICEHIGH=C:\\CINCO\\DRIVERS\\CELERY.SYS /V"
            ]);
          } else if (arg === "nude.dat") {
            appendDosBlock([
              "ACCESS DENIED: NUDE.DAT is encrypted with Cinco 4d3d3d3 security algorithm.",
              "Security incident reported to Paul."
            ]);
          } else if (arg === "oyster.prn") {
            appendDosBlock([
              "--- C:\\CINCO\\OYSTER.PRN (DOT MATRIX SPOOL) ---",
              "========================================",
              " CINCO IDENTITY RECEIPT: OYSTER (SMILING)",
              " TRANSACTION #4D3D-98",
              " STATUS: VERIFIED OK",
              "========================================"
            ]);
          } else if (!arg) {
            appendDosLine("Required parameter missing.");
          } else {
            appendDosLine("File not found - " + arg.toUpperCase());
          }
          break;

        case "mem":
          appendDosBlock([
            "Memory Type         Total       Used       Free",
            "----------------  --------   --------   --------",
            "Conventional          640K        82K       558K",
            "Upper (UMB)           128K        34K        94K",
            "Extended (XMS)     16,384K     2,048K    14,336K",
            "Expanded (EMS)     4d3d3d3K   4d3d3d3K        0K",
            "----------------  --------   --------   --------",
            "Total memory       17,152K     2,164K    14,988K",
            "",
            "Largest executable program size:       558K (571,392 bytes)",
            "Largest free upper memory block:        94K  (96,256 bytes)",
            "MS-DOS is resident in the high memory area."
          ]);
          break;

        case "format":
          if (arg === "c:" || arg === "c") {
            appendDosBlock([
              "WARNING: ALL DATA ON FIXED DISK DRIVE C: WILL BE LOST!",
              "Proceed with Format (Y/N)?"
            ]);
            dosFormatPrompt = true;
          } else {
            appendDosLine("Invalid drive specification.");
          }
          break;

        case "celery":
          appendDosBlock([
            "Executing CELERY.EXE...",
            "Loading Celery Man identity sequence into memory...",
            "Computer: Celery Man loaded."
          ]);
          playTayneSound("snd_yes");
          if (typeof turnKnob === "function") turnKnob("PRESETS", 1);
          break;

        case "tayne":
          appendDosBlock([
            "Executing TAYNE.COM...",
            "Tayne Studio 98 (Beta Edition) dancer sequence active.",
            "\"Now Tayne I can get into.\""
          ]);
          playTayneSound("snd_tayne");
          if (typeof turnKnob === "function") turnKnob("PRESETS", 1);
          break;

        case "4d3d3d3":
          appendDosBlock([
            "Executing 4D3D3D3.EXE...",
            "Kinetic acceleration registers primed: 4d3d3d3 ENGAGED."
          ]);
          playTayneSound("snd_4d3d");
          if (typeof turnKnob === "function") turnKnob("KNOB 1", 10);
          break;

        case "oyster":
          appendDosBlock([
            "Printing Oyster Smiling verification slip to OYSTER.PRN...",
            "Spooler ready. Oyster receipt sent to printer."
          ]);
          playTayneSound("snd_printout");
          if (typeof pressBtn === "function") pressBtn("SAVE");
          break;

        case "nude":
          appendDosBlock([
            "WARNING: Accessing NUDE.DAT...",
            "Cinco Security: Not suitable for work. Incident logged."
          ]);
          playTayneSound("snd_nsfw");
          if (typeof pressBtn === "function") pressBtn("FX");
          break;

        case "win":
        case "exit":
          document.getElementById("screen-dos")?.classList.remove("open");
          break;

        default:
          appendDosLine("Bad command or file name");
          break;
      }
      scrollToDosBottom();
    }
  });
}

document.getElementById("btn-dos-exit")?.addEventListener("click", () => {
  document.getElementById("screen-dos")?.classList.remove("open");
});


// Systray Volume Popup
$("systray-vol")?.addEventListener("click", (e) => {
  e.stopPropagation();
  $("volume-popup")?.classList.toggle("open");
});
$("vol-popup-close")?.addEventListener("click", () => {
  $("volume-popup")?.classList.remove("open");
});

// CINCO Manual TOC Switching
const MANUAL_SECTIONS = {
  "toc-welcome": "<h3>Welcome to Cinco Identity Generator 2.5™</h3><p>This workstation runs custom Cinco OS 2.5 firmware for the M-VAVE FM-1 Synthesizer Terminal, featuring 4d3d3d3 window cascading, rotoscoped SCUMM dancers, and LPC speech synthesis.</p>",
  "toc-controls": "<h3>Workstation & Synthesizer Controls</h3><p>Use keys Z through / for the lower manual, Q through O for the upper manual. Number keys 1-6 trigger row 1 buttons (FX, SCL, ENV, LFO, EDIT, GLO). Press [ and ] for octave shifts.</p>",
  "toc-identities": "<h3>Cinco Identity Routines</h3><p>Rotate PRESETS encoder to toggle dancer routines: Celery Man (default 4d3d3d3 sequence), Oyster Smiling, and Tayne (Beta). Press GLO for phonetic LPC speech generation.</p>",
  "toc-kinetics": "<h3>Kinetic Modulation (4d3d3d3)</h3><p>Engage Hat Wobble with LFO key (4). Flarhgunnstow arpeggiation mode engages with ARP key (9). Kick up the 4d3d3d3 with Macro Knob 1.</p>",
  "toc-boss": "<h3>Lotus 1-2-3 Stealth Boss Key</h3><p>Press EDIT key or Tools &gt; Lotus 1-2-3 to instantly summon corporate spreadsheet cover mode. Total corporate allocation: $32,820,000.</p>",
  "toc-osha": "<h3>OSHA Compliance Guidelines</h3><p>15-minute executive espresso recesses are mandatory under Cinco corporate policy. Maintain safe distance from Celery Man kinetic routines.</p>"
};

document.querySelectorAll(".manual-toc-item").forEach((item) => {
  item.addEventListener("click", () => {
    document.querySelectorAll(".manual-toc-item").forEach((i) => i.classList.remove("selected"));
    item.classList.add("selected");
    const view = $("manual-content-view");
    if (view && MANUAL_SECTIONS[item.id]) {
      view.innerHTML = MANUAL_SECTIONS[item.id];
    }
  });
});

// In-Universe Confirm Dialog for Factory Restore
function confirmStockModal() {
  return new Promise((resolve) => {
    const modal = $("modal-confirm-stock");
    const msg = $("confirm-stock-msg");
    if (msg) msg.textContent = t("stockConfirm");
    modal.classList.add("open");
    const cleanup = (res) => {
      modal.classList.remove("open");
      $("btn-confirm-stock-yes").removeEventListener("click", onYes);
      $("btn-confirm-stock-no").removeEventListener("click", onNo);
      $("btn-confirm-stock-x").removeEventListener("click", onNo);
      resolve(res);
    };
    const onYes = () => cleanup(true);
    const onNo = () => cleanup(false);
    $("btn-confirm-stock-yes").addEventListener("click", onYes);
    $("btn-confirm-stock-no").addEventListener("click", onNo);
    $("btn-confirm-stock-x").addEventListener("click", onNo);
  });
}

// ------------------------------------------------------------------ SysEx Installer Core
const sayK = (k, arg = "") => {
  lastKey = k;
  lastArg = arg;
  $("status").textContent = t(k) + arg;
};
const say = (txt) => {
  lastKey = null;
  $("status").textContent = txt;
};
const log = (msg) => {
  $("log").textContent += msg + "\\n";
  $("log").scrollTop = $("log").scrollHeight;
};

let image = null;
const meta = {
  version: "v2.5",
  product: "FM-1_555",
  pkg: "../firmware/cinco.fwsc"
};

let writing = false, stock = null, stockFileEpoch = 0;
const lockInstaller = (on) => {
  writing = on;
  $("go").disabled = on || !image;
  $("stock-go").disabled = on || !stock;
  $("stock-file").disabled = on;
  $("stock-recovery").disabled = on;
};

window.addEventListener("beforeunload", (e) => {
  if (writing) {
    e.preventDefault();
    e.returnValue = t("leave");
  }
});

(async () => {
  if (!navigator.requestMIDIAccess) {
    sayK("nomidi");
    return;
  }
  try {
    say("Loading Cinco 2.5 package (cinco.fwsc)...");
    const r = await fetch(meta.pkg);
    if (!r.ok) throw new Error(`${meta.pkg}: HTTP ${r.status}`);
    const pkg = new Uint8Array(await r.arrayBuffer());
    if (productOf(pkg) !== meta.product) {
      sayK("badpkg");
      return;
    }
    image = logicalImage(pkg);
    say(`Cinco Identity Generator ${meta.version} (cinco.fwsc) — Ready to install`);
    $("go").disabled = false;
  } catch (e) {
    sayK("loadfail", e.message);
  }
})();

$("go").addEventListener("click", async () => {
  if (writing) return;
  lockInstaller(true);
  let midi;
  try {
    midi = await navigator.requestMIDIAccess({ sysex: true });
  } catch (e) {
    sayK("denied");
    lockInstaller(false);
    return;
  }

  try {
    const up = new Updater(midi, log);
    const total = 74 + 1167;
    const step = (k, a) => {
      log(`${k} ${a ?? ""}`);
      if (k === "start") sayK("start");
      if (k === "verify") {
        sayK("verify");
        $("bar").value = (a / total) * 100;
      }
      if (k === "loader") sayK("loader");
      if (k === "write") {
        sayK("write");
        $("bar").value = ((74 + a) / total) * 100;
      }
      if (k === "reboot") sayK("reboot");
      if (k === "done") {
        $("bar").value = 100;
        sayK("done");
      }
    };

    const ota = await up.find((id) => /^ota-/i.test(id.model));
    if (ota) {
      ota.link.close();
      sayK((await up.resume(image, step, meta.product)) ? "done" : "stopped");
    } else {
      await up.install(image, meta.product, step);
    }
  } catch (e) {
    if (e && e.code && TEXT[lang][e.code]) sayK(e.code, e.detail || "");
    else sayK("error", e && e.message);
    log(String((e && e.stack) || e));
  }
  lockInstaller(false);
});

$("stock-file").addEventListener("change", async () => {
  const epoch = ++stockFileEpoch, file = $("stock-file").files[0];
  stock = null;
  lockInstaller(false);
  if (!file) return;
  try {
    if (file.size !== STOCK_V15_SIZE) throw new Error("File size does not match official FM-1 V15");
    const verified = await validateStockPackage(new Uint8Array(await file.arrayBuffer()));
    if (epoch !== stockFileEpoch) return;
    stock = verified;
    sayK("stockValid");
    lockInstaller(false);
  } catch (e) {
    if (epoch === stockFileEpoch) sayK("stockError", e.message);
  }
});

function saveArchive(archive) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(archive)], { type: "application/json" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = `Cinco-backup-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function archiveInfo(a) {
  let pos = a.indexOf(0);
  if (pos < 0) throw new Error("Invalid INFO header");
  const version = String.fromCharCode(...a.slice(0, pos));
  pos++;
  const engines = a[pos];
  pos += 5;
  for (let i = 0; i < engines; i++) {
    const end = a.indexOf(0, pos);
    if (end < 0) throw new Error("Invalid INFO header");
    pos = end + 1;
  }
  const ext = a.slice(pos + 1);
  const supported = (/^FELUCCA /i.test(version) || /^CINCO /i.test(version)) &&
    ext[0] === 16 && ext[1] === 0x55 && ext[2] === 1 &&
    ext[4] === 0x4d && ext[5] === 1 && ext[8] === 0x42 && ext[9] === 1 && (ext[10] & 1);
  return { version, supported };
}

$("stock-go").addEventListener("click", async () => {
  if (!stock || writing) return;
  const selected = stock;
  lockInstaller(true);
  let link = null;
  try {
    let midi;
    try {
      midi = await navigator.requestMIDIAccess({ sysex: true });
    } catch (e) {
      sayK("denied");
      return;
    }
    const up = new Updater(midi, log);
    const step = (k, n) => {
      log(`${k} ${n ?? ""}`);
      if (["start", "verify", "loader", "write", "reboot", "done"].includes(k)) sayK(k);
      if (k === "done") $("bar").value = 100;
    };
    const loader = await up.find((id) => id.model === "ota-FM-1");
    if (loader) {
      loader.link.close();
      if (!$("stock-recovery").checked) {
        sayK("stockNeedBackup");
        return;
      }
      if (!(await confirmStockModal())) return;
      sayK((await up.resume(selected.image, step, selected.product)) ? "done" : "stopped");
    } else {
      const device = await up.find((id) => id.model === "FM-1");
      if (!device) {
        sayK("notfound");
        return;
      }
      const input = device.link.input, output = device.link.output;
      device.link.close();
      link = new BackupConnection(input, output);
      const info = archiveInfo(await link.request([1, []]));
      if (!info.supported) {
        sayK("stockUnsupported");
        return;
      }
      const archive = await captureBackup(
        (r, o) => link.request(r, o),
        info.version,
        (done, total) => sayK("backup", `${Math.round((done / Math.max(1, total)) * 100)}%`)
      );
      saveArchive(archive);
      link.close();
      link = null;
      if (!(await confirmStockModal())) return;
      await up.install(selected.image, selected.product, step);
    }
  } catch (e) {
    if (e.code && TEXT[lang][e.code]) sayK(e.code, e.detail || "");
    else sayK("error", e.message);
    log(String(e.stack || e));
  } finally {
    if (link) link.close();
    lockInstaller(false);
  }
});
</script>
</body>
</html>
"""

html_content = template.replace("/*COMBINED_LIB_PLACEHOLDER*/", f"{combined_lib}\n\n{get_tayne_assets_js()}")

output_path = web_dir / "cinco_installer.html"
output_path.write_text(html_content, encoding="utf-8")
print(f"Generated {output_path} ({len(html_content)} bytes)")
