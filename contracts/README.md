# locveil-satellite — contract registry

The direction-labeled index required by `../locveil-commons/process/contracts.md` §2.
Every contract this repo OWNS and every pin it CONSUMES, one line each; details live in
the per-contract READMEs. Layout is the uniform org shape: `contracts/<name>/` owned,
`contracts/pins/<name>/` consumed. Pins are one-way-inward, version-stamped copies per
the `consumer-pins` invariant — owned elsewhere, **never hand-edited**; re-pin on a vN
bump.

## Owned

| Contract | Where | Version authority |
|---|---|---|
| [`esp32-site`](esp32-site/README.md) | artifact stays `provisioning/ansible/templates/esp32-site.conf.j2` (Plane-B nginx site); `esp32-site/` holds the STAMP + pointer README | `esp32-site/STAMP.json` + tag `esp32-site-v1` (owner guard: `scripts/check_esp32_site.py`; consumer: voice `contracts/pins/esp32-site/`) |

## Consumed (pins)

| Pin | Owner | Notes |
|---|---|---|
| [`ws-protocol`](pins/ws-protocol/README.md) | locveil-voice (tag `ws-protocol-v1`) | the WS wire protocol — **the doc wins, firmware adapts**; conformance: FW-1 (opens after DES-3, `phase-gates`); staleness: `register` reports `protocol_version` |
| [`wake-pack`](pins/wake-pack/README.md) | locveil-voice (tag `wake-pack-v1`) | sidecar stamp over the UNMODIFIED third-party HF pack — binaries never enter this tree; conformance: hash-at-publish (OPS-1) + hash-at-flash (FW-1) |

## Internal

| Contract | Where | Version authority |
|---|---|---|
| [`docs-manifest`](docs-manifest/README.md) | artifact stays `docs/manifest.json` (the user-facing docs inventory, `process/user-docs.md` §4); `docs-manifest/` holds the STAMP + pointer README | `docs-manifest/STAMP.json` (`docs-manifest-v1`, INTERNAL — no git tag; bumped only on a schema reshape; guard: `scripts/check_docs_manifest.py`) |

_Pending pin (not yet a folder): **device-integration** — the bridge's convention (tag
`device-integration-v1`) is pinned by **DES-4** together with the per-device descriptors
it governs; the descriptors themselves are per-instance config validated against that
pin, not contracts (`process/contracts.md` §1). **Explicitly N/A for the voice satellite
(`waveshare-lcd146`)** — owner ruling 2026-07-20, FW-1 requirements review O-4
(`docs/design/fw1_requirements.md`): the satellite is a voice-plane device WB7 reaches
over the pinned WS protocol; the bridge never actuates it, so it publishes no
descriptor. The guard's "never pinned" warning stays until DES-4's bridge-actuated
devices arrive — explained, not silenced._

Guards: layer 1 is the vendored `scripts/contract_guard.py` (commons
`packages/contract-guard/`, vendored at tag **`contract-guard-v3`** — never edit the
vendored file, re-pin to move; runs in `hooks/pre-commit` (`--relax-tags` mid-bump
tolerance) and the path-gated `contract-guard` CI job, `--check` only); layer 2 is the
per-contract guards and conformance tests listed above. *(This line said `contract-guard-v1` while the vendored
script was already v2 — the HK-12 round-2 live drift find, corrected by the OPS-12
re-vendor to v3.)*
