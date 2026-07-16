# locveil-satellite — journal (newest on top)

Dated record of work done; rotates per `ledger-discipline.md` §2 (whole days into
`docs/archive/journal/`, pointer here).

- **2026-07-16 — DES-3 input sharpened: docs-MCP is latest-only; latest = IDF v6.0.2.**
  Owner question ("does the docs MCP only serve the latest IDF? which version is
  that?") answered with verification, folded into the findings doc as §3.5 + the DES-3
  ledger note: the espressif-docs MCP returns `en/latest` docs + `master` source only
  (checked via returned source URLs); latest stable is v6.0.2 (2026-06-29), 5.x ended
  at v5.5.4, Waveshare's 5.3.2 demo is two minors + a major behind but uses the same
  `i2s_std` API family, so it stays a valid wiring reference. Posture recorded for
  DES-3: target v6.0.x after an esp-tflite-micro + SPD2010-components compat check,
  v5.5.x fallback; the vendor demo proves the hardware, never anchors our version —
  the earlier "known-good IDF version anchor" phrasing corrected in the same change.

- **2026-07-16 — DES-7: hardware findings doc committed (enclosure data + vendor
  software survey).** `docs/design/assets/des7-hardware-findings.md`, referenced from
  DES-7 (input evidence) and DES-3 (decision input). Casing verdict: everything CAD
  needs exists — the wiki's structural-diagram RAR holds a dimensioned 2D print
  (39.36×41.53 board, 3× M2.0-H3.5 bosses fully dimensioned, 9.0 mm stack) AND a full
  3D STEP assembly (219 components incl. the mic body and the 12×10×2.8 speaker);
  vendor URLs + sha256s pinned in the doc, files not committed (15 MB). Mic confirmed
  TOP-ported (Waveshare-hosted datasheet + SnapEDA/DFRobot) → the D-7 acoustic channel
  is a gasket-sealed hole over the mic body, no through-PCB port. `waveshareteam`
  survey: the board repo carries a complete NATIVE ESP-IDF 5.3.2 project (SPD2010 +
  PCM5101 + mic capture with the 32-bit/RIGHT-slot wiring truth + TCA9554 reset
  gating + esp-sr wake demo proving the audio pipeline on this exact hardware, factory
  .bin for bench restore) — validates DES-3's native-idf.py option; espressif-maintained
  SPD2010 display+touch registry components exist, so the consumption model is registry
  drivers + own glue, no vendoring of the demo's UNLICENSED code (repo has no license
  file); no 1.46 BSP in Waveshare's components repo yet — watch item.

- **2026-07-16 — DES-7: listening animation decided — variant B "waveform".** Three
  candidates mocked as an interactive page simulating the round 412×412 screen
  (idle/listening states, synthetic speech-amplitude drive; LottieFiles' free tier
  turned out generation-gated, so the mockups were built directly): A pulse rings /
  B waveform / C rim arc. Owner picked **B** — five center-weighted rounded bars driven
  by the capture-frame speech envelope, cyan→violet on black; idle = dim near-static
  dots. Spec folded into DES-7 (b); mockup committed as
  `docs/design/assets/des7-listening-mockup.html` (all three variants kept for the
  record).

- **2026-07-16 — DES-7 scope expanded: µVAD provenance decided (compiled into the app
  image).** Owner question "wake models come from my HF account — what about microVAD on
  ESP32?" surfaced a real hole: D-9 names `pymicro-vad` but neither D-12 nor any
  contracts pin covers the VAD model's on-device provenance/storage. Verified facts:
  the desktop wheel (voice `.venv`, pymicro-vad 2.0.1) embeds the model in the compiled
  extension — no `.tflite` ships; the ESPHome reference distributes the same
  Ahrendt-lineage model as `vad.json`+`vad.tflite` (micro-wake-word-models v2, ~16 KB
  tensor arena). Owner decision folded into DES-7 (b): bake the VAD model into the
  firmware image (vendored third-party source, provenance in the component README) —
  the models partition stays exactly the wake pack, no fourth pin, no publish-flow
  extension; D-10 byte-identity stays wake-model-only; one-time byte-diff vs the wheel's
  model at FW build.

