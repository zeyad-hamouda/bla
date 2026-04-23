#!/usr/bin/env python3
"""Generate a static QR code from a URL. The QR code never expires."""

import argparse
import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H


def generate_qr(url: str, output: Path, box_size: int, border: int) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output)
    print(f"QR code saved to: {output.resolve()}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a permanent static QR code from a URL."
    )
    parser.add_argument("url", help="The URL to encode in the QR code.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("qrcode.png"),
        help="Output image path (default: qrcode.png).",
    )
    parser.add_argument(
        "--box-size",
        type=int,
        default=10,
        help="Pixel size of each QR box (default: 10).",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Border width in boxes (default: 4, minimum recommended).",
    )
    args = parser.parse_args()

    generate_qr(args.url, args.output, args.box_size, args.border)
    return 0


if __name__ == "__main__":
    sys.exit(main())
