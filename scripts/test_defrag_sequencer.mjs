// test_defrag_sequencer.mjs - Comprehensive verification of Interactive Norton Disk Defragmenter Sequencer
import fs from 'fs';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';
console.log(`Loading WASM: ${wasmPath}`);
const bytes = fs.readFileSync(wasmPath);

function renderMs(ex, mem, ms) {
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

async function run() {
    const { instance } = await WebAssembly.instantiate(bytes, {});
    const ex = instance.exports;
    const mem = ex.memory;

    ex._initialize();
    ex.web_nor_erase();
    ex.web_boot();

    console.log("\n=== TEST 1: Groove Templates in seq_grid ===");
    for (let g = 0; g < 8; g++) {
        ex.web_cinco_set_groove_pattern(g);
        let kick = ex.web_cinco_get_seq_grid(0);
        let snare = ex.web_cinco_get_seq_grid(1);
        let chat = ex.web_cinco_get_seq_grid(2);
        let ohat = ex.web_cinco_get_seq_grid(3);
        let bass = ex.web_cinco_get_seq_grid(4);
        let stab = ex.web_cinco_get_seq_grid(5);
        console.log(`Groove ${g}: Kick=0x${kick.toString(16)}, Snare=0x${snare.toString(16)}, Bass=0x${bass.toString(16)}, Stab=0x${stab.toString(16)}`);
        if (kick === 0 && bass === 0) {
            throw new Error(`Groove ${g} template failed to load into seq_grid!`);
        }
    }
    console.log("-> Groove templates verification passed!");

    console.log("\n=== TEST 2: Enter Defrag Sequencer View Mode ===");
    // Press B_SEQ (button 9) to enter Defrag
    ex.web_buttons(1 << 9);
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 20);

    let view = ex.web_cinco_get_view();
    if (view !== 1) {
        throw new Error(`Expected view_mode 1, got ${view}`);
    }
    console.log("-> View mode is 1 (Disk Defragmenter)!");

    console.log("\n=== TEST 3: Track Selection via Black Keys & d_sel Encoder ===");
    // Black key places:
    // Place 0: F#3 (k=1)
    // Place 1: G#3 (k=3)
    // Place 2: A#3 (k=5)
    // Place 3: C#4 (k=8)
    // Place 4: D#4 (k=10)
    // Place 5: F#4 (k=13)
    const blackKeys = [1, 3, 5, 8, 10, 13];
    for (let r = 0; r < 6; r++) {
        let k = blackKeys[r];
        ex.web_keys(1 << k);
        renderMs(ex, mem, 20);
        ex.web_keys(0);
        renderMs(ex, mem, 20);
        let activeRow = ex.web_cinco_get_seq_row();
        if (activeRow !== r) {
            throw new Error(`Black key place ${r} (key ${k}) failed: expected seq_row ${r}, got ${activeRow}`);
        }
    }
    console.log("-> Black key track selection verified for all 6 tracks!");

    // Test d_sel encoder (role 0: EN_SELECT)
    ex.web_enc(0, 1); // d_sel = +1
    renderMs(ex, mem, 20);
    if (ex.web_cinco_get_seq_row() !== 0) { // (5 + 1) % 6 = 0
        throw new Error(`d_sel +1 failed: expected seq_row 0, got ${ex.web_cinco_get_seq_row()}`);
    }
    ex.web_enc(0, -1); // d_sel = -1
    renderMs(ex, mem, 20);
    if (ex.web_cinco_get_seq_row() !== 5) { // (0 - 1) % 6 = 5
        throw new Error(`d_sel -1 failed: expected seq_row 5, got ${ex.web_cinco_get_seq_row()}`);
    }
    console.log("-> d_sel encoder row navigation passed!");

    console.log("\n=== TEST 4: White Key Step Toggle ===");
    // Select Row 0 (Kick)
    ex.web_cinco_set_seq_row(0);
    ex.web_cinco_set_seq_grid(0, 0); // Clear row 0
    // White key places:
    const whiteKeys = [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26];
    for (let c = 0; c < 16; c++) {
        let k = whiteKeys[c];
        // Press white key to toggle bit c ON
        ex.web_keys(1 << k);
        renderMs(ex, mem, 20);
        ex.web_keys(0);
        renderMs(ex, mem, 20);

        let g = ex.web_cinco_get_seq_grid(0);
        if (((g >> c) & 1) !== 1) {
            throw new Error(`White key step ${c} (key ${k}) failed to turn ON: grid=0x${g.toString(16)}`);
        }

        // Press again to toggle bit c OFF
        ex.web_keys(1 << k);
        renderMs(ex, mem, 20);
        ex.web_keys(0);
        renderMs(ex, mem, 20);

        g = ex.web_cinco_get_seq_grid(0);
        if (((g >> c) & 1) !== 0) {
            throw new Error(`White key step ${c} (key ${k}) failed to turn OFF: grid=0x${g.toString(16)}`);
        }
    }
    console.log("-> White key step toggle verified for all 16 steps!");

    console.log("\n=== TEST 5: Pattern Fill Generator (d_k1) ===");
    ex.web_cinco_set_seq_row(0);
    // 0: Clear (0x0000)
    // 1: 4-on-floor (0x1111)
    // 2: Offbeat (0x4444)
    // 3: 8th notes (0x5555)
    // 4: 16th notes (0xFFFF)
    // 5: Syncopated (0x1449)
    // 6: Gallop (0x4994)
    // 7: Invert (~grid)
    const expectedFills = [0x1111, 0x4444, 0x5555, 0xFFFF, 0x1449, 0x4994];
    for (let i = 0; i < expectedFills.length; i++) {
        ex.web_enc(3, 1); // role 3: EN_K1
        renderMs(ex, mem, 20);
        let g = ex.web_cinco_get_seq_grid(0);
        if (g !== expectedFills[i]) {
            throw new Error(`Fill step ${i + 1} failed: expected 0x${expectedFills[i].toString(16)}, got 0x${g.toString(16)}`);
        }
    }
    // Test Invert fill (step 7)
    ex.web_enc(3, 1); // role 3: EN_K1 -> index 7 (Invert)
    renderMs(ex, mem, 20);
    let invG = ex.web_cinco_get_seq_grid(0);
    let expectedInv = (~0x4994) & 0xFFFF;
    if (invG !== expectedInv) {
        throw new Error(`Invert fill failed: expected 0x${expectedInv.toString(16)}, got 0x${invG.toString(16)}`);
    }
    console.log("-> Pattern fill generator verified!");

    console.log("\n=== TEST 6: Root Pitch Offset (d_k2) ===");
    ex.web_cinco_set_seq_pitch_offset(0);
    ex.web_enc(4, 3); // role 4: EN_K2
    renderMs(ex, mem, 20);
    let po = ex.web_cinco_get_seq_pitch_offset();
    if (po !== 3) {
        throw new Error(`Pitch offset failed: expected 3, got ${po}`);
    }
    ex.web_enc(4, -7); // role 4: EN_K2
    renderMs(ex, mem, 20);
    po = ex.web_cinco_get_seq_pitch_offset();
    if (po !== -4) {
        throw new Error(`Pitch offset failed: expected -4, got ${po}`);
    }
    console.log("-> Root pitch offset verified!");

    console.log("\n=== TEST 7: Template Loader via d_var (ALGO) ===");
    // Set groove pattern to 2 (Pumping House) via d_var
    ex.web_cinco_set_groove_pattern(0);
    ex.web_enc(1, 2); // role 1: EN_ALGO
    renderMs(ex, mem, 20);
    let pat = ex.web_cinco_get_groove_pattern();
    let houseKick = ex.web_cinco_get_seq_grid(0);
    if (houseKick !== 0x1111) {
        throw new Error(`d_var template loader failed: expected kick 0x1111, got 0x${houseKick.toString(16)}`);
    }
    console.log(`-> d_var loaded template successfully (pat=${pat})!`);

    console.log("\n=== TEST 8: Keyboard Muting in Defrag View Mode ===");
    // When view_mode == 1, pressing a key should NOT play loud synth notes
    ex.web_keys(1 << 7); // C4
    let audioKeyInDefrag = renderMs(ex, mem, 100);
    ex.web_keys(0);
    console.log(`Defrag mode key press audio: RMS=${audioKeyInDefrag.rms.toFixed(4)}, Peak=${audioKeyInDefrag.maxL.toFixed(4)}`);
    if (audioKeyInDefrag.rms > 0.005) {
        throw new Error(`Keys were not muted in defrag view mode! RMS=${audioKeyInDefrag.rms}`);
    }
    console.log("-> Keyboard live playback properly muted in defrag mode!");

    console.log("\n=== TEST 9: Persistent Defrag Mode (No Auto-Exit) ===");
    // Run playback for several bars to ensure defrag mode does not auto-exit
    ex.web_buttons(1 << 10); // B_PLAY
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    let playAudio = renderMs(ex, mem, 1500); // 1.5 seconds of beat playback
    console.log(`Defrag groove playback audio: RMS=${playAudio.rms.toFixed(4)}, Peak=${playAudio.maxL.toFixed(4)}`);
    if (playAudio.rms <= 0.001) {
        throw new Error(`Defrag groove generated no audio during playback!`);
    }
    if (ex.web_cinco_get_view() !== 1) {
        throw new Error(`Defrag mode auto-exited prematurely! view_mode=${ex.web_cinco_get_view()}`);
    }
    console.log("-> Defrag sequencer stayed active throughout playback!");

    // Stop playback
    ex.web_buttons(1 << 10);
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 50);

    // B_SEQ toggles back to dancers
    ex.web_buttons(1 << 9); // B_SEQ
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 50);
    if (ex.web_cinco_get_view() !== 0) {
        throw new Error(`B_SEQ did not toggle back to dancers: view_mode=${ex.web_cinco_get_view()}`);
    }
    console.log("-> B_SEQ cleanly toggled back to dancers!");

    console.log("\n=== TEST 10: State Save & Restore ===");
    ex.web_cinco_set_seq_grid(0, 0x1234);
    ex.web_cinco_set_seq_grid(4, 0x5678);
    ex.web_cinco_set_seq_row(3);
    ex.web_cinco_set_seq_pitch_offset(5);

    // Press B_SAVE (button 7)
    ex.web_buttons(1 << 7);
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 50);

    // Scramble values in memory
    ex.web_cinco_set_seq_grid(0, 0);
    ex.web_cinco_set_seq_grid(4, 0);
    ex.web_cinco_set_seq_row(0);
    ex.web_cinco_set_seq_pitch_offset(0);

    // Load state
    ex.web_cinco_load_state();
    renderMs(ex, mem, 50);

    let restoredKick = ex.web_cinco_get_seq_grid(0);
    let restoredBass = ex.web_cinco_get_seq_grid(4);
    let restoredRow = ex.web_cinco_get_seq_row();
    let restoredPo = ex.web_cinco_get_seq_pitch_offset();

    console.log(`Restored: Kick=0x${restoredKick.toString(16)}, Bass=0x${restoredBass.toString(16)}, Row=${restoredRow}, PitchOffset=${restoredPo}`);
    if (restoredKick !== 0x1234 || restoredBass !== 0x5678 || restoredRow !== 3 || restoredPo !== 5) {
        throw new Error(`State save/restore mismatch!`);
    }
    console.log("-> State save and restore of defrag sequence verified!");

    console.log("\n========================================================");
    console.log(" ALL INTERACTIVE DEFRAGMENTER SEQUENCER TESTS PASSED! ");
    console.log("========================================================");
}

run().catch(err => {
    console.error("TEST FAILED:", err);
    process.exit(1);
});
