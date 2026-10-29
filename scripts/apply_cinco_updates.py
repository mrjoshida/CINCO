#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Cinco Identity Generator 2.5™ Web OS Updater
import base64
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# 1. Base64 Assets
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

b64_assets = {}
for k, (mime, rel_p) in asset_map.items():
    p = REPO_ROOT / rel_p
    data = p.read_bytes()
    b64_assets[k] = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"

b64_js_def = "const TAYNE_ASSETS = " + json.dumps(b64_assets) + ";\n"

# 2. Shared CSS Block
shared_css = """
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
"""

tayne_window_html = """<!-- Windows 98 Application: Tayne Studio 98 -->
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
</div>"""

modal_nude_html = """<!-- Modal Dialog: Confirm Nude Tayne (NSFW) -->
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
</div>"""

screen_dos_html = """<!-- Fullscreen MS-DOS 7.10 Screen -->
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
      <span id="dos-prompt">C:\\CINCO&gt;</span>
      <input type="text" class="dos-input" id="dos-input" autocomplete="off" spellcheck="false" autofocus>
    </div>
  </div>
  <div style="margin-top:auto; padding-top:10px;">
    <button class="dialog-btn" id="btn-dos-exit" style="background:#333;color:#fff;border-color:#666;">Exit to Windows 98 (WIN)</button>
  </div>
</div>"""

js_window_manager = """// Window Management
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
"""

js_tayne_actions = """// Tayne Studio 98 Actions
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
"""

js_dos_terminal = """// MS-DOS 7.10 Interactive CLI
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
        appendDosLine("C:\\\\CINCO> " + raw);
        if (trimmed.toLowerCase() === "y") {
          appendDosBlock([
            "Formatting 4d3d3d3.00 MB...",
            "Format complete.",
            "",
            "Error writing partition table: Volume is locked by Managing Director Paul.",
            "Cinco Business Systems Protection: \\"Now Tayne I can get into.\\""
          ]);
        } else {
          appendDosLine("Format aborted.");
        }
        dosFormatPrompt = false;
        scrollToDosBottom();
        return;
      }

      appendDosLine("C:\\\\CINCO> " + raw);
      if (!trimmed) {
        scrollToDosBottom();
        return;
      }

      const parts = trimmed.split(/\\s+/);
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
            "  DIR           Display files in C:\\\\CINCO",
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
            " Directory of C:\\\\CINCO",
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
              "--- C:\\\\CINCO\\\\PAUL.TXT ---",
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
              "--- C:\\\\AUTOEXEC.BAT ---",
              "@ECHO OFF",
              "PROMPT $P$G",
              "PATH C:\\\\CINCO;C:\\\\DOS;C:\\\\WINDOWS",
              "SET SOUND=C:\\\\CINCO\\\\LPC10",
              "LH C:\\\\CINCO\\\\4D3D3D3.EXE /HIGH",
              "C:\\\\CINCO\\\\TAYNE.COM /AUTORUN"
            ]);
          } else if (arg === "config.sys") {
            appendDosBlock([
              "--- C:\\\\CONFIG.SYS ---",
              "DEVICE=C:\\\\DOS\\\\HIMEM.SYS",
              "DEVICE=C:\\\\DOS\\\\EMM386.EXE NOEMS",
              "DOS=HIGH,UMB",
              "FILES=40",
              "BUFFERS=40",
              "DEVICEHIGH=C:\\\\CINCO\\\\DRIVERS\\\\CELERY.SYS /V"
            ]);
          } else if (arg === "nude.dat") {
            appendDosBlock([
              "ACCESS DENIED: NUDE.DAT is encrypted with Cinco 4d3d3d3 security algorithm.",
              "Security incident reported to Paul."
            ]);
          } else if (arg === "oyster.prn") {
            appendDosBlock([
              "--- C:\\\\CINCO\\\\OYSTER.PRN (DOT MATRIX SPOOL) ---",
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
            "\\"Now Tayne I can get into.\\""
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
"""

