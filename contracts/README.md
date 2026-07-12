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

_Pending pin (not yet a folder): **device-integration** — the bridge's convention (tag
`device-integration-v1`) is pinned by **DES-4** together with the per-device descriptors
it governs; the descriptors themselves are per-instance config validated against that
pin, not contracts (`process/contracts.md` §1)._

Guards: layer 1 is the vendored `scripts/contract_guard.py` (commons
`packages/contract-guard/`, pinned at tag **`contract-guard-v1`** — never edit the
vendored file, re-pin to move; runs in `hooks/pre-commit` and the path-gated
`contract-guard` CI job, `--check` only); layer 2 is the per-contract guards and
conformance tests listed above.
