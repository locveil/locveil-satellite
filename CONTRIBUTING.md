# Contributing to locveil-satellite

This is the hardware member of the Locveil family: PCB projects, ESP-IDF firmware, and
the controller-side provisioning plane for the ESP32 voice satellites. This page is the
contributor front door — it narrates and links the normative sources; the sources
themselves are the law.

## The phase process

Work here moves through gated phases, in order: **DES (design) → PCB (board projects) →
FW (firmware)**, plus OPS for toolchain/operations. The gates are strict:

- No PCB work before its governing design is agreed.
- **No firmware work of any kind before the execution-layer decision is made** (the
  toolchain choice, including the mandatory pin/strapping audit — a hard-won lesson).
  Until then the firmware toolchain is deliberately *not installed*; day-one tooling is
  knowledge-side only.
- A task that needs physical hardware carries the `HW-GATED` marker and never blocks a
  software milestone.

The full invariants live in `CLAUDE.md` (repo LAW); ledger mechanics in
`../locveil-commons/process/ledger-discipline.md`. Every piece of work has a ledger ID
(`docs/LEDGER.md`).

## Per-phase toolchain map

| Phase | Tooling (wired today) |
|---|---|
| DES | Espressif docs + ESP component-registry MCP servers (`.mcp.json`) |
| PCB | pcbparts MCP (parts/footprints) + Serena over a cloned SKiDL (`scripts/bootstrap_references.sh` clones it into gitignored `references/`) |
| FW | **not yet chosen** — the execution-layer decision selects it; nothing to install until then |

## Pin discipline (contracts)

`contracts/README.md` is the registry: every contract this repo owns and every pin it
consumes, direction-labeled. Rules:

- Consume sibling artifacts **at their tags only**; a pin is a complete, byte-identical
  artifact copy with a `PIN.json` hash record — **never hand-edit a pin**, re-pin on a
  version bump.
- Owned surfaces (`contracts/<name>/`) carry a STAMP and an owner-side guard from day
  one; changing an owned artifact is a version bump, not an edit.
- Convention: `../locveil-commons/process/contracts.md`; coherence is enforced by the
  vendored `scripts/contract_guard.py` in pre-commit and CI.

## The leaf-truth corpus rule

`docs/devices/` is the per-device hardware **ground truth** (bench-confirmed dossiers:
deck-common + one file per device). Everything else derives from it — user-facing build
docs, per-device descriptors, board projects — and never duplicates it. If a dossier and
a derived doc disagree, the dossier wins; fix the derivation.

## Docs discipline

User-facing docs are inventoried in `docs/manifest.json` (schema:
`../locveil-commons/process/user-docs/manifest.schema.json`; convention:
`../locveil-commons/process/user-docs.md`). Every task completion records a docs
verdict against the manifest's node ids; a new user-facing doc is registered in the
manifest **in the same change** (the coherence guard `scripts/check_docs_manifest.py`
fails otherwise). Docs whose truth needs hardware or a later phase are declared as
pending-gate nodes — never written as fiction.

## Design entry points

`docs/design/` (internal): `esp32_satellite.md` is the consolidated satellite design;
`docs/review/` holds evidence passes. User docs derive from these, never point users at
them.
