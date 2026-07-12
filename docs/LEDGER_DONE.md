# locveil-satellite — DONE ledger

Completed entries, MOVED here on close. Frozen history — never re-edited. Rotates per
`ledger-discipline.md` §2 (archived IDs stay resolvable via `docs/archive/ledger/`).

## DES — design

- [x] **DES-6** [fleet] — **DONE 2026-07-12** (filed + executed same session; PROD-15 bridge
      delegation item 1b, satellite side). **Import the frozen bridge `ESP32/` tree.** The 34
      git-tracked files copied 1:1 from `../locveil-bridge/ESP32/` @ bridge `a80322f` into
      `imports/bridge-esp32/` (frozen reference — provenance + mining rules in
      `imports/README.md`; untracked local files and `.pio/` build output left behind; no
      history migration per the plain-move rule). This is DES-1's input corpus (bench-confirmed
      `docs/wb-*.md` build docs = leaf truth, `REQUIREMENTS.md` for the truth pass) and FW-phase
      source material (`src/`+`include/` → shared `components/`, per HK-4 the single-image
      architecture itself stays retired). Import confirmation filed repo-to-repo into the
      bridge's DRV-35 entry — unblocks its delete + DRV-7 retirement.

## PCB — board projects

## FW — firmware

## OPS — operations / toolchain
