import fs from 'fs';
import path from 'path';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';

function readCString(mem, ptr) {
    const bytes = new Uint8Array(mem.buffer);
    let str = "";
    while (bytes[ptr] !== 0) {
        str += String.fromCharCode(bytes[ptr]);
        ptr++;
    }
    return str;
}

async function run() {
    const bytes = fs.readFileSync(wasmPath);
    const { instance } = await WebAssembly.instantiate(bytes, {});
    const ex = instance.exports;
    const mem = ex.memory;

    ex._initialize();
    ex.web_nor_erase();
    ex.web_boot();

    function renderMs(ms, holdKey = true) {
        if (holdKey) {
            // Re-trigger key cleanly with note-on edge
            ex.web_keys(0);
        }
        let preN = Math.round(5 * 44.1);
        while (preN > 0) {
            let m = Math.min(preN, 128);
            ex.web_render(m);
            preN -= m;
        }
        if (holdKey) {
            ex.web_keys(1 << 5); // Middle key note-on
        }

        let n = Math.round(ms * 44.1);
        let peak = 0;
        let sumSq = 0;
        let totalSamples = 0;

        while (n > 0) {
            let m = Math.min(n, 128);
            ex.web_render(m);
            const l = new Float32Array(mem.buffer, ex.web_out_l(), m);
            const r = new Float32Array(mem.buffer, ex.web_out_r(), m);
            for (let i = 0; i < m; i++) {
                let al = Math.abs(l[i]);
                let ar = Math.abs(r[i]);
                if (al > peak) peak = al;
                if (ar > peak) peak = ar;
                sumSq += l[i] * l[i] + r[i] * r[i];
                totalSamples += 2;
            }
            n -= m;
        }
        const rms = Math.sqrt(sumSq / (totalSamples || 1));
        return { peak, rms };
    }

    function checkScreenNonBlank() {
        const u16 = new Uint16Array(mem.buffer, ex.web_screen(), 240 * 240);
        let nonZero = 0;
        let nonDesktop = 0;
        // Desktop color swapped byte order
        const C_DESKTOP_SWAPPED = ((0x6E1B >> 8) | (0x6E1B << 8)) & 0xFFFF;
        for (let i = 0; i < 240 * 240; i++) {
            if (u16[i] !== 0) nonZero++;
            if (u16[i] !== C_DESKTOP_SWAPPED && u16[i] !== 0) nonDesktop++;
        }
        return { nonZero, nonDesktop, isNonBlank: nonDesktop > 1000 };
    }

    // Let the system finish booting
    renderMs(150, false);

    const CHAR_NAMES = ["Celery", "Oyster", "Tayne", "Talk"];
    const KINETIC_NAMES = ["None", "Wobble", "Flail"];
    const NSFW_NAMES = ["SFW", "NSFW"];

    const EXPECTED_TITLES = {
        // Celery (0)
        "0_0_0": "Celery Man",
        "0_0_1": "NUDE CELERY MAN",
        "0_1_0": "Celery Man - Hat Wobble",
        "0_1_1": "NUDE CELERY - Hat Wobble",
        "0_2_0": "Celery Man - FLARHGUNNSTOW!",
        "0_2_1": "NUDE CELERY - FLARHGUNNSTOW",


        // Oyster (1)
        "1_0_0": "Oyster Smiling",
        "1_0_1": "NUDE OYSTER",
        "1_1_0": "Oyster - Hat Wobble",
        "1_1_1": "NUDE OYSTER - Hat Wobble",
        "1_2_0": "Oyster - FLARHGUNNSTOW!",
        "1_2_1": "NUDE OYSTER - FLARHGUNNSTOW",

        // Tayne (2)
        "2_0_0": "Tayne Classic",
        "2_0_1": "NUDE TAYNE",
        "2_1_0": "Tayne - Hat Wobble",
        "2_1_1": "NUDE TAYNE - Hat Wobble",
        "2_2_0": "Tayne - FLARHGUNNSTOW!",
        "2_2_1": "NUDE TAYNE - FLARHGUNNSTOW",

        // Talk (3)
        "3_0_0": "Computer Voice",
        "3_0_1": "NUDE COMPUTER VOICE",
        "3_1_0": "Computer Voice - Wobble",
        "3_1_1": "NUDE VOICE - Hat Wobble",
        "3_2_0": "Computer Voice - FLARH!",
        "3_2_1": "NUDE VOICE - FLARHGUNNSTOW",
    };

    const matrixResults = [];

    // --- 24-State Matrix Test ---
    let stateIdx = 1;
    for (let src = 0; src < 4; src++) {
        for (let kin = 0; kin < 3; kin++) {
            for (let nsfw = 0; nsfw < 2; nsfw++) {
                // Configure state
                ex.web_cinco_set_source(src);
                ex.web_cinco_set_nude(nsfw);
                if (kin === 0) {
                    ex.web_cinco_set_wobble(0);
                    ex.web_cinco_set_flail(0);
                } else if (kin === 1) {
                    ex.web_cinco_set_wobble(1);
                    ex.web_cinco_set_flail(0);
                } else if (kin === 2) {
                    ex.web_cinco_set_wobble(0);
                    ex.web_cinco_set_flail(1);
                }

                // Render some frames with key down to generate audio
                const audio = renderMs(50, true);

                const key = `${src}_${kin}_${nsfw}`;
                const expectedTitle = EXPECTED_TITLES[key];
                const actualTitle = readCString(mem, ex.web_cinco_get_title());
                const mosaic = ex.web_cinco_get_mosaic();
                const screen = checkScreenNonBlank();

                const titleMatch = (actualTitle === expectedTitle);
                const mosaicMatch = nsfw ? (mosaic > 1) : (mosaic === 1);
                const audioValid = (audio.peak > 0.001);
                const screenValid = screen.isNonBlank;

                const pass = titleMatch && mosaicMatch && audioValid && screenValid;

                matrixResults.push({
                    id: stateIdx++,
                    source: CHAR_NAMES[src],
                    kinetics: KINETIC_NAMES[kin],
                    nsfw: NSFW_NAMES[nsfw],
                    expectedTitle,
                    actualTitle,
                    mosaic,
                    audioPeak: audio.peak,
                    audioRms: audio.rms,
                    screenPixels: screen.nonDesktop,
                    titleMatch,
                    mosaicMatch,
                    audioValid,
                    screenValid,
                    pass
                });
            }
        }
    }

    // --- Envelope Profile Tests (0..3) ---
    const envExpected = [
        { mode: 0, name: "Snappy Brass", atk: 2, dec: 60, sus: 20, rel: 35, flt: 55 },
        { mode: 1, name: "Sustained Pad", atk: 75, dec: 90, sus: 127, rel: 100, flt: 10 },
        { mode: 2, name: "Staccato Pluck", atk: 0, dec: 25, sus: 0, rel: 15, flt: 65 },
        { mode: 3, name: "Punch Bass", atk: 0, dec: 45, sus: 40, rel: 25, flt: 70 },
    ];

    const envResults = [];
    for (const e of envExpected) {
        ex.web_cinco_set_env_mode(e.mode);
        renderMs(20, false);
        const curMode = ex.web_cinco_get_env_mode();
        const atk = ex.web_trk0_p(1); // P_ATK
        const dec = ex.web_trk0_p(2); // P_DEC
        const sus = ex.web_trk0_p(3); // P_SUS
        const rel = ex.web_trk0_p(4); // P_REL
        const flt = ex.web_trk0_p(5); // P_ED_FLT

        const pass = (curMode === e.mode && atk === e.atk && dec === e.dec && sus === e.sus && rel === e.rel && flt === e.flt);
        envResults.push({
            mode: e.mode,
            name: e.name,
            pass,
            atk, dec, sus, rel, flt,
            expected: e
        });
    }

    // --- Scale Mode Tests (0..4) ---
    const scaleExpected = [
        { mode: 0, name: "Chromatic", quant: 0, scale: 0 },
        { mode: 1, name: "Natural Minor", quant: 1, scale: 2 },
        { mode: 2, name: "Major", quant: 1, scale: 1 },
        { mode: 3, name: "Minor Pentatonic", quant: 1, scale: 6 },
        { mode: 4, name: "Blues / Dorian", quant: 1, scale: 12 },
    ];

    const scaleResults = [];
    for (const s of scaleExpected) {
        ex.web_cinco_set_scale_mode(s.mode);
        renderMs(20, false);
        const curMode = ex.web_cinco_get_scale_mode();
        const quant = ex.web_trk0_p(27); // P_QUANT
        const scale = ex.web_trk0_p(26); // P_SCALE

        const pass = (curMode === s.mode && quant === s.quant && scale === s.scale);
        scaleResults.push({
            mode: s.mode,
            name: s.name,
            pass,
            quant, scale,
            expected: s
        });
    }

    // --- Preset Persistence Tests ---
    // Set Pad (mode 1) and Blues (mode 4)
    ex.web_cinco_set_env_mode(1);
    ex.web_cinco_set_scale_mode(4);
    renderMs(20, false);

    const persistResults = [];
    for (let src = 0; src < 4; src++) {
        ex.web_cinco_set_source(src);
        renderMs(20, false);
        const curEnv = ex.web_cinco_get_env_mode();
        const curScale = ex.web_cinco_get_scale_mode();
        const atk = ex.web_trk0_p(1);
        const scale = ex.web_trk0_p(26);
        const pass = (curEnv === 1 && curScale === 4 && atk === 75 && scale === 12);
        persistResults.push({
            source: CHAR_NAMES[src],
            curEnv,
            curScale,
            atk,
            scale,
            pass
        });
    }

    // Emit full JSON output for python formatter
    const output = {
        matrixResults,
        envResults,
        scaleResults,
        persistResults,
        allPassed: (
            matrixResults.every(r => r.pass) &&
            envResults.every(r => r.pass) &&
            scaleResults.every(r => r.pass) &&
            persistResults.every(r => r.pass)
        )
    };

    console.log(JSON.stringify(output, null, 2));
    if (!output.allPassed) {
        process.exit(1);
    }
}

run().catch(err => {
    console.error("FATAL ERROR:", err);
    process.exit(1);
});
