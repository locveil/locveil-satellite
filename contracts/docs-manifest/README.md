# docs-manifest — the user-facing docs manifest (internal)

The **repo-internal contract** required by `../locveil-commons/process/user-docs.md` §4.
The artifact stays at its home, `docs/manifest.json` (it lives with what it describes);
this folder holds the STAMP + this pointer README. Schema (commons-owned, one org
vocabulary): `../locveil-commons/process/user-docs/manifest.schema.json`.

Version authority: `STAMP.json` (`docs-manifest-v1`) — bumped **only on a schema
reshape**, never for node edits. Nodes change under the node policy (user-docs.md §4):
additions ride the causing task, removals by tombstone or a filed supersession task;
every completion entry records a docs verdict against the manifest's node ids
(`user-facing-docs-are-done` invariant).

Guard (drift-guard pattern, layer 2): `scripts/check_docs_manifest.py` — manifest shape
vs the schema vocabulary, node↔tree coherence (registered paths exist unless
pending-gate; swept roots carry no unregistered docs), floor classes present,
`derives_from` targets exist, canonical stamps/guards exist. Runs in `hooks/pre-commit`
and the `contract-guard` CI job.
