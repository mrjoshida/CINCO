import fs from 'fs';

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

    function renderMs(ms, holdKey = false) {
        if (holdKey) {
            ex.web_keys(1 << 5);
        } else {
            ex.web_keys(0);
        }
        let n = Math.round(ms * 44.1);
        while (n > 0) {
            let m = Math.min(n, 128);
            ex.web_render(m);
            n -= m;
        }
    }

    // Let emulator boot settle
    renderMs(150, false);

    const BTN_MAP = {
        B_FX: 0,
        B_SCL: 1,
        B_ENV: 2,
        B_LFO: 3,
        B_EDIT: 4,
        B_GLO: 5,
        B_HOME: 6,
        B_SAVE: 7,
        B_ARP: 8,
        B_SEQ: 9,
    };

    const EN_PRESET = 2;

    const results = [];

    function pressButton(btnId) {
        ex.web_buttons(1 << btnId);
        renderMs(25, false);
        ex.web_buttons(0);
        renderMs(25, false);
    }

    function moveEncoder(role, steps) {
        ex.web_enc(role, steps);
        renderMs(30, false);
    }

    // Test 1: B_SEQ toggles defrag on and off
    {
        const initView = ex.web_cinco_get_view();
        pressButton(BTN_MAP.B_SEQ);
        const toggledOn = ex.web_cinco_get_view();
        const titleOn = readCString(mem, ex.web_cinco_get_title());
        pressButton(BTN_MAP.B_SEQ);
        const toggledOff = ex.web_cinco_get_view();

        const pass = (initView === 0 && toggledOn === 1 && toggledOff === 0 && titleOn === "Disk Defragmenter - C:");
        results.push({
            name: "B_SEQ Toggle",
            action: "Press B_SEQ (toggle 0 -> 1 -> 0)",
            initialView: initView,
            activeView: toggledOn,
            finalView: toggledOff,
            titleOn,
            pass
        });
    }

    // Helper to test exit from defrag
    function testDefragExit(testName, actionFn, actionDesc) {
        ex.web_cinco_set_view(1);
        renderMs(15, false);
        const viewBefore = ex.web_cinco_get_view();
        const titleBefore = readCString(mem, ex.web_cinco_get_title());

        actionFn();

        const viewAfter = ex.web_cinco_get_view();
        const titleAfter = readCString(mem, ex.web_cinco_get_title());

        const pass = (viewBefore === 1 && viewAfter === 0 && titleBefore === "Disk Defragmenter - C:" && titleAfter !== "Disk Defragmenter - C:");
        results.push({
            name: testName,
            action: actionDesc,
            viewBefore,
            viewAfter,
            titleBefore,
            titleAfter,
            pass
        });
    }

    // Test 2: B_FX clears defrag
    testDefragExit("B_FX Exit", () => pressButton(BTN_MAP.B_FX), "Press B_FX (NSFW toggle)");

    // Test 3: B_LFO clears defrag
    testDefragExit("B_LFO Exit", () => pressButton(BTN_MAP.B_LFO), "Press B_LFO (Hat Wobble)");

    // Test 4: B_ARP clears defrag
    testDefragExit("B_ARP Exit", () => pressButton(BTN_MAP.B_ARP), "Press B_ARP (Flarhgunnstow)");

    // Test 5: B_HOME clears defrag
    testDefragExit("B_HOME Exit", () => pressButton(BTN_MAP.B_HOME), "Press B_HOME (Reset/Home)");

    // Test 6: B_SAVE clears defrag
    testDefragExit("B_SAVE Exit", () => pressButton(BTN_MAP.B_SAVE), "Press B_SAVE (Printout/Save)");

    // Test 7: EN_PRESET clockwise (+1) clears defrag
    testDefragExit("Preset Enc CW", () => moveEncoder(EN_PRESET, 1), "Turn EN_PRESET Clockwise (+1)");

    // Test 8: EN_PRESET counter-clockwise (-1) clears defrag
    testDefragExit("Preset Enc CCW", () => moveEncoder(EN_PRESET, -1), "Turn EN_PRESET Counter-Clockwise (-1)");

    const allPassed = results.every(r => r.pass);

    console.log(JSON.stringify({
        results,
        allPassed
    }, null, 2));
}

run().catch(err => {
    console.error("Runner error:", err);
    process.exit(1);
});
