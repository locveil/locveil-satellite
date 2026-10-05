#!/usr/bin/env python3
"""docs-manifest coherence guard (HK-6, process/user-docs.md §4 — drift-guard pattern).

Verifies docs/manifest.json against the org vocabulary and against the tree: registered
paths exist unless pending-gate, swept roots carry no unregistered user-facing docs,
floor classes are staffed, derives_from leaf-truth and canonical stamp/guard targets
exist. Stdlib-only, --check only, exit 1 on any failure.

The vocabulary is NOT mirrored here (HK-13, OPS-18): it is read from the PINNED
commons schema, contracts/pins/docs-manifest-schema/manifest.schema.json — key sets,
enums, the id pattern and the surfaces cap all come from that file, so the checks move
with a re-pin and cannot drift from it. This script is that pin's conformance test
(stdlib has no JSON-Schema validator; the constructs the schema uses are applied by
hand below — a schema reshape that adds a new KIND of rule needs a matching edit here,
made in the re-pin task). docs/manifest.json itself is instance data, not a contract.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import re

MANIFEST = "docs/manifest.json"
SCHEMA = "contracts/pins/docs-manifest-schema/manifest.schema.json"


def load_vocabulary(root: Path) -> dict:
    """The org vocabulary, read from the pinned schema (never restated here)."""
    schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    node = schema["properties"]["nodes"]["items"]
    props = node["properties"]
    return {
        "top_required": set(schema["required"]),
        "top_allowed": set(schema["properties"]),
        "surfaces_max": schema["properties"]["surfaces"]["maxProperties"],
        "node_required": set(node["required"]),
        "node_allowed": set(props),
        "classes": set(props["class"]["enum"]),
        "audiences": set(props["audience"]["items"]["enum"]),
        "statuses": set(props["status"]["enum"]),
        "phases": set(props["phase"]["enum"]),
        "id_re": re.compile(props["id"]["pattern"]),
        "canonical_keys": set(props["canonical"]["required"]),
    }


# Floor (user-docs.md §1, capability-scoped): end-user needs a report pipeline (none
# here), canonical-reference needs a wire surface (esp32-site EXISTS -> required).
FLOOR = {"front-door", "quickstart", "operator", "contributor", "canonical-reference"}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errs: list[str] = []

    try:
        v = load_vocabulary(root)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL  pinned schema {SCHEMA} unreadable or not the expected shape: {exc!r} "
              "(the pin moves only by `scripts/repin.py docs-manifest-schema`)")
        return 1

    try:
        m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL  {MANIFEST} unreadable/unparseable: {exc}")
        return 1

    if not (v["top_required"] <= set(m) <= v["top_allowed"]):
        errs.append(f"top-level keys must include {sorted(v['top_required'])} and stay "
                    f"within {sorted(v['top_allowed'])}, got {sorted(m)}")
    surfaces = m.get("surfaces", {})
    if len(surfaces) > v["surfaces_max"]:
        errs.append(f"surfaces map exceeds {v['surfaces_max']} entries ({len(surfaces)})")

    nodes = m.get("nodes", [])
    if not nodes:
        errs.append("nodes list is empty")
    seen_ids, seen_paths, classes = set(), set(), set()
    for n in nodes:
        nid = n.get("id", "<missing-id>")
        missing = v["node_required"] - set(n)
        if missing:
            errs.append(f"node {nid}: missing {sorted(missing)}")
        unknown = set(n) - v["node_allowed"]
        if unknown:
            errs.append(f"node {nid}: unknown fields {sorted(unknown)} (never invent dialect fields)")
        if not v["id_re"].match(str(nid)):
            errs.append(f"node id {nid!r} violates the id pattern")
        if nid in seen_ids:
            errs.append(f"duplicate node id {nid}")
        seen_ids.add(nid)
        if n.get("class") not in v["classes"]:
            errs.append(f"node {nid}: class {n.get('class')!r} not in the org enum")
        classes.add(n.get("class"))
        aud = n.get("audience", [])
        if not aud or not set(aud) <= v["audiences"]:
            errs.append(f"node {nid}: audience {aud!r} invalid")
        if n.get("status") not in v["statuses"]:
            errs.append(f"node {nid}: status {n.get('status')!r} invalid")
        if "phase" in n and n["phase"] not in v["phases"]:
            errs.append(f"node {nid}: phase {n['phase']!r} invalid")
        for c in n.get("covers", []):
            if c not in surfaces:
                errs.append(f"node {nid}: covers {c!r} not in the surfaces map")
        path = n.get("path", "")
        seen_paths.add(path.rstrip("/"))
        if n.get("status") == "pending-gate":
            if not n.get("gate"):
                errs.append(f"node {nid}: pending-gate without a named gate")
        elif not (root / path).exists():
            errs.append(f"node {nid}: path {path} does not exist (only pending-gate may point at the future)")
        for src in n.get("derives_from", []):
            if not (root / src).exists():
                errs.append(f"node {nid}: derives_from {src} does not exist")
        can = n.get("canonical")
        if can:
            if set(can) != v["canonical_keys"]:
                errs.append(f"node {nid}: canonical needs exactly "
                            f"{'/'.join(sorted(v['canonical_keys']))}")
            for k in ("stamp", "guard"):
                if k in can and not (root / can[k]).exists():
                    errs.append(f"node {nid}: canonical {k} {can[k]} does not exist")

    missing_floor = FLOOR - classes
    if missing_floor:
        errs.append(f"floor classes unstaffed (no node, not even pending-gate): {sorted(missing_floor)}")

    # roots sweep: a user-facing doc committed under a root must be registered
    for r in m.get("roots", []):
        rp = root / r
        candidates = [rp] if rp.is_file() else sorted(rp.rglob("*.md")) if rp.is_dir() else []
        for f in candidates:
            rel = f.relative_to(root).as_posix()
            if rel not in seen_paths and not any(rel.startswith(p + "/") for p in seen_paths if p):
                errs.append(f"unregistered doc under swept root: {rel} (registration IS the manifest edit)")

    for e in errs:
        print(f"FAIL  {e}")
    if errs:
        print(f"\nFAIL: {len(errs)} docs-manifest coherence violation(s) (process/user-docs.md §4).")
        return 1
    print(f"OK: docs manifest coherent ({len(nodes)} nodes, {len(classes & FLOOR)}/{len(FLOOR)} floor classes staffed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
