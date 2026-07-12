# esp32-site — the Plane-B nginx site template (owned)

The **owned contract surface** for the WB7-side fleet-provisioning nginx site. The
artifact stays at its home, `provisioning/ansible/templates/esp32-site.conf.j2` (an
owned-surface-elsewhere per `../locveil-commons/process/contracts.md` §2); this folder
holds the STAMP + this pointer guide. Version authority: `STAMP.json` + tag
`esp32-site-v1`.

**Consumers:** locveil-voice pins the template
(`contracts/pins/esp32-site/`) — its ARCH-36 TLS e2e test drives a rendered instance
(the `/ws/` reverse-proxy block, mTLS client-DN header). Voice pinned pre-tag
(@ `37dcac5`, byte-identical to `esp32-site-v1`); its PIN.json fills version/tag at its
next re-pin.

**What v1 guarantees** (the surface consumers rely on):

- `:8081` (default) public bootstrap: `GET /esp32/provision/ca.crt`,
  `PUT /esp32/provision/pending/`, `GET /esp32/provision/cert/` — human approval is
  the gate;
- `:443` mTLS zone (`ssl_verify_client on`): `GET /esp32/firmware/`,
  `GET /esp32/models/` (static, operator/CI-published), optional `/ws/` reverse proxy
  forwarding `X-Client-Cert-DN` (the verified device identity);
- web-root path mapping: `/esp32/<x>` → `{{ esp32_srv_dir }}/<x>`.

**Owner-side guard** (layer 2, day one): `scripts/check_esp32_site.py` — asserts the
template still carries every guaranteed surface marker above; runs in
`hooks/pre-commit` and the `contract-guard` CI job. Changing the template =
a version bump here (STAMP `version`/`date` + new tag) — consumers re-pin on their
own cadence (staleness is never a push gate).

Known cosmetic nit (recorded, NOT fixed in v1 — any byte change would be a bump for a
comment): the template's header comment says `nginx/ansible/templates/…`; the real
path is `provisioning/ansible/templates/…`. Fold the fix into the next real bump.
