#!/usr/bin/env python3
"""Entry program for the news-image-20261120 bounty.

Standard library only. Copies the committed poster (entry.png) to the
output directory, byte for byte, so every run writes identical bytes.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
WANT_W, WANT_H = 1024, 1024


def validate_png(path):
    """Check the file is a whole PNG inside the gate limits.

    Parses the PNG signature and the IHDR chunk by hand: no image
    library is available in the grading sandbox.
    """
    with open(path, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (WANT_W, WANT_H):
        raise SystemExit("entry.png is %dx%d, want %dx%d"
                         % (width, height, WANT_W, WANT_H))
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    validate_png(src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    validate_png(dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
