# MeatLoaf PCB v1.1 firmware

## SPI3 hardware

The current PCB v1.1a, v1.1b and v1.1c designs use dedicated W5500 SPI3
with SCK on GPIO39, MISO on GPIO40 and MOSI on GPIO41. The SD card uses SPI2.
These boards require a v1.1 build with this pin map for Ethernet. The
N16R8 custom-filesystem test build was verified with SD and Ethernet.
Download the [v1.1 SPI3 firmware release](https://github.com/LeshanDaFo/MeatLoaf-Hardware-ClausS/releases/tag/pcb-v1.1-fw-20261112-spi3)
and load the matching ZIP as a custom package in the MeatLoaf Web Flasher.

| Module | Flash | PSRAM | Web interface |
| --- | ---: | ---: | --- |
| N8R8 | 8 MB | 8 MB | Not included |
| N16R8 | 16 MB | 8 MB | Included |

Both packages use the standard MeatLoaf LittleFS image. The release includes
SHA-256 checksums and the corresponding source.
