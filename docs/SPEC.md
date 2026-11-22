# Build Spec — Keyring Camera Rev 2 (Nov 2026)

All prices verified against live LCSC / AliExpress / JLCPCB / Australian retail pages.
**Per-finished-camera: ≈ AU$33–40.** Phase 1 (10 assembled PCBs): ~AU$137–146.

Per-camera cost build-up (10×, AUD):

| Line | Cost |
|---|---|
| PCB fab (live quote, single PCBs) | $0.33 |
| SMT components | $10.10 |
| JLC assembly fees + shipping share | $5.20 |
| Camera module (verified AF AU$8.06, deal-price caveats; wildcard AU$1.64; LilyGo FF AU$18 — rejected for AF) | $8.06 |
| Display | $3.37 |
| Battery (protected, JST) | $5.53 |
| Speaker | $0.56 |
| MicroSD | $5.70 |
| Case filament (home print) | $1.00 |
| **Total per camera** | **≈ AU$40** |

Wildcard path (AU$1.64 AF sample verifies): ≈ AU$33.
Worst case (checkout clamps the deal price): ≈ AU$49.

## Board BOM — soldered by JLCPCB (10×)

Everything JLC **Basic** except three Extended parts (US$3.07 feeder fee each: the only 5MP-capable MCU, the amp, the mic).

| Ref | Part | LCSC # | ≈AU$ @10 | Notes |
|---|---|---|---|---|
| U1 | ESP32-S3FH4R2 (4MB flash + 2MB PSRAM in-package) | C3013940 | 4.71 | 7×7 QFN56, 4,027 stock; larger EPAD than S3R8 (datasheet Fig 7-2) |
| U6 | MAX98357A I2S class-D amp (TQFN) | C910544 | 1.78 | 25.6k stock; WLP variant cheaper but riskier to assemble |
| MK1 | MSM261DGT003 PDM mic | C48227730 | 1.13 | ESP32-S3 reads PDM over I2S natively |
| Y1 | 40MHz crystal | C18214314 | 0.11 | required for the bare chip |
| U3 | TP4054 charger | PREF | 0.12 | unchanged; battery is the protected one |
| U4 | AP2112K-3.3 LDO 600mA | BASIC | 0.19 | replaced XC6206 (200mA < WiFi TX bursts of 240–350mA) |
| Q1 | AO3401A load switch | BASIC | 0.09 | shipping/shelf disconnect; optional-DNP |
| J1 | USB-C (TYPEC-304-BCP16) | C720629 | 0.47 | **top edge** of the board |
| J2 | 24P camera FPC | C883632 | 0.16 | **generic ESP32-CAM DVP map**; pin 24 = AF power |
| J3 | 12P display FPC | C52740844 | 0.16 | 4-wire SPI + backlight |
| J4 | MicroSD slot | C53144700 | 0.23 | right edge, card overhangs ~3.5mm |
| SW1–2 | TS-1187A ×2 | BASIC | 0.09 | shutter + function; SW1 on EXT1 wake |
| — | Passives, flash LED, LED FET | BASIC | 0.55 | all Basic |

JLC Economic Assembly fees (live): setup $8.18 + stencil $1.53 + 3 Extended loader fees $9.21 + hand-solder $3.58 + joints ≈ **AU$42/run**, on $2.10 PCB web-price. First-order coupons kill the PCB bill and clip $10. Watch: QFN X-ray $1.64/pc if enforced. OSP finish (free ENIG ended Jul 2026).

## Plug-in parts

