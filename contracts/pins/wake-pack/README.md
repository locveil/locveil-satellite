# wake-pack — the voice wake-word pack pin (consumed)

A **pinned, one-way-inward copy** of the voice-owned wake-pack **sidecar stamp**
(`consumer-pins` invariant). The pack itself (microWakeWord v2 manifest + `.tflite`) is
a third-party-format artifact on Hugging Face — **never forked, never retrained here**;
the pack binaries never enter this tree. What is pinned is voice's sidecar `STAMP.json`
alone (the owner enumerates no other artifact), at the tag `PIN.json` records: it
carries the HF repo/revision, URLs, and the **sha256 content hashes** every downstream
check verifies against.

Never hand-edit `STAMP.json`; the pin moves only by a re-pin ledger task running
`python3 scripts/repin.py wake-pack`.

**Conformance (layer 2 — both are hash checks against this pin):**

- **publish-time** — `scripts/publish_model_pack.py` (the `PIN.json` conformance
  pointer): verifies the artifact sha256s against this stamp before anything is served
  from the WB7 `/srv/esp32/models/`, and refuses to publish while this pin trails its
  owner;
- **flash-time** — FW-1a: the firmware's models partition holds the UNMODIFIED pack,
  hash-verified on load; the `register` message reports the pack version (the runtime
  staleness surface).
