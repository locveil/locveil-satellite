#!/usr/bin/env python3
"""esp32-site owner-side guard (layer 2, process/contracts.md §4 — OPS-3/PROD-16).

Asserts the owned Plane-B nginx site template still carries every surface marker the
`esp32-site-v1` contract guarantees (contracts/esp32-site/README.md "What v1
guarantees"). A dropped marker means a consumer-visible break — bump the STAMP version
and tag instead of silently editing. Stdlib-only, --check only, exit 1 on any miss.
"""

from __future__ import annotations

import sys
from pathlib import Path

TEMPLATE = Path("provisioning/ansible/templates/esp32-site.conf.j2")

# One marker per guaranteed surface; substring match on the raw template text.
MARKERS = {
    "public CA cert endpoint": "location = /esp32/provision/ca.crt",
    "CSR submission (PUT) zone": "location /esp32/provision/pending/",
    "CSR PUT method": "dav_methods PUT",
    "signed-cert poll zone": "location /esp32/provision/cert/",
    "mTLS client verification": "ssl_verify_client      on",
    "OTA firmware zone": "location /esp32/firmware/",
    "model pack zone": "location /esp32/models/",
    "WS reverse proxy (optional block)": "location /ws/",
    "verified device identity header": "X-Client-Cert-DN $ssl_client_s_dn",
}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    template = root / TEMPLATE
    if not template.is_file():
        print(f"FAIL  esp32-site artifact missing: {TEMPLATE}")
        return 1
    text = template.read_text(encoding="utf-8")
    missing = [f"{name}: {marker!r}" for name, marker in MARKERS.items()
               if marker not in text]
    for m in missing:
        print(f"FAIL  esp32-site marker gone — {m}")
    if missing:
        print(f"\nFAIL: {len(missing)} guaranteed surface(s) missing from {TEMPLATE} "
              "(contracts/esp32-site/README.md — a break needs a version bump, not an edit).")
        return 1
    print(f"OK: esp32-site v1 surface intact ({len(MARKERS)} markers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
