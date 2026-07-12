#!/usr/bin/env bash
# Bootstrap the gitignored references/ clones (OPS-2; `no-execution-toolchain-at-bootstrap`).
#
# Knowledge-side only: these are READ-ONLY clones for Serena's semantic navigation —
# nothing is installed, built, or imported from here. Idempotent: existing clones are
# updated, not re-cloned.

set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p references

clone_or_update() {
  local url="$1" dir="references/$2"
  if [ -d "$dir/.git" ]; then
    echo "== updating $dir"
    git -C "$dir" pull --ff-only
  else
    echo "== cloning $url -> $dir"
    git clone --depth 1 "$url" "$dir"
  fi
}

# SKiDL — the PCB-description library; Serena navigates this clone (day-one PCB knowledge
# path per HK-4 round 4). Whether skidl-skills joins the toolchain is DES-2's decision.
clone_or_update https://github.com/devbisme/skidl skidl

echo "OK: references/ ready (gitignored; Serena indexes them via the repo project)."
