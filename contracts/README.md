# contracts/ — pinned sibling-owned artifacts

This repo is a **consumer** of three versioned artifacts owned by sibling repos
(`consumer-pins` invariant in `CLAUDE.md`). Each is pinned here by a **one-way inward,
version-stamped sync** from the owner's committed artifact — never hand-edit a pin, never
treat a pin as source, never write into the owning repo. Re-pin on a vN bump and record
the new version here.

| Pin | Owner / source of truth | Status |
|---|---|---|
| **WS wire protocol** | `../locveil-voice/docs/guides/websocket-api.md` (voice `ws-protocol-doc-canonical`) | **Interim** — voice has no version stamp yet (voice ARCH-47 adds it, plus `register` version-reporting). Until then the pin is the doc at the voice commit recorded below; firmware is built against the doc, and the doc wins. |
| **Wake-word pack** | voice's released pack artifact (v2 manifest + `.tflite`, `../locveil-voice/docs/design/wakeword_models.md`) | **Pending firmware** — flash-time pin of the UNMODIFIED artifact, hash-verifiable; pack version reported in `register` (voice ARCH-47). Activates with the first FW task. |
| **Device-integration convention** | the bridge's versioned convention (`device-descriptor.schema.json` + guide; PROD-15 bridge delegation item 2) | **Pending bridge design** — once tagged, the schema is mirrored here and the per-device descriptors under `boards/` must conform (CI check; DES-4). |

Current interim pins:

- `voice-ws-protocol`: `websocket-api.md` @ locveil-voice `98e8fd0` (2026-07-12).
