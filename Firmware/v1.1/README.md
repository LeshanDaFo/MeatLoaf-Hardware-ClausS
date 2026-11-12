# MeatLoaf PCB v1.1 firmware

## SPI3 hardware

The current PCB v1.1a, v1.1b and v1.1c designs use dedicated W5500 SPI3
with SCK on GPIO39, MISO on GPIO40 and MOSI on GPIO41. The SD card uses SPI2.
These boards require a v1.1 build with this pin map for Ethernet. The
N16R8 custom-filesystem test build was verified with SD and Ethernet.
Ready-to-flash SPI3 packages are pending.