def update_emu_html():
    emu_path = REPO_ROOT / "web" / "emu" / "index.html"
    content = emu_path.read_text(encoding="utf-8")

    # 1. CSS
    if ".tayne-stage {" not in content:
        content = content.replace("</style>", f"{shared_css}\n</style>")

    # 2. Window titlebar controls
    for win_id in ["win-recycle", "win-defrag", "win-lotus", "win-manual"]:
        old_ctrl = f'<div class="win-controls">\n      <button class="win-btn win-close-btn" data-target="{win_id}">×</button>\n    </div>'
        new_ctrl = f"""<div class="win-controls">
      <button class="win-btn win-min-btn" data-target="{win_id}" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="{win_id}" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="{win_id}" title="Close">×</button>
    </div>"""
        content = content.replace(old_ctrl, new_ctrl)

    old_main_ctrl = """<div class="win-controls">
      <button class="win-btn" id="btn-win-min" title="Minimize">_</button>
      <button class="win-btn" id="btn-win-max" title="Maximize">口</button>
      <button class="win-btn win-close-btn" id="btn-win-close" title="Close">×</button>
    </div>"""
    new_main_ctrl = """<div class="win-controls">
      <button class="win-btn win-min-btn" id="btn-win-min" data-target="main-win" title="Minimize">_</button>
      <button class="win-btn win-max-btn" id="btn-win-max" data-target="main-win" title="Maximize">口</button>
      <button class="win-btn win-close-btn" id="btn-win-close" data-target="main-win" title="Close">×</button>
    </div>"""
    content = content.replace(old_main_ctrl, new_main_ctrl)

    # 3. Tayne Window HTML
    content = re.sub(
        r'<!-- Windows 98 Application: Tayne Studio 98 -->[\s\S]*?</div>\s*</div>\s*</div>',
        lambda m: tayne_window_html,
        content
    )

    # 4. Modal Nude
    if 'id="modal-confirm-nude"' not in content:
        content = content.replace('<!-- Modal Dialog: Confirm Empty Recycle Bin -->', f'{modal_nude_html}\n\n<!-- Modal Dialog: Confirm Empty Recycle Bin -->')

    # 5. Screen DOS HTML
    content = re.sub(
        r'<div id="screen-dos">[\s\S]*?</div>\s*</div>',
        lambda m: screen_dos_html,
        content
    )

    # 6. Inject base64 into JS
    if "const TAYNE_ASSETS = " not in content:
        content = content.replace('<script type="module">', f'<script type="module">\n{b64_js_def}')

    # 7. Window manager JS
    wm_pattern = r'// Window Management[\s\S]*?(?=// Main window controls)'
    content = re.sub(wm_pattern, lambda m: js_window_manager + "\n\n", content)

    # 8. Tayne Actions JS
    tayne_js_pattern = r'// Tayne Studio 98 Actions[\s\S]*?(?=// Recycle Bin Incineration)'
    content = re.sub(tayne_js_pattern, lambda m: js_tayne_actions + "\n\n", content)

    # 9. DOS Terminal JS
    dos_js_pattern = r'document\.getElementById\("btn-dos-exit"\)[\s\S]*?(?=// CINCO Manual TOC Switching)'
    content = re.sub(dos_js_pattern, lambda m: js_dos_terminal + "\n\n", content)

    emu_path.write_text(content, encoding="utf-8")
    print(f"Updated {emu_path} ({len(content)} bytes)")

