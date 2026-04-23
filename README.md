# QR Code Generator

A simple Python script that generates a **static** QR code from a URL. Static QR codes never expire — they encode the URL directly, so they work as long as the destination website is online.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python qr_generator.py "https://example.com"
python qr_generator.py "https://example.com" -o mysite.png
python qr_generator.py "https://example.com" --box-size 15 --border 4
```

## Why it never expires

- **Static QR codes** (what this script generates): the URL is encoded directly into the pixels. No server, no redirect, no expiration.
- **Dynamic QR codes** (from paid services like Bitly, QR Code Generator Pro, etc.): the QR encodes a short redirect URL; if the service shuts down or the subscription lapses, the QR stops working.

This script produces static codes, so they last forever as long as the target URL stays live.
