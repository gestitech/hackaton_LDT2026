#!/usr/bin/env python3
"""Decrypt the MSC disk image from the second megabyte of the RP2040 dump.

The image in the file is ciphertext. tud_msc_read10_cb XORs each sector with
a keystream derived from the LBA. XOR is symmetric, so the same function
decrypts. The result is a 1 MiB FAT12 superfloppy with no partition table.
Запуск
python decrypt_disk.py firmware_dump.bin -o disk.img
"""

import argparse
from pathlib import Path

DISK_OFFSET = 0x100000
SECTOR_SIZE = 512
SECTOR_COUNT = 2048

LBA_MUL = 0x38C9CDA0
LBA_ADD = 0x9E37A9EA
STATE_STEP = 0x41C64E6D


def byte_of(state, constant):
    return ((state + constant) & 0xFFFFFFFF) >> 24


def keystream_words(state):
    state &= 0xFFFFFFFF
    word0 = (
        byte_of(state, 0x61C8864F)
        | ((state >> 24) << 8)
        | (byte_of(state, 0x9E3779B1) << 16)
        | (byte_of(state, 0x3C6EF362) << 24)
    )
    word1 = (
        byte_of(state, 0xDAA66D13)
        | (byte_of(state, 0x78DDE6C4) << 8)
        | (byte_of(state, 0x17156075) << 16)
        | (byte_of(state, 0xB54CDA26) << 24)
    )
    word2 = (
        byte_of(state, 0x538453D7)
        | (byte_of(state, 0xF1BBCD88) << 8)
        | (byte_of(state, 0x8FF34739) << 16)
        | (byte_of(state, 0x2E2AC0EA) << 24)
    )
    word3 = (
        byte_of(state, 0xCC623A9B)
        | (byte_of(state, 0x6A99B44C) << 8)
        | (byte_of(state, 0x08D12DFD) << 16)
        | (byte_of(state, 0xA708A7AE) << 24)
    )
    return word0, word1, word2, word3


def decrypt_sector(sector, lba):
    if len(sector) != SECTOR_SIZE:
        raise ValueError("sector must be 512 bytes, got %d" % len(sector))
    state = (lba * LBA_MUL + LBA_ADD) & 0xFFFFFFFF
    out = bytearray(sector)
    for offset in range(0, SECTOR_SIZE, 16):
        for index, word in enumerate(keystream_words(state)):
            at = offset + index * 4
            current = int.from_bytes(out[at:at + 4], "little")
            out[at:at + 4] = (current ^ word).to_bytes(4, "little")
        state = (state + STATE_STEP) & 0xFFFFFFFF
    return bytes(out)


def decrypt_image(dump):
    disk = dump[DISK_OFFSET:DISK_OFFSET + SECTOR_COUNT * SECTOR_SIZE]
    if len(disk) != SECTOR_COUNT * SECTOR_SIZE:
        raise ValueError("dump does not contain a 1 MiB disk at offset 0x100000")
    parts = []
    for lba in range(SECTOR_COUNT):
        start = lba * SECTOR_SIZE
        parts.append(decrypt_sector(disk[start:start + SECTOR_SIZE], lba))
    return b"".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dump", type=Path, help="firmware dump, 2 MiB")
    parser.add_argument("-o", "--output", type=Path, default=Path("disk.img"))
    args = parser.parse_args()

    image = decrypt_image(args.dump.read_bytes())
    args.output.write_bytes(image)
    print("wrote %s (%d bytes)" % (args.output, len(image)))
    print("boot %s" % image[:3].hex())
    print("fs   %s" % image[54:59])


if __name__ == "__main__":
    main()
