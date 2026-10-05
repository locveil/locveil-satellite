# docs-manifest-schema — the org docs-manifest vocabulary pin (consumed)

A **pinned, one-way-inward copy** of the commons-owned schema every Locveil repo's
`docs/manifest.json` is written against (`../locveil-commons/process/user-docs.md` §4;
owner surface: commons `contracts/docs-manifest-schema/`). Everything here except this
README and `PIN.json` is the owner's bytes at the tag `PIN.json` records. Never
hand-edit; the pin moves only by a re-pin ledger task running
`python3 scripts/repin.py docs-manifest-schema`.

**Why it is pinned:** this repo's `docs/manifest.json` is instance data — it carries no
STAMP of its own (HK-13; the internal `docs-manifest` contract is retired, its
`docs-manifest-v1` tag stays as frozen history). The contract is the vocabulary, and
holding it here makes the manifest guard hermetic: it runs in the hook and in CI
without a commons checkout.

**Conformance (layer 2):** `scripts/check_docs_manifest.py` — reads the key sets, enums,
id pattern and surfaces cap from `manifest.schema.json` in this folder (no hand mirror)
and applies them to `docs/manifest.json`, then checks the manifest against the tree.
Stdlib has no JSON-Schema validator: a re-pin that brings a new KIND of rule (not just
new enum values or fields) needs a matching edit in that script, in the same task.