def update_installer_script():
    inst_path = REPO_ROOT / "scripts" / "generate_cinco_installer.py"
    content = inst_path.read_text(encoding="utf-8")

    # 1. CSS inside template
    if ".tayne-stage {" not in content:
        content = content.replace("</style>", f"{shared_css}\n</style>", 1)

    # 2. Window titlebar controls inside template
    for win_id in ["win-recycle", "win-defrag", "win-lotus", "win-manual"]:
        old_ctrl = f'<div class="win-controls">\n      <button class="win-btn win-close-btn" data-target="{win_id}">×</button>\n    </div>'
        new_ctrl = f"""<div class="win-controls">
      <button class="win-btn win-min-btn" data-target="{win_id}" title="Minimize">_</button>
      <button class="win-btn win-max-btn" data-target="{win_id}" title="Maximize">口</button>
      <button class="win-btn win-close-btn" data-target="{win_id}" title="Close">×</button>
    </div>"""
        content = content.replace(old_ctrl, new_ctrl, 1)

    old_main_ctrl = """<div class="win-controls">
      <button class="win-btn" id="btn-win-help" title="Setup Help">?</button>
      <button class="win-btn" id="btn-win-min" title="Minimize">_</button>
      <button class="win-btn" id="btn-win-close" title="Exit Setup">×</button>
    </div>"""
    new_main_ctrl = """<div class="win-controls">
      <button class="win-btn" id="btn-win-help" title="Setup Help">?</button>
      <button class="win-btn win-min-btn" id="btn-win-min" data-target="main-win" title="Minimize">_</button>
      <button class="win-btn win-max-btn" id="btn-win-max" data-target="main-win" title="Maximize">口</button>
      <button class="win-btn win-close-btn" id="btn-win-close" data-target="main-win" title="Exit Setup">×</button>
    </div>"""
    content = content.replace(old_main_ctrl, new_main_ctrl, 1)

    # 3. Tayne Window HTML inside template
    content = re.sub(
        r'<!-- Windows 98 Application: Tayne Studio 98 -->[\s\S]*?</div>\s*</div>\s*</div>',
        lambda m: tayne_window_html,
        content,
        count=1
    )

    # 4. Modal Nude
    if 'id="modal-confirm-nude"' not in content:
        content = content.replace('<!-- Modal Dialog: Confirm Empty Recycle Bin -->', f'{modal_nude_html}\n\n<!-- Modal Dialog: Confirm Empty Recycle Bin -->', 1)

    # 5. Screen DOS HTML
    content = re.sub(
        r'<div id="screen-dos">[\s\S]*?</div>\s*</div>',
        lambda m: screen_dos_html,
        content,
        count=1
    )

    # 6. Window manager JS
    wm_pattern = r'// Window Management[\s\S]*?(?=// Setup Wizard Window Controls)'
    content = re.sub(wm_pattern, lambda m: js_window_manager + "\n\n", content, count=1)

    # 7. Tayne Actions JS
    tayne_js_pattern = r'// Tayne Studio 98 Actions[\s\S]*?(?=// Recycle Bin Incineration)'
    content = re.sub(tayne_js_pattern, lambda m: js_tayne_actions + "\n\n", content, count=1)

    # 8. DOS Terminal JS
    dos_js_pattern = r'\$\("btn-dos-exit"\)[\s\S]*?(?=// Systray Volume Popup)'
    content = re.sub(dos_js_pattern, lambda m: js_dos_terminal + "\n\n", content, count=1)

    # 9. Update python generation logic at top/bottom of generate_cinco_installer.py:
    # Make sure generate_cinco_installer.py inlines b64_assets dynamically!
    if "import base64" not in content:
        content = "import base64\nimport json\n" + content

    if "def get_tayne_assets_js():" not in content:
        asset_loader_code = """
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
    return "const TAYNE_ASSETS = " + json.dumps(b64_dict) + ";\\n"
"""
        content = re.sub(r'combined_lib = f"""[\s\S]*?"""', lambda m: m.group(0) + "\n" + asset_loader_code, content, count=1)

    if 'html_content = template.replace("/*COMBINED_LIB_PLACEHOLDER*/", f"{combined_lib}\\n\\n{get_tayne_assets_js()}")' not in content:
        content = content.replace(
            'html_content = template.replace("/*COMBINED_LIB_PLACEHOLDER*/", combined_lib)',
            'html_content = template.replace("/*COMBINED_LIB_PLACEHOLDER*/", f"{combined_lib}\\n\\n{get_tayne_assets_js()}")'
        )

    inst_path.write_text(content, encoding="utf-8")
    print(f"Updated {inst_path} ({len(content)} bytes)")

def main():
    print("Updating web/emu/index.html...")
    update_emu_html()

    print("Updating scripts/generate_cinco_installer.py...")
    update_installer_script()

    print("Updates applied successfully.")

if __name__ == "__main__":
    main()
