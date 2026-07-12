# imports/ — frozen cross-repo import sources

Trees imported verbatim from sibling repos, kept as **frozen reference** — never edited,
never built from here. Tasks mine them; conforming rewrites land in their real homes
(`components/`, `boards/`, `docs/`). Pre-move history stays in the owning repo
(plain-move rule, PROD-15).

## bridge-esp32/ — the bridge's `ESP32/` deck-bridge scaffold

- **Source:** `../locveil-bridge/ESP32/` @ bridge commit `a80322f` (2026-07-12) — the 34
  git-tracked files, 1:1 (untracked local files, `.pio/` build output left behind).
- **Delegation:** PROD-15 bridge item 1b — this import confirms the handover; the bridge's
  **DRV-35** deletes its copy and retires DRV-7 (this copy then becomes the only one).
- **What it is:** the bench-evolved PIO/ESP-IDF single-image scaffold for the 4
  transport-source deck bridges (Revox A77, Revox B215, Pioneer CLD-D925, Panasonic
  NV-FS90; 3 drivers — Pioneer + Panasonic share baseband IR). The single-image FR-1
  approach is **RETIRED** (`per-device-apps` invariant — the GPIO14 double-booking);
  the architecture is not to be copied, the *facts* are the value:
  - `docs/wb-*.md` — bench-confirmed per-device build docs (**leaf truth** for DES-1's
    claim-by-claim harmonization; pin maps re-audited there);
  - `REQUIREMENTS.md` — FR-text feeding DES-1's truth pass; the bridge's VWB-38 promotes
    it into wb-mqtt-v1 (referencing this copy once DRV-35 deletes the original);
  - `src/` + `include/` — working driver/Wi-Fi/MQTT/OTA code, source material for the
    shared `components/` + per-device apps (FW phase, gated on DES-3).
