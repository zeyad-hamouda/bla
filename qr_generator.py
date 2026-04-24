#!/usr/bin/env python3
"""Generate a static QR code from a URL. The QR code never expires."""

import argparse
import sys
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H

SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "webp", "bmp", "svg"}


def _overlay_logo(qr_img: Image.Image, logo_path: Path, ratio: float) -> Image.Image:
    if not 0 < ratio <= 0.35:
        raise ValueError("--logo-ratio must be between 0 and 0.35")

    logo = Image.open(logo_path).convert("RGBA")
    qr_w, qr_h = qr_img.size
    target = int(qr_w * ratio)
    logo.thumbnail((target, target), Image.LANCZOS)

    pad = int(target * 0.12)
    bg_size = (logo.width + pad * 2, logo.height + pad * 2)
    bg = Image.new("RGB", bg_size, "white")
    bg.paste(logo, (pad, pad), mask=logo)

    pos = ((qr_w - bg.width) // 2, (qr_h - bg.height) // 2)
    qr_img.paste(bg, pos)
    return qr_img


def generate_qr(
    url: str,
    output: Path,
    size: int,
    border: int,
    fmt: str,
    logo: Path | None = None,
    logo_ratio: float = 0.22,
) -> None:
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{fmt}'. Choose from: {sorted(SUPPORTED_FORMATS)}"
        )

    if fmt == "svg":
        if logo is not None:
            raise ValueError("--logo is not supported with SVG output")
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

        if logo is not None:
            img = _overlay_logo(img, logo, logo_ratio)

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
    parser.add_argument(
        "--logo",
        type=Path,
        default=None,
        help="Optional path to a logo image to overlay in the center of the QR code.",
    )
    parser.add_argument(
        "--logo-ratio",
        type=float,
        default=0.22,
        help="Logo size as a fraction of QR width (default: 0.22, max: 0.35).",
    )
    args = parser.parse_args()

    if args.size <= 0:
        parser.error("--size must be a positive integer")
    if args.logo is not None and not args.logo.exists():
        parser.error(f"logo file not found: {args.logo}")

    output = args.output or Path(f"qrcode.{args.format}")
    generate_qr(
        args.url,
        output,
        args.size,
        args.border,
        args.format,
        logo=args.logo,
        logo_ratio=args.logo_ratio,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
