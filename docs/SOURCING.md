# Sourcing Notes — verified Nov 2026

Everything here was verified against live pages (LCSC price ladders, AliExpress SKU matrices rendered in a real browser, JLCPCB fee pages + cart quote tool, AU retail). Anything listed as caveats was a live page observation, not an assumption.

## Camera modules (the decisive line)

**Buy line: listing 1005004530278821** — seller "Camera Module Factory Store" (4.9★, 254+ sold).

1. The page **defaults to "21mm 66 Degree" at AU$1.70 — fixed focus. Change the SKU.**
2. Selected SKU: **"21mm 72 Degree AF"** → AU$8.06 each. 10× = AU$80.60, minus the AU$4-off-AU$20 coupon ≈ **AU$76.60 (~AU$7.66/module)** — cheapest verified AF source found.
3. Caveats: AF SKUs carry **"Max 1 pc/shopper at this price"** — the 10-unit deal rate must be confirmed at checkout; extras may revert to AU$18.26 (blended worst case ≈ AU$17 → ~AU$49/camera).
4. "21mm"/"78mm"/"15CM" are **FPC cable lengths**, not focal lengths. 21mm likely fits the keyring case; verify against the case's camera bay before ordering.
5. Delivery estimate: ~Nov 27 – Dec 04 to AU. Same-seller AF anchor as of 18 Nov was AU$10.91 ("78mm 72 Degree AF") — the 21mm SKU is the same AF class, cheaper.

**AF wildcard:** listing 1005006789346620 — "78mm 72° AF"-labelled variant at **AU$1.64** (4.8★, 115 sold). Cheap "AF" labels are sometimes fixed-focus: order **3–4 teardown samples (~AU$10)**, run the VCM click-test + a devboard image sweep through esp32-camera before committing the batch.

**Fixed-focus fallback (rejected for the flagship, kept as plan-B):** LilyGo US$11.90 (~AU$18) 5MP FF OV5640 24P, lilygo.cc item "Regular/Fisheye Lens Camera" (the famous "$2.80" was the 2MP OV2640 — corrected twice, do not trust that number).

**Rejected listings, for the record:**
- 1005007480635043: OV5640 100–200° ultra-wide line — no AF SKU exists, connector unpublished, AU shipping unconfirmed. Only relevant later as a novelty third module.
- Seeed 114993115 (OV5640 AF for XIAO): genuinely reputable, AU$23.25@10 at Core Electronics — but wired to the XIAO pinout (pin 24 = 2.8V analog, not the generic map) and ~3× the price. Its existence is the reason we locked the **generic 24P DVP map**: it keeps the whole cheap tier attachable.
- SincereFirst / cameramodule.com (Guangzhou factory, SGS-audited): has SF4V564085AFBY-ESP (OV5640 AF, 24-pin gold-finger DVP, "ESP32 compatible") plus a 150° ultra-wide FF OV5640 and a full custom-module intake (sensor+lens+FOV+IR+FPC). **Quote-only, no published pinouts/MOQ** — a Phase-2 supplier for volume (100+ units) and custom-FOV wedding modules, not the Christmas order. Their "ESP32 compatible" claim needs a pinout PDF matched against the generic map before any module touches our board.
- Arducam OV5640 AF (B0158): 20-pin 2.54mm ArduCAM pinout, NOT 24P-compatible.
- IADIY DCM5M120M7F2: real AF 24P, $16@10, 14–21 day lead — too slow for the deadline.
- JoyPicks AF: marketplace-tier trust, inconsistent specs.
- JLCPCB parts library: no orderable 24P camera module; bare OV5640 BGA exists (C2844952, X-ray required) — not practical.

## Board parts

| Part | Source | Price | Verified |
|---|---|---|---|
| ESP32-S3FH4R2 | LCSC C3013940 | $3.04@10 USD, 4,027 stock | ✅ live |
| MAX98357AETE+T | LCSC C910544 | $1.15@10, 25.6k stock | ✅ live |
| MSM261DGT003 PDM mic | LCSC C48227730 | $0.73@10 | ✅ live |
| 1.14″ ST7789 display | LCSC C2890618 | $2.17@10 | ✅ live (274–344 stock; re-check at order) |
| 1511 speaker 8Ω | LCSC C530539 | $0.36@10 | ✅ live — **confirm 3Ω-vs-8Ω spec-field clash with LCSC chat**; alt C50198758 |
| 402025 150mAh LiPo protected JST | Ecocell AU ecocell.com.au | AU$5.03+GST @10, 273 stock | ✅ live |
| MicroSD 32GB | Toshiba M203 AU$5.70 (CPL) → retail AU$15 | brand-name only | estimate |
| Batteries via LCSC | IMPOSSIBLE — UN3480 dangerous goods | — | ✅ confirmed policy |

Old BOM's "W25Q128 16MB at $0.62" (C49211308) was wrong — that LCSC code is a TDSEMIC clone at $2.24@10; external flash dropped entirely (in-package flash).

## JLCPCB discounts (live check Nov 2026)

| Discount | Amount | Condition |
|---|---|---|
| New-user PCB coupon | $6 | auto on signup, min $2 |
| New-user SMT coupon | $10 | auto |
| New-user stencil coupon | $7 | auto; same-order applicability unverified |
| New-user shipping coupon | $10 | **bills ≥ $15 → express only** |
| Monthly PCBA coupons (all users) | $6 + $9 | auto each month; **lapse 30 Nov** (fresh set Dec 1) |
| Monthly $10 PCBA coupon | $10 | requires EasyEDA files — dead for KiCad users |
| "No Setup Fee" banner | up to $8.18 | Economic applicability only provable at checkout |
| Web-price PCB discount | ~$2 | automatic |
| App instant-checkout | $1–20 random | desktop app; only documented stacking exception |

**Stacking rule (JLC article, Nov 16 2026): one coupon per order batch.** Historically a PCB coupon lands on the PCB segment and an SMT coupon on the assembly segment — assume one; the checkout page is final. Unused coupon value is forfeited.

## Phase-1 JLC order (10 boards)

- PCB: **$2.10** web price (single PCBs — do NOT panelize: live quote showed +$37 for a 4-across panel)
- SMT components: ~$65
- Fees: setup $8.18 + stencil $1.53 + 3 Extended $9.21 + hand-solder $3.58 + joints ≈ $27.30
- Shipping: airmail ~$6–9 (15–25 days → order by ~Dec 1) or UPS ~$26 ($10 coupon applies there)
- **First order with coupons: ~$88–94 (~AU$137–146)**; if the No-Setup-Fee promo fires: ~$80–84 (~AU$124–130)
- Watch at checkout: QFN X-ray $1.64/pc if enforced
- Signup package: register first, read **My Coupons** — issuance is region/payment-dependent; core $6/$10/$7/$10 pieces confirmed both ways

## Comparison camera (RewindPix PS135, for the eventual video positioning)

Sony IMX258 (13MP→10.7MP, 1.12µm, 1/3.06″, **fixed focus**), Novatek NT96565 action-cam SoC, stock OEM mainboard (X94-MB-V1.1, closed NVTIPC firmware), A$210 retail (A$301 alloy), 8,170+ Kickstarter backers, ~$1.37M. No AF, no display, no audio, no sharing, no AI. We are not competing with it — it validates the non-phone camera market and leaves our lane (shareable, personalized, AF, open) empty. Reviewers' complaints: shutter lag, ~25% keeper rate, 1/60s floor — our AF attacks exactly that.
