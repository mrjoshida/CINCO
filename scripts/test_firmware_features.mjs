import fs from 'fs';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';

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

async function main() {
    console.log(`Loading WASM: ${wasmPath}`);
    const bytes = fs.readFileSync(wasmPath);
    const { instance } = await WebAssembly.instantiate(bytes, {});
    const ex = instance.exports;
    const mem = ex.memory;

    ex._initialize();
    ex.web_nor_erase();
    ex.web_boot();

    console.log("\n--- TEST 1: All 16 Presets ---");
    const presetNames = [
        "Celery Man",
        "Oyster Smiling",
        "Tayne Classic",
        "Computer Voice",
        "Celery 4D Supersaw",
        "Oyster Velvet Chime",
        "Tayne BETA Rave",
        "Nude Tayne Acid 303",
        "Cinco C-Phone",
        "Plucked Celery Harp",
        "Hat Wobble Organ",
        "Paul Rudd Deluxe",
        "Executive Coffee Pad",
        "OSHA Warning Sync",
        "Cinco D-Pants Filter",
        "Identity 2.5 Cyber Choir"
    ];

    for (let p = 0; p < 16; p++) {
        ex.web_cinco_set_preset(p);
        renderMs(ex, mem, 20); // allow engine crossfade to settle
        let src = ex.web_cinco_get_preset();
        if (src !== p) {
            throw new Error(`Preset mismatch: set ${p}, got ${src}`);
        }
        // Key down note 60 (Middle C)
        ex.web_keys(1 << 12);
        let audio = renderMs(ex, mem, 100);
        ex.web_keys(0);
        renderMs(ex, mem, 50);

        console.log(`Preset ${p} [${presetNames[p]}]: RMS=${audio.rms.toFixed(4)}, Peak=${audio.maxL.toFixed(4)}`);
        if (audio.rms <= 0.0001) {
            throw new Error(`Preset ${p} [${presetNames[p]}] generated no audio!`);
        }
        if (audio.maxL > 1.05 || audio.maxR > 1.05) {
            throw new Error(`Preset ${p} exceeded headroom! Peak=${audio.maxL}`);
        }
    }
    console.log("-> All 16 Presets passed!");

    console.log("\n--- TEST 2: All 16 Synth Algorithms on Track 0 ---");
    const algoNames = [
        "4D Brass [Dual Saw]",
        "Flarh Sync [Hard Sync]",
        "Oyster Sub [Sub Bass]",
        "Cinco CZ [Reso Trapezoid]",
        "Tayne FM4 [Cascade Bell]",
        "Paul Rudd [FM Slap Bass]",
        "Mancierge [Formant Choir]",
        "C-Phone [8-Bit Lofi]",
        "Plucked Celery [Physical]",
        "Flarh Cloud [Granular]",
        "Executive [B3 Organ]",
        "Boardroom [Trio Unison]",
        "Oyster Glass [CZ String]",
        "Solid Bass [DX7 House]",
        "Robo-Vowel [Formant Morph]",
        "D-Pants [Filtered Noise]"
    ];

    for (let a = 0; a < 16; a++) {
        ex.web_cinco_set_algo(a);
        renderMs(ex, mem, 20); // allow engine crossfade to settle
        let algo = ex.web_cinco_get_algo();
        if (algo !== a) {
            throw new Error(`Algo mismatch: set ${a}, got ${algo}`);
        }
        ex.web_keys(1 << 12);
        let audio = renderMs(ex, mem, 100);
        ex.web_keys(0);
        renderMs(ex, mem, 50);

        console.log(`Algo ${a} [${algoNames[a]}]: RMS=${audio.rms.toFixed(4)}, Peak=${audio.maxL.toFixed(4)}`);
        if (audio.rms <= 0.0001) {
            throw new Error(`Algo ${a} [${algoNames[a]}] generated no audio!`);
        }
    }
    console.log("-> All 16 Algorithms passed!");

    console.log("\n--- TEST 3: All 8 90s Groove Styles ---");
    const grooveNames = [
        "Eurodance 90s",
        "Rave Breakbeat",
        "Pumping House",
        "Acid Trance 303",
        "Happy Hardcore",
        "Speed Garage",
        "Belgian Techno",
        "Italo Disco"
    ];

    // Enable PLAY button (B_PLAY = 1 << 10)
    ex.web_buttons(1 << 10);
    renderMs(ex, mem, 30);
    ex.web_buttons(0);
    renderMs(ex, mem, 30);

    for (let g = 0; g < 8; g++) {
        ex.web_cinco_set_groove_pattern(g);
        let pat = ex.web_cinco_get_groove_pattern();
        if (pat !== g) {
            throw new Error(`Groove pattern mismatch: set ${g}, got ${pat}`);
        }
        let audio = renderMs(ex, mem, 400);
        console.log(`Groove ${g} [${grooveNames[g]}]: RMS=${audio.rms.toFixed(4)}, Peak=${audio.maxL.toFixed(4)}`);
        if (audio.rms <= 0.001) {
            throw new Error(`Groove ${g} [${grooveNames[g]}] produced no sound!`);
        }
    }

    // Stop PLAY button
    ex.web_buttons(1 << 10);
    renderMs(ex, mem, 30);
    ex.web_buttons(0);
    renderMs(ex, mem, 50);
    console.log("-> All 8 Groove styles passed!");

    console.log("\n--- TEST 4: Resonance & Overdrive DSP Fix ---");
    // Select Celery Man preset
    ex.web_cinco_set_preset(0);
    // Turn EN_K1 (role 3) to 0
    ex.web_enc(3, -127);
    renderMs(ex, mem, 20);

    const pDist = ex.web_param_dist();
    const pE5 = ex.web_param_e5();
    const pLevel = ex.web_param_level();

    // K1=0:
    // P_DIST should be 0
    // P_E5 should be 24
    // P_LEVEL should be 100
    let dist_0 = ex.web_trk0_p(pDist);
    let res_0 = ex.web_trk0_p(pE5);
    let lvl_0 = ex.web_trk0_p(pLevel);
    console.log(`K1=0: DIST=${dist_0}, RES=${res_0}, LEVEL=${lvl_0}`);
    if (dist_0 !== 0) throw new Error(`Expected DIST=0 at K1=0, got ${dist_0}`);
    if (res_0 !== 24) throw new Error(`Expected RES=24 at K1=0, got ${res_0}`);
    if (lvl_0 !== 100) throw new Error(`Expected LEVEL=100 at K1=0, got ${lvl_0}`);

    // Turn EN_K1 to 127
    ex.web_enc(3, 127);
    renderMs(ex, mem, 20);
    let dist_127 = ex.web_trk0_p(pDist);
    let res_127 = ex.web_trk0_p(pE5);
    let lvl_127 = ex.web_trk0_p(pLevel);
    console.log(`K1=127: DIST=${dist_127}, RES=${res_127}, LEVEL=${lvl_127}`);
    // P_DIST: ((127-100)*12)/27 = 12
    if (dist_127 !== 12) throw new Error(`Expected DIST=12 at K1=127, got ${dist_127}`);
    // P_E5: 24 + (127*68)/127 = 92
    if (res_127 !== 92) throw new Error(`Expected RES=92 at K1=127, got ${res_127}`);
    // P_LEVEL: 100 - (127*22)/127 = 78
    if (lvl_127 !== 78) throw new Error(`Expected LEVEL=78 at K1=127, got ${lvl_127}`);

    // Render audio at max K1 with note on to verify sweet spot resonance cuts through without clipping
    ex.web_keys(1 << 12);
    let audio_k127 = renderMs(ex, mem, 200);
    ex.web_keys(0);
    renderMs(ex, mem, 50);
    console.log(`High Q resonance audio: RMS=${audio_k127.rms.toFixed(4)}, Peak=${audio_k127.maxL.toFixed(4)}`);
    if (audio_k127.maxL > 1.0) {
        throw new Error(`Audio clipped above 1.0! Peak=${audio_k127.maxL}`);
    }
    console.log("-> Resonance DSP Fix passed!");

    console.log("\n--- TEST 5: Encoder Dual-Mode & Cyclic Controls ---");
    // Test ALGO encoder (role 1) without buttons: cycles algorithms
    ex.web_cinco_set_algo(0);
    ex.web_enc(1, 1);
    renderMs(ex, mem, 20);
    if (ex.web_cinco_get_algo() !== 1) throw new Error(`Algo encoder did not increment algo!`);

    // Test ALGO encoder (role 1) with B_PLAY (1 << 10) held: cycles groove pattern
    ex.web_cinco_set_groove_pattern(0);
    ex.web_buttons(1 << 10); // B_PLAY held
    renderMs(ex, mem, 20);
    ex.web_enc(1, 1);
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 20);
    if (ex.web_cinco_get_groove_pattern() !== 1) throw new Error(`Algo encoder with B_PLAY held did not increment groove pattern!`);

    // Test PRESET encoder (role 2): cycles presets 0..15
    ex.web_cinco_set_preset(0);
    for (let step = 1; step <= 16; step++) {
        ex.web_enc(2, 1);
        renderMs(ex, mem, 20);
        let expected = step % 16;
        if (ex.web_cinco_get_preset() !== expected) {
            throw new Error(`Preset encoder step ${step}: expected ${expected}, got ${ex.web_cinco_get_preset()}`);
        }
    }
    console.log("-> Encoder dual-mode & cyclic controls passed!");

    console.log("\n============================================");
    console.log(" ALL FIRMWARE FEATURE VERIFICATIONS PASSED! ");
    console.log("============================================");
}

main().catch(err => {
    console.error("FAILED:", err);
    process.exit(1);
});
