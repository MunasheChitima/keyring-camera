# Firmware

Firmware for the keyring camera — ESP32-S3 (ESP-IDF or Arduino framework), targeting the board spec in `../docs/SPEC.md`.

**Status: planned, not yet written.** This document is the feature contract the PCB was designed around.

## Feature plan

| Feature | Source | Notes |
|---|---|---|
| Camera + **autofocus** | esp32-camera **PR #831** (`ov5640_af`, official AF support) | Firmware AF blob uploads over SCCB at init; AF module needs 3.3V on its pin 24 (AF_VCC) |
| JPEG capture → MicroSD | esp32-camera + SD_MMC/SPI | ~0.5–1mAh per shot burst |
| 1.14″ ST7789 preview UI | TFT_eSPI or LovyanGFX | preview a few seconds, then sleep to save mA |
| Deep sleep (~15µA) + EXT1 wake | ESP-IDF sleep API | double-press → boots into find-me |
| Find-me mode | chirp via MAX98357A + SoftAP beacon | capped ~5 min session |
| Idle "am I home?" scan | timer wake, WiFi quick connect | every 30 min, ~60–75µA average |
| Friends-gallery auto-upload | HTTPS POST w/ invite token | runs post-capture before deep sleep; ~+0.15mAh/photo |
| Audio: shutter sound | MAX98357A I2S | |
| PDM mic capture | I2S PDN in | MSM261DGT003 |
| Games | keypad FPC + buttons | 4-key diamond + 2 side buttons |
| Offline voice commands | Espressif ESP-SR (WakeNet + MultiNet) | models ~1–2MB fit 4MB flash + 2MB PSRAM |
| Assistant (optional, networked) | gallery Worker backend → LLM → speech out via MAX98357A | friends' WiFi; jailbreak layer |

## Suggested structure

```
firmware/
  main/           # app entry, sleep/deep-sleep state machine
  components/
    cam/          # esp32-camera wrapper + ov5640_af init
    audio/        # PDM in, MAX98357A out, chirp assets
    ui/           # ST7789 preview + menus
    findme/       # chirp + SoftAP
    gallery/      # HTTPS upload client (token, retry, offline queue on SD)
    games/        # ROM loader / simple games
```

## Bring-up order (when PCBs arrive)

1. Bench test with a devboard FIRST (before gifting): camera init, AF sweep works, SD writes, WiFi boots, speaker chirps, sleep current measures ~15µA (if it's >50µA, find the leak before anything ships).
2. Flash one camera end-to-end: photo → SD → preview → sleep → find-me.
3. Then the gallery upload, then games, then voice.
