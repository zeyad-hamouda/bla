#!/usr/bin/env python3
"""Generate a static QR code from a URL. The QR code never expires."""

import argparse
import sys
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H

SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "webp", "bmp", "svg"}


def generate_qr(
    url: str,
    output: Path,
    size: int,
    border: int,
    fmt: str,
) -> None:
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{fmt}'. Choose from: {sorted(SUPPORTED_FORMATS)}"
        )

    if fmt == "svg":
        import qrcode.image.svg as svg_mod

        qr = qrcode.QRCode(
            error_correction=ERROR_CORRECT_H,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(image_factory=svg_mod.SvgImage)
        img.save(str(output))
    else:
        qr = qrcode.QRCode(
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        img = img.resize((size, size), resample=Image.NEAREST)

        save_format = "JPEG" if fmt in ("jpg", "jpeg") else fmt.upper()
        img.save(output, format=save_format)

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
        default=None,
        help="Output image path (default: qrcode.<format>).",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=512,
        help="Output image size in pixels, width and height (default: 512). "
        "Ignored for SVG.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=sorted(SUPPORTED_FORMATS),
        default="png",
        help="Output image format (default: png).",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Border width in QR boxes (default: 4, minimum recommended).",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("--size must be a positive integer")

    output = args.output or Path(f"qrcode.{args.format}")
    generate_qr(args.url, output, args.size, args.border, args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