- **2026-07-16 — OPS-10 DONE: scope-guard re-pinned scope-v5 → scope-v6.** Found while
  sweeping the board for delegations and pin drift (result: no pending satellite
  delegations; both contract pins current at their owners' newest tags — `ws-protocol-v1`,
  `wake-pack-v1`; the DES-4 `device-integration-v1.1` request still fires at authoring
  time). scope-v6 = 1.3.0, the UNREFERENCED-evidence check (HK-10/IMPL-2). Vendored from
  the commons tag, toml header bumped, `unreferenced` left at the consumer default (warn).
  Green on first run, 0 warnings — every doc in `docs/design/` + `docs/review/` is
  ledger-referenced.

- **2026-07-16 — DES-7 filed: voice-satellite hardware is the Waveshare
  ESP32-S3-Touch-LCD-1.46B (owner decision).** Owner disclosed 3 units already on the
  desk (bought 2025) — the selection happened outside the repo; the corpus had zero
  mention of the board (exhaustive grep across satellite/voice/commons). Specs verified
  against the Waveshare wiki, official schematic, and demo code: S3R8 8 MB octal PSRAM +
  16 MB flash, single MSM261S4030H0R I2S mic, PCM5101A + NS8002 speaker path, SPD2010
  412×412 round touch LCD, Li-ion/USB-C. Fit against `esp32_satellite.md`: every v1
  requirement is met (mic class D-5, separate-I2S topology D-8, wake-pack flash
  partition D-12, OTA A/B). Two design tensions became DES-7 scope instead of blockers:
  D-2's "headless" amends to "display support OPTIONAL in firmware" (owner wants a
  minimal listening animation as a nice-to-have — the Siri-like idea, not Siri's UI),
  and the §14 v2 ES8311/AEC/2-mic path is CLOSED on this hardware (v2 = new hardware).
  Voice-satellite PCB phase collapses to none; FW-1's `HW-GATED` hardware-selection
  reason lifts once DES-7 lands (FW still gated on DES-3).

- **2026-07-15 — OPS-9 DONE: the PROD-25 one-liner was a dud — explicit tag fetch.**
  Watched OPS-8's pushed run instead of trusting it: FAILED, same 2× TAG-MISSING.
  `fetch-tags: true` is a no-op on checkout's default shallow single-commit fetch
  (actions/checkout#1467 — the flag only drops `--no-tags`; auto-following can't see
  tags on unfetched commits). The OPS-8 repro had passed because `clone --no-tags`
  isn't checkout's real fetch shape — this time reproduced from the EXACT state
  (init + single-sha depth-1 fetch) before trusting the fix. Fix: explicit
  `git fetch --tags --depth=1 origin` step; green locally from the exact state; the
  pushed run is monitored and its verdict lands in the board write-back.
  Blast radius filed back to PROD-25: commons' own post-fix run dd7c270
  failed identically (convention §4 prescribes the dead one-liner; commons workflow
  still broken), voice BUILD-38 was verified by simulation only.

- **2026-07-15 — OPS-8 DONE: contract-guard CI checkout fetches tags (PROD-25).**
  The v2 `TAG-MISSING` rule reads `git tag -l`, but `actions/checkout` defaults to a
  tag-less shallow clone — since OPS-5 re-vendored v2, this repo's guard job was
  latently broken: the next `contracts/**` push would have fired 2× false TAG-MISSING
  (`esp32-site-v1`, `docs-manifest-v1`), nothing wrong in the contracts. One-line fix
  per `process/contracts.md` §4: `fetch-tags: true` on the checkout (shallow stays
  fine). Both sides reproduced locally: tag-less clone fails exactly as CI would, tags
  make it green. Board text reconciled at intake — its "rides the v2 re-pin" framing
  was stale for satellite (re-pin already done); fix landed standalone. Stale v1 header
  comment in the workflow fixed in the same change. OPS-8 written back to PROD-25.

- **2026-07-14 — OPS-7 DONE: model-pack publish flow — hash-at-publish is machinery now.**
  `scripts/publish_model_pack.py` (stdlib-only, workstation-side — publish from where
  the pin lives; ssh/scp transport; outside the DES-5 broker, no CA key involved).
  Nothing lands in `/srv/esp32/models/<client_id>/` unless every file's sha256 matches
  `contracts/pins/wake-pack/STAMP.json`; drift on already-published files is refused
  (breaking change per the STAMP — pin bump then `--allow-replace`); re-runs idempotent;
  remote copies re-hashed post-copy. Verified live against the HF upstream (both hashes
  green) + the full local failure matrix; the ssh branch mirrors the local one and is
  untested until a controller session — recorded honestly in the DONE entry. README
  publish section rewritten around the tool (kept user-grade, no tracking refs — the
  OPS-4 rule); firmware publishing stays plain copies under dormant OPS-1. Sprint-01's
  0.3-session satellite row is thereby executed. docs: provisioning-runbook.
