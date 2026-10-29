#!/usr/bin/env python3
"""
Generate the authentic Windows 98 styled web/emu/index.html for CINCO OS 2.5.
Pure, zero-dependency HTML & CSS with interactive Win98 desktop, menu bar, and taskbar.
"""

import os
import re

OUTPUT_PATH = "web/emu/index.html"

# Read original JS logic from web/emu/index.html
with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
    orig = f.read()

# Extract script block
m = re.search(r"(<script type=\"module\">.*?</script>)", orig, re.DOTALL)
if not m:
    raise RuntimeError("Could not find script block in web/emu/index.html")
orig_script = m.group(1)

html_content = r'''<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-only
     CINCO OS 2.5 Enterprise Synthesizer Workstation
     Cinco Business Systems, Inc. [v2.5] (Celery Man Edition)
     Portions derived from Felucca by Leo Kuroshita (@kurogedelic), Hügelton Instruments (GPL-3.0) -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CINCO OS 2.5 — Cinco Identity Generator</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 fill=%22%23000080%22/%3E%3Crect x=%223%22 y=%222%22 width=%2210%22 height=%224%22 fill=%22%23fff%22/%3E%3Crect x=%223%22 y=%228%22 width=%2210%22 height=%226%22 fill=%22%23c0c0c0%22/%3E%3Ctext x=%224%22 y=%2213%22 font-family=%22monospace%22 font-size=%226%22 font-weight=%22bold%22 fill=%22%23000080%22%3E5%3C/text%3E%3C/svg%3E">
<meta name="description" content="CINCO OS 2.5 (Celery Man Edition) enterprise synthesizer workstation running directly in your browser via WebAssembly.">
<style>
/* DotGothic16 for hardware knob labels */
@font-face { font-family: "DotGothic16"; src: url("fonts/DotGothic16-subset.woff") format("woff"); font-display: swap; }

:root {
  --win-bg: #008080;
  --win-gray: #c0c0c0;
  --win-light: #ffffff;
  --win-lighter: #dfdfdf;
  --win-dark: #808080;
  --win-darker: #0a0a0a;
  --win-blue: #000080;
  --win-blue-light: #1084d0;
  --body: #1d1d1f; --tray: #141415; --part: #2a2a2d; --edge: #3a3a3e; --label: #d6d6d8;
  --lit: #fff4d6; --green: #5fe08a; color-scheme: light;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 12px 10px 40px;
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
  user-select: none;
}

a { color: inherit; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Desktop Icons on Teal Canvas */
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
  width: 68px;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  color: #ffffff;
}

.desktop-icon:focus, .desktop-icon:hover {
  text-decoration: none;
}

.desktop-icon .icon-img {
  width: 32px;
  height: 32px;
  margin-bottom: 4px;
  filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.8));
}

.desktop-icon .icon-lbl {
  font-size: 11px;
  padding: 1px 3px;
  background: transparent;
  color: #ffffff;
  text-shadow: 1px 1px 1px #000;
  border-radius: 2px;
  line-height: 1.2;
}

.desktop-icon:focus .icon-lbl, .desktop-icon:active .icon-lbl {
  background: var(--win-blue);
  outline: 1px dotted #ffff80;
}

@media (max-width: 1080px) {
  .desktop-icons { display: none; }
}

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

/* Main Application Window Frame */
.win-window {
  width: 100%;
  max-width: 1040px;
  background-color: var(--win-gray);
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
}

.win-titlebar {
  height: 22px;
  background: linear-gradient(90deg, var(--win-blue), var(--win-blue-light));
  color: #ffffff;
  padding: 2px 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: bold;
  font-size: 11px;
  cursor: default;
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
  font-family: monospace;
  font-size: 9px;
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

/* Menu Bar */
.win-menubar {
  display: flex;
  background: var(--win-gray);
  padding: 2px 6px;
  border-bottom: 1px solid var(--win-dark);
  position: relative;
}

.menu-item {
  position: relative;
  padding: 2px 7px;
  cursor: pointer;
  color: #000000;
}

.menu-item:hover, .menu-item.active {
  background: var(--win-blue);
  color: #ffffff;
}

.menu-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: var(--win-gray);
  min-width: 190px;
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: 2px 2px 5px rgba(0,0,0,0.4);
  padding: 2px 0;
  z-index: 100;
}

.menu-item.active .menu-dropdown {
  display: block;
}

.dropdown-item {
  padding: 4px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #000000;
  font-weight: normal;
  cursor: pointer;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: var(--win-blue);
  color: #ffffff;
}

.dropdown-divider {
  height: 1px;
  background: var(--win-dark);
  border-bottom: 1px solid var(--win-light);
  margin: 3px 2px;
}

.dropdown-shortcut {
  font-size: 10px;
  color: #666;
  margin-left: 16px;
}

.dropdown-item:hover .dropdown-shortcut {
  color: #dfdfdf;
}

/* Window Content Client Area */
.win-content {
  padding: 6px;
  background: var(--win-gray);
}

.client-inset {
  background: #101012;
  border-top: 2px solid var(--win-dark);
  border-left: 2px solid var(--win-dark);
  border-right: 2px solid var(--win-light);
  border-bottom: 2px solid var(--win-light);
  box-shadow: inset 1px 1px 0 var(--win-darker), inset -1px -1px 0 var(--win-lighter);
  position: relative;
  overflow: hidden;
}

/* Device Simulator SVG/Canvas */
.device {
  position: relative;
  width: 100%;
  aspect-ratio: 1000 / 624;
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
  touch-action: manipulation;
}

.device svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.device canvas {
  position: absolute;
  image-rendering: crisp-edges;
  image-rendering: pixelated;
  background: #000;
}

.hit {
  position: absolute;
  touch-action: none;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  border-radius: 10px;
}

.hit.knob {
  cursor: ns-resize;
  border-radius: 50%;
}

.hit:focus-visible {
  outline: 2px solid var(--lit);
  outline-offset: 2px;
}

.face { transition: fill .05s; }
.dim .face.btn { fill: #3a3934; }
.lit .face.btn { fill: var(--lit); }
.lit text { fill: #1d1d1f; }
.green .face.btn { fill: var(--green); }
.green text { fill: #0d2414; }
.face.key { fill: #0c0c0d; stroke: var(--edge); stroke-width: 1.5; }
.slit { fill: #3a3a3c; transition: fill .05s; }
.dim .slit { fill: #77777b; }
.lit .slit { fill: #ececee; filter: drop-shadow(0 0 3px rgba(255, 255, 255, .6)); }

@keyframes breath-btn { 0%, 100% { fill: #3a3934; } 50% { fill: #d8cfb6; } }
@keyframes breath-slit { 0%, 100% { fill: #3a3a3c; } 50% { fill: #c8c8ca; } }
@keyframes breath-btn-lo { 0%, 100% { fill: #3a3934; } 50% { fill: #aca592; } }
@keyframes breath-slit-lo { 0%, 100% { fill: #3a3a3c; } 50% { fill: #a1a1a3; } }
.breath .face.btn { animation: breath-btn 1.13s ease-in-out infinite; }
.breath .slit { animation: breath-slit 1.13s ease-in-out infinite; }
.dimlo .breath .face.btn { animation-name: breath-btn-lo; }
.dimlo .breath .slit { animation-name: breath-slit-lo; }
@media (prefers-reduced-motion: reduce) {
  .breath .face.btn, .breath .slit { animation: none; }
  .breath .face.btn { fill: #aca592; }
  .breath .slit { fill: #a1a1a3; }
}

.mid .slit { fill: #9a9a9e; }
.dimlo .mid .slit { fill: #8a8a8e; }
.held .face { stroke: var(--lit); stroke-width: 3; }
.latched .face { stroke: #79b8ff; stroke-width: 3; }

.start {
  position: absolute;
  inset: 0;
  display: grid;
  place-content: center;
  justify-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, .6);
  border-radius: 4% / 6%;
}

.start[hidden] { display: none; }

.start button {
  font-family: "MS Sans Serif", Tahoma, Arial, sans-serif;
  font-size: 14px;
  font-weight: bold;
  padding: 8px 24px;
  background: var(--win-gray);
  color: #000;
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  cursor: pointer;
}

.start button:active {
  border-top: 2px solid var(--win-darker);
  border-left: 2px solid var(--win-darker);
  border-right: 2px solid var(--win-light);
  border-bottom: 2px solid var(--win-light);
  box-shadow: none;
  padding-top: 9px;
  padding-left: 25px;
}

.start button:disabled { opacity: .5; cursor: progress; }
.start p { margin: 0; max-width: 32em; text-align: center; color: #fff; text-shadow: 1px 1px 1px #000; }

/* Keyboard Instructions Bar */
.keys-bar {
  margin-top: 4px;
  padding: 3px 6px;
  background: var(--win-gray);
  border-top: 1px solid var(--win-dark);
  border-left: 1px solid var(--win-dark);
  border-right: 1px solid var(--win-light);
  border-bottom: 1px solid var(--win-light);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 10px;
  color: #222;
}

.keys-bar span { white-space: nowrap; }
.keys-bar select { font-family: inherit; font-size: 10px; }

kbd {
  font-family: monospace;
  font-size: 10px;
  font-weight: bold;
  background: #ffffff;
  border-top: 1px solid var(--win-light);
  border-left: 1px solid var(--win-light);
  border-right: 1px solid var(--win-darker);
  border-bottom: 1px solid var(--win-darker);
  padding: 0 4px;
  color: #000;
}

/* Sunken Window Status Bar */
.win-statusbar {
  display: flex;
  gap: 3px;
  padding: 3px 4px 1px;
  background: var(--win-gray);
  border-top: 1px solid var(--win-light);
}

.status-panel {
  padding: 2px 6px;
  background: var(--win-gray);
  border-top: 1px solid var(--win-dark);
  border-left: 1px solid var(--win-dark);
  border-right: 1px solid var(--win-light);
  border-bottom: 1px solid var(--win-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 10px;
  color: #333;
}

.status-panel.main-panel { flex: 1; }

/* Bottom Windows 98 Taskbar */
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
  z-index: 1000;
  box-shadow: 0 -1px 0 var(--win-dark);
}

.taskbar-left {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.start-btn {
  height: 22px;
  background: var(--win-gray);
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 6px;
  font-family: inherit;
  font-size: 11px;
  font-weight: bold;
  cursor: pointer;
}

.start-btn:active, .start-btn.pressed {
  border-top: 2px solid var(--win-darker);
  border-left: 2px solid var(--win-darker);
  border-right: 2px solid var(--win-light);
  border-bottom: 2px solid var(--win-light);
  box-shadow: none;
  padding-top: 1px;
  padding-left: 7px;
}

.start-logo {
  width: 14px;
  height: 14px;
}

.task-pill {
  height: 22px;
  max-width: 220px;
  background: var(--win-gray);
  border-top: 2px solid var(--win-darker);
  border-left: 2px solid var(--win-darker);
  border-right: 2px solid var(--win-light);
  border-bottom: 2px solid var(--win-light);
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0 8px;
  font-size: 11px;
  font-weight: bold;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background-color: #dcdcdc;
  box-shadow: inset 1px 1px 0 var(--win-dark);
}

.task-pill.inactive {
  background-color: var(--win-gray);
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  font-weight: normal;
}

.systray {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 22px;
  padding: 0 6px;
  background: var(--win-gray);
  border-top: 1px solid var(--win-dark);
  border-left: 1px solid var(--win-dark);
  border-right: 1px solid var(--win-light);
  border-bottom: 1px solid var(--win-light);
  font-size: 11px;
  color: #000;
}

/* Start Menu */
.start-menu {
  display: none;
  position: fixed;
  bottom: 28px;
  left: 2px;
  width: 195px;
  background: var(--win-gray);
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
  z-index: 2000;
  display: flex;
}

.start-menu:not(.open) {
  display: none;
}

.start-menu-side {
  width: 24px;
  background: linear-gradient(180deg, #000080, #1084d0);
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  color: #ffffff;
  font-weight: bold;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 8px 3px;
  text-shadow: 1px 1px 0 #000;
}

.start-menu-side span {
  font-weight: 900;
  color: #dfdfdf;
}

.start-menu-items {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 3px 0;
}

.start-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px;
  cursor: pointer;
  color: #000;
  font-size: 11px;
}

.start-item:hover {
  background: var(--win-blue);
  color: #fff;
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

/* Modal Dialog for "About CINCO OS 2.5" */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 5000;
  align-items: center;
  justify-content: center;
}

.modal-overlay.open {
  display: flex;
}

.modal-dialog {
  width: 360px;
  background: var(--win-gray);
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: 2px 2px 10px rgba(0,0,0,0.6);
  padding: 3px;
}

.modal-body {
  padding: 16px 14px 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-header-row {
  display: flex;
  gap: 14px;
  align-items: center;
}

.modal-logo {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}

.modal-info h3 {
  margin: 0 0 4px;
  font-size: 13px;
  color: var(--win-blue);
}

.modal-info p {
  margin: 0;
  font-size: 11px;
  color: #333;
}

.modal-box {
  background: #ffffff;
  padding: 8px 10px;
  border-top: 1px solid var(--win-dark);
  border-left: 1px solid var(--win-dark);
  border-right: 1px solid var(--win-light);
  border-bottom: 1px solid var(--win-light);
  font-size: 11px;
  line-height: 1.4;
}

.modal-btn-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

.dialog-btn {
  min-width: 72px;
  padding: 4px 14px;
  background: var(--win-gray);
  border-top: 2px solid var(--win-light);
  border-left: 2px solid var(--win-light);
  border-right: 2px solid var(--win-darker);
  border-bottom: 2px solid var(--win-darker);
  box-shadow: inset 1px 1px 0 var(--win-lighter), inset -1px -1px 0 var(--win-dark);
  cursor: pointer;
  font-family: inherit;
  font-size: 11px;
  font-weight: bold;
}

.dialog-btn:active {
  border-top: 2px solid var(--win-darker);
  border-left: 2px solid var(--win-darker);
  border-right: 2px solid var(--win-light);
  border-bottom: 2px solid var(--win-light);
  box-shadow: none;
  padding-top: 5px;
  padding-left: 15px;
}
</style>
</head>
<body>

<!-- Windows 98 Desktop Icons -->
<div class="desktop-icons">
  <div class="desktop-icon" id="d-mycomp" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="3" y="3" width="26" height="19" rx="1" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <rect x="5" y="5" width="22" height="15" fill="#008080"/>
      <path d="M12 22 L8 28 L24 28 L20 22 Z" fill="#808080" stroke="#000" stroke-width="1.5"/>
      <rect x="7" y="27" width="18" height="2" fill="#dfdfdf"/>
    </svg>
    <span class="icon-lbl">My Computer</span>
  </div>

  <a class="desktop-icon" href="installer/" id="d-installer" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <rect x="4" y="2" width="24" height="28" rx="2" fill="#000080" stroke="#000" stroke-width="1.5"/>
      <rect x="8" y="4" width="16" height="8" fill="#ffffff"/>
      <rect x="18" y="6" width="4" height="5" fill="#808080"/>
      <rect x="8" y="16" width="16" height="10" fill="#c0c0c0" stroke="#000" stroke-width="1"/>
      <text x="11" y="24" font-family="monospace" font-size="9" font-weight="bold" fill="#000080">5</text>
    </svg>
    <span class="icon-lbl">Setup Wizard</span>
  </a>

  <a class="desktop-icon" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank" id="d-manual" tabindex="0">
    <svg class="icon-img" viewBox="0 0 32 32">
      <path d="M6 3 L22 3 L27 8 L27 29 L6 29 Z" fill="#ffffff" stroke="#000" stroke-width="1.5"/>
      <path d="M22 3 L22 8 L27 8 Z" fill="#c0c0c0" stroke="#000" stroke-width="1"/>
      <line x1="9" y1="12" x2="23" y2="12" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="16" x2="23" y2="16" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="20" x2="23" y2="20" stroke="#000" stroke-width="1.5"/>
      <line x1="9" y1="24" x2="18" y2="24" stroke="#000" stroke-width="1.5"/>
    </svg>
    <span class="icon-lbl">CINCO Manual</span>
  </a>

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
    <span class="icon-lbl">Disk Defrag</span>
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

<!-- Main Application Window -->
<main class="win-window bevel-raised" id="main-win">
  <!-- Titlebar -->
  <div class="win-titlebar" id="win-drag-bar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <rect x="3" y="2" width="10" height="4" fill="#fff"/>
        <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
        <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
      </svg>
      <span>Cinco Identity Generator 2.5™ - [CINCO OS 2.5]</span>
    </div>
    <div class="win-controls">
      <button class="win-btn" id="btn-win-min" title="Minimize">_</button>
      <button class="win-btn" id="btn-win-max" title="Maximize">口</button>
      <button class="win-btn" id="btn-win-close" title="Close">×</button>
    </div>
  </div>

  <!-- Menu Bar -->
  <nav class="win-menubar">
    <div class="menu-item" tabindex="0">
      <span><u>F</u>ile</span>
      <div class="menu-dropdown">
        <div class="dropdown-item" id="m-switch-on"><span><u>P</u>ower Switch</span><span class="dropdown-shortcut">Ctrl+O</span></div>
        <div class="dropdown-item" id="m-restart"><span><u>R</u>eset Terminal</span><span class="dropdown-shortcut">Ctrl+R</span></div>
        <div class="dropdown-divider"></div>
        <a class="dropdown-item" href="installer/"><span><u>F</u>lash Hardware...</span></a>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item" id="m-exit"><span>E<u>x</u>it</span><span class="dropdown-shortcut">Alt+F4</span></div>
      </div>
    </div>

    <div class="menu-item" tabindex="0">
      <span><u>D</u>ancers</span>
      <div class="menu-dropdown">
        <div class="dropdown-item" id="m-celery"><span><u>C</u>elery Man (Default)</span></div>
        <div class="dropdown-item" id="m-oyster"><span><u>O</u>yster Smiling</span></div>
        <div class="dropdown-item" id="m-tayne"><span><u>T</u>ayne (BETA)</span></div>
        <div class="dropdown-item" id="m-speech"><span><u>S</u>peech Synthesizer</span></div>
      </div>
    </div>

    <div class="menu-item" tabindex="0">
      <span><u>K</u>inetics</span>
      <div class="menu-dropdown">
        <div class="dropdown-item" id="m-wobble"><span><u>H</u>at Wobble (LFO)</span><span class="dropdown-shortcut">4</span></div>
        <div class="dropdown-item" id="m-flail"><span><u>F</u>larhgunnstow (ARP)</span><span class="dropdown-shortcut">9</span></div>
        <div class="dropdown-item" id="m-nude"><span><u>N</u>ude Tayne Mode (FX)</span><span class="dropdown-shortcut">1</span></div>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item" id="m-k4d"><span>Kick up the <u>4</u>d3d3d3</span><span class="dropdown-shortcut">K1</span></div>
      </div>
    </div>

    <div class="menu-item" tabindex="0">
      <span><u>T</u>ools</span>
      <div class="menu-dropdown">
        <div class="dropdown-item" id="m-defrag"><span>Disk <u>D</u>efragmenter</span><span class="dropdown-shortcut">SEQ</span></div>
        <div class="dropdown-item" id="m-boss"><span>Lotus 1-2-3 <u>B</u>oss Key</span><span class="dropdown-shortcut">EDIT</span></div>
        <div class="dropdown-item" id="m-screensaver"><span>After Dark <u>S</u>creensaver</span></div>
      </div>
    </div>

    <div class="menu-item" tabindex="0">
      <span><u>H</u>elp</span>
      <div class="menu-dropdown">
        <a class="dropdown-item" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank"><span>CINCO 2.5 <u>M</u>anual</span></a>
        <a class="dropdown-item" href="https://github.com/mrjoshida/CINCO" target="_blank"><span>GitHub <u>R</u>epository</span></a>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item" id="m-about"><span><u>A</u>bout CINCO OS 2.5...</span></div>
      </div>
    </div>
  </nav>

  <!-- Client Inset Area -->
  <div class="win-content">
    <div class="client-inset">
      <div class="device" id="device">
        <svg id="panel" viewBox="0 0 1000 624" aria-hidden="true"></svg>
        <canvas id="screen" width="240" height="240" role="img" aria-label="The screen"></canvas>
        <div class="start" id="start"><button id="go" type="button">Switch on</button><p id="status" hidden></p></div>
      </div>
    </div>

    <!-- Shortcut Keys Bar -->
    <div class="keys-bar">
      <span><kbd>Z</kbd>–<kbd>'</kbd> <kbd>Q</kbd>–<kbd>O</kbd> Synthesizer Keys</span>
      <span><kbd>1</kbd>–<kbd>=</kbd> FX … REC</span>
      <span><kbd>[</kbd> <kbd>]</kbd> Octave</span>
      <span><kbd>↑</kbd> <kbd>↓</kbd> Select</span>
      <span><kbd>←</kbd> <kbd>→</kbd> Algo</span>
      <span><kbd>Shift</kbd>-click holds a button</span>
      <span id="midiknobs" hidden><label><input type="checkbox" id="knobson"> MIDI CC 20–27 turn knobs</label>
      <select id="knobmode" aria-label="How the controller sends CC 20–26" hidden>
        <option value="abs">absolute</option>
        <option value="bin">relative 64±n</option>
        <option value="twos">relative 2's complement</option>
        <option value="sign">relative sign bit</option>
      </select></span>
    </div>
  </div>

  <!-- Sunken Status Bar -->
  <footer class="win-statusbar">
    <div class="status-panel main-panel" id="status-main">Ready - Click 'Switch on' to initialize CINCO OS 2.5</div>
    <div class="status-panel">User: Paul (Managing Director)</div>
    <div class="status-panel">OS: CINCO OS 2.5</div>
    <div class="status-panel">Bus: ST7789 12MHz SPI</div>
    <div class="status-panel">DSP: 4d3d3d3</div>
  </footer>
</main>

<!-- Bottom Taskbar -->
<footer class="win-taskbar">
  <div class="taskbar-left">
    <button class="start-btn" id="start-btn">
      <svg class="start-logo" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <rect x="3" y="2" width="10" height="4" fill="#fff"/>
        <rect x="3" y="8" width="10" height="6" fill="#c0c0c0"/>
        <text x="4" y="13" font-family="monospace" font-size="6" font-weight="bold" fill="#000080">5</text>
      </svg>
      <span>Start</span>
    </button>

    <div class="task-pill" id="task-pill-main">
      <svg width="14" height="14" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <text x="4" y="12" font-family="monospace" font-size="9" font-weight="bold" fill="#fff">5</text>
      </svg>
      <span>Cinco Identity Generator 2.5™</span>
    </div>

    <a class="task-pill inactive" href="installer/">
      <svg width="14" height="14" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#808080"/>
        <text x="4" y="12" font-family="monospace" font-size="9" font-weight="bold" fill="#fff">💾</text>
      </svg>
      <span>Setup Wizard</span>
    </a>
  </div>

  <div class="systray">
    <span title="Audio Worklet 44.1 kHz">🔊</span>
    <span title="MIDI Controller Active">🎛️</span>
    <span id="systray-clock">12:00 PM</span>
  </div>
</footer>

<!-- Start Menu -->
<div class="start-menu" id="start-menu">
  <div class="start-menu-side">
    <span>CINCO</span> OS 2.5
  </div>
  <div class="start-menu-items">
    <div class="start-item" id="sm-app">
      <span class="start-item-icon">🎛️</span>
      <span><b>Identity Generator 2.5</b></span>
    </div>
    <a class="start-item" href="installer/">
      <span class="start-item-icon">💾</span>
      <span>Hardware Setup Wizard</span>
    </a>
    <div class="start-item" id="sm-defrag">
      <span class="start-item-icon">📊</span>
      <span>Disk Defragmenter</span>
    </div>
    <a class="start-item" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank">
      <span class="start-item-icon">📖</span>
      <span>System Manual</span>
    </a>
    <div class="start-divider"></div>
    <div class="start-item" id="sm-about">
      <span class="start-item-icon">ℹ️</span>
      <span>About CINCO OS...</span>
    </div>
    <div class="start-divider"></div>
    <div class="start-item" id="sm-shutdown">
      <span class="start-item-icon">⭕</span>
      <span>Shut <u>D</u>own...</span>
    </div>
  </div>
</div>

<!-- About Modal Dialog -->
<div class="modal-overlay" id="about-modal">
  <div class="modal-dialog bevel-raised">
    <div class="win-titlebar">
      <span>About CINCO OS 2.5</span>
      <button class="win-btn" id="modal-close">×</button>
    </div>
    <div class="modal-body">
      <div class="modal-header-row">
        <svg class="modal-logo" viewBox="0 0 32 32">
          <rect width="32" height="32" rx="4" fill="#000080"/>
          <rect x="6" y="4" width="20" height="8" fill="#fff"/>
          <rect x="6" y="16" width="20" height="12" fill="#c0c0c0"/>
          <text x="8" y="26" font-family="monospace" font-size="14" font-weight="bold" fill="#000080">5</text>
        </svg>
        <div class="modal-info">
          <h3>Cinco Identity Generator 2.5™</h3>
          <p>CINCO OS 2.5 Enterprise Workstation Platform</p>
          <p>Version @VERSION@@PREVIEW@</p>
        </div>
      </div>

      <div class="modal-box">
        <b>Cinco Business Systems, Inc.</b><br>
        Portions derived from Felucca by Leo Kuroshita, Hügelton Instruments (GPL-3.0).<br><br>
        <b>Licensed to:</b><br>
        &nbsp;&nbsp;Paul (Senior Managing Director)<br>
        &nbsp;&nbsp;Department of Identity Operations<br><br>
        <b>Hardware Memory Available:</b> 73,728 Bytes SRAM<br>
        <b>Dynamic Heap:</b> 301,984 Bytes DRAM<br>
        <b>Display Bus:</b> 12 MHz SPI ST7789
      </div>

      <div class="modal-btn-row">
        <button class="dialog-btn" id="modal-ok">OK</button>
      </div>
    </div>
  </div>
</div>

'''