| Part | AU$ @10 | Where & confidence |
|---|---|---|
| OV5640 AF 24P DVP module — click SKU **"21mm 72 Degree AF"** | 8.06 | listing 1005004530278821 (Camera Module Factory Store, 4.9★, 254+ sold), free ship, ~Nov 27–Dec 04 to AU. **Default variant is FF — change it.** "Max 1 pc/shopper at this price": 10x deal rate must be confirmed at checkout; extras may revert to AU$18.26. 21mm/78mm = FPC cable length; 21mm suits the keyring case |
| AF wildcard — listing 1005006789346620, "78mm 72° AF" variant | 1.64 (sample first) | 4.8★, 115 sold; cheap "AF" labels are sometimes fixed-focus — 3–4-unit teardown (~AU$10) settles it |
| 1.14″ ST7789 240×135 | 3.37 | LCSC C2890618 ($2.17@10, 274–344 stock); AliExpress US$1.00–1.60 fallback |
| 402025 LiPo 150mAh, protected, JST | 5.53 | Ecocell AU (273 in stock, 20+ @ AU$5.03+GST); never with the LCSC/PCBA shipment (UN3480) |
| 1511 speaker 8Ω 0.5W | 0.56 | LCSC C530539 ($0.36@10; confirm 3Ω-vs-8Ω spec-field with LCSC chat), cleaner alt C50198758 |
| MicroSD 32GB | 5.70–15 | Toshiba M203 AU$5.70 (CPL) to retail AU$15; brand-name only for gifts |

## PCB design spec — deltas that matter

- **~25 × 26mm, 2-layer, 0.8mm**; r ≈ 3mm corner notch under the keyring post lug. **Order as single PCBs, NOT a panel** (live quote: panel adds ~$37; surcharge avoided is ~$5).
- **RF:** bare chip → meandered inverted-F antenna, top edge, Espressif keep-out; no copper/parts in the zone; battery + SD below the ground pour. HexSense 17.5×30.5mm board is the proportions reference.
- **Edge placement (case-driven):** USB-C top edge centred (case mouth 9.4mm at x −0.5); TF slot right edge; camera FPC top-left with Ø6.4 lens aperture; display FPC behind glass; shutter left wall y 10.4; function right wall y 10.9.
- **Battery bay** = the case's full-length rear strip; speaker fires down through the lid grille.
- **Firmware shapes the board:** deep sleep ~15µA (~260 days idle); double-press EXT1 wake → find-me (chirp + SoftAP); 30-min "am I home" scan (~75µA avg → ~2 months/charge); AF via esp32-camera PR #831 (ov5640_af); PDM mic + MAX98357 audio; games on the 4-key pad + 2 side buttons.

## Phased plan

1. **Now (~AU$137–146):** schematic + footprints (generic 24P map, top-edge USB-C, AF power pin, r3 notch, S3FH4R2 EPAD) → 10 single PCBs, Economic Assembly, coupons on.
2. **Parallel (~AU$10):** 3–4 teardown samples of the AU$1.64 AF variant; VCM click-test + devboard image sweep decides AU$40 vs AU$33.
3. **PCBs arrive (~1–2 wks):** order AF batch (whichever tier won), Ecocell batteries, display + speaker (LCSC), SD cards. All hand-attached — no reflow of plugs.
4. **Anytime:** print case halves (files in `/case`), 0.16mm, face-down, no supports. Firmware flashes over USB-C.

## Ruled out (do not re-litigate)

- MCU-less / IP-cam-SoC (Ingenic-class): proprietary SDK, no AF driver. *The proprietary wall is real.*
- Raw OV5640 die + standalone AF barrel: 3–5× a finished module.
- Espressif S3 modules (WROOM-1 / MINI-1): Economic-Assembly-incompatible at JLC; MINI-1 collides with FPC zones.
- ESP32-C3 cost-down: saves ~AU$3, forfeits PSRAM → 5MP and AF.
- LIR coin cells; bare TFT glass; always-on BLE beacons; OV3660 (no AF in driver); 2MP downgrade (worse version of a buyable product — *"might as well buy a Canon G6"*).
- Arducam 64MP Hawk-eye / IMX258-class sensors: MIPI-only; our board is DVP. A v2 (ESP32-P4 + MIPI) closes that gap — see ROADMAP.
