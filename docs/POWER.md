# Power & Battery Model (402025, 150mAh protected)

Cell: Ecocell 402025, 3.7V, **150mAh**, ~127mAh usable after depth-of-discharge and LDO losses.

## Keyring duty cycle (the mode that matters most is *not* being used)

| Mode | Draw | Runtime implication |
|---|---|---|
| Deep sleep (idle baseline) | ~15µA (10µS3 + ~2µA LDO + ~3µA misc) | **~9 months shelf**; battery self-discharge (~3–5%/mo) rivals the electronics |
| Per shot | ~0.5–1mAh (boot 1s @40mA + AF/capture/JPEG/SD 3–5s @150–250mA + preview @70mA + shutter audio ~0.02mAh) | **~130–200 photos/charge** |
| Per shot with gallery upload | +2–3s WiFi @150mA ≈ +0.15mAh | negligible |
| Find-me event | double-press → chirp + SoftAP, ~180–220mA mostly speaker | capped 5-min session ≈ 15–20mAh ≈ 13% of the cell → ~6 searches/charge |
| Idle "am I home?" scan | timer wake every 30 min: boot + quick WiFi scan ≈ 60–75µA avg | **~2 months between charges**, and produces a "last seen home/away" timestamp |
| Continuous BLE beacon (OpenHaystack-style) | mA-class average | days–weeks — murders this cell; rejected except as a switchable "lost mode" |

## Charging

- TP4054, USB-C. Cell carries its own protection board (JST 2-pin).
- No soldered battery leads — plug connectors (the whole point of the protected cell).

## Design notes that came out of this model

1. 350mAh-class cells (the old plan) were overprovisioned by 2.3× and didn't fit the case as well — downsizing to 402025 was a win on cost, fit, AND capacity safety margin.
2. The idle scheme (30-min scan) is the only passive-findability option that coexists with a small cell. Expectations: this is a camera that helps you find keys, not an AirTag.
3. Deep-sleep wake path: shutter button on an EXT1-capable GPIO so double-press boots straight into find-me with zero firmware polling.
4. Original BOM's battery line (350mAh ~$4.50 bundled with case) was replaced by a real AU-sourced protected cell at ~AU$5.53 that actually ships.