- **2026-07-14 — sprint-01 intake: OPS-1 split, OPS-7 filed (model-pack publish flow;
  the sprint row's "OPS-1a" renumbered).** The sprint-01 satellite row pulled
  (`../locveil-commons/board/sprints/sprint-01.md`, §4 partial-dependency split).
  Intake wrinkle, caught by the guard's own count: the coordinator pre-named the split
  half "OPS-1a", but scope-guard's declaration regex is numeric-only (`(PFX)-\d+\b`) —
  a letter-suffixed row parses as PROSE, invisible to ledger enforcement (it landed
  that way in `a181f5d` for ~one commit; the aliases table is numeric-only too, so no
  alias escape). Renumbered to **OPS-7** with the sprint-row name recorded in the task
  text. UPSTREAM FINDING to report to commons: sprints.md §4 says splits need "no new
  syntax", but the sprint machinery minted letter-suffix IDs its own guard can't parse —
  either §4 forbids them explicitly or scope-guard learns them; commons' call.
  Reconciled clean otherwise: the zero-dependency claim holds (pin `wake-pack-v1` +
  upstream HF artifacts + deployed `/srv/esp32/models/` layout; no FW/bench/hardware
  needed). OPS-7 takes the PROD-16 hash-at-publish amendment wholesale; OPS-1 narrows
  to the firmware half, dormant until FW-1 produces an image. Sprint side-finds disposition:
  the D-17/workbench-panel reconciliation was already discharged by the PROD-24 DES-5
  expansion (same day, `44d7646`); the DES-4 `device-integration-v1.1` wrinkle was
  already recorded at OPS-3 intake; the `process/sprints.md` §6 vacuous-line finding is
  a commons doc finding — becomes scope only if DES-3 is selected in a future sprint.

- **2026-07-14 — PROD-24 delegation pulled: DES-5 expanded (broker + verbs + operator
  credential), OPS-6 ansible earmark filed.** The Workbench shell council's satellite
  delegation: DES-5 (cert lifecycle) absorbs the privileged broker — one privileged code
  path, two peer clients (`esp32-provision` CLI + the workbench provisioning page); the
  owner overruled D-17's CLI-only reading (CA-key boundary survives, the SSH-only gate
  does not — D-17's second amendment lands via the expanded design), plus the full verb
  vocabulary (`list/status/approve/reject-pending` now, `revoke-issued/renew` from DES-5's
  original core) and the workstation operator-credential question (home-CA client cert vs
  separate secret). Reconciled clean: `provisioning/README.md` verbs match (today's
  `revoke` = the board's `reject-pending` — drop-pending only, exactly the gap DES-5 was
  filed on), D-17 already carried the "config-ui may call the same scripts later" hook,
  `provisioning/ansible/deploy.yml` exists as the OPS-6 target. OPS-6 filed as an EARMARK
  (owner: not this sprint; blocked on DES-5 by definition). Binding conditions recorded in
  the ledger: no write API before PROD-4's auth decision; the workbench page stays dormant
  until DES-5 + first light. IDs written back into the board's PROD-24 entry (commons
  commit). Normative source: `../locveil-commons/docs/design/workbench.md` §6.
- **2026-07-14 — OPS-5: contract-guard re-vendored @ v2 (PROD-22) — TAG-MISSING fired here too.** Third instance org-wide of the STAMP-names-a-nonexistent-tag false green; docs-manifest-v1 created at the STAMP's landing commit. Executed by the commons session on owner instruction; satellite added to the PROD-22 delegation list at execution (the original named bridge+voice only).
## 2026-07-12 — PROD-17 delegation pulled: user-docs convention adopted (OPS-4 filed + executed)

Unattended session, same pattern as OPS-3. All three delegation items under one ID:
the docs manifest born (`docs/manifest.json`, 7 nodes, `docs-manifest-v1` INTERNAL
stamp, coherence guard as pre-commit stage 4 + CI step), `CONTRIBUTING.md` created,
the provisioning-README user-grade pass done, scope-guard re-pinned `scope-v5`
(1.2.0, docs-verdict rule + the new shared-invariants block). Reconciliation notes:
the FW/PCB-gated doc classes went in as **pending-gate nodes** naming their gates
(`FW-1 first light`; deck builds gate on the first bench-verified board and
`derives_from` the `docs/devices/` dossiers) — declared, not written; the
canonical-reference floor slot is staffed by OPS-3's `esp32-site` surface (stamp +
guard already existed — the two delegations composed cleanly). Discovered-and-fixed
in the pass: the publish example still said `jarvis.*` (the pack is `irina`), and the
root README pointed users at the ledger. `docs_verdict_since` set to **2026-07-13**,
not today: the four completions dated 2026-07-12 predate the rule and DONE is frozen
history — the OPS-4 entry carries a voluntary verdict line anyway as the format
exemplar. Upstream nit reported in the board write-back: the commons skeleton
manifest's `$comment` key fails its own schema (`additionalProperties: false`).

