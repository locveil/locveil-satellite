# ws-protocol — the voice WS wire protocol pin (consumed)

A **pinned, one-way-inward copy** of the voice-owned WS wire protocol
(`consumer-pins` invariant; voice `ws-protocol-doc-canonical`). Voice is the source of
truth: artifact `docs/guides/websocket-api.md`, stamped under voice
`contracts/ws-protocol/` (tag `ws-protocol-v1`). **The doc wins, firmware adapts.**
Never hand-edit any file here — re-pin on a vN bump.

| File | Origin | What it is |
|---|---|---|
| `websocket-api.md` | voice (byte-identical @ `ws-protocol-v1`) | The wire protocol: register → PCM → end; reply channel `speak_begin`/PCM/`speak_end`; `protocol_version` in every `registered` ack |
| `STAMP.json` | voice (byte-identical) | The owner's version stamp (code constant: voice `irene/core/ws_protocol.py::WS_PROTOCOL_VERSION`) |
| `PIN.json` | **satellite-stamped** | The pin record: tag/commit, file hashes, conformance pointer |

Conformance (layer 2): pending FW-1 — no firmware exists yet (`phase-gates`: FW opens
after DES-3). Until then the pinned doc is the build contract; the FW-1 conformance
test binds the firmware's register/stream/reply handling to this pin when it lands.
Staleness (never a push gate): the satellite `register` message reports
`protocol_version`; voice compares (voice ARCH-48).

Re-pin:

```bash
git -C ../locveil-voice show ws-protocol-vN:docs/guides/websocket-api.md \
  > contracts/pins/ws-protocol/websocket-api.md
git -C ../locveil-voice show ws-protocol-vN:contracts/ws-protocol/STAMP.json \
  > contracts/pins/ws-protocol/STAMP.json
# update PIN.json (version, tag, owner_commit, files sha256s, pin_date), then:
python3 scripts/contract_guard.py --check
```
