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

- [x] **OPS-2** — **DONE 2026-07-12** — **Wire the day-one toolchain** (HK-4 round 4;
      knowledge-side only per `no-execution-toolchain-at-bootstrap`). Root `.mcp.json` with
      the four servers: `pcbparts` (HTTP `https://pcbparts.dev/mcp`, keyless — JLCPCB/
      Mouser/DigiKey parametric search + KiCad footprints), `espressif-docs` (HTTP
      `https://mcp.espressif.com/docs` — OAuth via GitHub on first `/mcp` use; 401 until
      then is expected; 40 req/h / 200 req/day per user), `esp-component-registry` (HTTP
      `https://components.espressif.com/mcp`, keyless), `serena` (stdio, `uvx` from
      `oraios/serena`, `--project-from-cwd`). `scripts/bootstrap_references.sh` clones SKiDL
      into gitignored `references/` for Serena (run + verified: clone lands, gitignore
      holds; pcbparts + registry probed 200 on MCP initialize). Per-phase nested CLAUDE.md
      wired: `docs/design/` (DES — docs+registry MCPs, corpus ground rules), `boards/` (PCB
      — pcbparts+serena, bootstrap prereq, strapping-audit rule), `components/` (FW —
      DES-3 gate, docs+registry, Tools-MCP explicitly deferred to DES-3). No PlatformIO, no
      skidl-skills, no ESP-IDF Tools MCP — DES-3/DES-2 own those decisions.
