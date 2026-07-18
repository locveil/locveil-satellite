#!/usr/bin/env python3
"""Model-pack publish flow — hash-at-publish vs the wake-pack STAMP (OPS-7).

Publishes the pinned wake-word pack into the Plane-B model zone
(`/srv/esp32/models/<client_id>/`) with MANDATORY sha256 verification against
`contracts/pins/wake-pack/STAMP.json` — the same hashes the firmware verifies at
flash time (process/contracts.md §4, binary-pack class: hash manifest at publish,
hash verification at load). Runs workstation-side, where the pin lives; the
controller transport is plain ssh/scp. Not privileged — no CA key involved; this
tool stays outside the DES-5 broker by design.

  publish_model_pack.py verify  [--from DIR]
  publish_model_pack.py publish --node ID [--node ID ...]
                                (--dest DIR | --host [user@]HOST)
                                [--from DIR] [--allow-replace] [--srv-dir PATH]

Sources: --from DIR uses local copies of the pack files; without it every file is
fetched from the STAMP's own URLs into a temp dir. Either way nothing is published
until every file's sha256 matches the STAMP.

Replacing an already-published file whose hash differs is REFUSED by default: per
the STAMP, replacing a published model file is a breaking change (flashed devices
verify the old hashes). --allow-replace overrides after you have bumped the pin.
Identical files are skipped (idempotent). Exit 1 on any mismatch or refusal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STAMP = REPO_ROOT / "contracts" / "pins" / "wake-pack" / "STAMP.json"
VALID_ID = re.compile(r"^[A-Za-z0-9_-]+$")  # same untrusted-input rule as the CSR scripts


def freshness_gate(fail_on: str) -> None:
    """Wake-pack pin staleness via the vendored repin tool (HK-12 §5, OPS-13).

    Publishing IS touch-the-family: a publish against a pin the owner has since bumped
    would push bytes the fleet's flash-time verification no longer agrees with — so
    `publish` hard-fails on ANY staleness (including an unreachable tag source: publish
    needs the network anyway). `verify` runs the same check warn-only, keeping offline
    bench runs legal. Closes the publishes-without-committing gap the re-pin flow left.
    """
    r = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "repin.py"),
                        "--check", "--family", "wake-pack", "--fail-on", fail_on],
                       cwd=REPO_ROOT)
    if r.returncode != 0:
        sys.exit("FAIL: wake-pack pin freshness gate — re-pin first "
                 "(scripts/repin.py wake-pack, its own ledger task), then publish")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_stamp() -> dict[str, dict]:
    stamp = json.loads(STAMP.read_text())
    files = stamp["pack"]["files"]
    print(f"stamp: {stamp['contract']} v{stamp['version']} (tag {stamp['tag']}) — "
          f"pack '{stamp['pack']['word']}', {len(files)} file(s)")
    return files


def gather_sources(files: dict[str, dict], from_dir: Path | None, tmp: Path) -> dict[str, Path]:
    """Resolve every STAMP file to a local path — local dir or fetched from the STAMP URLs."""
    sources: dict[str, Path] = {}
    for name, meta in files.items():
        if from_dir is not None:
            src = from_dir / name
            if not src.is_file():
                sys.exit(f"FAIL: {from_dir} has no '{name}' (the STAMP requires it)")
        else:
            src = tmp / name
            print(f"fetch: {meta['url']}")
            with urllib.request.urlopen(meta["url"]) as r, src.open("wb") as out:
                out.write(r.read())
        sources[name] = src
    return sources


def verify_sources(files: dict[str, dict], sources: dict[str, Path]) -> bool:
    ok = True
    for name, meta in files.items():
        actual = sha256(sources[name])
        if actual == meta["sha256"]:
            print(f"  OK   {name}  {actual}")
        else:
            print(f"  FAIL {name}\n       expected {meta['sha256']}\n       actual   {actual}")
            ok = False
    return ok


# ---------------------------------------------------------------- publish targets

class LocalTarget:
    def __init__(self, dest: Path):
        self.dest = dest

    def existing_hashes(self, relpaths: list[str]) -> dict[str, str]:
        return {rp: sha256(self.dest / rp) for rp in relpaths if (self.dest / rp).is_file()}

    def install(self, src: Path, relpath: str) -> None:
        target = self.dest / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(src.read_bytes())

    def __str__(self) -> str:
        return str(self.dest)


class SshTarget:
    def __init__(self, host: str, srv_models: str):
        self.host, self.root = host, srv_models.rstrip("/")

    def existing_hashes(self, relpaths: list[str]) -> dict[str, str]:
        paths = " ".join(shlex.quote(f"{self.root}/{rp}") for rp in relpaths)
        # sha256sum errors on missing files; tolerate — absent is a normal first publish
        out = subprocess.run(["ssh", self.host, f"sha256sum {paths} 2>/dev/null || true"],
                             capture_output=True, text=True, check=True).stdout
        hashes: dict[str, str] = {}
        for line in out.splitlines():
            digest, _, path = line.partition("  ")
            if path.startswith(self.root + "/"):
                hashes[path[len(self.root) + 1:]] = digest.strip()
        return hashes

    def install(self, src: Path, relpath: str) -> None:
        remote = f"{self.root}/{relpath}"
        tmp = f"/tmp/publish_model_pack.{relpath.replace('/', '.')}"
        subprocess.run(["scp", "-q", str(src), f"{self.host}:{tmp}"], check=True)
        subprocess.run(["ssh", self.host,
                        f"install -D -m644 {shlex.quote(tmp)} {shlex.quote(remote)} "
                        f"&& rm -f {shlex.quote(tmp)}"], check=True)
        # re-hash after copy: publish is verified end-to-end, not assumed
        got = self.existing_hashes([relpath]).get(relpath)
        want = sha256(src)
        if got != want:
            sys.exit(f"FAIL: post-copy hash mismatch on {self.host}:{remote} "
                     f"(expected {want}, got {got})")

    def __str__(self) -> str:
        return f"{self.host}:{self.root}"


def publish(files: dict[str, dict], sources: dict[str, Path], nodes: list[str],
            target, allow_replace: bool) -> None:
    relpaths = [f"{node}/{name}" for node in nodes for name in files]
    existing = target.existing_hashes(relpaths)

    refused = []
    for node in nodes:
        for name, meta in files.items():
            rp = f"{node}/{name}"
            if rp in existing and existing[rp] != meta["sha256"] and not allow_replace:
                refused.append((rp, existing[rp]))
    if refused:
        for rp, got in refused:
            print(f"  REFUSE {rp} — published file differs from the STAMP (has {got})")
        sys.exit("FAIL: replacing a published model file is a breaking change "
                 "(flashed devices verify the old hashes) — bump the pin, then --allow-replace")

    for node in nodes:
        for name, meta in files.items():
            rp = f"{node}/{name}"
            if existing.get(rp) == meta["sha256"]:
                print(f"  up-to-date {target}/{rp}")
            else:
                target.install(sources[name], rp)
                print(f"  published  {target}/{rp}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--from", dest="from_dir", type=Path, metavar="DIR",
                        help="use local pack files instead of fetching the STAMP URLs")
    sub.add_parser("verify", parents=[common])
    pub = sub.add_parser("publish", parents=[common])
    pub.add_argument("--node", action="append", required=True, metavar="CLIENT_ID")
    dest = pub.add_mutually_exclusive_group(required=True)
    dest.add_argument("--dest", type=Path, metavar="DIR",
                      help="local models root (testing / staged publish)")
    dest.add_argument("--host", metavar="[USER@]HOST",
                      help="publish over ssh into --srv-dir on the controller")
    pub.add_argument("--srv-dir", default="/srv/esp32/models", metavar="PATH")
    pub.add_argument("--allow-replace", action="store_true")
    args = ap.parse_args()

    if args.cmd == "publish":
        bad = [n for n in args.node if not VALID_ID.match(n)]
        if bad:
            sys.exit(f"FAIL: invalid client_id(s): {', '.join(bad)} (need ^[A-Za-z0-9_-]+$)")

    freshness_gate("any" if args.cmd == "publish" else "none")
    files = load_stamp()
    with tempfile.TemporaryDirectory(prefix="wake-pack.") as tmp:
        sources = gather_sources(files, args.from_dir, Path(tmp))
        print("verify vs STAMP:")
        if not verify_sources(files, sources):
            sys.exit("FAIL: pack does not match the pinned STAMP — nothing published")
        if args.cmd == "publish":
            target = LocalTarget(args.dest) if args.dest else SshTarget(args.host, args.srv_dir)
            publish(files, sources, args.node, target, args.allow_replace)
    print("OK")


if __name__ == "__main__":
    main()