# Custom UI glue scripts to attach menu actions and taskbar clock
glue_script = r'''
// ------------------------------------------------------------------ Windows 98 UI System
// Live digital clock in systray
function updateClock() {
  const now = new Date();
  let h = now.getHours();
  const m = String(now.getMinutes()).padStart(2, "0");
  const ampm = h >= 12 ? "PM" : "AM";
  h = h % 12 || 12;
  const clockEl = document.getElementById("systray-clock");
  if (clockEl) clockEl.textContent = `${h}:${m} ${ampm}`;
}
setInterval(updateClock, 1000);
updateClock();

// Menu bar dropdowns
document.querySelectorAll(".menu-item").forEach((item) => {
  item.addEventListener("click", (e) => {
    e.stopPropagation();
    const wasActive = item.classList.contains("active");
    document.querySelectorAll(".menu-item").forEach((i) => i.classList.remove("active"));
    if (!wasActive) item.classList.add("active");
  });
});

document.addEventListener("click", () => {
  document.querySelectorAll(".menu-item").forEach((i) => i.classList.remove("active"));
  const sm = document.getElementById("start-menu");
  const sb = document.getElementById("start-btn");
  if (sm) sm.classList.remove("open");
  if (sb) sb.classList.remove("pressed");
});

// Start button toggle
const startBtn = document.getElementById("start-btn");
const startMenu = document.getElementById("start-menu");
if (startBtn && startMenu) {
  startBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = startMenu.classList.toggle("open");
    startBtn.classList.toggle("pressed", isOpen);
  });
}

// Modal dialog handlers
const aboutModal = document.getElementById("about-modal");
const showAbout = () => { if (aboutModal) aboutModal.classList.add("open"); };
const closeAbout = () => { if (aboutModal) aboutModal.classList.remove("open"); };

document.getElementById("m-about")?.addEventListener("click", showAbout);
document.getElementById("sm-about")?.addEventListener("click", showAbout);
document.getElementById("modal-ok")?.addEventListener("click", closeAbout);
document.getElementById("modal-close")?.addEventListener("click", closeAbout);

// Interactive menu actions to hardware controls
function pressBtn(name) {
  const b = buttons.find((x) => x.name.startsWith(name) || x.name === name);
  if (b) {
    btnBy.set("ui", b.bit);
    syncButtons();
    setTimeout(() => { btnBy.delete("ui"); syncButtons(); }, 120);
  }
}

function turnKnob(roleName, steps) {
  const k = knobs.find((x) => x.role === EN[roleName] || x.key === roleName);
  if (k) turn(k, steps);
}

document.getElementById("m-switch-on")?.addEventListener("click", () => {
  const go = document.getElementById("go");
  if (go && !go.disabled) go.click();
});

document.getElementById("m-restart")?.addEventListener("click", () => {
  window.location.reload();
});

document.getElementById("m-exit")?.addEventListener("click", () => {
  if (confirm("Shut down CINCO OS 2.5?")) window.location.href = "about:blank";
});

document.getElementById("sm-shutdown")?.addEventListener("click", () => {
  if (confirm("Shut down CINCO OS 2.5?")) window.location.href = "about:blank";
});

// Menu shortcuts to synthesizer voices & modes
document.getElementById("m-celery")?.addEventListener("click", () => { turnKnob("PRESETS", 1); });
document.getElementById("m-oyster")?.addEventListener("click", () => { turnKnob("PRESETS", 1); });
document.getElementById("m-tayne")?.addEventListener("click", () => { turnKnob("PRESETS", 1); });
document.getElementById("m-wobble")?.addEventListener("click", () => pressBtn("LFO"));
document.getElementById("m-flail")?.addEventListener("click", () => pressBtn("ARP"));
document.getElementById("m-nude")?.addEventListener("click", () => pressBtn("FX"));
document.getElementById("m-k4d")?.addEventListener("click", () => turnKnob("KNOB 1", 10));
document.getElementById("m-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("d-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("sm-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("m-boss")?.addEventListener("click", () => pressBtn("EDIT"));

// Window controls
document.getElementById("btn-win-min")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  const pill = document.getElementById("task-pill-main");
  if (win && pill) {
    win.style.display = win.style.display === "none" ? "flex" : "none";
    pill.classList.toggle("inactive", win.style.display === "none");
  }
});

document.getElementById("task-pill-main")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  const pill = document.getElementById("task-pill-main");
  if (win && pill) {
    win.style.display = "flex";
    pill.classList.remove("inactive");
  }
});

document.getElementById("btn-win-max")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  if (!win) return;
  if (win.style.maxWidth === "100%") {
    win.style.maxWidth = "1040px";
  } else {
    win.style.maxWidth = "100%";
  }
});

document.getElementById("btn-win-close")?.addEventListener("click", () => {
  if (confirm("Shut down CINCO OS 2.5?")) window.location.href = "installer/";
});
'''

# Insert glue script just before </script> in orig_script
modified_script = orig_script.replace("</script>", glue_script + "\n</script>")

full_page = html_content + modified_script + "\n</body>\n</html>\n"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(full_page)

print(f"Generated Windows 98 styled {OUTPUT_PATH} ({len(full_page)} bytes)")
