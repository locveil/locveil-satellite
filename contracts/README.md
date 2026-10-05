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
| [`esp32-site`](esp32-site/README.md) | artifact stays `provisioning/ansible/templates/esp32-site.conf.j2` (Plane-B nginx site); `esp32-site/` holds the STAMP + pointer README | `esp32-site/STAMP.json` + tag `esp32-site-v1.1.0` (owner guard: `scripts/check_esp32_site.py`; consumer: voice `contracts/pins/esp32-site/`) |

## Consumed (pins)

| Pin | Owner | Notes |
|---|---|---|
| [`ws-protocol`](pins/ws-protocol/README.md) | locveil-voice (tag `ws-protocol-v1.1.0`) | the WS wire protocol — the guide plus its machine core (golden frames, transcripts, schema); **the doc wins, firmware adapts**; conformance: FW-1a's data-driven test over the pinned fixtures (not written yet — the PIN names none); staleness: `register` reports `protocol_version` (the major) |
| [`wake-pack`](pins/wake-pack/README.md) | locveil-voice (tag `wake-pack-v1.0.1`) | sidecar stamp over the UNMODIFIED third-party HF pack — the STAMP is the whole pinned set, binaries never enter this tree; conformance: hash-at-publish (`scripts/publish_model_pack.py`) + hash-at-flash (FW-1a) |
| [`docs-manifest-schema`](pins/docs-manifest-schema/README.md) | locveil-commons (tag `docs-manifest-schema-v1.0.0`) | the org docs-manifest vocabulary (`process/user-docs.md` §4) — `docs/manifest.json` is instance data validated against it, not a contract; conformance: `scripts/check_docs_manifest.py`, which reads its key sets and enums from the pinned schema |

_Pending pin (not yet a folder): **device-integration** — the bridge's convention is
pinned by **DES-4** together with the per-device descriptors it governs, at the bridge's
README-split cut `device-integration-v1.2.0` (HK-13 — the first cut whose enumerated set
is pinnable; DES-4 adds the `.repin.toml` family, the pin and its conformance test in one
change); the descriptors themselves are per-instance config validated
against that pin, not contracts (`process/contracts.md` §1). **Explicitly N/A for the voice satellite
(`waveshare-lcd146`)** — owner ruling 2026-07-20, FW-1 requirements review O-4
(`docs/design/fw1_requirements.md`): the satellite is a voice-plane device WB7 reaches
over the pinned WS protocol; the bridge never actuates it, so it publishes no
descriptor. Until DES-4 the family is deliberately not declared in `.repin.toml`
(a declaration needs a conformance test that resolves; none can exist before a
descriptor does) — this paragraph and the DES-4 ledger entry are the visible record._

Guards: layer 1 is the vendored `scripts/contract_guard.py` (commons
`packages/contract-guard/`, vendored at tag **`contract-guard-v4.0.0`** — tag + sha256
recorded in `.repin.toml`; never edit the vendored file, re-vendor with
`scripts/repin.py tool contract-guard`); it runs in `hooks/pre-commit` (`--relax-tags`
mid-bump tolerance) and the `contract-guard` CI job — every push and PR, no path gate
(HK-13) — `--check` only. The same job runs `scripts/repin.py --check --touched <base>`:
staleness is advisory here until FW first light, **touching a pin that trails its owner
fails**. Layer 2 is the per-contract guards and conformance tests listed above.
