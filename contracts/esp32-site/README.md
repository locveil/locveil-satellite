# esp32-site — the Plane-B nginx site template (owned)

The **owned contract surface** for the WB7-side fleet-provisioning nginx site. The
artifact stays at its home, `provisioning/ansible/templates/esp32-site.conf.j2` (an
owned-surface-elsewhere per `../locveil-commons/process/contracts.md` §2); this folder
holds the STAMP + this pointer guide. Version authority: `STAMP.json` + its tag
(currently `esp32-site-v1.1.0`). The STAMP's `artifacts` list is the pinned set — the
template alone; this README is an index and how-to, never part of a pin.

**Consumers:** locveil-voice pins the template + STAMP
(`contracts/pins/esp32-site/`) — its ARCH-36 TLS e2e test drives a rendered instance
(the `/ws/` reverse-proxy block, mTLS client-DN header).

**What v1 guarantees** (the surface consumers rely on — every 1.x cut):

- `:8081` (default) public bootstrap: `GET /esp32/provision/ca.crt`,
  `PUT /esp32/provision/pending/`, `GET /esp32/provision/cert/` — human approval is
  the gate;
- `:443` mTLS zone (`ssl_verify_client on`): `GET /esp32/firmware/`,
  `GET /esp32/models/` (static, operator/CI-published), optional `/ws/` reverse proxy
  forwarding `X-Client-Cert-DN` (the verified device identity);
- web-root path mapping: `/esp32/<x>` → `{{ esp32_srv_dir }}/<x>`.

**Owner-side guard** (layer 2, day one): `scripts/check_esp32_site.py` — asserts the
template still carries every guaranteed surface marker above; runs in
`hooks/pre-commit` and the `contract-guard` CI job. The template is byte-locked to the
STAMP's tag (contract-guard CONTENT-DRIFT): **any edit to it is a cut** — STAMP
`version` + `date` and a new three-part tag in the same change. Levels
(`contracts.md` §3): major = a guaranteed surface breaks; minor = the surface or the
pinned set grows; patch = bytes only (a comment, whitespace). Consumers re-pin by
their own ledger tasks (staleness ladder, `contracts.md` §5).

## Changelog (the stamp defines, this narrates)

- **1.1.0** (2026-10-05, OPS-15 — HK-13 / PROD-28): STAMP declares `artifacts` (the
  template only). Template: header comment now names its real path
  (`provisioning/ansible/templates/…`, was `nginx/ansible/templates/…`) — no directive
  changed. Tags are three-part from this cut on.
- **1** (2026-07-12, OPS-3 — PROD-16): first tag; stamped the template as already
  shipped and consumed.
