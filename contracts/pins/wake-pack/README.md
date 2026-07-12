# wake-pack — the voice wake-word pack pin (consumed)

A **pinned, one-way-inward copy** of the voice-owned wake-pack **sidecar stamp**
(`consumer-pins` invariant). The pack itself (microWakeWord v2 manifest + `.tflite`) is
a third-party-format artifact on Hugging Face — **never forked, never retrained here**;
the pack binaries never enter this tree. What is pinned is voice's sidecar `STAMP.json`
(tag `wake-pack-v1`), which carries the HF repo/revision, URLs, and **sha256 content
hashes** — the hash surface every downstream check verifies against.

| File | Origin | What it is |
|---|---|---|
| `STAMP.json` | voice (byte-identical @ `wake-pack-v1`) | Sidecar stamp: pack word/display, HF repo + revision, per-file URLs + sha256s |
| `PIN.json` | **satellite-stamped** | The pin record: tag/commit, stamp hash, conformance pointer |

Conformance (layer 2, both hash checks against this pin):

- **publish-time** (OPS-1): the pipeline that publishes model packs into the WB7
  `/srv/esp32/models/` verifies the artifact sha256s against this stamp before serving;
- **flash-time** (FW-1): the firmware's flash data partition holds the UNMODIFIED pack,
  hash-verified on load; the `register` message reports the pack version (staleness
  surface, never a push gate).

Re-pin:

```bash
git -C ../locveil-voice show wake-pack-vN:contracts/wake-pack/STAMP.json \
  > contracts/pins/wake-pack/STAMP.json
# update PIN.json (version, tag, owner_commit, files sha256s, pin_date), then:
python3 scripts/contract_guard.py --check
```
