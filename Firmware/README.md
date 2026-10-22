# MeatLoaf-Hardware-ClausS — Firmware

This directory is for **prebuilt firmware packages** corresponding to the project's hardware revisions and ESP32-S3 memory variants.

The underlying MeatLoaf firmware project is maintained at [idolpx/meatloaf](https://github.com/idolpx/meatloaf). These packages are project-specific builds; consult the upstream firmware license before redistribution.

## Firmware variants

| Hardware | PlatformIO environment | Flash | PSRAM |
| --- | --- | --- | --- |
| PCB v1.0, N8R8 | `meatloaf-claus-s3-pcb-v1_0-n8r8` | 8 MB | 8 MB |
| PCB v1.0, N16R8 | `meatloaf-claus-s3-pcb-v1_0-n16r8` | 16 MB | 8 MB |

These are the **intended environment names**. Publish binaries only after their configuration and partition layout have been verified for the target hardware.

## Identifying the memory variant

The memory suffix describes the module configuration, not the carrier-board
layout. In [Espressif's DevKitC-1 ordering table](https://docs.espressif.com/projects/esp-idf/en/v5.3.1/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html),
`N` is the flash capacity and `R` is the PSRAM capacity, both in megabytes.
`R` does not describe the ESP32-S3's internal SRAM. For example:

| Module suffix | Flash | PSRAM |
| --- | ---: | ---: |
| `N8` | 8 MB | None |
| `N8R2` | 8 MB | 2 MB |
| `N8R8` | 8 MB | 8 MB |
| `N16R8V` | 16 MB | 8 MB |
| `N32R8V` | 32 MB | 8 MB |

The additional `V` used by Espressif identifies a 1.8 V flash/PSRAM
configuration. Third-party board names may use similar suffixes without
following every detail of Espressif's naming scheme.

The module marking is a useful first indication. Before selecting a package,
verify it against the following mapping whenever possible:

| Detected hardware | Firmware variant |
| --- | --- |
| ESP32-S3 with 8 MB flash and 8 MB PSRAM | `meatloaf-claus-s3-pcb-v1_0-n8r8` |
| ESP32-S3 with 16 MB flash and 8 MB PSRAM | `meatloaf-claus-s3-pcb-v1_0-n16r8` |

If either memory size is unknown, or if the detected configuration differs
from both rows, do not select either firmware variant without further
verification.

### Check the module marking or installed firmware

Use these methods first:

1. **Read the metal module shield.** Look for the complete module name, for
   example `ESP32-S3-WROOM-1-N8R8`. A label on the carrier PCB identifies a
   compatible board outline; it cannot identify the memory fitted to the
   removable module.
2. **Use MeatLoaf `sysinfo`.** If working MeatLoaf firmware is already
   installed, connect to its serial console and enter `sysinfo`. The output
   includes `Flash size` and `PSRAM size`.

### Check with esptool 5.3.1

The `flash-id` command reads chip and memory information without erasing or
overwriting the installed firmware.

#### Requirements

- Python 3.10 or newer
- esptool 5.3.1
- a data-capable USB cable
- the USB programming port of the ESP32-S3 development board
- a USB-UART driver if required by the board's interface chip

Install the documented esptool version from a terminal or command prompt:

**Windows**

```powershell
py -m pip install --upgrade "esptool==5.3.1"
```

**macOS and Linux**

```bash
python3 -m pip install --upgrade "esptool==5.3.1"
```

After installation, the `esptool` command should be available. If the command
is not found, restart the terminal or use `py -m esptool` on Windows and
`python3 -m esptool` on macOS or Linux in place of `esptool` below.

#### Find the serial port

Disconnect other serial devices if the port is difficult to identify. Compare
the port list before and after connecting the ESP32-S3 board.

**Windows**

Open **Device Manager > Ports (COM & LPT)** and note the new port, for example
`COM5`. It can also be listed from PowerShell or Command Prompt:

```powershell
py -m serial.tools.list_ports
```

**macOS**

```bash
ls /dev/cu.usb*
```

A typical result is `/dev/cu.usbserial-0001` or `/dev/cu.usbmodem*`.

**Linux**

```bash
python3 -m serial.tools.list_ports
```

Typical ports are `/dev/ttyUSB0` and `/dev/ttyACM0`. The user may need
permission to access the serial device, depending on the Linux distribution.

CP210x, CH34x, and FTDI USB-UART interfaces may require a vendor driver if the
operating system does not create a serial port. Native USB connections may not
require an additional driver. Close serial monitors and other programs using
the selected port before running esptool.

#### Read and interpret the result

Use the command for the detected port:

**Windows**

```powershell
esptool --port COM5 flash-id
```

**macOS**

```bash
esptool --port /dev/cu.usbserial-0001 flash-id
```

**Linux**

```bash
esptool --port /dev/ttyUSB0 flash-id
```

All port names above are examples and must be replaced when the detected name
is different. A successfully tested esptool 5.3.1 query on an N16R8 module
included the following lines:

```text
Chip type: ESP32-S3 (QFN56) (revision v0.2)
Features: Wi-Fi, BT 5 (LE), Dual Core + LP Core, 240MHz, Embedded PSRAM 8MB (AP_3v3)

Flash Memory Information:
Detected flash size: 16MB
```

This output identifies an ESP32-S3 with 16 MB flash and 8 MB PSRAM, so the
correct package is `meatloaf-claus-s3-pcb-v1_0-n16r8`. Correspondingly, an
ESP32-S3 with 8 MB flash and 8 MB PSRAM requires
`meatloaf-claus-s3-pcb-v1_0-n8r8`.

The amount of information reported by `flash-id` depends on the chip, board,
connection, and esptool support. If the `Features` line does not state the
PSRAM size, do not infer it from the flash size. Check the module marking,
vendor documentation, or `sysinfo` from correctly configured firmware.

The command and behavior are described in the
[official esptool v5 documentation](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/index.html).

#### If esptool cannot connect

Most development boards enter download mode automatically. If automatic reset
fails, use the buttons on the removable ESP32-S3 development board:

1. Hold **BOOT** (`GPIO0`).
2. Press and release **EN** or **RESET** while continuing to hold **BOOT**.
3. Start the `flash-id` command and release **BOOT** when esptool begins to
   connect.

On PCB v1.0, the carrier's ROOT button `SW1` pulls `GPIO0` low but is not
connected to the module's `EN` pin. Use the module's EN/RESET control for the
reset step. See
Espressif's [download-mode instructions](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html)
for additional troubleshooting.

For custom diagnostic firmware, ESP-IDF can report PSRAM with
[`esp_psram_get_size()`](https://docs.espressif.com/projects/esp-faq/en/latest/software-framework/storage/psram.html).
A result of zero from firmware built without the correct PSRAM support does not
prove that the physical module has no PSRAM; check the module marking or vendor
documentation as well.

Select a firmware package only after identifying both the carrier revision and
the module's flash capacity. The packages currently published here target
N8R8 and N16R8 configurations; another physically compatible DevKitC-1 variant
is not automatically supported by those packages.

## Web flashing

A flashable ZIP package can be installed using the web flasher at [meatloaf.cc](https://meatloaf.cc/) on a compatible browser and supported USB connection.

1. Identify the PCB revision and the memory variant printed on the removable ESP32-S3 module. Do not infer the memory capacity from the carrier-board silkscreen; see [Identifying the memory variant](#identifying-the-memory-variant).
2. Download the matching firmware ZIP from this repository or its GitHub Releases.
3. Connect the board using its supported USB programming connector and a data-capable cable.
4. Open the MeatLoaf web flasher in a browser with Web Serial support (typically Chrome or Edge).
5. Choose **Connect**, select the board's serial device, and select the custom ZIP package using the site's upload workflow.
6. Follow the flasher's instructions, then restart the board if required.

USB-UART drivers may be needed depending on the adapter and operating system (for example CP2102 or FT232RQ). On Linux, access permissions for serial devices may also need configuration.

**Warning:** Use only a package for the exact flash capacity and hardware configuration. An N16R8 partition scheme must not be assumed to work on an N8R8 device.

## Flashing with PlatformIO

If you have the matching MeatLoaf source tree and the named PlatformIO environments configured, use the commands below. Replace the port with the one detected on your computer.

**PCB v1.0 — N16R8**

```bash
pio run -e meatloaf-claus-s3-pcb-v1_0-n16r8 -t upload --upload-port /dev/cu.usbserial-0001
pio run -e meatloaf-claus-s3-pcb-v1_0-n16r8 -t uploadfs --upload-port /dev/cu.usbserial-0001
```

**PCB v1.0 — N8R8**

```bash
pio run -e meatloaf-claus-s3-pcb-v1_0-n8r8 -t upload --upload-port /dev/cu.usbserial-0001
pio run -e meatloaf-claus-s3-pcb-v1_0-n8r8 -t uploadfs --upload-port /dev/cu.usbserial-0001
```

`upload` writes the firmware; `uploadfs` writes the filesystem image, including web-interface assets where provided by the build. A complete installation may require both.

The example serial port is macOS-specific and **not guaranteed to be the same on another computer**.

## Release checklist

Before publishing a package, verify:

- [ ] Exact PCB revision and ESP32-S3 variant
- [ ] Flash size, PSRAM settings, and partition layout
- [ ] Firmware and filesystem images fit within the physical flash
- [ ] Web interface and persistent configuration storage work after reboot
- [ ] Package flashes successfully on the target hardware
- [ ] Firmware version/commit and upstream licensing are documented

## Licensing

Firmware licensing is separate from the custom hardware license. Preserve all applicable upstream license notices and fulfill source-code distribution obligations where required. Do not assume the hardware license applies to firmware binaries.
