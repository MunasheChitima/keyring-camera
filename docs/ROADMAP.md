# Roadmap

## Phase 1 — Christmas gifts (now)
Schematic + footprints → JLC 10-board order (~AU$137–146 with coupons) → AF modules (AU$8.06 click-line or AU$1.64 wildcard after teardown) → hand-assembly → print cases → 5–10 finished gifts.

Decision framework for fleet composition (settled Nov 2026): **camera quality tier is locked at 5MP AF** — a downgraded camera is "a worse version of something you could just buy." But the generic 24P map allows a mixed fleet later (AF for enthusiasts, FF for casuals) without PCB changes.

## Phase 2 — Content (parallel, zero extra cost)
- Film the build as it happens: JLC unboxing, hand-assembly, teardown-verdict on the AU$1.64 wildcard ("is the AU$1.64 autofocus real?"), case printing, gifting.
- Positioning vs RewindPix PS135 (verified Nov 2026): they built a better camera (10.7MP Sony, no AF) and sold 8,000 units at A$210 on a Novatek action-cam mainboard; **we hand-assembled a better object** (AF, display, audio, sharing, personalization, open) at ~1/5 the price. Their complaint list (shutter lag, ~25% keeper rate) is our AF's pitch.

## Phase 3 — The friends' gallery (weekend of firmware, post-Christmas)
Camera → HTTPS POST (invite token) → **Cloudflare R2 (free tier) + Workers** → private token-gated gallery page + Web Push ("Mun took a photo"). No logins (the link is the account), delete button, revoke-able invites. Cost: AU$0/month. One less thing the user does: auto-upload fires before deep sleep.

This deliberately avoids everything that would turn it into an unmanageable platform: private-by-invitation only, no discovery, no profiles.

## Phase 4 — Weddings & events (January field test)
Disposable wedding table cameras are an existing, paid tradition. Our version:
- Parametric engraved shells (couple's names from the case script + colour themes)
- 6–10 cameras on tables → every photo auto-posts to **the couple's private gallery** — live push notifications during the reception, full set on the projector by midnight
- Rental model preferred (hardware returns, amortizes the BOM)
- Reliability bar jumps: test one camera through a full event-day battery run before the first paid gig
- Volume unlocks factory sourcing: SincereFirst custom-FOV modules (e.g., table-portrait lens) at 100+ unit pricing

## Phase 5 — Open platform
Firmware + case files public on GitHub with a README people can build from (offline wake-word voice commands via ESP-SR work on this hardware immediately; the gallery server doubles as an optional assistant backend — LLM via a Worker, speech via the MAX98357A).

## v2 — ESP32-P4 + MIPI (the optics race)
What blocks better sensors on v1: ESP32-S3 speaks DVP only; MIPI sensors (IMX258/IMX335-class) need a CSI receiver + ISP. v2: **ESP32-P4 (MIPI CSI ×2 + hardware ISP) + ESP32-C6 WiFi co-processor (~US$1.30)** + IMX335/GC2093-class modules (2µm pixels). ≈ +AU$16–19 BOM, real engineering (MIPI differential layout, ISP bring-up). Sequence: **v1 proves the product, v2 proves the image quality** — start it with a video published and a wedding gig earned.

## Funding reality check (settled Nov 2026)
- Phase 1 is the only big spend (~AU$150). Everything else phases.
- Recoupment: sponsored gifts (enthusiast friends chip in ~AU$20–25); surplus builds sold post-Christmas at AU$79–89 vs ~AU$31 BOM (FF variant) — 3 sales ≈ Phase 1 paid back.
- The gallery and assistant are firmware weekends, not December money.
