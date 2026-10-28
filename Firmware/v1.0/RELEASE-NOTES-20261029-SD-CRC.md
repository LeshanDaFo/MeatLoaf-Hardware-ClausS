# MeatLoaf PCB v1.0 firmware update — SD CRC compatibility

This update refreshes the prebuilt firmware packages for the MeatLoaf Hardware
PCB v1.0. It incorporates the SD-card SPI CRC initialization compatibility fix
accepted upstream in
[idolpx/meatloaf pull request #69](https://github.com/idolpx/meatloaf/pull/69).

## Changes

- Retry the SPI `CMD59` CRC-enable command once after a 10 ms delay when the
  first command reports `ESP_ERR_NOT_SUPPORTED`.
- Preserve the existing PCB v1.0 GPIO mapping, IEC split/inverted lines,
  direct SRQ support, ROOT-button behavior, and the existing project-specific
  network fixes.
- Preserve the published partition layouts, flash offsets, bootloader images,
  update images, and web-flasher ZIP format.

## Supported packages

| Package | Target |
| --- | --- |
| `meatloaf.meatloaf-claus-s3-pcb-v1_0-n8r8.20261029.06.zip` | ESP32-S3, 8 MB flash, 8 MB PSRAM; LittleFS without the web interface |
| `meatloaf.meatloaf-claus-s3-pcb-v1_0-n16r8.20261029.06.zip` | ESP32-S3, 16 MB flash, 8 MB PSRAM; LittleFS with the web interface |

Firmware version: `1.4.8311ea72`  
Build commit: `c5835474`  
Official upstream base: `068aea35085990cbe6e6a527dcd502deca9bb741`  
SD CRC fix commit: `0675f5152359ee38311cfdb82a955908154a5ca0`  
Build platform: PlatformIO Espressif32 `6.13.0`  
Framework: ESP-IDF `5.5.3`

## Installation

Select the ZIP that exactly matches the ESP32-S3 flash and PSRAM capacity.
Install it with the existing custom-ZIP workflow in the MeatLoaf web flasher.
The ZIP contains `release.json`, `bootloader.bin`, `partitions.bin`, `main.bin`,
`update.bin`, and `storage.bin`, including all required flash offsets.

## Verification status

- Both N8R8 and N16R8 environments build successfully.
- ZIP structure, image headers, partition tables, flash offsets, image sizes,
  and SHA-256 checksums were verified.
- The upstream CRC-retry patch is present in the ESP-IDF source used by the
  build.
- No PCB v1.1b or v1.3 pin mappings or build environments were used.
- A final hardware test was completed successfully with the updated PCB v1.0
  firmware. The previously incompatible SHANSU 64 GB SDXC card was detected,
  confirming the SD-card CRC compatibility fix in the newly compiled firmware.

Only the hardware behavior described above is recorded as tested here. The
successful SDXC test does not by itself certify every function of both memory
variants.

The initial `20261020.18` packages remain available as historical artifacts.
