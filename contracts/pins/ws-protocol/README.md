# ws-protocol — the voice WS wire protocol pin (consumed)

A **pinned, one-way-inward copy** of the voice-owned WS wire protocol
(`consumer-pins` invariant; voice `ws-protocol-doc-canonical`). Voice is the source of
truth: the guide `docs/guides/websocket-api.md` and, beside it, the hand-written machine
core under voice `contracts/ws-protocol/`. **The doc wins, firmware adapts.**

Everything in this folder except this README and `PIN.json` is the owner's bytes — the
set voice's STAMP enumerates at the tag `PIN.json` records, plus that STAMP, copied flat.
Never hand-edit; the pin moves only by a re-pin ledger task running
`python3 scripts/repin.py ws-protocol`.

## What the pin holds

| File(s) | What it is |
|---|---|
| `websocket-api.md` | **the protocol.** Register → PCM → end; the reply channel `speak_begin`/PCM/`speak_end`; `protocol_version` in every `registered` ack. Its section "The machine-readable core" is the ONLY description of the files below that firmware may rely on |
| `frames.golden.json` | every JSON frame of the four channels as data: keys, JSON types, and cases with a verdict (`valid` — must accept; `invalid` — may reject, must not fault), plus `unknown` frame types (must ignore) and `malformed` text (must survive) |
| `transcript.*.jsonl` | nine recorded scenarios, one JSON object per line, order binding per connection and direction |
| `ws-protocol.schema.json` | the frame reference as a JSON Schema — for host-side tools; the least of the three |
| `STAMP.json` | the owner's version stamp, verbatim |

The core is **subordinate to the document**: where a file disagrees with the guide, the
guide is right and the file has a bug — report it to voice, never patch it here.

## How the firmware uses it (FW-1a)

FW-1a builds its conformance test as a **data-driven table** over this folder:

- `frames.golden.json` — the satellite's two channels (`audio`, `reply`): every `valid`
  server frame is accepted (including each `<frame>/unknown-field` case), every
  `unknown` type is ignored with the connection kept, every `malformed` text is
  survived, no `invalid` case faults; the frames the firmware SENDS match the `valid`
  client-frame shapes (the server refuses an opening frame whose keys have the wrong
  JSON type); a case marked `"retired": true` is SKIPPED — it states nothing any more,
  whatever its `verdict` says;
- four transcripts replayed against the session state machine: `audio-batch`,
  `reply-burst`, `satellite-pair`, `reconnect`, with the guide's transcript rules (T-1
  onward — the list grows by minor releases) applied.

The other five transcripts and the `output` / `observe` frames describe channels and
modes the satellite does not use; they are pinned because a pin is always the owner's
complete set. Names here (files, frames, case ids, transcripts) are stable for the
whole of major 1 and safe to turn into generated identifiers; retired cases are marked,
never removed — which is why the harness must read the mark.

**Conformance (layer 2):** not written yet — it is FW-1a's deliverable. Until then
`PIN.json` carries no `conformance` pointer and contract-guard warns
`PIN-NO-CONFORMANCE`; FW-1a adds the test and its path in `.repin.toml` together.

**Staleness:** `scripts/repin.py --check` (hook: warn; CI: touching this folder while
the pin trails fails). At runtime the satellite's `register` message reports
`protocol_version` — the protocol's major — and voice compares (voice ARCH-48).
