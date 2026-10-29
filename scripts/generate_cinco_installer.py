#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Cinco Identity Generator 2.5™ Web Installer Generator
# Cinco Business Systems, Inc. [v2.5] (Celery Man Edition)
# Generates web/cinco_installer.html with authentic Windows 98 Setup Wizard UI
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

template = """<!doctype html>
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
    --win-darker: #0a0a0a;
    --win-blue: #000080;
    --win-blue-light: #1084d0;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 20px 10px 48px;
    background-color: var(--win-bg);
    color: #000000;
    font-family: "MS Sans Serif", Tahoma, "Segoe UI", Arial, sans-serif;
    font-size: 11px;
    line-height: 1.4;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  /* Desktop Icons on Teal Background */
  .desktop-icons {
    position: fixed;
    top: 16px;
    left: 16px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    z-index: 5;
    user-select: none;
  }
  .desktop-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 74px;
    text-align: center;
    cursor: pointer;
    text-decoration: none;
    color: #ffffff;
    font-size: 11px;
    font-family: "MS Sans Serif", Tahoma, sans-serif;
    text-shadow: 1px 1px 1px #000000;
  }
  .desktop-icon svg {
    margin-bottom: 3px;
    filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.6));
  }
  .desktop-icon span {
    padding: 1px 3px;
    border-radius: 1px;
    word-break: break-word;
    line-height: 1.2;
  }
  .desktop-icon:hover span,
  .desktop-icon:focus span {
    background: var(--win-blue);
    outline: 1px dotted #ffff80;
  }

  /* Main Windows 98 Setup Window */
  .win98-window {
    width: 580px;
    max-width: 96vw;
    background: var(--win-gray);
    border: 1px solid #000000;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark),
                2px 2px 8px rgba(0, 0, 0, 0.4);
    padding: 3px;
    margin: auto 0 16px;
    position: relative;
    z-index: 20;
  }

  /* Title Bar */
  .win98-titlebar {
    background: linear-gradient(90deg, var(--win-blue) 0%, var(--win-blue-light) 100%);
    height: 22px;
    padding: 2px 3px 2px 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    user-select: none;
  }
  .win98-title-left {
    display: flex;
    align-items: center;
    gap: 5px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .win98-title-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }
  .win98-title-text {
    color: #ffffff;
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 0.2px;
  }
  .win98-title-controls {
    display: flex;
    align-items: center;
    gap: 2px;
  }
  .win98-title-btn {
    width: 16px;
    height: 14px;
    background: var(--win-gray);
    border: none;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark);
    font-family: "MS Sans Serif", Tahoma, sans-serif;
    font-size: 9px;
    font-weight: bold;
    line-height: 12px;
    text-align: center;
    color: #000000;
    cursor: pointer;
    padding: 0;
  }
  .win98-title-btn:active {
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
    padding: 1px 0 0 1px;
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
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-dark), inset -1px -1px var(--win-light);
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
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
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
  progress#bar::-webkit-progress-bar {
    background: #ffffff;
  }
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
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
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

  /* Log Terminal Box (DOS Command Prompt sunken black window) */
  #log {
    background: #000000;
    color: #00ff66;
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
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

  /* Windows 98 Authentic Buttons */
  .win98-btn {
    background: var(--win-gray);
    color: #000000;
    font-family: "MS Sans Serif", Tahoma, "Segoe UI", Arial, sans-serif;
    font-size: 11px;
    padding: 3px 12px;
    min-width: 75px;
    min-height: 23px;
    border: 1px solid #000000;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark);
    cursor: pointer;
    outline: none;
    user-select: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    box-sizing: border-box;
    text-align: center;
  }
  .win98-btn:active:not(:disabled),
  .win98-btn.pressed {
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
    padding: 4px 11px 2px 13px;
  }
  .win98-btn:focus-visible {
    outline: 1px dotted #000000;
    outline-offset: -4px;
  }
  .win98-btn:disabled {
    color: var(--win-dark);
    text-shadow: 1px 1px 0 var(--win-light);
    cursor: default;
  }
  .win98-btn-default {
    font-weight: bold;
    border: 2px solid #000000;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark);
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

  /* Dialog Status Bar (3 Sunken Segments) */
  .win98-statusbar {
    display: flex;
    gap: 2px;
    margin-top: 6px;
    font-size: 10.5px;
    user-select: none;
  }
  .statusbar-cell {
    background: var(--win-gray);
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-dark), inset -1px -1px var(--win-light);
    padding: 2px 6px;
    color: #222222;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Fixed Windows 98 Taskbar */
  .win98-taskbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 28px;
    background: var(--win-gray);
    border-top: 2px solid var(--win-light);
    box-shadow: inset 0 1px 0 var(--win-lighter);
    display: flex;
    align-items: center;
    padding: 2px 3px;
    z-index: 10000;
    user-select: none;
  }
  .win98-start-btn {
    height: 22px;
    background: var(--win-gray);
    border: 1px solid #000000;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark);
    font-family: "MS Sans Serif", Tahoma, sans-serif;
    font-size: 11px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 1px 6px 1px 4px;
    cursor: pointer;
    outline: none;
  }
  .win98-start-btn:active,
  .win98-start-btn.pressed {
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
    padding: 2px 5px 0 5px;
  }
  .taskbar-divider {
    width: 2px;
    height: 18px;
    border-left: 1px solid var(--win-dark);
    border-right: 1px solid var(--win-light);
    margin: 0 4px;
  }
  .taskbar-app {
    height: 22px;
    background: #e0e0e0;
    border: 1px solid #000000;
    box-shadow: inset 1px 1px var(--win-darker), inset -1px -1px var(--win-light),
                inset 2px 2px var(--win-dark), inset -2px -2px var(--win-lighter);
    font-family: "MS Sans Serif", Tahoma, sans-serif;
    font-size: 11px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 1px 8px;
    max-width: 190px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .taskbar-tray {
    margin-left: auto;
    height: 22px;
    background: var(--win-gray);
    border: 1px solid var(--win-dark);
    box-shadow: inset 1px 1px var(--win-dark), inset -1px -1px var(--win-light);
    padding: 2px 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: "MS Sans Serif", Tahoma, monospace;
    font-size: 11px;
  }

  /* Start Menu Popup */
  .win98-start-menu {
    position: fixed;
    bottom: 28px;
    left: 2px;
    width: 230px;
    background: var(--win-gray);
    border: 1px solid #000000;
    box-shadow: inset 1px 1px var(--win-light), inset -1px -1px var(--win-darker),
                inset 2px 2px var(--win-lighter), inset -2px -2px var(--win-dark),
                3px 3px 10px rgba(0,0,0,0.5);
    display: none;
    z-index: 10001;
    font-family: "MS Sans Serif", Tahoma, sans-serif;
    font-size: 11px;
  }
  .win98-start-menu.open {
    display: flex;
  }
  .start-menu-sidebar {
    width: 26px;
    background: linear-gradient(180deg, var(--win-blue) 0%, var(--win-blue-light) 100%);
    display: flex;
    align-items: flex-end;
    padding: 8px 4px;
    color: #ffffff;
    font-weight: bold;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    letter-spacing: 2px;
    font-size: 13px;
    user-select: none;
  }
  .start-menu-items {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 3px 1px;
  }
  .start-menu-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    text-decoration: none;
    color: #000000;
    cursor: pointer;
  }
  .start-menu-item:hover {
    background: var(--win-blue);
    color: #ffffff;
  }
  .start-menu-divider {
    height: 1px;
    background: var(--win-dark);
    border-bottom: 1px solid var(--win-light);
    margin: 3px 1px;
  }

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
  .footer-links a:hover {
    color: #ffff80;
  }

  @media (max-width: 768px) {
    .desktop-icons {
      display: none;
    }
    .win98-window {
      width: 100%;
      max-width: 100%;
      margin: 0 0 16px;
    }
    .hw-grid {
      grid-template-columns: 1fr;
    }
    .banner-pc-art {
      display: none;
    }
  }
</style>
</head>
<body>

<!-- Windows 98 Desktop Icons -->
<div class="desktop-icons" aria-label="Desktop Shortcuts">
  <div class="desktop-icon" tabindex="0" onclick="alert('Cinco Identity Generator 2.5 Workstation\nDestination Terminal: M-VAVE FM-1 (AC7916A)')">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <rect x="4" y="3" width="24" height="18" rx="2" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
      <rect x="7" y="6" width="18" height="12" fill="#008080"/>
      <rect x="13" y="21" width="6" height="4" fill="#808080"/>
      <rect x="8" y="25" width="16" height="4" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
    </svg>
    <span>My Computer</span>
  </div>

  <div class="desktop-icon" tabindex="0" onclick="alert('WebMIDI Network Neighborhood\nProtocol: Direct SysEx Over USB')">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <rect x="2" y="4" width="16" height="12" rx="1" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
      <rect x="4" y="6" width="12" height="8" fill="#000080"/>
      <rect x="14" y="14" width="16" height="12" rx="1" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
      <rect x="16" y="16" width="12" height="8" fill="#000080"/>
      <line x1="10" y1="20" x2="10" y2="28" stroke="#000" stroke-width="2"/>
      <line x1="22" y1="26" x2="22" y2="28" stroke="#000" stroke-width="2"/>
      <line x1="6" y1="28" x2="26" y2="28" stroke="#000" stroke-width="2"/>
    </svg>
    <span>Network</span>
  </div>

  <div class="desktop-icon" tabindex="0" onclick="alert('Recycle Bin (0 items discarded)')">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <path d="M8 8 L10 28 L22 28 L24 8 Z" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
      <ellipse cx="16" cy="8" rx="8" ry="3" fill="#a0a0a0" stroke="#000" stroke-width="1"/>
      <line x1="12" y1="12" x2="13" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="16" y1="12" x2="16" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="20" y1="12" x2="19" y2="24" stroke="#808080" stroke-width="1.5"/>
    </svg>
    <span>Recycle Bin</span>
  </div>

  <a class="desktop-icon" href="../" title="Launch Web Browser Emulator">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <rect x="3" y="3" width="26" height="20" rx="2" fill="#202020" stroke="#00ff66" stroke-width="1"/>
      <rect x="6" y="6" width="20" height="14" fill="#001a00"/>
      <text x="8" y="16" fill="#00ff66" font-family="monospace" font-size="8" font-weight="bold">CELERY</text>
      <rect x="12" y="23" width="8" height="3" fill="#555"/>
      <rect x="8" y="26" width="16" height="3" fill="#202020" stroke="#00ff66" stroke-width="1"/>
    </svg>
    <span>Paul's PC</span>
  </a>

  <a class="desktop-icon" href="../firmware/cinco.fwsc" download title="Download Firmware Package">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <path d="M6 3 L22 3 L26 7 L26 29 L6 29 Z" fill="#000080" stroke="#000" stroke-width="1"/>
      <rect x="9" y="4" width="12" height="8" fill="#ffffff"/>
      <rect x="11" y="5" width="3" height="6" fill="#808080"/>
      <rect x="9" y="16" width="14" height="10" rx="1" fill="#ffffff"/>
      <text x="11" y="23" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">FWSC</text>
    </svg>
    <span>cinco.fwsc</span>
  </a>

  <a class="desktop-icon" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank" rel="noopener" title="Open Cinco Documentation">
    <svg width="32" height="32" viewBox="0 0 32 32">
      <rect x="5" y="4" width="22" height="24" rx="2" fill="#dcd8cf" stroke="#000" stroke-width="1"/>
      <rect x="8" y="7" width="16" height="3" fill="#000080"/>
      <line x1="8" y1="14" x2="24" y2="14" stroke="#000" stroke-width="1"/>
      <line x1="8" y1="18" x2="24" y2="18" stroke="#000" stroke-width="1"/>
      <line x1="8" y1="22" x2="18" y2="22" stroke="#000" stroke-width="1"/>
    </svg>
    <span>Manual</span>
  </a>
</div>

<!-- Centered Windows 98 Setup Window -->
<main class="win98-window" role="dialog" aria-labelledby="win98-title">
  <!-- Title Bar -->
  <div class="win98-titlebar">
    <div class="win98-title-left">
      <svg class="win98-title-icon" viewBox="0 0 16 16">
        <rect x="1" y="1" width="14" height="14" rx="1" fill="#000080"/>
        <rect x="3" y="2" width="10" height="4" fill="#ffffff"/>
        <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
        <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
      </svg>
      <span class="win98-title-text" id="win98-title">Cinco Identity Generator 2.5 Setup Wizard</span>
    </div>
    <div class="win98-title-controls">
      <button class="win98-title-btn" id="win-help" title="Setup Help">?</button>
      <button class="win98-title-btn" id="win-close" title="Exit Setup">✕</button>
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
      <button class="win98-btn" id="lang" title="Toggle Language (English / 日本語)" style="min-width: 54px; height: 21px; font-size: 10px; padding: 1px 6px;">English</button>
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
    <p style="font-size: 10.5px; color: #444444; margin: 0 0 6px;">
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
        <p style="margin: 6px 0;"><button id="stock-go" class="win98-btn" disabled data-t="stockGo">Back up and return to official V15</button></p>
        <p style="font-size: 10.5px; color: #444444; margin: 4px 0;" data-t="stockBackup"></p>
        <p style="font-size: 10.5px; color: #444444; margin: 4px 0;">
          <label><input id="stock-recovery" type="checkbox"> <span data-t="stockRecovery">Resume an interrupted update: I already saved a complete backup to this computer</span></label>
        </p>
      </div>
    </details>

    <!-- Bottom Command Button Bar -->
    <div class="win98-command-bar">
      <a href="../" class="win98-btn" id="emu-link" style="margin-right: auto;">
        ⚡ <span data-t="emuLink">Launch Browser Emulator</span>
      </a>
      <button class="win98-btn" disabled>&lt; Back</button>
      <button id="go" class="win98-btn win98-btn-default" disabled>
        <span data-t="install">Install &gt;</span>
      </button>
      <button class="win98-btn" id="cancel-btn">Cancel</button>
    </div>

    <!-- Window Status Bar (Sunken 3D Cells) -->
    <div class="win98-statusbar">
      <div class="statusbar-cell" style="flex: 2;">
        <span data-t="license"></span>
        <a href="https://github.com/mrjoshida/CINCO" target="_blank" rel="noopener" style="color: var(--win-blue);">github.com/mrjoshida/CINCO</a>
      </div>
      <div class="statusbar-cell" style="flex: 1; text-align: center;">Target: FM-1</div>
      <div class="statusbar-cell" style="flex: 1; text-align: center;">WebMIDI SysEx</div>
    </div>
  </div>
</main>

<!-- External Links Footer -->
<footer class="footer-links">
  <a href="../">⚡ Web Emulator</a>
  <a href="https://github.com/mrjoshida/CINCO">GitHub Repository</a>
  <a href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md">Cinco Manual</a>
  <a href="../firmware/cinco.fwsc" download>Download Firmware (cinco.fwsc)</a>
</footer>

<!-- Windows 98 Start Menu Popup -->
<div class="win98-start-menu" id="start-menu" role="menu">
  <div class="start-menu-sidebar">Windows 98</div>
  <div class="start-menu-items">
    <a class="start-menu-item" href="../">
      <span>⚡</span>
      <span>Web Emulator</span>
    </a>
    <a class="start-menu-item" href="../firmware/cinco.fwsc" download>
      <span>💾</span>
      <span>Download cinco.fwsc</span>
    </a>
    <a class="start-menu-item" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank" rel="noopener">
      <span>📖</span>
      <span>Cinco Manual</span>
    </a>
    <a class="start-menu-item" href="https://github.com/mrjoshida/CINCO" target="_blank" rel="noopener">
      <span>🐙</span>
      <span>GitHub Repository</span>
    </a>
    <div class="start-menu-divider"></div>
    <div class="start-menu-item" onclick="alert('Cinco Identity Generator 2.5™\\nCinco Business Systems, Inc.\\nCelery Man Edition [v2.5]\\nTarget: M-VAVE FM-1 (AC7916A)\\nLicensed under GPL-3.0')">
      <span>ℹ️</span>
      <span>About Cinco 2.5...</span>
    </div>
  </div>
</div>

<!-- Windows 98 Fixed Bottom Taskbar -->
<div class="win98-taskbar">
  <button class="win98-start-btn" id="start-btn" aria-haspopup="true" aria-expanded="false">
    <svg width="16" height="16" viewBox="0 0 16 16" style="vertical-align: middle;">
      <rect x="2" y="2" width="5" height="5" fill="#f25022"/>
      <rect x="8" y="2" width="5" height="5" fill="#7fba00"/>
      <rect x="2" y="8" width="5" height="5" fill="#00a4ef"/>
      <rect x="8" y="8" width="5" height="5" fill="#ffb900"/>
    </svg>
    <span>Start</span>
  </button>
  <div class="taskbar-divider"></div>
  <div class="taskbar-app">
    <svg width="14" height="14" viewBox="0 0 16 16" style="flex-shrink: 0;">
      <rect x="1" y="1" width="14" height="14" rx="1" fill="#000080"/>
      <rect x="3" y="2" width="10" height="4" fill="#ffffff"/>
      <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
      <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
    </svg>
    <span>💽 Cinco 2.5 Setup</span>
  </div>
  <div class="taskbar-tray">
    <!-- Volume Icon -->
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#000000" stroke-width="1.2" title="Master Audio">
      <path d="M2 5h3l4-4v14l-4-4H2V5z"/>
      <path d="M12 5a4.5 4.5 0 0 1 0 6"/>
      <path d="M14 3a7.5 7.5 0 0 1 0 10"/>
    </svg>
    <!-- MIDI Port Icon -->
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#000000" stroke-width="1.2" title="WebMIDI SysEx Connected">
      <circle cx="8" cy="8" r="6"/>
      <circle cx="5" cy="8" r="1" fill="#000000"/>
      <circle cx="8" cy="5" r="1" fill="#000000"/>
      <circle cx="11" cy="8" r="1" fill="#000000"/>
      <circle cx="6.5" cy="11" r="1" fill="#000000"/>
      <circle cx="9.5" cy="11" r="1" fill="#000000"/>
    </svg>
    <span id="tray-clock">12:00 PM</span>
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
    emuLink: "Launch Browser Emulator",
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
    emuLink: "Webエミュレータを起動",
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

// Windows 98 UI Controls
$("cancel-btn").addEventListener("click", () => {
  if (confirm("Cancel Cinco Identity Generator 2.5 Setup and return to Web Emulator?")) {
    window.location.href = "../";
  }
});

$("win-close").addEventListener("click", () => {
  if (confirm("Exit Cinco Identity Generator 2.5 Setup?")) {
    window.location.href = "../";
  }
});

$("win-help").addEventListener("click", () => {
  alert("Cinco Identity Generator 2.5 Setup Wizard\\n\\n1. Connect your M-VAVE FM-1 via USB-C to this computer.\\n2. Click 'Install >' to flash cinco.fwsc over WebMIDI SysEx.\\n3. Do not disconnect the cable during flashing.\\n\\nEnjoy CINCO OS 2.5!");
});

// Start Menu Toggle
$("start-btn").addEventListener("click", (e) => {
  e.stopPropagation();
  const isOpen = $("start-menu").classList.toggle("open");
  $("start-btn").classList.toggle("pressed", isOpen);
  $("start-btn").setAttribute("aria-expanded", isOpen ? "true" : "false");
});

document.addEventListener("click", (e) => {
  if (!$("start-menu").contains(e.target) && e.target !== $("start-btn")) {
    $("start-menu").classList.remove("open");
    $("start-btn").classList.remove("pressed");
    $("start-btn").setAttribute("aria-expanded", "false");
  }
});

// Live Taskbar Clock
function updateClock() {
  const d = new Date();
  let h = d.getHours();
  const m = String(d.getMinutes()).padStart(2, "0");
  const ampm = h >= 12 ? "PM" : "AM";
  h = h % 12 || 12;
  const el = $("tray-clock");
  if (el) el.textContent = `${h}:${m} ${ampm}`;
}
setInterval(updateClock, 1000);
updateClock();

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
      if (!confirm(t("stockConfirm"))) return;
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
      if (!confirm(t("stockConfirm"))) return;
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

html_content = template.replace("/*COMBINED_LIB_PLACEHOLDER*/", combined_lib)

output_path = web_dir / "cinco_installer.html"
output_path.write_text(html_content, encoding="utf-8")
print(f"Generated {output_path} ({len(html_content)} bytes)")
