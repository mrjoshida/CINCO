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

    function renderMs(ms) {
        let n = Math.round(ms * 44.1);
        while (n > 0) {
            let m = Math.min(n, 128);
            ex.web_render(m);
            n -= m;
        }
    }

    // Let the system finish booting
    renderMs(100);

    const P_ATK = 1;
    const P_DEC = 2;
    const P_SUS = 3;
    const P_REL = 4;
    const P_ED_FLT = 5;
    const P_SCALE = 26;
    const P_QUANT = 27;

    const results = [];

    function test(name, fn) {
        try {
            fn();
            results.push({ name, status: 'PASS' });
            console.log(`[PASS] ${name}`);
        } catch (e) {
            results.push({ name, status: 'FAIL', error: e.message });
            console.error(`[FAIL] ${name}: ${e.message}`);
        }
    }

    function assert(cond, msg) {
        if (!cond) throw new Error(msg);
    }

    // 1. Matrix Combinations: Oyster + NSFW
    test("Oyster + NSFW renders 'NUDE OYSTER' with mosaic > 1", () => {
        ex.web_cinco_set_source(1); // SRC_OYSTER
        ex.web_cinco_set_nude(1);
        ex.web_cinco_set_wobble(0);
        ex.web_cinco_set_flail(0);
        renderMs(50);
        const title = readCString(mem, ex.web_cinco_get_title());
        const mosaic = ex.web_cinco_get_mosaic();
        assert(title === "NUDE OYSTER", `Expected 'NUDE OYSTER', got '${title}'`);
        assert(mosaic > 1, `Expected mosaic > 1, got ${mosaic}`);
    });

    // 2. Matrix Combinations: Tayne + Hat Wobble + NSFW
    test("Hat Wobble + NSFW renders 'NUDE TAYNE - Hat Wobble' with mosaic > 1", () => {
        ex.web_cinco_set_source(2); // SRC_TAYNE
        ex.web_cinco_set_wobble(1);
        ex.web_cinco_set_flail(0);
        ex.web_cinco_set_nude(1);
        renderMs(50);
        const title = readCString(mem, ex.web_cinco_get_title());
        const mosaic = ex.web_cinco_get_mosaic();
        assert(title === "NUDE TAYNE - Hat Wobble", `Expected 'NUDE TAYNE - Hat Wobble', got '${title}'`);
        assert(mosaic > 1, `Expected mosaic > 1, got ${mosaic}`);
    });

    // 3. Matrix Combinations: Tayne + Flarhgunnstow + NSFW
    test("Flarhgunnstow + NSFW renders 'NUDE TAYNE - FLARHGUNNSTOW' with mosaic > 1", () => {
        ex.web_cinco_set_source(2); // SRC_TAYNE
        ex.web_cinco_set_wobble(0);
        ex.web_cinco_set_flail(1);
        ex.web_cinco_set_nude(1);
        renderMs(50);
        const title = readCString(mem, ex.web_cinco_get_title());
        const mosaic = ex.web_cinco_get_mosaic();
        assert(title === "NUDE TAYNE - FLARHGUNNSTOW", `Expected 'NUDE TAYNE - FLARHGUNNSTOW', got '${title}'`);
        assert(mosaic > 1, `Expected mosaic > 1, got ${mosaic}`);
    });

    // 4. Matrix Combinations: Celery + NSFW
    test("Celery + NSFW renders 'NUDE CELERY MAN' with mosaic > 1", () => {
        ex.web_cinco_set_source(0); // SRC_CELERY
        ex.web_cinco_set_wobble(0);
        ex.web_cinco_set_flail(0);
        ex.web_cinco_set_nude(1);
        renderMs(50);
        const title = readCString(mem, ex.web_cinco_get_title());
        const mosaic = ex.web_cinco_get_mosaic();
        assert(title === "NUDE CELERY MAN", `Expected 'NUDE CELERY MAN', got '${title}'`);
        assert(mosaic > 1, `Expected mosaic > 1, got ${mosaic}`);
    });

    // 4b. Clear NSFW and verify Celery Man default
    test("Celery (Non-nude) renders 'Celery Man' with mosaic == 1", () => {
        ex.web_cinco_set_nude(0);
        renderMs(50);
        const title = readCString(mem, ex.web_cinco_get_title());
        const mosaic = ex.web_cinco_get_mosaic();
        assert(title === "Celery Man", `Expected 'Celery Man', got '${title}'`);
        assert(mosaic === 1, `Expected mosaic === 1, got ${mosaic}`);
    });

    // 5. B_ENV cycles brass/pad/pluck/bass and changes P_ATK, P_DEC, P_SUS, P_REL, P_ED_FLT
    test("B_ENV button cycling configures trk[0] envelopes", () => {
        // Initially mode 0 (Brass)
        assert(ex.web_cinco_get_env_mode() === 0, `Expected initial env 0, got ${ex.web_cinco_get_env_mode()}`);
        assert(ex.web_trk0_p(P_ATK) === 2, `Expected P_ATK=2, got ${ex.web_trk0_p(P_ATK)}`);
        assert(ex.web_trk0_p(P_DEC) === 60, `Expected P_DEC=60, got ${ex.web_trk0_p(P_DEC)}`);
        assert(ex.web_trk0_p(P_SUS) === 20, `Expected P_SUS=20, got ${ex.web_trk0_p(P_SUS)}`);
        assert(ex.web_trk0_p(P_REL) === 35, `Expected P_REL=35, got ${ex.web_trk0_p(P_REL)}`);
        assert(ex.web_trk0_p(P_ED_FLT) === 55, `Expected P_ED_FLT=55, got ${ex.web_trk0_p(P_ED_FLT)}`);

        // Press B_ENV (1 << 2) -> Mode 1: Sustained Pad
        ex.web_buttons(1 << 2);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 1, `Expected env 1, got ${ex.web_cinco_get_env_mode()}`);
        assert(ex.web_trk0_p(P_ATK) === 75, `Expected P_ATK=75, got ${ex.web_trk0_p(P_ATK)}`);
        assert(ex.web_trk0_p(P_DEC) === 90, `Expected P_DEC=90, got ${ex.web_trk0_p(P_DEC)}`);
        assert(ex.web_trk0_p(P_SUS) === 127, `Expected P_SUS=127, got ${ex.web_trk0_p(P_SUS)}`);
        assert(ex.web_trk0_p(P_REL) === 100, `Expected P_REL=100, got ${ex.web_trk0_p(P_REL)}`);
        assert(ex.web_trk0_p(P_ED_FLT) === 10, `Expected P_ED_FLT=10, got ${ex.web_trk0_p(P_ED_FLT)}`);

        // Press B_ENV -> Mode 2: Staccato Pluck
        ex.web_buttons(1 << 2);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 2, `Expected env 2, got ${ex.web_cinco_get_env_mode()}`);
        assert(ex.web_trk0_p(P_ATK) === 0, `Expected P_ATK=0, got ${ex.web_trk0_p(P_ATK)}`);
        assert(ex.web_trk0_p(P_DEC) === 25, `Expected P_DEC=25, got ${ex.web_trk0_p(P_DEC)}`);
        assert(ex.web_trk0_p(P_SUS) === 0, `Expected P_SUS=0, got ${ex.web_trk0_p(P_SUS)}`);
        assert(ex.web_trk0_p(P_REL) === 15, `Expected P_REL=15, got ${ex.web_trk0_p(P_REL)}`);
        assert(ex.web_trk0_p(P_ED_FLT) === 65, `Expected P_ED_FLT=65, got ${ex.web_trk0_p(P_ED_FLT)}`);

        // Press B_ENV -> Mode 3: Punch Bass
        ex.web_buttons(1 << 2);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 3, `Expected env 3, got ${ex.web_cinco_get_env_mode()}`);
        assert(ex.web_trk0_p(P_ATK) === 0, `Expected P_ATK=0, got ${ex.web_trk0_p(P_ATK)}`);
        assert(ex.web_trk0_p(P_DEC) === 45, `Expected P_DEC=45, got ${ex.web_trk0_p(P_DEC)}`);
        assert(ex.web_trk0_p(P_SUS) === 40, `Expected P_SUS=40, got ${ex.web_trk0_p(P_SUS)}`);
        assert(ex.web_trk0_p(P_REL) === 25, `Expected P_REL=25, got ${ex.web_trk0_p(P_REL)}`);
        assert(ex.web_trk0_p(P_ED_FLT) === 70, `Expected P_ED_FLT=70, got ${ex.web_trk0_p(P_ED_FLT)}`);

        // Press B_ENV -> Cycles back to Mode 0: Snappy Brass
        ex.web_buttons(1 << 2);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 0, `Expected env 0, got ${ex.web_cinco_get_env_mode()}`);
        assert(ex.web_trk0_p(P_ATK) === 2, `Expected P_ATK=2, got ${ex.web_trk0_p(P_ATK)}`);
        assert(ex.web_trk0_p(P_DEC) === 60, `Expected P_DEC=60, got ${ex.web_trk0_p(P_DEC)}`);
    });

    // 6. B_SCL cycles chromatic/minor/major/pentatonic/blues and sets P_QUANT and P_SCALE
    test("B_SCL button cycling configures trk[0] scale and quantization", () => {
        // Initially mode 0 (Chromatic)
        assert(ex.web_cinco_get_scale_mode() === 0, `Expected initial scale 0, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 0, `Expected P_QUANT=0, got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 0, `Expected P_SCALE=0, got ${ex.web_trk0_p(P_SCALE)}`);

        // Press B_SCL (1 << 1) -> Mode 1: Natural Minor
        ex.web_buttons(1 << 1);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_scale_mode() === 1, `Expected scale 1, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 1, `Expected P_QUANT=1 (QN_SNAP), got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 2, `Expected P_SCALE=2, got ${ex.web_trk0_p(P_SCALE)}`);

        // Press B_SCL -> Mode 2: Major
        ex.web_buttons(1 << 1);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_scale_mode() === 2, `Expected scale 2, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 1, `Expected P_QUANT=1 (QN_SNAP), got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 1, `Expected P_SCALE=1, got ${ex.web_trk0_p(P_SCALE)}`);

        // Press B_SCL -> Mode 3: Minor Pentatonic
        ex.web_buttons(1 << 1);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_scale_mode() === 3, `Expected scale 3, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 1, `Expected P_QUANT=1 (QN_SNAP), got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 6, `Expected P_SCALE=6, got ${ex.web_trk0_p(P_SCALE)}`);

        // Press B_SCL -> Mode 4: Blues / Dorian
        ex.web_buttons(1 << 1);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_scale_mode() === 4, `Expected scale 4, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 1, `Expected P_QUANT=1 (QN_SNAP), got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 3, `Expected P_SCALE=3, got ${ex.web_trk0_p(P_SCALE)}`);

        // Press B_SCL -> Cycles back to Mode 0: Chromatic
        ex.web_buttons(1 << 1);
        renderMs(30);
        ex.web_buttons(0);
        renderMs(30);
        assert(ex.web_cinco_get_scale_mode() === 0, `Expected scale 0, got ${ex.web_cinco_get_scale_mode()}`);
        assert(ex.web_trk0_p(P_QUANT) === 0, `Expected P_QUANT=0 (QN_CHROM), got ${ex.web_trk0_p(P_QUANT)}`);
        assert(ex.web_trk0_p(P_SCALE) === 0, `Expected P_SCALE=0, got ${ex.web_trk0_p(P_SCALE)}`);
    });

    // 7. Persistence across source/character switches
    test("Envelope and Scale persist seamlessly across character switches", () => {
        // Set env to Pad (mode 1: ATK=75, DEC=90)
        ex.web_cinco_set_env_mode(1);
        // Set scale to Blues (mode 4: QUANT=1, SCALE=3)
        ex.web_cinco_set_scale_mode(4);
        renderMs(30);

        // Switch to Oyster
        ex.web_cinco_set_source(1);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 1, "Env mode preserved in Oyster");
        assert(ex.web_trk0_p(P_ATK) === 75, "P_ATK preserved in Oyster");
        assert(ex.web_cinco_get_scale_mode() === 4, "Scale mode preserved in Oyster");
        assert(ex.web_trk0_p(P_SCALE) === 3, "P_SCALE preserved in Oyster");

        // Switch to Tayne
        ex.web_cinco_set_source(2);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 1, "Env mode preserved in Tayne");
        assert(ex.web_trk0_p(P_ATK) === 75, "P_ATK preserved in Tayne");
        assert(ex.web_cinco_get_scale_mode() === 4, "Scale mode preserved in Tayne");
        assert(ex.web_trk0_p(P_SCALE) === 3, "P_SCALE preserved in Tayne");

        // Switch to Celery
        ex.web_cinco_set_source(0);
        renderMs(30);
        assert(ex.web_cinco_get_env_mode() === 1, "Env mode preserved in Celery");
        assert(ex.web_trk0_p(P_ATK) === 75, "P_ATK preserved in Celery");
        assert(ex.web_cinco_get_scale_mode() === 4, "Scale mode preserved in Celery");
        assert(ex.web_trk0_p(P_SCALE) === 3, "P_SCALE preserved in Celery");
    });

    const failed = results.filter(r => r.status === 'FAIL');
    if (failed.length > 0) {
        console.error(`\nFAILED: ${failed.length} / ${results.length} tests failed.`);
        process.exit(1);
    } else {
        console.log(`\nALL ${results.length} MATRIX VERIFICATION TESTS PASSED (100%)!`);
        process.exit(0);
    }
}

run().catch(err => {
    console.error("FATAL:", err);
    process.exit(1);
});
