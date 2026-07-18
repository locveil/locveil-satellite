# tflm-compat — the FW-2 esp-tflite-micro / IDF-v6.0.2 compat spike

The FW phase's first act (`docs/design/fw_execution_layer.md` E-2): `esp-tflite-micro`
declares `idf >=5.0` but has zero v6 CI and a maintainer-confirmed v6 incompatibility
(upstream issue #125 — "use release/v5.5 for now"), with the known breakage living in
the camera examples we don't use. This harness proves (or disproves) that the parts the
D-9 wake stack actually needs compile and link on **IDF v6.0.2 / esp32s3**:

- the **TFLM core** (interpreter + op resolver + a tiny-model invoke —
  the upstream `hello_world` sine model, Apache-2.0, vendored with provenance),
- the **micro-features frontend** (`tensorflow/lite/experimental/microfrontend` — the
  microWakeWord feature pipeline class: window → FFT → filterbank → log/PCAN).

**Keeper project**: on FW-1 this becomes the wake-stack component's standing build test.
The dependency is pinned exact (`==1.3.7`) and `dependencies.lock` is committed — the
verified-version pin the FW-2 pass outcome records.

Build (the machine wrinkle applies — the custom lzma-less python3 shadows the distro):

    export PATH="/usr/bin:$PATH"
    source ~/esp/v6.0.2/esp-idf/export.sh
    idf.py set-target esp32s3 && idf.py build

Compile-only is the spike's verdict; running on the bench is a bonus check, not the gate.
