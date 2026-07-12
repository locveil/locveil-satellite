# components/ — shared ESP-IDF firmware components

The shared pieces every device app builds from (HK-4: `locveil_wifi`, `locveil_wb_mqtt`,
`locveil_ota`, `locveil_identity`, `locveil_ir_baseband`). There is **one firmware app per
device** (compile-time identity + an NVS identity assertion at boot) — a single
multi-device image is explicitly retired (`per-device-apps` invariant).

Empty at bootstrap: no firmware work before DES-3 (`phase-gates`).
