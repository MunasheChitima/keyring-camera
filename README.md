# Keyring Camera

A custom ESP32-S3 keyring snapshot camera with **true autofocus**, WiFi find-me, audio, games, a private friends gallery, and personalized 3D-printed shells — hand-assembled in a 10-board JLCPCB run by [@MunasheChitima](https://github.com/MunasheChitima). Started as Christmas gifts; the long game is YouTube content, a friends photo-sharing gallery, and a wedding/event camera line.

**Status (Nov 2026):** design + sourcing locked and verified, case files built and validated. Next action: lock the schematic + footprints and place the JLCPCB order (10 assembled boards, ~AU$137–146 with coupons, before the ~1 Dec airmail window).

## What it is

| Spec | Detail |
|---|---|
| MCU | ESP32-S3FH4R2 — 4MB flash + 2MB PSRAM in-package, WiFi + BLE |
| Camera | OV5640 5MP with **true VCM autofocus** (24-pin FPC module, generic ESP32-CAM DVP map) |
| Display | 1.14″ ST7789 240×135 SPI |
| Audio | PDM MEMS mic + MAX98357A I2S amp + 1511 speaker (shutter sound, find-me chirp, voice future) |
| Storage | MicroSD |
| Power | 150mAh protected LiPo (JST), USB-C charge, TP4054, ~15µA deep sleep |
| Extras | Find-me (double-press → chirp + SoftAP), 30-min "am I home" scan, 4-key game pad, open/jailbreakable firmware plan |

Per-finished-camera BOM: **≈ AU$33–40** (wildcard-vs-verified AF module). Everything verified against live LCSC / AliExpress / JLCPCB / AU retail pages Nov 2026.

## Repo layout

- [`docs/SPEC.md`](docs/SPEC.md) — the full build spec (v2): BOM, costs, PCB design deltas, phased plan
- [`docs/SOURCING.md`](docs/SOURCING.md) — verified suppliers, exact product/SKU click lines, caveats, JLCPCB coupon math
- [`docs/POWER.md`](docs/POWER.md) — battery/duty-cycle model for keyring use
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — gifts → video → gallery → weddings; v2 (ESP32-P4 + MIPI) path
- [`hardware/BOM.csv`](hardware/BOM.csv) — board BOM with LCSC part numbers
- [`case/`](case/) — parametric 3D-printable shells (BMO and mini-camera variants), validated STL/STEP, print settings
- [`firmware/`](firmware/) — firmware feature plan (autofocus driver, find-me, gallery upload, AI tiers)
- [`docs/spec-page.html`](docs/spec-page.html) — the styled one-page version of the spec

## License

TBD. Hardware/Case/Firmware licensing will be set on public release (candidate: CERN-OHL-HW for hardware, GPL-3.0 or MIT for firmware, CC-BY-4.0 for docs).