## 2026-07-12 — PROD-16 delegation pulled: the contracts pins-shape cut (OPS-3 filed + executed; DES-4/OPS-1 amended)

Unattended session (owner approved the analysis, stepped away). Pulled the PROD-16
satellite delegation from the board; `task-start-reconciliation` produced four deltas
that reshaped execution: **(1)** `ws-protocol-v1` + `wake-pack-v1` were ALREADY tagged
(voice ARCH-47 executed the same afternoon, voice `9f371b9`) — the delegation's interim
"unstamped PIN.json now, stamp later" step collapsed; both pins landed stamped and
strict, and the WS doc had moved +17/−3 since our interim commit-ref pin (`98e8fd0`), so
the re-pin at the tag was substantive, not cosmetic. **(2)** `contracts/README.md` was
stale in all three rows, not just the one line the delegation named — replaced wholesale
by the §2 registry. **(3)** A reconciliation DISCOVERY: this repo OWNS a contract nobody
delegated — voice's registry pins our Plane-B nginx template (`esp32-site`, pre-tag
@ `37dcac5`, "version/tag fill in when the satellite stamps this surface") — stood the
owned surface up: STAMP + pointer README + tag `esp32-site-v1` (byte-identical to
voice's copy, verified) + day-one owner guard `scripts/check_esp32_site.py`; the
template's stale comment path (`nginx/` vs `provisioning/`) stays as recorded debt —
fixing a comment is a byte change is a version bump. **(4)** The bridge's
`device-integration-v1` tag carries the PRE-convention STAMP (core fix landed post-tag,
`eb08146`/VWB-41, no bump) — recorded as a DES-4 intake wrinkle with the preferred
`v1.1` repo-to-repo request; deliberately NOT filed into the bridge tonight (their
ledger, their session). Enforcement: `contract_guard.py` vendored @ `contract-guard-v1`,
CI job + three-stage pre-commit; both guards green, **0 warnings**. Ledger: OPS-3
straight to DONE (the DES-6 filed+executed pattern); DES-4 + OPS-1 amended in place;
IDs written back into the board's PROD-16 entry (commons commit).

## 2026-07-12 — cross-repo-board block re-pinned @ scope-v4 (PROD-15 close follow-through)

The shared block now names this repo (`../locveil-satellite`) as the fourth sibling; block
text between the markers + the `.scope-guard.toml` hash updated from the commons source per
the `process/claude-md.md` §3 flow (mechanical re-pin, no other content change —
journal-line only, no ledger task). PROD-15 closed on the board the same day.

## 2026-07-12 — deck corpus harmonized, docs/devices/ layer born (DES-1)

Interactive session. Owner decisions: three-layer doc taxonomy (architecture/ =
narratives, design/ = decisions, **devices/ = per-device hardware ground truth** — the
voice satellite gets its own dossier there at PCB phase); slugs **revox-a77 / revox-b215
/ pioneer-cld925 / panasonic-fs90** (fix the `[dev:]` tags + future `boards/<slug>/`);
trim to engineering truth; imports deleted in this close. Landed: `docs/devices/`
(deck-common + 4 dossiers + img/), `docs/review/des1-truth-pass.md`. Merge headline:
build docs won 7/8 direct conflicts (B215 "RS-232 vs TTL" dissolved — it's open-collector
Serie I/O; A77 "switch common" model was wrong — pin PAIRS), but the FS90
**rail-isolation check went the other way** — the newer build doc had dropped the
research pass's non-negotiable safety gate; reinstated. Code sweep: zero unique bench
truth (placeholders throughout); GPIO14 triple-booked across three drivers — the
concrete `per-device-apps` evidence, now recorded in deck-common §5. Pin re-audit vs
Espressif docs: no legacy pin sits on a strapping pin; GPIO14=MTMS noted.
`imports/bridge-esp32/` deleted (absorbed; import commit `0d950a9` keeps it resolvable);
bridge VWB-38 note filed repo-to-repo (wb-mqtt-v1 promotion source → the truth pass §2).
Owner verdict on the imported code recorded: reference-only, docs were the value.

## 2026-07-12 — day-one toolchain wired (OPS-2)

Root `.mcp.json` (the single MCP config, per HK-4 round 4): `pcbparts` + `espressif-docs`
+ `esp-component-registry` (all HTTP; docs server needs a one-time GitHub OAuth via `/mcp`
— a 401 before that is expected, and it's rate-limited 40/h · 200/day per user) + `serena`
(stdio via `uvx`, project-from-cwd). `scripts/bootstrap_references.sh` clones SKiDL into
gitignored `references/` for Serena — run today, clone verified, gitignore holds; pcbparts
and the registry answered 200 to an MCP initialize probe. Per-phase nested CLAUDE.md
landed: `docs/design/` (DES), `boards/` (PCB), `components/` (FW) — each states its
`phase-gates` gate + MCP set. Deliberately absent (`no-execution-toolchain-at-bootstrap`):
PlatformIO (DES-3), skidl-skills (DES-2), and the ESP-IDF *Tools* MCP (build/flash —
execution-side, rides DES-3; noted in `components/CLAUDE.md` so nobody wires it early).

## 2026-07-12 — bridge ESP32/ tree imported (DES-6; PROD-15 bridge delegation item 1b)

Board-intake reconciliation found the one delegated action without a local ID: the bridge's
frozen `ESP32/` deck-bridge scaffold awaited a satellite-side pull (bridge DRV-35 BLOCKED on
our confirmation). Filed **DES-6**, executed same session: 34 git-tracked files @ bridge
`a80322f` → `imports/bridge-esp32/`, verbatim (rules + provenance: `imports/README.md`).
Value is the *facts*, not the architecture — the bench-confirmed `docs/wb-*.md` build docs
are DES-1's leaf truth, `REQUIREMENTS.md` feeds its truth pass (and bridge VWB-38's
wb-mqtt-v1 promotion), `src/` is FW-phase component material; the single-image FR-1 shape
stays retired (`per-device-apps`). Confirmation written into bridge DRV-35 (repo-to-repo
filing) so its delete + DRV-7 retirement can proceed.

## 2026-07-12 — design corpus + provisioning plane imported from locveil-voice (BUILD-22)

Plain moves, frozen history stays in voice (`git -C ../locveil-voice log --follow` for
pre-move history). Landed: `docs/design/esp32_satellite.md` (the authoritative ARCH-22
consolidated design; §4.1–4.3 wire tables demoted to a pointer at voice's
`websocket-api.md` + the `contracts/` pin, per the PROD-15 delegation),
`docs/design/ws_esp32_transport.md` (superseded lineage, frozen),
`docs/architecture/esp32.md` + `docs/images/esp32-{fit,turn}.{dot,png}` (cross-repo links
re-pointed), and the **Plane-B fleet-provisioning tree** voice `nginx/` → `provisioning/`
(D-6-as-amended; ansible playbook + CA/provisioning scripts + nginx site template; the
operator-local `inventory.ini`/`group_vars/all.yml` copied on disk and gitignored here —
the WB7 deployment itself is untouched, this is a repo-side handover). Voice keeps a
pinned copy of `esp32-site.conf.j2` for its TLS-e2e test (its tether; re-pin direction is
voice-pulls-from-here). Imported tasks: **DES-5** (ex voice ARCH-44, cert lifecycle) +
**FW-1** (ex voice ARCH-23, firmware build — reconcile at start, HK-4 amendments noted
inline). Interim WS-protocol pin recorded in `contracts/README.md`.

## 2026-07-12 — repo bootstrapped from process/new-repo-template

Instantiated by voice **BUILD-22** (board **PROD-15**, council HK-4) from
`../locveil-commons/process/new-repo-template/` at **scope-v3** — CLAUDE.md with the two
pinned shared blocks + the repo-local LAW (esp32-only-charter, phase-gates, hw-gated,
per-device-tags, per-device-apps, consumer-pins, no-execution-toolchain-at-bootstrap),
ledger triad, vendored `scripts/scope_guard.py` @ scope-v3, pre-commit hook
(`core.hooksPath hooks`), `ledger-guard` CI. Skeleton directories: `components/`,
`boards/`, `provisioning/`, `contracts/`. Born backlog DES-1..DES-4 + OPS-1..OPS-2 seeded
from the PROD-15 entry. No deviations from the template.
