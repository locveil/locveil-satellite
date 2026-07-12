#!/usr/bin/env python3
"""docs-manifest coherence guard (HK-6, process/user-docs.md §4 — drift-guard pattern).

Verifies docs/manifest.json against the org vocabulary (commons
process/user-docs/manifest.schema.json — mirrored here as stdlib checks, no deps) and
against the tree: registered paths exist unless pending-gate, swept roots carry no
unregistered user-facing docs, floor classes are staffed, derives_from leaf-truth and
canonical stamp/guard targets exist. Stdlib-only, --check only, exit 1 on any failure.
Bump contracts/docs-manifest/STAMP.json only when the SCHEMA reshapes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import re

MANIFEST = "docs/manifest.json"
STAMP = "contracts/docs-manifest/STAMP.json"

TOP_KEYS = {"repo", "roots", "surfaces", "nodes"}
NODE_REQUIRED = {"id", "path", "class", "audience", "status"}
NODE_ALLOWED = NODE_REQUIRED | {"covers", "phase", "hw_gated", "gate", "derives_from",
                                "diagram", "canonical", "note"}
CLASSES = {"front-door", "quickstart", "operator", "howto", "narrative", "end-user",
           "canonical-reference", "contributor", "diagram"}
AUDIENCES = {"end-user", "operator", "tester", "integrator", "contributor"}
STATUSES = {"ok", "banner", "pending-gate"}
PHASES = {"DES", "PCB", "FW", "OPS"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9/_-]*$")

# Floor (user-docs.md §1, capability-scoped): end-user needs a report pipeline (none
# here), canonical-reference needs a wire surface (esp32-site EXISTS -> required).
FLOOR = {"front-door", "quickstart", "operator", "contributor", "canonical-reference"}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errs: list[str] = []

    try:
        m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL  {MANIFEST} unreadable/unparseable: {exc}")
        return 1

    if set(m) != TOP_KEYS:
        errs.append(f"top-level keys must be exactly {sorted(TOP_KEYS)}, got {sorted(m)}")
    surfaces = m.get("surfaces", {})
    if len(surfaces) > 10:
        errs.append(f"surfaces map exceeds 10 entries ({len(surfaces)})")

    nodes = m.get("nodes", [])
    if not nodes:
        errs.append("nodes list is empty")
    seen_ids, seen_paths, classes = set(), set(), set()
    for n in nodes:
        nid = n.get("id", "<missing-id>")
        missing = NODE_REQUIRED - set(n)
        if missing:
            errs.append(f"node {nid}: missing {sorted(missing)}")
        unknown = set(n) - NODE_ALLOWED
        if unknown:
            errs.append(f"node {nid}: unknown fields {sorted(unknown)} (never invent dialect fields)")
        if not ID_RE.match(str(nid)):
            errs.append(f"node id {nid!r} violates the id pattern")
        if nid in seen_ids:
            errs.append(f"duplicate node id {nid}")
        seen_ids.add(nid)
        if n.get("class") not in CLASSES:
            errs.append(f"node {nid}: class {n.get('class')!r} not in the org enum")
        classes.add(n.get("class"))
        aud = n.get("audience", [])
        if not aud or not set(aud) <= AUDIENCES:
            errs.append(f"node {nid}: audience {aud!r} invalid")
        if n.get("status") not in STATUSES:
            errs.append(f"node {nid}: status {n.get('status')!r} invalid")
        if "phase" in n and n["phase"] not in PHASES:
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
            if set(can) != {"invariant", "stamp", "guard"}:
                errs.append(f"node {nid}: canonical needs exactly invariant/stamp/guard")
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

    # stamp coherence
    try:
        stamp = json.loads((root / STAMP).read_text(encoding="utf-8"))
        want = f"{stamp.get('contract')}-v{stamp.get('version')}"
        if stamp.get("tag") != want:
            errs.append(f"{STAMP}: tag {stamp.get('tag')!r} != {want!r}")
        if stamp.get("artifact") != MANIFEST:
            errs.append(f"{STAMP}: artifact {stamp.get('artifact')!r} != {MANIFEST!r}")
    except Exception as exc:  # noqa: BLE001
        errs.append(f"{STAMP} unreadable/unparseable: {exc}")

    for e in errs:
        print(f"FAIL  {e}")
    if errs:
        print(f"\nFAIL: {len(errs)} docs-manifest coherence violation(s) (process/user-docs.md §4).")
        return 1
    print(f"OK: docs manifest coherent ({len(nodes)} nodes, {len(classes & FLOOR)}/{len(FLOOR)} floor classes staffed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
