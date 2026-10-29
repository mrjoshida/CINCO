#!/usr/bin/env python3
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

html_content = f"""<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-only
     Cinco Identity Generator 2.5™ Web Installer
     Cinco Business Systems, Inc. [v2.5] (Celery Man Edition)
     Portions derived from Felucca by Leo Kuroshita (@kurogedelic), Hügelton Instruments (GPL-3.0) -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cinco Identity Generator 2.5™ — Web Installer</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 rx=%223%22 fill=%22%23000%22/%3E%3Ctext x=%222%22 y=%2212%22 font-family=%22monospace%22 font-size=%2210%22 font-weight=%22bold%22 fill=%22%2300ff66%22%3E5%3C/text%3E%3C/svg%3E">
<meta name="description" content="Connect your M-VAVE FM-1 via USB-C in Chrome or Edge. Installs Cinco Identity Generator 2.5 (Celery Man Edition) directly over WebMIDI SysEx.">
<style>
  :root {{
    --bg: #0d0e12;
    --panel: #16181f;
    --panel-border: #282b37;
    --panel-inner: #0f1015;
    --fg: #e2e4ea;
    --dim: #8b8f9e;
    --dimmer: #545766;
    --accent: #00ff66;
    --accent-glow: rgba(0, 255, 102, 0.25);
    --accent-bg: #082613;
    --amber: #ffb000;
    --cyan: #38bdf8;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  }}
  @media (prefers-color-scheme: light) {{
    :root[data-theme="light"] {{
      --bg: #e5e7eb;
      --panel: #ffffff;
      --panel-border: #d1d5db;
      --panel-inner: #f3f4f6;
      --fg: #111827;
      --dim: #4b5563;
      --dimmer: #9ca3af;
      --accent: #059669;
      --accent-glow: rgba(5, 150, 105, 0.2);
      --accent-bg: #d1fae5;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--fg);
    font: 14px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  main {{
    max-width: 620px;
    margin: 0 auto;
    padding: 36px 16px 64px;
  }}
  .workstation-frame {{
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    padding: 24px;
    margin-bottom: 24px;
  }}
  .brand-header {{
    border-bottom: 1px solid var(--panel-border);
    padding-bottom: 16px;
    margin-bottom: 20px;
  }}
  .corp-tag {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    color: var(--dim);
    text-transform: uppercase;
    margin-bottom: 8px;
  }}
  .corp-badge {{
    background: var(--panel-inner);
    border: 1px solid var(--panel-border);
    padding: 2px 8px;
    border-radius: 3px;
    color: var(--accent);
    font-weight: 700;
  }}
  h1 {{
    font-size: 22px;
    font-weight: 700;
    margin: 0 0 6px;
    letter-spacing: -0.01em;
    color: #fff;
  }}
  .subtitle {{
    font-size: 13px;
    color: var(--dim);
    margin: 0;
  }}
  .lang-toggle {{
    background: none;
    border: 1px solid var(--panel-border);
    color: var(--dim);
    padding: 3px 10px;
    font-size: 11px;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
  }}
  .lang-toggle:hover {{
    color: var(--fg);
    border-color: var(--dim);
  }}
  .desc-box {{
    background: var(--panel-inner);
    border-left: 3px solid var(--accent);
    padding: 12px 14px;
    border-radius: 0 4px 4px 0;
    margin-bottom: 20px;
    font-size: 13.5px;
  }}
  .desc-box p {{ margin: 0; }}
  .desc-box p + p {{ margin-top: 8px; }}
  .warn-text {{
    color: var(--amber);
    font-size: 12px;
  }}
  .btn-row {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 24px 0;
  }}
  .btn-install {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-family: var(--mono);
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.04em;
    background: var(--accent);
    color: #06180c;
    border: none;
    padding: 14px 24px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease-in-out;
    box-shadow: 0 4px 16px var(--accent-glow);
    width: 100%;
  }}
  .btn-install:hover:not(:disabled) {{
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 255, 102, 0.35);
  }}
  .btn-install:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }}
  .btn-emu {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #1b2230;
    color: var(--cyan);
    border: 1px solid #2d3b52;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 13.5px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.15s;
    text-align: center;
  }}
  .btn-emu:hover {{
    background: #242e42;
    border-color: #425575;
    color: #60a5fa;
  }}
  progress {{
    width: 100%;
    height: 6px;
    border-radius: 3px;
    margin: 12px 0;
    accent-color: var(--accent);
    background: var(--panel-inner);
    border: none;
  }}
  progress::-webkit-progress-bar {{
    background: var(--panel-inner);
    border-radius: 3px;
  }}
  progress::-webkit-progress-value {{
    background: var(--accent);
    border-radius: 3px;
  }}
  .status-line {{
    font-family: var(--mono);
    font-size: 13px;
    color: var(--accent);
    min-height: 1.5em;
    margin-bottom: 8px;
    word-break: break-all;
  }}
  pre#log {{
    background: var(--panel-inner);
    border: 1px solid var(--panel-border);
    border-radius: 4px;
    padding: 10px 12px;
    color: var(--dim);
    font-family: var(--mono);
    font-size: 11px;
    max-height: 160px;
    overflow-y: auto;
    white-space: pre-wrap;
    margin: 0 0 20px;
  }}
  .specs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 16px 0;
    font-family: var(--mono);
    font-size: 11.5px;
    color: var(--dim);
  }}
  .spec-item {{
    background: var(--panel-inner);
    border: 1px solid var(--panel-border);
    padding: 6px 10px;
    border-radius: 4px;
  }}
  .spec-label {{ color: var(--dimmer); display: block; font-size: 10px; text-transform: uppercase; }}
  .spec-val {{ color: var(--fg); font-weight: 600; }}
  details.stock-box {{
    background: var(--panel-inner);
    border: 1px solid var(--panel-border);
    border-radius: 6px;
    padding: 12px 14px;
    margin-top: 20px;
    font-size: 13px;
  }}
  details.stock-box summary {{
    cursor: pointer;
    font-weight: 600;
    color: var(--dim);
    user-select: none;
  }}
  details.stock-box summary:hover {{ color: var(--fg); }}
  .stock-content {{
    margin-top: 14px;
    border-top: 1px solid var(--panel-border);
    padding-top: 12px;
  }}
  .stock-content input[type="file"] {{
    font-family: var(--mono);
    font-size: 12px;
    margin: 8px 0;
    color: var(--dim);
  }}
  .btn-stock {{
    background: #2a2d39;
    color: #fff;
    border: 1px solid #3e4253;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
    font-family: inherit;
    margin-top: 6px;
  }}
  .btn-stock:hover:not(:disabled) {{ background: #373b4b; }}
  .btn-stock:disabled {{ opacity: 0.3; cursor: default; }}
  footer {{
    font-size: 11.5px;
    color: var(--dimmer);
    line-height: 1.6;
    margin-top: 28px;
    padding-top: 20px;
    border-top: 1px solid var(--panel-border);
  }}
  footer a {{ color: var(--dim); text-decoration: underline; }}
  footer a:hover {{ color: var(--fg); }}
  .nav-links {{
    margin: 10px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }}
  .nav-links a {{
    font-weight: 600;
    color: var(--dim);
    text-decoration: none;
  }}
  .nav-links a:hover {{ color: var(--cyan); text-decoration: underline; }}
</style>
</head>
<body>
<main>
  <div class="workstation-frame">
    <div class="brand-header">
      <div class="corp-tag">
        <span>CINCO BUSINESS SYSTEMS, INC.</span>
        <div>
          <span class="corp-badge">[v2.5]</span>
          <button class="lang-toggle" id="lang">English</button>
        </div>
      </div>
      <h1>Cinco Identity Generator 2.5™</h1>
      <p class="subtitle">Official WebMIDI SysEx Hardware Flasher (Celery Man Edition)</p>
    </div>

    <div class="desc-box">
      <p data-t="intro"></p>
      <p class="warn-text" data-t="warn"></p>
    </div>

    <div class="specs-grid">
      <div class="spec-item">
        <span class="spec-label">Target Hardware</span>
        <span class="spec-val">M-VAVE FM-1 (AC7916A)</span>
      </div>
      <div class="spec-item">
        <span class="spec-label">Target Binary</span>
        <span class="spec-val">cinco.fwsc (FM-1_925)</span>
      </div>
      <div class="spec-item">
        <span class="spec-label">OS Environment</span>
        <span class="spec-val">Paul's Computer OS 2.5</span>
      </div>
      <div class="spec-item">
        <span class="spec-label">Protocol</span>
        <span class="spec-val">WebMIDI SysEx (Direct)</span>
      </div>
    </div>

    <div class="btn-row">
      <button id="go" class="btn-install" disabled>
        <span data-t="install">INSTALL CINCO 2.5 (cinco.fwsc)</span>
      </button>
      <a href="../" class="btn-emu" id="emu-link">
        ⚡ <span data-t="emuLink">Try in Browser without Hardware (Web Emulator) →</span>
      </a>
    </div>

    <progress id="bar" max="100" value="0"></progress>
    <div id="status" class="status-line"></div>
    <pre id="log" aria-label="Console log output"></pre>

    <p style="font-size:12px; color:var(--dim); margin:0 0 10px;">
      <span data-t="direct"></span>
    </p>
    <p style="font-size:11.5px; color:var(--dimmer); margin:0 0 16px;">
      <span data-t="brick"></span>
      <a href="https://github.com/kurogedelic/FM-1-transporter" target="_blank" rel="noopener" style="color:var(--dim)">FM-1-transporter</a>
    </p>

    <details class="stock-box">
      <summary data-t="stockTitle">Restore Factory M-VAVE Firmware (Stock V15)</summary>
      <div class="stock-content">
        <p style="color:var(--dim); margin-top:0;" data-t="back"></p>
        <p><a href="https://www.m-vave.com/download" target="_blank" rel="noopener" style="color:var(--cyan)">M-VAVE Downloads</a></p>
        <p><label><span data-t="stockFile" style="font-weight:600; color:var(--dim);">Official FM-1.fwsc:</span><br>
           <input id="stock-file" type="file" accept=".fwsc"></label></p>
        <p><button id="stock-go" class="btn-stock" disabled data-t="stockGo">Back up and return to official V15</button></p>
        <p style="font-size:12px; color:var(--dim);" data-t="stockBackup"></p>
        <p style="font-size:12px; color:var(--dim);">
          <label><input id="stock-recovery" type="checkbox"> <span data-t="stockRecovery">Resume an interrupted update: I already saved a complete backup to this computer</span></label>
        </p>
      </div>
    </details>
  </div>

  <footer>
    <div class="nav-links">
      <a href="../">⚡ Web Emulator</a>
      <a href="https://github.com/mrjoshida/CINCO">GitHub Repository</a>
      <a href="https://github.com/mrjoshida/CINCO/blob/main/docs/cinco/manual.md">Cinco Manual</a>
      <a href="../firmware/cinco.fwsc" download>Download Firmware (cinco.fwsc)</a>
    </div>
    <p>Cinco Identity Generator 2.5™ · Cinco Business Systems, Inc. · Tribute instrument based on Felucca by Leo Kuroshita (@kurogedelic), Hügelton Instruments (<a href="https://www.gnu.org/licenses/gpl-3.0.html" target="_blank" rel="noopener">GPL-3.0</a>).<br>
    Includes JieLi AC79 SDK files (uboot.boot, cfg_tool.bin, eq_cfg_hw.bin under Apache-2.0). M-VAVE and FM-1 are trademarks of their respective owners.<br>
    <span data-t="license"></span> <a href="https://github.com/mrjoshida/CINCO" target="_blank" rel="noopener">github.com/mrjoshida/CINCO</a></p>
  </footer>
</main>

<script type="module">
{combined_lib}

const $ = (id) => document.getElementById(id);

const TEXT = {{
  en: {{
    intro: "Connect your M-VAVE FM-1 via USB-C in Chrome or Edge. Installs Cinco Identity Generator 2.5 (Celery Man Edition) directly over WebMIDI SysEx.",
    warn: "Do not unplug the USB-C cable while writing.",
    install: "INSTALL CINCO 2.5 (cinco.fwsc)",
    emuLink: "Try in Browser without Hardware (Web Emulator) →",
    other: "日本語",
    direct: "Connect the USB cable directly to your computer. No probe or Transporter hardware is required.",
    brick: "If an install fails and the FM-1 no longer starts, recovery requires a Transporter or hardware UBoot:",
    beta: "Cinco Identity Generator 2.5 is custom firmware for M-VAVE FM-1. Provided as-is without warranty under GPL-3.0.",
    back: "Get official FM-1 V15 from M-VAVE and select the unmodified FM-1.fwsc. The browser validates it locally; it is never uploaded to any server.",
    stockTitle: "Restore Factory M-VAVE Firmware (Stock V15)",
    stockFile: "Official FM-1.fwsc",
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
  }},
  ja: {{
    intro: "FM-1 を USB-C で接続してください（Chrome または Edge 対応）。Cinco Identity Generator 2.5 (Celery Man Edition) を WebMIDI SysEx 経由で直接インストールします。",
    warn: "書き込み中は USB ケーブルを抜かないでください。",
    install: "Cinco 2.5 をインストール (cinco.fwsc)",
    emuLink: "実機なしでブラウザで体験する（Webエミュレータ）→",
    other: "English",
    direct: "USB ケーブルはパソコンに直接つないでください。Transporter 等の追加機材は不要です。",
    brick: "万一インストールに失敗して起動しなくなった場合の復旧には Transporter が必要です:",
    beta: "Cinco Identity Generator 2.5 は M-VAVE FM-1 向けカスタムファームウェアです。自己責任でお使いください。",
    back: "M-VAVEから公式FM-1 V15を取得し、未変更のFM-1.fwscを選んでください。ファイルはこのブラウザ内で検証し、サーバーへ送りません。",
    stockTitle: "公式V15に戻す（工場出荷時ファームウェア）",
    stockFile: "公式FM-1.fwsc",
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
  }}
}};

let lang = (navigator.language || "en").toLowerCase().startsWith("ja") ? "ja" : "en";
const t = (k) => TEXT[lang][k] || TEXT["en"][k] || "";
let lastKey = null, lastArg = "";

function applyLang() {{
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-t]").forEach((e) => {{
    const val = t(e.dataset.t);
    if (val) e.textContent = val;
  }});
  $("lang").textContent = t("other");
  if (lastKey) $("status").textContent = t(lastKey) + lastArg;
}}

$("lang").addEventListener("click", () => {{
  lang = lang === "ja" ? "en" : "ja";
  applyLang();
}});
applyLang();

const sayK = (k, arg = "") => {{
  lastKey = k;
  lastArg = arg;
  $("status").textContent = t(k) + arg;
}};
const say = (txt) => {{
  lastKey = null;
  $("status").textContent = txt;
}};
const log = (msg) => {{
  $("log").textContent += msg + "\\n";
  $("log").scrollTop = $("log").scrollHeight;
}};

let image = null;
const meta = {{
  version: "v2.5",
  product: "FM-1_925",
  pkg: "../firmware/cinco.fwsc"
}};

let writing = false, stock = null, stockFileEpoch = 0;
const lockInstaller = (on) => {{
  writing = on;
  $("go").disabled = on || !image;
  $("stock-go").disabled = on || !stock;
  $("stock-file").disabled = on;
  $("stock-recovery").disabled = on;
}};

window.addEventListener("beforeunload", (e) => {{
  if (writing) {{
    e.preventDefault();
    e.returnValue = t("leave");
  }}
}});

(async () => {{
  if (!navigator.requestMIDIAccess) {{
    sayK("nomidi");
    return;
  }}
  try {{
    say("Loading Cinco 2.5 package (cinco.fwsc)...");
    const r = await fetch(meta.pkg);
    if (!r.ok) throw new Error(`${{meta.pkg}}: HTTP ${{r.status}}`);
    const pkg = new Uint8Array(await r.arrayBuffer());
    if (productOf(pkg) !== meta.product) {{
      sayK("badpkg");
      return;
    }}
    image = logicalImage(pkg);
    say(`Cinco Identity Generator ${{meta.version}} (cinco.fwsc) — Ready to install`);
    $("go").disabled = false;
  }} catch (e) {{
    sayK("loadfail", e.message);
  }}
}})();

$("go").addEventListener("click", async () => {{
  if (writing) return;
  lockInstaller(true);
  let midi;
  try {{
    midi = await navigator.requestMIDIAccess({{ sysex: true }});
  }} catch (e) {{
    sayK("denied");
    lockInstaller(false);
    return;
  }}

  try {{
    const up = new Updater(midi, log);
    const total = 74 + 1167;
    const step = (k, a) => {{
      log(`${{k}} ${{a ?? ""}}`);
      if (k === "start") sayK("start");
      if (k === "verify") {{
        sayK("verify");
        $("bar").value = (a / total) * 100;
      }}
      if (k === "loader") sayK("loader");
      if (k === "write") {{
        sayK("write");
        $("bar").value = ((74 + a) / total) * 100;
      }}
      if (k === "reboot") sayK("reboot");
      if (k === "done") {{
        $("bar").value = 100;
        sayK("done");
      }}
    }};

    const ota = await up.find((id) => /^ota-/i.test(id.model));
    if (ota) {{
      ota.link.close();
      sayK((await up.resume(image, step, meta.product)) ? "done" : "stopped");
    }} else {{
      await up.install(image, meta.product, step);
    }}
  }} catch (e) {{
    if (e && e.code && TEXT[lang][e.code]) sayK(e.code, e.detail || "");
    else sayK("error", e && e.message);
    log(String((e && e.stack) || e));
  }}
  lockInstaller(false);
}});

$("stock-file").addEventListener("change", async () => {{
  const epoch = ++stockFileEpoch, file = $("stock-file").files[0];
  stock = null;
  lockInstaller(false);
  if (!file) return;
  try {{
    if (file.size !== STOCK_V15_SIZE) throw new Error("File size does not match official FM-1 V15");
    const verified = await validateStockPackage(new Uint8Array(await file.arrayBuffer()));
    if (epoch !== stockFileEpoch) return;
    stock = verified;
    sayK("stockValid");
    lockInstaller(false);
  }} catch (e) {{
    if (epoch === stockFileEpoch) sayK("stockError", e.message);
  }}
}});

function saveArchive(archive) {{
  const url = URL.createObjectURL(new Blob([JSON.stringify(archive)], {{ type: "application/json" }}));
  const a = document.createElement("a");
  a.href = url;
  a.download = `Cinco-backup-${{new Date().toISOString().slice(0, 10)}}.json`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}}

function archiveInfo(a) {{
  let pos = a.indexOf(0);
  if (pos < 0) throw new Error("Invalid INFO header");
  const version = String.fromCharCode(...a.slice(0, pos));
  pos++;
  const engines = a[pos];
  pos += 5;
  for (let i = 0; i < engines; i++) {{
    const end = a.indexOf(0, pos);
    if (end < 0) throw new Error("Invalid INFO header");
    pos = end + 1;
  }}
  const ext = a.slice(pos + 1);
  const supported = (/^FELUCCA /i.test(version) || /^CINCO /i.test(version)) &&
    ext[0] === 16 && ext[1] === 0x55 && ext[2] === 1 &&
    ext[4] === 0x4d && ext[5] === 1 && ext[8] === 0x42 && ext[9] === 1 && (ext[10] & 1);
  return {{ version, supported }};
}}

$("stock-go").addEventListener("click", async () => {{
  if (!stock || writing) return;
  const selected = stock;
  lockInstaller(true);
  let link = null;
  try {{
    let midi;
    try {{
      midi = await navigator.requestMIDIAccess({{ sysex: true }});
    }} catch (e) {{
      sayK("denied");
      return;
    }}
    const up = new Updater(midi, log);
    const step = (k, n) => {{
      log(`${{k}} ${{n ?? ""}}`);
      if (["start", "verify", "loader", "write", "reboot", "done"].includes(k)) sayK(k);
      if (k === "done") $("bar").value = 100;
    }};
    const loader = await up.find((id) => id.model === "ota-FM-1");
    if (loader) {{
      loader.link.close();
      if (!$("stock-recovery").checked) {{
        sayK("stockNeedBackup");
        return;
      }}
      if (!confirm(t("stockConfirm"))) return;
      sayK((await up.resume(selected.image, step, selected.product)) ? "done" : "stopped");
    }} else {{
      const device = await up.find((id) => id.model === "FM-1");
      if (!device) {{
        sayK("notfound");
        return;
      }}
      const input = device.link.input, output = device.link.output;
      device.link.close();
      link = new BackupConnection(input, output);
      const info = archiveInfo(await link.request([1, []]));
      if (!info.supported) {{
        sayK("stockUnsupported");
        return;
      }}
      const archive = await captureBackup(
        (r, o) => link.request(r, o),
        info.version,
        (done, total) => sayK("backup", `${{Math.round((done / Math.max(1, total)) * 100)}}%`)
      );
      saveArchive(archive);
      link.close();
      link = null;
      if (!confirm(t("stockConfirm"))) return;
      await up.install(selected.image, selected.product, step);
    }}
  }} catch (e) {{
    if (e.code && TEXT[lang][e.code]) sayK(e.code, e.detail || "");
    else sayK("error", e.message);
    log(String(e.stack || e));
  }} finally {{
    if (link) link.close();
    lockInstaller(false);
  }}
}});
</script>
</body>
</html>
"""

output_path = web_dir / "cinco_installer.html"
output_path.write_text(html_content, encoding="utf-8")
print(f"Generated {output_path} ({len(html_content)} bytes)")
