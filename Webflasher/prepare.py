"""Prepare local flash manifests from the public Carrier releases."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
from urllib.request import urlopen
from zipfile import ZipFile

RELEASES = "https://github.com/LeshanDaFo/Meatloaf-Hardware-ClausS/releases/download"
V11_COMMIT = "3a9d39908fd5d758952bdff338049fd054ee3a6e"
CHECKSUMS = {
    ("v1.0", "n8r8"): "313cc5f8f5ba9d7ec5d6a6621394a7f2aaceb88999010a334d9d0aff28fca000",
    ("v1.0", "n16r8"): "af235b785f90350310cf9dca61a3ee371eb0d0a20708bd23858ea946089370ca",
    ("v1.1", "n8r8"): "473603695a5b23bd4ac6f4e67acff69a27e7cd1158cabce33e206b87a9d44265",
    ("v1.1", "n16r8"): "956b738e8d0c8d502fe3dfad3f8c18cc2d5f62ce164c3fb47ece28f3a2216e1e",
}
OUTPUT = Path(__file__).resolve().parent / "firmware"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prepare(board, module, checksum, packages):
    if board == "v1.0":
        tag = "pcb-v1.0-fw-20261029-sd-crc"
        filename = f"meatloaf.meatloaf-claus-s3-pcb-v1_0-{module}.20261029.06.zip"
    else:
        tag = "pcb-v1.1-fw-20261112-spi3"
        filename = f"meatloaf-claus-s3-pcb-v1_1-{module}-{V11_COMMIT}.zip"

    url = f"{RELEASES}/{tag}/{filename}"
    local = packages / filename if packages else None
    if local and local.is_file():
        payload = local.read_bytes()
    else:
        with urlopen(url, timeout=60) as response:
            payload = response.read()
    require(hashlib.sha256(payload).hexdigest() == checksum, f"SHA-256 mismatch: {filename}")

    with ZipFile(io.BytesIO(payload)) as archive:
        metadata = json.loads(archive.read("release.json"))
        offsets = {entry["filename"]: int(entry["offset"], 16) for entry in metadata["files"]}
        partitions = {
            label.rstrip(b"\0").decode(): (address, size)
            for magic, _, _, address, size, label, _ in struct.iter_unpack(
                "<HBBII16sI", archive.read("partitions.bin")
            )
            if magic == 0x50AA
        }
        flash_size = (8 if module == "n8r8" else 16) * 1024 * 1024
        require(max(address + size for address, size in partitions.values()) == flash_size,
                f"Incorrect flash size: {filename}")
        expected = {"bootloader.bin": 0, "partitions.bin": 0x8000}
        expected.update({f"{label}.bin": partitions[label][0] for label in ("main", "update", "storage")})
        require(offsets == expected, f"Unexpected flash offsets: {filename}")
        limits = {"bootloader.bin": 0x8000, "partitions.bin": 0x1000}
        limits.update({f"{label}.bin": partitions[label][1] for label in ("main", "update", "storage")})
        images = {name: archive.read(name) for name in offsets}
        require(all(0 < len(image) <= limits[name] for name, image in images.items()),
                f"An image exceeds its partition: {filename}")
        require(len(images["storage.bin"]) == limits["storage.bin"],
                f"Incomplete LittleFS image: {filename}")

    key = f"{board}-{module}"
    directory = OUTPUT / key
    directory.mkdir(parents=True, exist_ok=True)
    for name, image in images.items():
        (directory / name).write_bytes(image)
    name = f"Meatloaf Carrier {board} {module.upper()}"
    manifest = {
        "name": name,
        "version": metadata["version"],
        "new_install_prompt_erase": True,
        "new_install_improv_wait_time": 0,
        "builds": [{
            "chipFamily": "ESP32-S3",
            "improv": False,
            "parts": [{"path": name, "offset": offset} for name, offset in sorted(
                offsets.items(), key=lambda part: part[1]
            )],
        }],
    }
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Verified {filename}")
    return {
        "name": name,
        "version": metadata["version"],
        "web": module == "n16r8",
        "manifest": f"./firmware/{key}/manifest.json",
        "download": url,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", type=Path, help="Directory with downloaded release ZIPs")
    args = parser.parse_args()
    catalog = {
        f"{board}-{module}": prepare(board, module, checksum, args.packages)
        for (board, module), checksum in CHECKSUMS.items()
    }
    (OUTPUT / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")


if __name__ == "__main__":
    main()
