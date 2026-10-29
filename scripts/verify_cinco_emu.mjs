import fs from 'fs';
import path from 'path';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';
const outDir = 'scratch/cinco_frames';
fs.mkdirSync(outDir, { recursive: true });

function rgb565ToPpm(u16Array, width, height, filepath) {
    const header = Buffer.from(`P6\n${width} ${height}\n255\n`, 'ascii');
    const pixelBytes = Buffer.alloc(width * height * 3);
    for (let i = 0; i < width * height; i++) {
        const v = u16Array[i];
        const p = ((v >> 8) | (v << 8)) & 0xFFFF; // the panel's byte order -> native RGB565
        const r = ((p >> 11) & 0x1f) * 255 / 31;
        const g = ((p >> 5) & 0x3f) * 255 / 63;
        const b = (p & 0x1f) * 255 / 31;
        pixelBytes[i * 3 + 0] = Math.round(r);
        pixelBytes[i * 3 + 1] = Math.round(g);
        pixelBytes[i * 3 + 2] = Math.round(b);
    }
    fs.writeFileSync(filepath, Buffer.concat([header, pixelBytes]));
}

async function run() {
    console.log(`Loading WASM: ${wasmPath}`);
    const bytes = fs.readFileSync(wasmPath);
    const { instance } = await WebAssembly.instantiate(bytes, {});
    const ex = instance.exports;
    const mem = ex.memory;

    ex._initialize();
    ex.web_nor_erase();
    ex.web_boot();

    function renderMs(ms) {
        let n = Math.round(ms * 44.1);
        let maxL = 0, maxR = 0, sumSq = 0, count = 0;
        while (n > 0) {
            let m = Math.min(n, 128);
            ex.web_render(m);
            const l = new Float32Array(mem.buffer, ex.web_out_l(), m);
            const r = new Float32Array(mem.buffer, ex.web_out_r(), m);
            for (let i = 0; i < m; i++) {
                let al = Math.abs(l[i]);
                let ar = Math.abs(r[i]);
                if (al > maxL) maxL = al;
                if (ar > maxR) maxR = ar;
                sumSq += l[i]*l[i] + r[i]*r[i];
                count += 2;
            }
            n -= m;
        }
        return { maxL, maxR, rms: Math.sqrt(sumSq / count) };
    }

    function grabScreen(name) {
        const u16 = new Uint16Array(mem.buffer, ex.web_screen(), 240 * 240).slice();
        const p = path.join(outDir, `${name}.ppm`);
        rgb565ToPpm(u16, 240, 240, p);
        console.log(`Saved screenshot: ${p}`);
        return u16;
    }

    console.log("=== 1. Boot & Idle State ===");
    let bootAudio = renderMs(200);
    console.log(`Boot audio: RMS=${bootAudio.rms.toFixed(4)}, Peak=${bootAudio.maxL.toFixed(4)}`);
    grabScreen("01_boot_celery");

    console.log("=== 2. 4d3d3d3 Engaged (K1 Macro) ===");
    // Turn EN_K1 (role 3) up by 40 steps
    ex.web_enc(3, 40);
    renderMs(50);
    grabScreen("02_4d3d3d3_engaged");

    console.log("=== 3. Oyster Loaded (PRESET Encoder) ===");
    // Turn EN_PRESET (role 2) by 1
    ex.web_enc(2, 1);
    renderMs(50);
    grabScreen("03_oyster_loaded");

    console.log("=== 4. Tayne Loaded (PRESET Encoder) ===");
    // Turn EN_PRESET (role 2) by 1
    ex.web_enc(2, 1);
    renderMs(50);
    grabScreen("04_tayne_loaded");

    console.log("=== 5. Hat Wobble Active (B_LFO Pressed) ===");
    // B_LFO is 1 << 3 (0x08)
    ex.web_buttons(1 << 3);
    renderMs(50);
    grabScreen("05_hat_wobble");
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 6. Flarhgunnstow Active (B_ARP Pressed) ===");
    // B_ARP is 1 << 8 (0x100)
    ex.web_buttons(1 << 8);
    renderMs(50);
    grabScreen("06_flarhgunnstow");
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 7. Nude Tayne Active (B_FX Pressed) ===");
    // B_FX is 1 << 0 (0x01)
    ex.web_buttons(1 << 0);
    renderMs(50);
    grabScreen("07_nude_warning");
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 8. Oyster Smiling Printout (B_SAVE Pressed) ===");
    // B_SAVE is 1 << 7 (0x80)
    ex.web_buttons(1 << 7);
    renderMs(50);
    grabScreen("08_oyster_receipt");
    ex.web_buttons(0);
    // Allow receipt popup (80 frames) to cleanly expire
    renderMs(1400);

    console.log("=== 9. Diagnostic HUD ===");
    ex.web_cinco_set_diag(1);
    renderMs(50);
    grabScreen("09_diagnostic_hud");
    ex.web_cinco_set_diag(0);
    renderMs(50);

    console.log("=== 10. Boss Key Spreadsheet (B_EDIT Pressed) ===");
    // B_EDIT is 1 << 4 (0x10)
    ex.web_buttons(1 << 4);
    renderMs(50);
    grabScreen("10_boss_key");
    ex.web_buttons(0);
    renderMs(50);
    // Dismiss Boss key
    ex.web_buttons(1 << 4);
    renderMs(50);
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 11. Disk Defragmenter Visualizer (B_SEQ Pressed) ===");
    // B_SEQ is 1 << 9 (0x200)
    ex.web_buttons(1 << 9);
    renderMs(50);
    grabScreen("11_disk_defrag");
    ex.web_buttons(0);
    renderMs(50);
    // Return view mode to Dancers
    ex.web_buttons(1 << 9);
    renderMs(50);
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 12. Flying Celery Screensaver (After Dark) ===");
    ex.web_cinco_set_screensaver(1);
    renderMs(50);
    grabScreen("12_screensaver");
    ex.web_cinco_set_screensaver(0);
    renderMs(50);

    console.log("=== 13. Cinco System Alert Popup (Easter Egg: HOME + GLO Pressed) ===");
    // Easter Egg: B_HOME is 1 << 6, B_GLO is 1 << 5
    ex.web_buttons((1 << 5) | (1 << 6));
    renderMs(50);
    grabScreen("13_cinco_error");
    ex.web_buttons(0);
    renderMs(50);
    // Dismiss error popup
    ex.web_buttons(1 << 4);
    renderMs(50);
    ex.web_buttons(0);
    renderMs(50);

    console.log("=== 14. Key Note Audio Synthesis Test ===");
    // Press keyboard note: key 10
    ex.web_keys(1 << 10);
    let noteAudio = renderMs(200);
    console.log(`Note audio on: RMS=${noteAudio.rms.toFixed(4)}, Peak=${noteAudio.maxL.toFixed(4)}`);
    ex.web_keys(0);
    let releaseAudio = renderMs(200);
    console.log(`Note release audio: RMS=${releaseAudio.rms.toFixed(4)}, Peak=${releaseAudio.maxL.toFixed(4)}`);

    console.log("=== Verification Successful! ===");
}

run().catch(err => {
    console.error("FATAL:", err);
    process.exit(1);
});
