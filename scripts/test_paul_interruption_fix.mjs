// test_paul_interruption_fix.mjs - Verification that typing '7' or using sequencer does not trigger Paul speech or reset
import fs from 'fs';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';
console.log(`Loading WASM: ${wasmPath}`);
const bytes = fs.readFileSync(wasmPath);

function renderMs(ex, mem, ms) {
    let n = Math.round(ms * 44.1);
    while (n > 0) {
        let m = Math.min(n, 128);
        ex.web_render(m);
        n -= m;
    }
}

async function run() {
    const { instance } = await WebAssembly.instantiate(bytes, {});
    const ex = instance.exports;
    const mem = ex.memory;

    ex._initialize();
    ex.web_nor_erase();
    ex.web_boot();

    console.log("\n=== TEST 1: Inhibit Screensaver in Sequencer Mode ===");
    // Enter Sequencer Mode
    ex.web_buttons(1 << 9); // B_SEQ
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 20);

    if (ex.web_cinco_get_view() !== 1) {
        throw new Error(`Expected view_mode 1, got ${ex.web_cinco_get_view()}`);
    }

    // Advance device clock by 25 seconds (25,000 ms) without input
    renderMs(ex, mem, 25000);

    // Verify screensaver is NOT active
    // View mode should still be 1
    if (ex.web_cinco_get_view() !== 1) {
        throw new Error(`Sequencer view was interrupted! view_mode=${ex.web_cinco_get_view()}`);
    }
    console.log("-> 25s idle passed in sequencer mode without screensaver triggering!");

    console.log("\n=== TEST 2: Safe B_HOME in Sequencer Mode ===");
    // Set a preset other than Celery Man (e.g. preset 2: Tayne)
    ex.web_cinco_set_preset(2);
    renderMs(ex, mem, 20);
    if (ex.web_cinco_get_preset() !== 2) {
        throw new Error(`Failed to set preset 2`);
    }

    // Now press B_HOME (button 6) while in Sequencer Mode (view_mode == 1)
    ex.web_buttons(1 << 6); // B_HOME
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 20);

    // It should exit to view_mode 0
    if (ex.web_cinco_get_view() !== 0) {
        throw new Error(`Expected view_mode 0 after B_HOME, got ${ex.web_cinco_get_view()}`);
    }
    // But it should NOT have reset preset to 0!
    if (ex.web_cinco_get_preset() !== 2) {
        throw new Error(`B_HOME performed a full system reset! Preset was reset from 2 to ${ex.web_cinco_get_preset()}`);
    }
    console.log("-> B_HOME cleanly exited defrag without full reset or interruption!");

    console.log("\n=== TEST 3: Step 7 Input in Sequencer Mode (White Key 6) ===");
    // Re-enter sequencer mode
    ex.web_buttons(1 << 9); // B_SEQ
    renderMs(ex, mem, 20);
    ex.web_buttons(0);
    renderMs(ex, mem, 20);

    ex.web_cinco_set_seq_row(0); // Kick
    ex.web_cinco_set_seq_grid(0, 0); // Clear

    // Step 7 corresponds to white key index 6 (WHITE[6] = 11, Note B3)
    const whiteKeys = [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26];
    const keyStep7 = whiteKeys[6]; // 11
    ex.web_keys(1 << keyStep7);
    renderMs(ex, mem, 20);
    ex.web_keys(0);
    renderMs(ex, mem, 20);

    let grid = ex.web_cinco_get_seq_grid(0);
    if (((grid >> 6) & 1) !== 1) {
        throw new Error(`Step 7 failed to toggle ON in seq_grid! grid=0x${grid.toString(16)}`);
    }
    if (ex.web_cinco_get_view() !== 1) {
        throw new Error(`Pressing Step 7 exited sequencer mode! view_mode=${ex.web_cinco_get_view()}`);
    }
    console.log("-> Step 7 successfully toggled without exiting sequencer mode!");

    console.log("\n=== TEST 4: Verify build/emu/index.html Keyboard Bindings ===");
    const html = fs.readFileSync('build/emu/index.html', 'utf8');
    // Ensure Digit7 is not mapped to ROW2
    if (html.includes('Digit7", "Digit8", "Digit9", "Digit0", "Minus", "Equal"].forEach((c, i) => KEYMAP[c] = { btn: B[ROW2[i]] }')) {
        throw new Error("build/emu/index.html still overwrites Digit7 with B[ROW2] (B_HOME)!");
    }
    if (!html.includes('KEYMAP.Escape = { btn: B["HOME"] };')) {
        throw new Error("KEYMAP.Escape missing B['HOME']!");
    }
    if (!html.includes('KEYMAP.Space = { btn: B["PLAY"] };')) {
        throw new Error("KEYMAP.Space missing B['PLAY']!");
    }
    if (!html.includes('Digit7: 6')) {
        throw new Error("Sequencer mode Digit7 step 7 mapping missing!");
    }
    console.log("-> Computer keyboard bindings in index.html verified!");

    console.log("\n=======================================================");
    console.log(" PAUL GREETING INTERRUPTION & SEQUENCER FIX VERIFIED! ");
    console.log("=======================================================");
}

run().catch(err => {
    console.error("TEST FAILED:", err);
    process.exit(1);
});
