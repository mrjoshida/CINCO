#!/usr/bin/env python3
"""
Overhaul CINCO OS 2.5 Workstation.
Builds the updated generate_win98_workstation.py and web/emu/index.html.
Eliminates ALL native browser alert() and confirm() calls and replaces them
with authentic in-universe Windows 98 application windows and dialogs.
"""

import os
import re

def generate():
    # Read the current web/emu/index.html
    with open("web/emu/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Additional CSS for Windows 98 Applications & Dialogs
    css_addition = r'''
/* ==========================================================================
   CINCO OS 2.5 In-Universe Windows 98 Applications & Dialogs
   ========================================================================== */
.app-window {
  position: fixed;
  background-color: var(--win-gray);
  z-index: 100;
  display: none;
  flex-direction: column;
  box-shadow: 3px 3px 12px rgba(0,0,0,0.5);
  user-select: none;
  max-width: 96vw;
  max-height: 88vh;
  overflow: hidden;
}

.app-window.open {
  display: flex;
}

.win-titlebar.inactive {
  background: linear-gradient(90deg, #808080, #a0a0a0) !important;
  color: #dfdfdf !important;
}

/* Recycle Bin Explorer Table */
.recycle-address-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 6px;
  background: var(--win-gray);
  border-bottom: 1px solid var(--win-dark);
  font-size: 11px;
}

.recycle-address-box {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  padding: 1px 6px;
  flex: 1;
  font-family: monospace;
}

.recycle-body {
  background: #ffffff;
  flex: 1;
  overflow: auto;
  min-height: 180px;
}

.recycle-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  text-align: left;
}

.recycle-table th {
  background: var(--win-gray);
  border-right: 1px solid var(--win-light);
  border-bottom: 1px solid var(--win-dark);
  border-top: 1px solid var(--win-light);
  border-left: 1px solid var(--win-dark);
  padding: 2px 6px;
  font-weight: normal;
  cursor: default;
}

.recycle-table td {
  padding: 3px 6px;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

.recycle-table tr:hover {
  background-color: #f0f4ff;
}

.recycle-table tr:focus, .recycle-table tr.selected {
  background-color: var(--win-selection) !important;
  color: #ffffff !important;
  outline: 1px dotted #ffff80;
}

.file-icon {
  display: inline-block;
  margin-right: 4px;
}

/* Lotus 1-2-3 Table */
.lotus-row-hdr {
  background: var(--win-gray);
  border: 1px solid #808080;
  padding: 2px 4px;
  text-align: center;
  font-weight: bold;
  user-select: none;
}

/* Manual Help TOC Tree */
.manual-tree-item {
  padding: 3px 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 1px;
  margin-bottom: 1px;
}

.manual-tree-item:hover {
  background: #e0e0e0;
}

.manual-tree-item.active {
  background: var(--win-selection);
  color: #ffffff;
  outline: 1px dotted #ffff80;
}

/* Defrag Clusters */
.cluster-block {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 1px;
  transition: background-color 0.15s ease;
}
.cluster-allocated { background-color: #000080; }
.cluster-free { background-color: #ffffff; border: 1px solid #e0e0e0; }
.cluster-fragmented { background-color: #ff0000; }
.cluster-unmovable { background-color: #008000; }
.cluster-active { background-color: #ffff00 !important; box-shadow: 0 0 3px #ffff00; }
'''

    if "/* Recycle Bin Explorer Table */" not in html:
        html = html.replace("</style>", css_addition + "\n</style>", 1)

    # 2. Update Desktop Icons in HTML
    # Full bin icon with crumpled papers
    full_bin_icon = '''  <div class="desktop-icon" id="d-recycle" tabindex="0">
    <svg class="icon-img" id="recycle-desktop-svg" viewBox="0 0 32 32">
      <polygon points="10,3 15,2 17,8 11,8" fill="#ffffff" stroke="#000" stroke-width="1"/>
      <polygon points="16,3 22,4 20,8 14,8" fill="#dfdfdf" stroke="#000" stroke-width="1"/>
      <rect x="13" y="1" width="5" height="4" fill="#000080"/>
      <path d="M7 8 L25 8 L23 28 L9 28 Z" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <line x1="5" y1="8" x2="27" y2="8" stroke="#000" stroke-width="2"/>
      <rect x="12" y="5" width="8" height="3" fill="#808080" stroke="#000" stroke-width="1"/>
      <line x1="12" y1="12" x2="12" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="16" y1="12" x2="16" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="20" y1="12" x2="20" y2="24" stroke="#808080" stroke-width="1.5"/>
    </svg>
    <span class="icon-lbl">Recycle Bin</span>
  </div>'''

    html = re.sub(
        r'<div class="desktop-icon" id="d-recycle" tabindex="0">[\s\S]*?Recycle Bin\s*</span>\s*</div>',
        full_bin_icon,
        html
    )

    # Change d-installer and d-manual from <a> to <div>
    html = re.sub(
        r'<a class="desktop-icon" href="installer/" id="d-installer" tabindex="0">([\s\S]*?)</a>',
        r'<div class="desktop-icon" id="d-installer" tabindex="0">\1</div>',
        html
    )
    html = re.sub(
        r'<a class="desktop-icon" href="https://github\.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL\.md" target="_blank" id="d-manual" tabindex="0">([\s\S]*?)</a>',
        r'<div class="desktop-icon" id="d-manual" tabindex="0">\1</div>',
        html
    )

    # 3. Update Menu Bar Help item:
    html = html.replace(
        '<a class="dropdown-item" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank"><span>CINCO 2.5 <u>M</u>anual</span></a>',
        '<div class="dropdown-item" id="m-manual"><span>CINCO 2.5 <u>M</u>anual</span></div>'
    )

    # 4. Update Start Menu items:
    sm_old = '''    <a class="start-item" href="installer/">
      <span class="start-item-icon">💿</span>
      <span>Hardware Setup Wizard</span>
    </a>
    <a class="start-item" href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/MANUAL.md" target="_blank">
      <span class="start-item-icon">📖</span>
      <span>System Manual</span>
    </a>'''

    sm_new = '''    <div class="start-item" id="sm-installer">
      <span class="start-item-icon">💿</span>
      <span>Hardware Setup Wizard...</span>
    </div>
    <div class="start-item" id="sm-manual">
      <span class="start-item-icon">📖</span>
      <span>System Help & Manual</span>
    </div>'''
    html = html.replace(sm_old, sm_new)

    # 5. Update Taskbar to include pills for all managed windows:
    taskbar_old = '''    <a class="task-pill inactive" href="installer/">
      <svg width="14" height="14" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#808080"/>
        <text x="4" y="12" font-family="monospace" font-size="9" font-weight="bold" fill="#fff">💾</text>
      </svg>
      <span>Setup Wizard</span>
    </a>'''

    taskbar_new = '''    <div class="task-pill inactive" id="task-pill-recycle" style="display:none;">
      <span style="font-size:12px;">🗑️</span>
      <span>Recycle Bin</span>
    </div>
    <div class="task-pill inactive" id="task-pill-tayne" style="display:none;">
      <span style="font-size:12px;">🎩</span>
      <span>Tayne Studio 98</span>
    </div>
    <div class="task-pill inactive" id="task-pill-defrag" style="display:none;">
      <span style="font-size:12px;">💾</span>
      <span>Defrag Drive C:</span>
    </div>
    <div class="task-pill inactive" id="task-pill-lotus" style="display:none;">
      <span style="font-size:12px;">📊</span>
      <span>Lotus 1-2-3</span>
    </div>
    <div class="task-pill inactive" id="task-pill-manual" style="display:none;">
      <span style="font-size:12px;">📖</span>
      <span>CINCO Manual</span>
    </div>
    <div class="task-pill inactive" id="task-pill-setup" style="display:none;">
      <span style="font-size:12px;">💿</span>
      <span>Setup Wizard</span>
    </div>'''
    html = html.replace(taskbar_old, taskbar_new)

    # 6. Windows & Dialogs HTML
    new_windows_html = r'''
<!-- =======================================================================
     Application Windows & Authentic Windows 98 Dialogs
     ======================================================================= -->

<!-- 1. Recycle Bin Window -->
<div class="win-window bevel-raised app-window" id="win-recycle" style="top:50px;left:80px;width:580px;height:380px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <path d="M3 4 L13 4 L11 14 L5 14 Z" fill="#c0c0c0" stroke="#fff" stroke-width="0.5"/>
        <line x1="2" y1="4" x2="14" y2="4" stroke="#fff" stroke-width="1.5"/>
        <rect x="6" y="2" width="4" height="2" fill="#808080"/>
        <line x1="6" y1="6" x2="6" y2="12" stroke="#808080" stroke-width="1"/>
        <line x1="8" y1="6" x2="8" y2="12" stroke="#808080" stroke-width="1"/>
        <line x1="10" y1="6" x2="10" y2="12" stroke="#808080" stroke-width="1"/>
      </svg>
      <span>Recycle Bin</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-min" title="Minimize">_</button>
      <button class="win-btn win-btn-max" title="Maximize">口</button>
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <nav class="win-menubar">
    <div class="menu-item" tabindex="0"><span><u>F</u>ile</span></div>
    <div class="menu-item" tabindex="0"><span><u>E</u>dit</span></div>
    <div class="menu-item" tabindex="0"><span><u>V</u>iew</span></div>
    <div class="menu-item" tabindex="0"><span><u>G</u>o</span></div>
    <div class="menu-item" tabindex="0"><span>F<u>a</u>vorites</span></div>
    <div class="menu-item" tabindex="0"><span><u>H</u>elp</span></div>
  </nav>
  <div class="win-toolbar" style="padding:2px 4px;">
    <button class="toolbar-btn" id="btn-empty-recycle" title="Empty Recycle Bin">
      <span style="font-size:12px;">🗑️</span> Empty Recycle Bin
    </button>
  </div>
  <div class="recycle-address-bar">
    <span style="color:#555;">Address</span>
    <div class="recycle-address-box bevel-thin-sunken">
      <span style="font-size:11px;">🗑️</span>
      <span>C:\RECYCLED</span>
    </div>
  </div>
  <div class="recycle-body bevel-sunken" id="recycle-list-container">
    <table class="recycle-table" id="recycle-table">
      <thead>
        <tr>
          <th style="width:200px;">Name</th>
          <th style="width:110px;">Original Location</th>
          <th style="width:120px;">Date Deleted</th>
          <th style="width:100px;">Type</th>
          <th style="width:70px;text-align:right;">Size</th>
        </tr>
      </thead>
      <tbody id="recycle-tbody">
        <tr tabindex="0">
          <td><span class="file-icon">🎵</span> tayne_beta_leaked_v1.raw</td>
          <td>C:\CINCO\TAYNE</td>
          <td>10/24/98 04:32 PM</td>
          <td>RAW Audio Sample</td>
          <td style="text-align:right;">4,210 KB</td>
        </tr>
        <tr tabindex="0">
          <td><span class="file-icon">📄</span> paul_sandwich_order.txt</td>
          <td>C:\MYDOCU~1</td>
          <td>10/28/98 12:15 PM</td>
          <td>Text Document</td>
          <td style="text-align:right;">1 KB</td>
        </tr>
        <tr tabindex="0">
          <td><span class="file-icon">💾</span> corrupted_cluster_4d3d.dat</td>
          <td>C:\CINCO\SYS</td>
          <td>10/29/98 09:04 AM</td>
          <td>DAT Memory Dump</td>
          <td style="text-align:right;">64 KB</td>
        </tr>
        <tr tabindex="0">
          <td><span class="file-icon">📝</span> oyster_receipt_unpaid.doc</td>
          <td>C:\CINCO\FINANCE</td>
          <td>10/26/98 02:40 PM</td>
          <td>WordPad Document</td>
          <td style="text-align:right;">12 KB</td>
        </tr>
        <tr tabindex="0">
          <td><span class="file-icon">🎬</span> celery_unapproved_moves.avi</td>
          <td>C:\CINCO\VIDEO</td>
          <td>10/27/98 11:22 PM</td>
          <td>Video Clip</td>
          <td style="text-align:right;">8,900 KB</td>
        </tr>
      </tbody>
    </table>
    <div class="recycle-empty-msg" id="recycle-empty-msg" style="display:none;padding:28px;text-align:center;color:#666;">
      <i>The Recycle Bin is empty.</i>
    </div>
  </div>
  <footer class="win-statusbar" style="font-size:10px;">
    <div class="status-panel" id="recycle-status-count" style="flex:1;">5 object(s)</div>
    <div class="status-panel" id="recycle-status-size" style="width:110px;text-align:right;">13.1 MB</div>
  </footer>
</div>

<!-- Confirm File Delete Dialog (Recycle Bin) -->
<div class="modal-overlay" id="modal-confirm-recycle">
  <div class="modal-dialog bevel-raised" style="width:360px;">
    <div class="win-titlebar">
      <span>Confirm Multiple File Delete</span>
      <button class="win-btn" id="btn-confirm-recycle-x">×</button>
    </div>
    <div class="modal-body" style="padding:14px 16px;">
      <div style="display:flex;gap:14px;align-items:center;">
        <svg style="width:36px;height:36px;flex-shrink:0;" viewBox="0 0 32 32">
          <path d="M16 2 L30 28 L2 28 Z" fill="#ffcc00" stroke="#000" stroke-width="1.5"/>
          <text x="14" y="24" font-family="sans-serif" font-size="18" font-weight="bold" fill="#000">!</text>
        </svg>
        <div style="font-size:11px;line-height:1.4;">
          Are you sure you want to permanently incinerate these 5 Cinco memory assets?
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:14px;">
        <button class="dialog-btn" id="btn-confirm-recycle-yes" style="min-width:64px;font-weight:bold;">Yes</button>
        <button class="dialog-btn" id="btn-confirm-recycle-no" style="min-width:64px;">No</button>
      </div>
    </div>
  </div>
</div>

<!-- 2. Tayne Studio 98 Window -->
<div class="win-window bevel-raised app-window" id="win-tayne" style="top:70px;left:120px;width:520px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <circle cx="8" cy="7" r="4" fill="#ffcc99"/>
        <rect x="5" y="3" width="6" height="2" fill="#222"/>
        <text x="5" y="15" font-family="monospace" font-size="7" font-weight="bold" fill="#fff">T</text>
      </svg>
      <span>Tayne Studio 98 (Beta Edition)</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-min" title="Minimize">_</button>
      <button class="win-btn win-btn-max" title="Maximize">口</button>
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <nav class="win-menubar">
    <div class="menu-item" tabindex="0"><span><u>F</u>ile</span></div>
    <div class="menu-item" tabindex="0"><span><u>S</u>equence</span></div>
    <div class="menu-item" tabindex="0"><span><u>D</u>ancer</span></div>
    <div class="menu-item" tabindex="0"><span><u>R</u>ender</span></div>
    <div class="menu-item" tabindex="0"><span>Cinco<u>N</u>et</span></div>
    <div class="menu-item" tabindex="0"><span><u>H</u>elp</span></div>
  </nav>
  <div style="padding:10px;display:flex;flex-direction:column;gap:10px;">
    <!-- Profile Card -->
    <div class="bevel-sunken" style="background:#ffffff;padding:12px;display:flex;gap:14px;align-items:center;">
      <div style="width:84px;height:84px;background:#000080;border:2px solid #000;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;flex-shrink:0;">
        <span style="font-size:32px;">🎩</span>
        <span style="font-size:9px;font-family:monospace;letter-spacing:1px;color:#00ff00;font-weight:bold;">TAYNE</span>
      </div>
      <div style="flex:1;font-size:11px;line-height:1.5;">
        <div style="font-weight:bold;font-size:13px;color:var(--win-blue);">Tayne Beta (Dancer Model 2.5)</div>
        <div style="display:flex;align-items:center;gap:6px;margin:4px 0;">
          <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#00aa00;box-shadow:0 0 5px #00ff00;"></span>
          <b id="tayne-status-card" style="color:#006600;">Dancer Sequence Loaded</b>
        </div>
        <div><b>Classification:</b> High-Kinetics Choreographic Asset</div>
        <div><b>Neural Vectors:</b> 4d3d3d3 Engaged | 30 FPS Lock</div>
        <div><b>OSHA Safety Status:</b> Grade B (Hat Wobble Ready)</div>
      </div>
    </div>

    <!-- Quick Action Controls -->
    <div class="bevel-thin-sunken" style="background:var(--win-gray);padding:8px 10px;">
      <div style="font-size:10px;font-weight:bold;margin-bottom:8px;color:#333;">QUICK ACTION CONTROLS</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(140px, 1fr));gap:6px;">
        <button class="dialog-btn" id="btn-tayne-load" style="height:26px;font-size:10px;font-weight:bold;">Load Tayne into Terminal</button>
        <button class="dialog-btn" id="btn-tayne-wobble" style="height:26px;font-size:10px;">🎩 Hat Wobble</button>
        <button class="dialog-btn" id="btn-tayne-flarh" style="height:26px;font-size:10px;">🔥 Flarhgunnstow</button>
        <button class="dialog-btn" id="btn-tayne-nude" style="height:26px;font-size:10px;color:#aa0000;font-weight:bold;">🔞 Nude Tayne (NSFW)</button>
        <button class="dialog-btn" id="btn-tayne-receipt" style="height:26px;font-size:10px;">🖨️ Print Oyster Receipt</button>
      </div>
    </div>
  </div>
  <footer class="win-statusbar" style="font-size:10px;">
    <div class="status-panel" id="tayne-engine-status" style="flex:1;">Sequence: TAYNE_BETA.SEQ</div>
    <div class="status-panel" style="width:110px;">Buffer: 128 KB</div>
    <div class="status-panel" style="width:80px;">READY</div>
  </footer>
</div>

<!-- 3. Disk Defragmenter Window -->
<div class="win-window bevel-raised app-window" id="win-defrag" style="top:90px;left:160px;width:530px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect x="2" y="2" width="12" height="12" fill="#c0c0c0" stroke="#000" stroke-width="1"/>
        <line x1="4" y1="5" x2="8" y2="5" stroke="#000" stroke-width="1"/>
        <circle cx="11" cy="11" r="1.5" fill="#00ff00"/>
      </svg>
      <span>Defragmenting Drive C:</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-min" title="Minimize">_</button>
      <button class="win-btn win-btn-max" title="Maximize">口</button>
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <div style="padding:10px;display:flex;flex-direction:column;gap:8px;">
    <!-- Drive Selector Header -->
    <div style="display:flex;align-items:center;gap:8px;">
      <svg width="22" height="22" viewBox="0 0 32 32">
        <rect x="2" y="6" width="28" height="20" rx="2" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
        <line x1="6" y1="12" x2="16" y2="12" stroke="#000" stroke-width="2"/>
        <circle cx="24" cy="20" r="2.5" fill="#00ff00"/>
      </svg>
      <span style="font-weight:bold;font-size:11px;">Drive C: (Cinco 4D3D3D3 Partition)</span>
    </div>

    <!-- Progress indicator -->
    <div>
      <div style="display:flex;justify-content:space-between;margin-bottom:3px;font-size:11px;">
        <span id="defrag-progress-text" style="font-weight:bold;">42% Complete</span>
        <span id="defrag-time-est" style="color:#555;">Est. time: 00:02:18</span>
      </div>
      <div class="bevel-sunken" style="height:18px;background:#ffffff;padding:2px;display:flex;">
        <div id="defrag-progress-bar" style="width:42%;background:linear-gradient(90deg, #000080, #1084d0);height:100%;transition:width 0.2s ease;"></div>
      </div>
    </div>

    <!-- Cluster Grid Visualizer -->
    <div class="bevel-sunken" style="background:#ffffff;padding:6px;">
      <div id="defrag-cluster-grid" style="display:grid;grid-template-columns:repeat(24, 1fr);gap:2px;max-height:160px;overflow:hidden;">
        <!-- Filled with cluster blocks in JS -->
      </div>
    </div>

    <!-- Cluster Map Legend -->
    <div class="bevel-thin-sunken" style="background:var(--win-gray);padding:6px 8px;display:flex;flex-wrap:wrap;gap:12px;font-size:10px;">
      <div style="display:flex;align-items:center;gap:4px;">
        <span style="display:inline-block;width:10px;height:10px;background:#000080;border:1px solid #000;"></span>
        <span>■ Allocated</span>
      </div>
      <div style="display:flex;align-items:center;gap:4px;">
        <span style="display:inline-block;width:10px;height:10px;background:#ffffff;border:1px solid #808080;"></span>
        <span>■ Free</span>
      </div>
      <div style="display:flex;align-items:center;gap:4px;">
        <span style="display:inline-block;width:10px;height:10px;background:#ff0000;border:1px solid #000;"></span>
        <span>■ 4d3d3d3 Fragmented</span>
      </div>
      <div style="display:flex;align-items:center;gap:4px;">
        <span style="display:inline-block;width:10px;height:10px;background:#008000;border:1px solid #000;"></span>
        <span>■ Unmovable</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div style="display:flex;justify-content:flex-end;gap:6px;margin-top:2px;">
      <button class="dialog-btn" id="btn-defrag-pause" style="min-width:64px;">Pause</button>
      <button class="dialog-btn" id="btn-defrag-stop" style="min-width:64px;">Stop</button>
      <button class="dialog-btn" id="btn-defrag-details" style="min-width:94px;">Show Details</button>
    </div>
  </div>
  <footer class="win-statusbar" style="font-size:10px;">
    <div class="status-panel" id="defrag-status-panel" style="flex:1;">Optimizing Cluster Sectors...</div>
    <div class="status-panel" style="width:130px;">ST7789 Frame Buffer</div>
  </footer>
</div>

<!-- 4. Lotus 1-2-3 Spreadsheet Window -->
<div class="win-window bevel-raised app-window" id="win-lotus" style="top:45px;left:70px;width:680px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#fff" stroke="#000" stroke-width="1"/>
        <rect width="16" height="4" fill="#000080"/>
        <line x1="0" y1="8" x2="16" y2="8" stroke="#808080"/>
        <line x1="6" y1="4" x2="6" y2="16" stroke="#808080"/>
        <line x1="11" y1="4" x2="11" y2="16" stroke="#808080"/>
      </svg>
      <span>Lotus 1-2-3 (Boss Mode) — [CORPORATE_BUDGET.WK1]</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-min" title="Minimize">_</button>
      <button class="win-btn win-btn-max" title="Maximize">口</button>
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <nav class="win-menubar">
    <div class="menu-item" tabindex="0"><span><u>W</u>orksheet</span></div>
    <div class="menu-item" tabindex="0"><span><u>R</u>ange</span></div>
    <div class="menu-item" tabindex="0"><span><u>C</u>opy</span></div>
    <div class="menu-item" tabindex="0"><span><u>M</u>ove</span></div>
    <div class="menu-item" tabindex="0"><span><u>F</u>ile</span></div>
    <div class="menu-item" tabindex="0"><span><u>P</u>rint</span></div>
    <div class="menu-item" tabindex="0"><span><u>G</u>raph</span></div>
    <div class="menu-item" tabindex="0"><span><u>D</u>ata</span></div>
    <div class="menu-item" tabindex="0"><span><u>S</u>ystem</span></div>
    <div class="menu-item" tabindex="0"><span><u>Q</u>uit</span></div>
  </nav>
  <div style="background:var(--win-gray);padding:2px 4px;display:flex;gap:4px;align-items:center;font-size:11px;">
    <div class="bevel-thin-sunken" style="background:#ffffff;padding:1px 6px;width:34px;font-weight:bold;">A1</div>
    <div class="bevel-thin-sunken" style="background:#ffffff;padding:1px 6px;flex:1;font-family:monospace;">'Q3 Cinco Business Systems Enterprise Forecast</div>
  </div>
  <div class="bevel-sunken" style="background:#ffffff;overflow:auto;max-height:280px;">
    <table class="lotus-table" style="width:100%;border-collapse:collapse;font-family:'Courier New', monospace;font-size:11px;">
      <thead>
        <tr style="background:var(--win-gray);text-align:center;">
          <th style="width:28px;border:1px solid #808080;padding:2px;"> </th>
          <th style="border:1px solid #808080;padding:2px;width:240px;">A</th>
          <th style="border:1px solid #808080;padding:2px;width:120px;">B</th>
          <th style="border:1px solid #808080;padding:2px;width:110px;">C</th>
          <th style="border:1px solid #808080;padding:2px;width:80px;">D</th>
          <th style="border:1px solid #808080;padding:2px;width:60px;">E</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="lotus-row-hdr">1</td>
          <td colspan="5" style="border:1px solid #d0d0d0;padding:3px;font-weight:bold;background:#e8f0fe;">Q3 Cinco Business Systems Enterprise Forecast</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">2</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">----------------------------------------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">------------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">-----------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">--------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">------</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">3</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">Celery Stalk Procurement</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$4,200,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#008000;font-weight:bold;">APPROVED</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">CORP-OPS</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">100%</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">4</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">Tayne Beta Research & Development</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$18,500,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#aa0000;font-weight:bold;">CONFIDENTIAL</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">R&D-SEC</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">99.4%</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">5</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">Oyster Smiling High-Resolution Printing</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$320,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#b08000;font-weight:bold;">PENDING</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">MKTG-PRN</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">45%</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">6</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">4d3d3d3 Macro Overclocking</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$9,800,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#000080;font-weight:bold;">ENGAGED</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">DSP-CORE</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">120%</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">7</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">----------------------------------------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">------------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">-----------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">--------</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">------</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">8</td>
          <td style="border:1px solid #d0d0d0;padding:3px;font-weight:bold;">TOTAL CORPORATE ALLOCATION</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;font-weight:bold;">$32,820,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;font-weight:bold;color:#000080;">SIGNED (PAUL)</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">AUDIT-OK</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">--</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">9</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">Executive Espresso Reserves</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$140,000</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#008000;">DISBURSED</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">OSHA-REC</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">100%</td>
        </tr>
        <tr>
          <td class="lotus-row-hdr">10</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">OSHA Compliance Reserve</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">$0</td>
          <td style="border:1px solid #d0d0d0;padding:3px;color:#666;">EXEMPT</td>
          <td style="border:1px solid #d0d0d0;padding:3px;">LEGAL</td>
          <td style="border:1px solid #d0d0d0;padding:3px;text-align:right;">0%</td>
        </tr>
      </tbody>
    </table>
  </div>
  <footer class="win-statusbar" style="font-size:10px;">
    <div class="status-panel" style="flex:1;">READY | A1 | CALC</div>
    <div class="status-panel" style="width:60px;">NUM</div>
    <div class="status-panel" style="width:60px;">CAPS</div>
  </footer>
</div>

<!-- 5. CINCO Help & User Manual Window -->
<div class="win-window bevel-raised app-window" id="win-manual" style="top:60px;left:130px;width:660px;height:450px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <path d="M3 2 L12 2 L14 4 L14 14 L3 14 Z" fill="#fff" stroke="#000" stroke-width="1"/>
        <text x="6" y="11" font-family="sans-serif" font-size="8" font-weight="bold" fill="#000080">?</text>
      </svg>
      <span>Cinco Business Systems Help — User Reference Guide</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-min" title="Minimize">_</button>
      <button class="win-btn win-btn-max" title="Maximize">口</button>
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <div class="win-toolbar" style="padding:2px 4px;">
    <button class="toolbar-btn" id="btn-manual-contents">📖 Contents</button>
    <button class="toolbar-btn" id="btn-manual-search">🔍 Search</button>
    <button class="toolbar-btn" id="btn-manual-print">🖨️ Print</button>
    <div class="toolbar-separator"></div>
    <button class="toolbar-btn" id="btn-manual-back">⬅ Back</button>
    <button class="toolbar-btn" id="btn-manual-forward">➡ Forward</button>
  </div>
  <div style="display:flex;flex:1;overflow:hidden;background:#ffffff;" class="bevel-sunken">
    <!-- Left Pane: TOC Tree -->
    <div style="width:190px;border-right:2px solid var(--win-gray);background:#f4f4f4;overflow-y:auto;padding:6px;font-size:11px;flex-shrink:0;">
      <div style="font-weight:bold;margin-bottom:6px;color:#444;">📚 Help Topics</div>
      <div class="manual-tree-item active" data-topic="welcome" id="toc-welcome">
        <span>📄 Welcome</span>
      </div>
      <div class="manual-tree-item" data-topic="controls" id="toc-controls">
        <span>🎛️ Hardware Controls</span>
      </div>
      <div class="manual-tree-item" data-topic="identities" id="toc-identities">
        <span>🕺 Dancers & Identities</span>
      </div>
      <div class="manual-tree-item" data-topic="kinetics" id="toc-kinetics">
        <span>⚡ 4d3d3d3 Kinetics</span>
      </div>
      <div class="manual-tree-item" data-topic="boss" id="toc-boss">
        <span>📊 Boss Key & Defrag</span>
      </div>
      <div class="manual-tree-item" data-topic="osha" id="toc-osha">
        <span>☕ OSHA Compliance</span>
      </div>
    </div>
    <!-- Right Pane: Topic Content View -->
    <div id="manual-content-view" style="flex:1;padding:12px 16px;overflow-y:auto;font-size:11px;line-height:1.5;">
      <!-- Populated dynamically via JS -->
    </div>
  </div>
  <footer class="win-statusbar" style="font-size:10px;">
    <div class="status-panel" id="manual-status-panel" style="flex:1;">Topic: Welcome to CINCO OS 2.5</div>
    <div class="status-panel" style="width:140px;">Cinco Corp © 1998</div>
  </footer>
</div>

<!-- 6. Setup Wizard Launcher Dialog -->
<div class="win-window bevel-raised app-window" id="win-setup-launcher" style="top:110px;left:200px;width:440px;">
  <div class="win-titlebar">
    <div class="win-titlebar-left">
      <svg class="win-title-icon" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#000080"/>
        <text x="4" y="12" font-family="monospace" font-size="9" font-weight="bold" fill="#fff">💾</text>
      </svg>
      <span>Cinco Setup & Hardware Flasher</span>
    </div>
    <div class="win-controls">
      <button class="win-btn win-btn-close" title="Close">×</button>
    </div>
  </div>
  <div style="display:flex;background:#ffffff;" class="bevel-sunken">
    <div style="width:110px;background:linear-gradient(180deg, #000080, #1084d0);padding:14px 8px;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;flex-shrink:0;">
      <svg width="48" height="48" viewBox="0 0 32 32">
        <rect x="2" y="2" width="28" height="28" rx="2" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
        <rect x="6" y="4" width="20" height="10" fill="#fff"/>
        <rect x="18" y="6" width="5" height="6" fill="#808080"/>
        <rect x="6" y="18" width="20" height="10" fill="#000080"/>
        <text x="12" y="26" font-family="monospace" font-size="8" font-weight="bold" fill="#fff">5</text>
      </svg>
      <b style="font-size:10px;margin-top:6px;font-family:monospace;">CINCO SETUP</b>
    </div>
    <div style="flex:1;padding:12px 14px;font-size:11px;line-height:1.45;">
      <h3 style="margin:0 0 6px;font-size:12px;color:var(--win-blue);">Cinco Hardware Installation Wizard</h3>
      <p style="margin:0 0 6px;">This utility flashes official Cinco OS 2.5 firmware onto physical <b>M-VAVE FM-1</b> synthesizer hardware via WebMIDI SysEx.</p>
      <div style="background:#f4f4f4;border:1px solid #ddd;padding:6px;margin-bottom:6px;font-size:10px;">
        <b>• Target Device:</b> M-VAVE FM-1 (USB MIDI)<br>
        <b>• Product ID:</b> FM-1_555 (Cinco Firmware 2.5)<br>
        <b>• Interface:</b> WebMIDI High-Speed SysEx Flasher
      </div>
      <p style="margin:0;font-size:10px;color:#555;">Click <b>Launch Setup Wizard</b> to open the flasher.</p>
    </div>
  </div>
  <div style="padding:8px 10px;display:flex;justify-content:flex-end;gap:6px;background:var(--win-gray);">
    <a href="installer/" class="dialog-btn" id="btn-launch-installer" style="text-decoration:none;display:inline-flex;align-items:center;font-weight:bold;color:#000;">Launch Setup Wizard ▶</a>
    <button class="dialog-btn" id="btn-cancel-installer">Cancel</button>
  </div>
</div>

<!-- 7. Windows 98 Shut Down Dialog -->
<div class="modal-overlay" id="modal-shutdown">
  <div class="modal-dialog bevel-raised" style="width:360px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left">
        <svg class="win-title-icon" viewBox="0 0 16 16">
          <rect width="16" height="16" fill="#000080"/>
          <circle cx="8" cy="8" r="5" fill="none" stroke="#fff" stroke-width="1.5"/>
          <line x1="8" y1="3" x2="8" y2="8" stroke="#fff" stroke-width="1.5"/>
        </svg>
        <span>Shut Down Windows</span>
      </div>
      <button class="win-btn" id="btn-shutdown-x">×</button>
    </div>
    <div class="modal-body" style="padding:14px 16px;">
      <div style="display:flex;gap:14px;align-items:flex-start;">
        <svg style="width:40px;height:40px;flex-shrink:0;" viewBox="0 0 32 32">
          <rect x="2" y="2" width="28" height="20" rx="1" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
          <rect x="4" y="4" width="24" height="16" fill="#008080"/>
          <path d="M12 22 L8 29 L24 29 L20 22 Z" fill="#808080" stroke="#000" stroke-width="1.5"/>
          <circle cx="16" cy="12" r="4" fill="none" stroke="#fff" stroke-width="1.5"/>
          <line x1="16" y1="8" x2="16" y2="12" stroke="#fff" stroke-width="1.5"/>
        </svg>
        <div style="flex:1;">
          <div style="font-size:11px;font-weight:bold;margin-bottom:8px;">What do you want the computer to do?</div>
          <div style="display:flex;flex-direction:column;gap:6px;font-size:11px;">
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="radio" name="shutdown-action" id="shutdown-opt-off" value="off" checked>
              <span>Shut down the computer</span>
            </label>
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="radio" name="shutdown-action" id="shutdown-opt-restart" value="restart">
              <span>Restart the computer</span>
            </label>
            <label style="display:flex;align-items:center;gap:6px;cursor:pointer;">
              <input type="radio" name="shutdown-action" id="shutdown-opt-dos" value="dos">
              <span>Restart the computer in MS-DOS mode</span>
            </label>
          </div>
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:6px;margin-top:14px;">
        <button class="dialog-btn" id="btn-shutdown-ok" style="min-width:64px;font-weight:bold;">OK</button>
        <button class="dialog-btn" id="btn-shutdown-cancel" style="min-width:64px;">Cancel</button>
        <button class="dialog-btn" id="btn-shutdown-help" style="min-width:64px;">Help</button>
      </div>
    </div>
  </div>
</div>

<!-- Iconic Windows 98 Safe to Turn Off Screen -->
<div id="screen-shutdown" style="display:none;position:fixed;inset:0;background:#000000;z-index:99999;flex-direction:column;align-items:center;justify-content:center;color:#ff8000;font-family:'Courier New', monospace;text-align:center;padding:20px;">
  <div style="font-size:32px;font-weight:bold;letter-spacing:1px;line-height:1.4;margin-bottom:30px;text-shadow:0 0 10px #ff6600;">
    It's now safe to turn off<br>your computer.
  </div>
  <button class="dialog-btn" id="btn-turn-on" style="font-size:12px;padding:6px 16px;font-weight:bold;background:var(--win-gray);color:#000;font-family:'MS Sans Serif', Tahoma, sans-serif;cursor:pointer;">
    Turn On / Restart Workstation
  </button>
</div>

<!-- MS-DOS Mode Screen -->
<div id="screen-dos" style="display:none;position:fixed;inset:0;background:#000000;z-index:99999;flex-direction:column;color:#dfdfdf;font-family:'Courier New', monospace;font-size:14px;padding:24px;">
  <div>Cinco Business Systems(R) MS-DOS 7.10</div>
  <div>(C)Copyright Cinco Corp 1981-1998. All rights reserved.</div>
  <br>
  <div>C:\CINCO> rem OSHA Compliance check passed.</div>
  <div>C:\CINCO> rem Identity generator offline. Type 'exit' to restart Windows.</div>
  <br>
  <div style="display:flex;align-items:center;gap:6px;">
    <span>C:\CINCO></span>
    <input type="text" id="dos-input" style="background:#000000;border:none;color:#ffffff;font-family:'Courier New', monospace;font-size:14px;outline:none;width:300px;" value="" placeholder="type 'exit' here" autofocus>
  </div>
  <div style="margin-top:24px;">
    <button class="dialog-btn" id="btn-dos-exit" style="background:var(--win-gray);color:#000;font-size:11px;font-family:'MS Sans Serif', sans-serif;">
      Return to CINCO OS 2.5 (EXIT)
    </button>
  </div>
</div>

<!-- 8. Coffee Break Information Dialog -->
<div class="modal-overlay" id="modal-coffee">
  <div class="modal-dialog bevel-raised" style="width:360px;">
    <div class="win-titlebar">
      <div class="win-titlebar-left">
        <svg class="win-title-icon" viewBox="0 0 16 16">
          <circle cx="8" cy="8" r="7" fill="#000080"/>
          <text x="6" y="12" font-family="serif" font-size="11" font-weight="bold" fill="#fff">i</text>
        </svg>
        <span>Cinco Executive Coffee Service</span>
      </div>
      <button class="win-btn" id="btn-coffee-x">×</button>
    </div>
    <div class="modal-body" style="padding:14px 16px;">
      <div style="display:flex;gap:14px;align-items:center;">
        <svg style="width:36px;height:36px;flex-shrink:0;" viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="14" fill="#000080"/>
          <text x="13" y="24" font-family="serif" font-size="22" font-weight="bold" fill="#fff">i</text>
        </svg>
        <div style="font-size:11px;line-height:1.45;">
          Managing Director Paul has taken a 15-minute executive espresso recess. OSHA vigilance level restored to 100%.
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;margin-top:14px;">
        <button class="dialog-btn" id="btn-coffee-ok" style="min-width:64px;font-weight:bold;">OK</button>
      </div>
    </div>
  </div>
</div>
'''

    if 'id="win-recycle"' in html:
        html = re.sub(r'<!-- =======================================================================\s*Application Windows & Authentic Windows 98 Dialogs[\s\S]*?(?=<script type="module">)', lambda _: new_windows_html + '\n', html)
    else:
        html = html.replace('<script type="module">', new_windows_html + '\n<script type="module">')

    # 7. JavaScript modifications
    # Replace alert() on coffee break
    old_coffee_js = '''document.getElementById("btn-coffee")?.addEventListener("click", () => {
  const el = document.getElementById("status-coffee");
  if (el) el.textContent = "☕ 100% (Hot)";
  alert("Cinco Coffee Service:\\nManaging Director Paul has taken a coffee break.\\nOSHA vigilance level restored to 100%.");
});'''

    new_coffee_js = '''document.getElementById("btn-coffee")?.addEventListener("click", () => {
  const el = document.getElementById("status-coffee");
  if (el) el.textContent = "☕ 100% (Hot)";
  document.getElementById("modal-coffee")?.classList.add("open");
});
document.getElementById("btn-coffee-ok")?.addEventListener("click", () => {
  document.getElementById("modal-coffee")?.classList.remove("open");
});
document.getElementById("btn-coffee-x")?.addEventListener("click", () => {
  document.getElementById("modal-coffee")?.classList.remove("open");
});'''
    html = html.replace(old_coffee_js, new_coffee_js)

    # Replace Desktop and Start Menu handlers, window manager, and shutdown handlers
    # Find the block starting at Desktop Icons Launchers
    js_section_to_replace = r'''// Desktop Icons Launchers
document.getElementById("d-app")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  if (win) { win.style.display = "flex"; }
  document.getElementById("task-pill-main")?.classList.remove("inactive");
});
document.getElementById("d-tayne")?.addEventListener("click", () => selectIdentity(2, "Tayne Beta"));
document.getElementById("d-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("d-boss")?.addEventListener("click", () => pressBtn("EDIT"));
document.getElementById("d-recycle")?.addEventListener("click", () => alert("Recycle Bin is currently empty."));

document.getElementById("sm-app")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  if (win) { win.style.display = "flex"; }
  document.getElementById("task-pill-main")?.classList.remove("inactive");
});
document.getElementById("sm-tayne")?.addEventListener("click", () => selectIdentity(2, "Tayne Beta"));
document.getElementById("sm-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("sm-boss")?.addEventListener("click", () => pressBtn("EDIT"));
document.getElementById("sm-shutdown")?.addEventListener("click", () => {
  if (confirm("Shut down CINCO OS 2.5 Workstation?")) window.location.href = "about:blank";
});

// Menu shortcuts
document.getElementById("m-switch-on")?.addEventListener("click", () => {
  const go = document.getElementById("go");
  if (go && !go.disabled) go.click();
});
document.getElementById("m-restart")?.addEventListener("click", () => window.location.reload());
document.getElementById("m-exit")?.addEventListener("click", () => {
  if (confirm("Exit CINCO OS 2.5?")) window.location.href = "about:blank";
});
document.getElementById("m-celery")?.addEventListener("click", () => selectIdentity(0, "Celery Man"));
document.getElementById("m-oyster")?.addEventListener("click", () => selectIdentity(1, "Oyster Smiling"));
document.getElementById("m-tayne")?.addEventListener("click", () => selectIdentity(2, "Tayne Beta"));
document.getElementById("m-speech")?.addEventListener("click", () => selectIdentity(3, "Speech Synth"));
document.getElementById("m-wobble")?.addEventListener("click", () => pressBtn("LFO"));
document.getElementById("m-flail")?.addEventListener("click", () => pressBtn("ARP"));
document.getElementById("m-nude")?.addEventListener("click", () => {
  selectIdentity(2, "Tayne Beta");
  pressBtn("FX");
  send({ type: "cinco", fn: "trigger_nsfw" });
});
document.getElementById("m-k4d")?.addEventListener("click", () => updateMacro(96));
document.getElementById("m-defrag")?.addEventListener("click", () => pressBtn("SEQ"));
document.getElementById("m-boss")?.addEventListener("click", () => pressBtn("EDIT"));
document.getElementById("m-screensaver")?.addEventListener("click", () => send({ type: "cinco", fn: "set_screensaver", args: [1] }));

// Window min / max / close
document.getElementById("btn-win-min")?.addEventListener("click", () => {
  const win = document.getElementById("main-win");
  const pill = document.getElementById("task-pill-main");
  if (win && pill) {
    win.style.display = "none";
    pill.classList.add("inactive");
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
  win.style.maxWidth = win.style.maxWidth === "100%" ? "1060px" : "100%";
});
document.getElementById("btn-win-close")?.addEventListener("click", () => {
  if (confirm("Shut down CINCO OS 2.5?")) window.location.href = "installer/";
});'''

    new_js_logic = r'''// ------------------------------------------------------------------ Window Management & Taskbar Integration
let topZIndex = 200;

const Windows = {
  main: { id: "main-win", pillId: "task-pill-main" },
  recycle: { id: "win-recycle", pillId: "task-pill-recycle" },
  tayne: { id: "win-tayne", pillId: "task-pill-tayne" },
  defrag: { id: "win-defrag", pillId: "task-pill-defrag" },
  lotus: { id: "win-lotus", pillId: "task-pill-lotus" },
  manual: { id: "win-manual", pillId: "task-pill-manual" },
  setup: { id: "win-setup-launcher", pillId: "task-pill-setup" }
};

function bringToFront(winKey) {
  const cfg = Windows[winKey];
  if (!cfg) return;
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);
  if (!win) return;

  topZIndex += 2;
  win.style.zIndex = topZIndex;

  // Set active titlebar, inactive for others
  document.querySelectorAll(".win-window").forEach(w => {
    const tb = w.querySelector(".win-titlebar");
    if (tb) {
      if (w === win) tb.classList.remove("inactive");
      else tb.classList.add("inactive");
    }
  });

  // Taskbar pill active state
  document.querySelectorAll(".task-pill").forEach(p => p.classList.add("inactive"));
  if (pill) pill.classList.remove("inactive");
}

function openWindow(winKey) {
  const cfg = Windows[winKey];
  if (!cfg) return;
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);
  if (!win) return;

  win.style.display = "flex";
  if (pill) {
    pill.style.display = "flex";
    pill.classList.remove("inactive");
  }
  bringToFront(winKey);
}

function closeWindow(winKey) {
  const cfg = Windows[winKey];
  if (!cfg) return;
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);
  if (win) win.style.display = "none";
  if (pill) {
    pill.style.display = "none";
    pill.classList.add("inactive");
  }
}

function minimizeWindow(winKey) {
  const cfg = Windows[winKey];
  if (!cfg) return;
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);
  if (win) win.style.display = "none";
  if (pill) pill.classList.add("inactive");
}

function toggleWindowPill(winKey) {
  const cfg = Windows[winKey];
  if (!cfg) return;
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);
  if (!win) return;

  const isHidden = (win.style.display === "none" || getComputedStyle(win).display === "none");
  const isTop = (parseInt(win.style.zIndex || "0", 10) >= topZIndex && !isHidden && pill && !pill.classList.contains("inactive"));

  if (isHidden) {
    openWindow(winKey);
  } else if (isTop) {
    minimizeWindow(winKey);
  } else {
    bringToFront(winKey);
  }
}

// Attach window controls and pill listeners for all windows
Object.keys(Windows).forEach(winKey => {
  const cfg = Windows[winKey];
  const win = document.getElementById(cfg.id);
  const pill = document.getElementById(cfg.pillId);

  if (pill) {
    pill.addEventListener("click", () => toggleWindowPill(winKey));
  }

  if (win) {
    win.addEventListener("mousedown", () => bringToFront(winKey));

    const minBtn = win.querySelector(".win-btn-min");
    const maxBtn = win.querySelector(".win-btn-max");
    const closeBtn = win.querySelector(".win-btn-close");

    minBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      minimizeWindow(winKey);
    });

    maxBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      if (winKey === "main") {
        win.style.maxWidth = win.style.maxWidth === "100%" ? "1060px" : "100%";
      } else {
        if (win.dataset.maximized === "true") {
          win.style.top = win.dataset.origTop || "60px";
          win.style.left = win.dataset.origLeft || "60px";
          win.style.width = win.dataset.origWidth || "560px";
          win.style.height = win.dataset.origHeight || "380px";
          win.dataset.maximized = "false";
        } else {
          win.dataset.origTop = win.style.top;
          win.dataset.origLeft = win.style.left;
          win.dataset.origWidth = win.style.width;
          win.dataset.origHeight = win.style.height;
          win.style.top = "10px";
          win.style.left = "10px";
          win.style.width = "calc(100vw - 20px)";
          win.style.height = "calc(100vh - 54px)";
          win.dataset.maximized = "true";
        }
      }
    });

    closeBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      if (winKey === "main") {
        document.getElementById("modal-shutdown")?.classList.add("open");
      } else {
        closeWindow(winKey);
      }
    });
  }
});

// Window draggable titlebars
document.querySelectorAll(".app-window").forEach(win => {
  const tb = win.querySelector(".win-titlebar");
  if (!tb) return;

  let isDragging = false;
  let startX = 0, startY = 0, origLeft = 0, origTop = 0;

  tb.addEventListener("mousedown", (e) => {
    if (e.target.closest(".win-btn")) return;
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    const rect = win.getBoundingClientRect();
    origLeft = rect.left;
    origTop = rect.top;

    const onMouseMove = (ev) => {
      if (!isDragging) return;
      const dx = ev.clientX - startX;
      const dy = ev.clientY - startY;
      const newL = Math.max(0, Math.min(window.innerWidth - 60, origLeft + dx));
      const newT = Math.max(0, Math.min(window.innerHeight - 60, origTop + dy));
      win.style.left = `${newL}px`;
      win.style.top = `${newT}px`;
      win.style.right = "auto";
      win.style.bottom = "auto";
    };

    const onMouseUp = () => {
      isDragging = false;
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  });
});

// ------------------------------------------------------------------ 1. Recycle Bin Window & Incinerator Dialog
const dRecycle = document.getElementById("d-recycle");
const winRecycle = document.getElementById("win-recycle");
const btnEmptyRecycle = document.getElementById("btn-empty-recycle");
const modalConfirmRecycle = document.getElementById("modal-confirm-recycle");
const btnConfirmRecycleYes = document.getElementById("btn-confirm-recycle-yes");
const btnConfirmRecycleNo = document.getElementById("btn-confirm-recycle-no");
const btnConfirmRecycleX = document.getElementById("btn-confirm-recycle-x");
const recycleTbody = document.getElementById("recycle-tbody");
const recycleEmptyMsg = document.getElementById("recycle-empty-msg");
const recycleStatusCount = document.getElementById("recycle-status-count");
const recycleStatusSize = document.getElementById("recycle-status-size");

const openRecycle = () => openWindow("recycle");
dRecycle?.addEventListener("click", openRecycle);
dRecycle?.addEventListener("dblclick", openRecycle);

btnEmptyRecycle?.addEventListener("click", () => {
  modalConfirmRecycle?.classList.add("open");
});

const closeConfirmRecycle = () => modalConfirmRecycle?.classList.remove("open");
btnConfirmRecycleNo?.addEventListener("click", closeConfirmRecycle);
btnConfirmRecycleX?.addEventListener("click", closeConfirmRecycle);

btnConfirmRecycleYes?.addEventListener("click", () => {
  if (recycleTbody) recycleTbody.innerHTML = "";
  if (recycleEmptyMsg) recycleEmptyMsg.style.display = "block";
  if (recycleStatusCount) recycleStatusCount.textContent = "0 object(s)";
  if (recycleStatusSize) recycleStatusSize.textContent = "0 bytes";

  // Swap desktop icon to empty bin
  const svgEl = document.getElementById("recycle-desktop-svg");
  if (svgEl) {
    svgEl.innerHTML = `
      <path d="M7 8 L25 8 L23 28 L9 28 Z" fill="#c0c0c0" stroke="#000" stroke-width="1.5"/>
      <line x1="5" y1="8" x2="27" y2="8" stroke="#000" stroke-width="2"/>
      <rect x="12" y="5" width="8" height="3" fill="#808080" stroke="#000" stroke-width="1"/>
      <line x1="12" y1="12" x2="12" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="16" y1="12" x2="16" y2="24" stroke="#808080" stroke-width="1.5"/>
      <line x1="20" y1="12" x2="20" y2="24" stroke="#808080" stroke-width="1.5"/>
    `;
  }
  closeConfirmRecycle();
});

// Selection highlighting in Recycle Bin list
recycleTbody?.addEventListener("click", (e) => {
  const row = e.target.closest("tr");
  if (!row) return;
  recycleTbody.querySelectorAll("tr").forEach(r => r.classList.remove("selected"));
  row.classList.add("selected");
});

// ------------------------------------------------------------------ 2. Tayne Studio 98 Window
const openTayneStudio = () => openWindow("tayne");
document.getElementById("d-tayne")?.addEventListener("click", openTayneStudio);
document.getElementById("d-tayne")?.addEventListener("dblclick", openTayneStudio);
document.getElementById("sm-tayne")?.addEventListener("click", openTayneStudio);
document.getElementById("tb-tayne")?.addEventListener("click", openTayneStudio);

document.getElementById("btn-tayne-load")?.addEventListener("click", () => {
  selectIdentity(2, "TAYNE BETA");
  const el = document.getElementById("tayne-status-card");
  if (el) el.textContent = "Loaded in Terminal";
});

document.getElementById("btn-tayne-wobble")?.addEventListener("click", () => {
  pressBtn("LFO");
});

document.getElementById("btn-tayne-flarh")?.addEventListener("click", () => {
  pressBtn("ARP");
});

document.getElementById("btn-tayne-nude")?.addEventListener("click", () => {
  selectIdentity(2, "TAYNE BETA");
  pressBtn("FX");
  send({ type: "cinco", fn: "trigger_nsfw" });
});

document.getElementById("btn-tayne-receipt")?.addEventListener("click", () => {
  selectIdentity(1, "Oyster Smiling");
  pressBtn("SAVE");
  send({ type: "cinco", fn: "trigger_receipt" });
});

// ------------------------------------------------------------------ 3. Disk Defragmenter Window
const clusterGrid = document.getElementById("defrag-cluster-grid");
let defragInterval = null;
let defragPercent = 42;
let defragPaused = false;

function initDefragGrid() {
  if (!clusterGrid || clusterGrid.children.length > 0) return;
  for (let i = 0; i < 240; i++) {
    const block = document.createElement("div");
    block.className = "cluster-block";
    if (i < 40) block.classList.add("cluster-allocated");
    else if (i < 48) block.classList.add("cluster-unmovable");
    else if (i < 96) block.classList.add(i % 3 === 0 ? "cluster-fragmented" : "cluster-allocated");
    else if (i < 150) block.classList.add(i % 5 === 0 ? "cluster-free" : "cluster-allocated");
    else block.classList.add("cluster-free");
    clusterGrid.appendChild(block);
  }
}

function startDefragAnim() {
  initDefragGrid();
  if (defragInterval) return;
  defragInterval = setInterval(() => {
    if (defragPaused || !clusterGrid) return;

    // Pick random fragmented or free block to defrag
    const frags = clusterGrid.querySelectorAll(".cluster-fragmented");
    if (frags.length > 0) {
      const idx = Math.floor(Math.random() * frags.length);
      const target = frags[idx];
      target.classList.add("cluster-active");
      setTimeout(() => {
        target.classList.remove("cluster-active", "cluster-fragmented");
        target.classList.add("cluster-allocated");
      }, 150);
    }

    if (defragPercent < 99) {
      defragPercent += 1;
      const textEl = document.getElementById("defrag-progress-text");
      const barEl = document.getElementById("defrag-progress-bar");
      if (textEl) textEl.textContent = `${defragPercent}% Complete`;
      if (barEl) barEl.style.width = `${defragPercent}%`;
    }
  }, 350);
}

const openDefrag = () => {
  openWindow("defrag");
  startDefragAnim();
};
document.getElementById("d-defrag")?.addEventListener("click", openDefrag);
document.getElementById("d-defrag")?.addEventListener("dblclick", openDefrag);
document.getElementById("sm-defrag")?.addEventListener("click", openDefrag);
document.getElementById("m-defrag")?.addEventListener("click", openDefrag);

document.getElementById("btn-defrag-pause")?.addEventListener("click", (e) => {
  defragPaused = !defragPaused;
  e.target.textContent = defragPaused ? "Resume" : "Pause";
});

document.getElementById("btn-defrag-stop")?.addEventListener("click", () => {
  clearInterval(defragInterval);
  defragInterval = null;
  const statusEl = document.getElementById("defrag-status-panel");
  if (statusEl) statusEl.textContent = "Defragmentation Stopped.";
});

document.getElementById("btn-defrag-details")?.addEventListener("click", () => {
  pressBtn("SEQ");
});

// ------------------------------------------------------------------ 4. Lotus 1-2-3 (Boss Mode) Window
const openLotus = () => {
  openWindow("lotus");
  pressBtn("EDIT");
};
document.getElementById("d-boss")?.addEventListener("click", openLotus);
document.getElementById("d-boss")?.addEventListener("dblclick", openLotus);
document.getElementById("sm-boss")?.addEventListener("click", openLotus);
document.getElementById("m-boss")?.addEventListener("click", openLotus);

// ------------------------------------------------------------------ 5. CINCO Help & User Manual Window
const manualTopics = {
  welcome: `
    <h3 style="margin-top:0;color:var(--win-blue);">Welcome to CINCO OS 2.5 Workstation</h3>
    <p><b>Executive Memorandum — Cinco Business Systems, Inc.</b></p>
    <p><b>From:</b> Paul (Senior Managing Director)<br>
    <b>To:</b> Department of Identity Operations<br>
    <b>Subject:</b> Enterprise Identity Synthesis & Workstation Deployment</p>
    <hr style="border:none;border-top:1px solid #c0c0c0;margin:8px 0;">
    <p>Welcome to your state-of-the-art Windows 98 workstation. This terminal is equipped with the proprietary <b>4D3D3D3 neural choreographic coprocessor</b> and real-time fixed-point AudioWorklet DSP sound engine.</p>
    <p>Ensure that all generated dancers maintain appropriate corporate posture. Do not engage unapproved NSFW dancer sequences without express executive authorization.</p>
  `,
  controls: `
    <h3 style="margin-top:0;color:var(--win-blue);">Hardware Controls Reference</h3>
    <p>The Cinco OS 2.5 workstation interfaces directly with physical M-VAVE FM-1 synthesizers and virtual WebAudio worklets:</p>
    <ul>
      <li><b>MACRO (K1):</b> 4D3D3D3 Macro Engager (0-1023). Values > 80 engage hyper-kinetic dance acceleration.</li>
      <li><b>TEMPO (K2):</b> Master Sequencer BPM (60-240 BPM). Sets master clock rate.</li>
      <li><b>TONE (K3):</b> Filter Cutoff / Identity Timbre Brightness.</li>
      <li><b>MIX (K4):</b> Synthesizer Wet/Dry Identity Balance.</li>
    </ul>
    <p><b>Console Buttons (panel.c):</b></p>
    <ul>
      <li><code>FX</code> — Special FX / Nude Tayne Mode</li>
      <li><code>LFO</code> — Hat Wobble Kinetic Modulation</li>
      <li><code>ARP</code> — Flarhgunnstow Arpeggiator</li>
      <li><code>EDIT</code> — Lotus 1-2-3 Boss Concealment Mode</li>
      <li><code>SEQ</code> — Disk Defragmenter Cluster Display</li>
      <li><code>SAVE</code> — High-Resolution Oyster Receipt Printout</li>
    </ul>
  `,
  identities: `
    <h3 style="margin-top:0;color:var(--win-blue);">Dancers & Identity Profiles</h3>
    <p>Cinco Business Systems provides 4 certified enterprise dancer profiles:</p>
    <ol>
      <li><b>Celery Man (Identity 0):</b> The foundational corporate entertainer. Balanced kinetic agility, smooth transitions, 100% OSHA certified.</li>
      <li><b>Oyster Smiling (Identity 1):</b> Dental excellence specialist. Produces high-resolution corporate printouts and receipts.</li>
      <li><b>Tayne Beta (Identity 2):</b> Advanced choreographic sequence asset. Features enhanced hat elasticity, wobble dynamics, and multi-tier sequences.</li>
      <li><b>Speech Synth (Identity 3):</b> SAM-based phoneme vocalizer with robotic pitch tracking.</li>
    </ol>
  `,
  kinetics: `
    <h3 style="margin-top:0;color:var(--win-blue);">4d3d3d3 Kinetics Engine</h3>
    <p>The 4d3d3d3 calculation pipeline governs all non-Euclidean choreographic movement:</p>
    <ul>
      <li><b>Hat Wobble:</b> Resonant low-frequency kinetic oscillation applied to dancer headwear. Oscillates at 2.4 Hz to 8.8 Hz.</li>
      <li><b>Flarhgunnstow:</b> High-velocity multi-limb flailing sequence designed to relieve office tension and boost morale.</li>
      <li><b>Nude Tayne Protocol:</b> <i>RESTRICTED.</i> Generates unapproved NSFW dancer sequences. Triggers immediate OSHA audit warnings and requires executive signoff.</li>
    </ul>
  `,
  boss: `
    <h3 style="margin-top:0;color:var(--win-blue);">Boss Key & Disk Defragmenter</h3>
    <p><b>Lotus 1-2-3 Boss Concealment:</b></p>
    <p>Pressing the <code>EDIT</code> button or clicking the desktop Lotus 1-2-3 icon instantly conceals all synthesizer activities behind the Q3 Corporate Budget forecast.</p>
    <p><b>Drive C: Defragmenter:</b></p>
    <p>Pressing <code>SEQ</code> or opening Cinco Defrag scans and reorganizes fragmented 4d3d3d3 data clusters on the ST7789 display memory map.</p>
  `,
  osha: `
    <h3 style="margin-top:0;color:var(--win-blue);">OSHA Workplace Compliance Guidelines</h3>
    <p>Guidelines for safe operation of the Cinco 2.5 Workstation:</p>
    <ul>
      <li><b>Mandatory Coffee Recesses:</b> Click the <i>☕ Coffee</i> status indicator to log Managing Director Paul's executive espresso recess and restore vigilance to 100%.</li>
      <li><b>Celery Limits:</b> Maximum recommended intake is 14 stalks per 8-hour shift.</li>
      <li><b>CRT Degaussing:</b> Degauss the monitor regularly using the <i>Degauss CRT</i> button to clear magnetic field buildup.</li>
    </ul>
  `
};

function showManualTopic(topicKey) {
  const contentView = document.getElementById("manual-content-view");
  const statusPanel = document.getElementById("manual-status-panel");
  if (contentView && manualTopics[topicKey]) {
    contentView.innerHTML = manualTopics[topicKey];
  }
  document.querySelectorAll(".manual-tree-item").forEach(item => {
    item.classList.toggle("active", item.dataset.topic === topicKey);
  });
  if (statusPanel) {
    statusPanel.textContent = `Topic: ${topicKey.charAt(0).toUpperCase() + topicKey.slice(1)}`;
  }
}

const openManual = () => {
  openWindow("manual");
  showManualTopic("welcome");
};
document.getElementById("d-manual")?.addEventListener("click", openManual);
document.getElementById("d-manual")?.addEventListener("dblclick", openManual);
document.getElementById("sm-manual")?.addEventListener("click", openManual);
document.getElementById("m-manual")?.addEventListener("click", openManual);

document.querySelectorAll(".manual-tree-item").forEach(item => {
  item.addEventListener("click", () => {
    const t = item.dataset.topic;
    if (t) showManualTopic(t);
  });
});
showManualTopic("welcome");

// ------------------------------------------------------------------ 6. Setup Wizard Launcher Window
const openSetupLauncher = () => openWindow("setup");
document.getElementById("d-installer")?.addEventListener("click", openSetupLauncher);
document.getElementById("d-installer")?.addEventListener("dblclick", openSetupLauncher);
document.getElementById("sm-installer")?.addEventListener("click", openSetupLauncher);
document.getElementById("btn-cancel-installer")?.addEventListener("click", () => closeWindow("setup"));

// ------------------------------------------------------------------ 7. Windows 98 Shut Down Dialog & Screens
const modalShutdown = document.getElementById("modal-shutdown");
const screenShutdown = document.getElementById("screen-shutdown");
const screenDos = document.getElementById("screen-dos");
const dosInput = document.getElementById("dos-input");

const showShutdownDialog = () => {
  modalShutdown?.classList.add("open");
};

const closeShutdownDialog = () => {
  modalShutdown?.classList.remove("open");
};

document.getElementById("sm-shutdown")?.addEventListener("click", showShutdownDialog);
document.getElementById("m-exit")?.addEventListener("click", showShutdownDialog);
document.getElementById("btn-win-close")?.addEventListener("click", showShutdownDialog);
document.getElementById("btn-shutdown-cancel")?.addEventListener("click", closeShutdownDialog);
document.getElementById("btn-shutdown-x")?.addEventListener("click", closeShutdownDialog);
document.getElementById("btn-shutdown-help")?.addEventListener("click", () => {
  closeShutdownDialog();
  openManual();
  showManualTopic("osha");
});

document.getElementById("btn-shutdown-ok")?.addEventListener("click", () => {
  const action = document.querySelector('input[name="shutdown-action"]:checked')?.value || "off";
  closeShutdownDialog();

  if (action === "off") {
    if (screenShutdown) screenShutdown.style.display = "flex";
  } else if (action === "restart") {
    window.location.reload();
  } else if (action === "dos") {
    if (screenDos) {
      screenDos.style.display = "flex";
      dosInput?.focus();
    }
  }
});

// Restart button on "Safe to turn off" screen
document.getElementById("btn-turn-on")?.addEventListener("click", () => {
  if (screenShutdown) screenShutdown.style.display = "none";
});

// MS-DOS mode return
const exitDos = () => {
  if (screenDos) screenDos.style.display = "none";
};
document.getElementById("btn-dos-exit")?.addEventListener("click", exitDos);
dosInput?.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    if (dosInput.value.trim().toLowerCase() === "exit") {
      dosInput.value = "";
      exitDos();
    } else {
      dosInput.value = "";
    }
  }
});

// ------------------------------------------------------------------ App & Menu Shortcuts
document.getElementById("d-app")?.addEventListener("click", () => openWindow("main"));
document.getElementById("d-app")?.addEventListener("dblclick", () => openWindow("main"));
document.getElementById("sm-app")?.addEventListener("click", () => openWindow("main"));

document.getElementById("m-switch-on")?.addEventListener("click", () => {
  const go = document.getElementById("go");
  if (go && !go.disabled) go.click();
});
document.getElementById("m-restart")?.addEventListener("click", () => window.location.reload());
document.getElementById("m-celery")?.addEventListener("click", () => selectIdentity(0, "Celery Man"));
document.getElementById("m-oyster")?.addEventListener("click", () => selectIdentity(1, "Oyster Smiling"));
document.getElementById("m-tayne")?.addEventListener("click", () => selectIdentity(2, "Tayne Beta"));
document.getElementById("m-speech")?.addEventListener("click", () => selectIdentity(3, "Speech Synth"));
document.getElementById("m-wobble")?.addEventListener("click", () => pressBtn("LFO"));
document.getElementById("m-flail")?.addEventListener("click", () => pressBtn("ARP"));
document.getElementById("m-nude")?.addEventListener("click", () => {
  selectIdentity(2, "Tayne Beta");
  pressBtn("FX");
  send({ type: "cinco", fn: "trigger_nsfw" });
});
document.getElementById("m-k4d")?.addEventListener("click", () => updateMacro(96));
document.getElementById("m-screensaver")?.addEventListener("click", () => send({ type: "cinco", fn: "set_screensaver", args: [1] }));'''

    html = html.replace(js_section_to_replace, new_js_logic)

    # Now verify zero alert() and confirm()
    remaining_alerts = re.findall(r'\balert\(', html)
    remaining_confirms = re.findall(r'\bconfirm\(', html)
    print(f"Remaining alerts: {len(remaining_alerts)}, confirms: {len(remaining_confirms)}")
    if remaining_alerts or remaining_confirms:
        raise RuntimeError(f"Still found alerts: {remaining_alerts} or confirms: {remaining_confirms}")

    # Generate new generate_win98_workstation.py
    new_generator = f'''#!/usr/bin/env python3
"""
Generate CINCO OS 2.5 Workstation (Windows 98 Desktop & Multimedia Application OS)
Overhauls web/emu/index.html into an authentic, immersive 1998 Windows environment.
Eliminates ALL browser alert() and confirm() calls with authentic in-universe dialogs.
"""

OUTPUT_HTML = "web/emu/index.html"

def main():
    with open("web/emu/index.html", "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Successfully generated {{OUTPUT_HTML}} ({{len(HTML_CONTENT)}} bytes)")

HTML_CONTENT = r\'\'\'{html}\'\'\'

if __name__ == "__main__":
    main()
'''

    with open("scripts/generate_win98_workstation.py", "w", encoding="utf-8") as f:
        f.write(new_generator)
    print("Wrote scripts/generate_win98_workstation.py")

    with open("web/emu/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote web/emu/index.html")

if __name__ == "__main__":
    generate()
