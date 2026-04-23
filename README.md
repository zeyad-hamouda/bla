# QR Code Generator

A simple Python script that generates a **static** QR code from a URL. Static QR codes never expire — they encode the URL directly, so they work as long as the destination website is online.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Default: 512x512 PNG saved as qrcode.png
python qr_generator.py "https://example.com"

# Custom size (pixels, square)
python qr_generator.py "https://example.com" --size 1024

# Custom output file
python qr_generator.py "https://example.com" -o mysite.png

# Different format (png, jpeg, webp, bmp, svg)
python qr_generator.py "https://example.com" -f svg
python qr_generator.py "https://example.com" -f jpeg --size 2048
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `url` | — | URL to encode (required). |
| `-o, --output` | `qrcode.<format>` | Output file path. |
| `-s, --size` | `512` | Output image size in pixels (square). Ignored for SVG. |
| `-f, --format` | `png` | `png`, `jpeg`, `webp`, `bmp`, or `svg`. |
| `--border` | `4` | Quiet-zone border in QR boxes (4 is the minimum recommended). |

The generated file is saved in the current directory — just open it or move/share it like any other image.

## Why it never expires

- **Static QR codes** (what this script generates): the URL is encoded directly into the pixels. No server, no redirect, no expiration.
- **Dynamic QR codes** (from paid services like Bitly, QR Code Generator Pro, etc.): the QR encodes a short redirect URL; if the service shuts down or the subscription lapses, the QR stops working.

This script produces static codes, so they last forever as long as the target URL stays live.
