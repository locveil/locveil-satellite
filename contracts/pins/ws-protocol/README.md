# ws-protocol — the voice WS wire protocol pin (consumed)

A **pinned, one-way-inward copy** of the voice-owned WS wire protocol
(`consumer-pins` invariant; voice `ws-protocol-doc-canonical`). Voice is the source of
truth: the guide `docs/guides/websocket-api.md`, stamped under voice
`contracts/ws-protocol/`. **The doc wins, firmware adapts.**

Everything in this folder except this README and `PIN.json` is the owner's bytes — the
set voice's STAMP enumerates at the tag `PIN.json` records, plus that STAMP. Never
hand-edit; the pin moves only by a re-pin ledger task running
`python3 scripts/repin.py ws-protocol`.

**Why it is pinned:** the firmware is built against this document — register → PCM →
end, the reply channel `speak_begin`/PCM/`speak_end`, `protocol_version` in every
`registered` ack. When voice's machine core lands in the pinned set (golden frames,
transcripts, schema — subordinate to the document), the firmware's conformance test
reads those fixtures from here.

**Conformance (layer 2):** not written yet — it is FW-1a's deliverable. Until then
`PIN.json` carries no `conformance` pointer and contract-guard warns
`PIN-NO-CONFORMANCE`; FW-1a adds the test and its path in `.repin.toml` together.

**Staleness:** `scripts/repin.py --check` (hook: warn; CI: touching this folder while
the pin trails fails). At runtime the satellite's `register` message reports
`protocol_version` — the protocol's major — and voice compares (voice ARCH-48).
