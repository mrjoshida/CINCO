import fs from 'fs';

const wasmPath = process.argv[2] || 'build/emu/felucca.wasm';

function renderMs(ex, ms) {
    let n = Math.round(ms * 44.1);
    while (n > 0) {
        let m = Math.min(n, 128);
        ex.web_render(m);
        n -= m;
    }
}

function resetModes(ex) {
    if (ex.web_cinco_clear_popups) ex.web_cinco_clear_popups();
    ex.web_cinco_set_screensaver(0);
    ex.web_cinco_set_boss(0);
    ex.web_cinco_set_view(0);
    ex.web_cinco_set_diag(0);
    ex.web_cinco_set_wobble(0);
    ex.web_cinco_set_flail(0);
    ex.web_cinco_set_nude(0);
    ex.web_cinco_set_source(0);
}

const MODES = [
    {
        name: "Celery Man",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(0); // SRC_CELERY
        }
    },
    {
        name: "Tayne Beta",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(2); // SRC_TAYNE
        }
    },
    {
        name: "Oyster Smiling",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(1); // SRC_OYSTER
        }
    },
    {
        name: "Hat Wobble",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(0);
            ex.web_cinco_set_wobble(1);
        }
    },
    {
        name: "Flarhgunnstow",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(0);
            ex.web_cinco_set_flail(1);
        }
    },
    {
        name: "Nude Tayne",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_source(2);
            ex.web_cinco_set_nude(1);
        }
    },
    {
        name: "Disk Defragmenter",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_view(1);
        }
    },
    {
        name: "Lotus 1-2-3 Boss Key",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_boss(1);
        }
    },
    {
        name: "After Dark Screensaver",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_set_screensaver(1);
        }
    },
    {
        name: "NSFW Dialog Popup",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_trigger_nsfw();
        },
        frame: (ex) => {
            ex.web_cinco_trigger_nsfw();
        }
    },
    {
        name: "Error Dialog Popup",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_trigger_error();
        },
        frame: (ex) => {
            ex.web_cinco_trigger_error();
        }
    },
    {
        name: "Oyster Receipt Popup",
        setup: (ex) => {
            resetModes(ex);
            ex.web_cinco_trigger_receipt();
        },
        frame: (ex) => {
            ex.web_cinco_trigger_receipt();
        }
    }
];

async function run() {
    const bytes = fs.readFileSync(wasmPath);

    // Helper to benchmark a mode over 60 frames (~2000 ms simulated time)
    async function benchmarkMode(modeDef) {
        const { instance } = await WebAssembly.instantiate(bytes, {});
        const ex = instance.exports;
        ex._initialize();
        ex.web_nor_erase();
        ex.web_boot();
        renderMs(ex, 150);

        // Transition to mode
        modeDef.setup(ex);
        // Settle for 100 ms (allowing initial layout redraw)
        renderMs(ex, 100);

        // Reset display stats
        ex.web_lcd_stats_reset();

        let max_frame_pixels = 0;

        // Loop 60 frames (advance ~33 ms per frame)
        for (let f = 0; f < 60; f++) {
            const prev_pixels = ex.web_lcd_get_pixels();
            const prev_calls = ex.web_lcd_get_calls();

            if (modeDef.frame) {
                modeDef.frame(ex);
            }
            renderMs(ex, 33.333);

            const cur_pixels = ex.web_lcd_get_pixels();
            const cur_calls = ex.web_lcd_get_calls();

            const frame_pixels = cur_pixels - prev_pixels;
            if (frame_pixels > max_frame_pixels) {
                max_frame_pixels = frame_pixels;
            }
        }

        const total_pixels = ex.web_lcd_get_pixels();
        const total_calls = ex.web_lcd_get_calls();
        const total_full_clears = ex.web_lcd_get_full_clears();

        const avg_pixels_per_frame = total_pixels / 60;
        const peak_pixels_per_frame = max_frame_pixels;
        // 12 MHz SPI, 2 bytes/px: (pixels * 2 * 8) / 12000 ms
        const avg_spi_time_ms = (avg_pixels_per_frame * 16) / 12000;
        const peak_spi_time_ms = (peak_pixels_per_frame * 16) / 12000;
        const avg_calls_per_frame = total_calls / 60;
        const full_clears = total_full_clears;

        const pass = (peak_spi_time_ms <= 33.3) && (full_clears === 0) && (avg_calls_per_frame <= 20);

        return {
            name: modeDef.name,
            avg_pixels_per_frame,
            peak_pixels_per_frame,
            avg_spi_time_ms,
            peak_spi_time_ms,
            avg_calls_per_frame,
            full_clears,
            pass
        };
    }

    const results = [];
    for (const mode of MODES) {
        const res = await benchmarkMode(mode);
        results.push(res);
    }

    const allPassed = results.every(r => r.pass);
    const output = {
        total_modes: results.length,
        all_passed: allPassed,
        results
    };

    console.log(JSON.stringify(output, null, 2));
}

run().catch(err => {
    console.error("Test runner error:", err);
    process.exit(1);
});
