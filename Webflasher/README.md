# MeatLoaf Carrier Board Web Flasher

From this directory, run:

```sh
python3 prepare.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://localhost:8765/> in desktop Chrome or Edge. The browser loads
ESP Web Tools over the internet. Select the carrier family and confirm the
N8R8 or N16R8 marking on the ESP32-S3 module before connecting.

`prepare.py` downloads the four pinned public release ZIPs, verifies their
SHA-256 digests and generates local manifests from the published flash offsets.
Use `--packages DIRECTORY` to reuse matching ZIPs already downloaded.

For the hardware test, back up LittleFS, install on a v1.0 and a v1.1 board,
check the serial startup log, and verify SD access and Ethernet where fitted.
Check the web interface on N16R8. The same v1.1 packages cover v1.1a, v1.1b
and v1.1c.

GitHub Pages deploys this directory through the Webflasher workflow. Update the
pinned release and checksums in `prepare.py` after approving a new public release.
