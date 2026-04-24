# Adaptive landing page for GSG Academy

Small static page that routes users to the right app store based on their device:

- **iOS** → App Store listing (`CONFIG.iosUrl`)
- **Android + app live** → Google Play listing (`CONFIG.androidUrl`)
- **Everything else** (desktop, Android before rollout, unknown OS) → fallback card showing the app icon and a "gradually rolling out globally" message.

## Setup

1. Open `index.html` and edit the `CONFIG` block at the bottom:
   - `iosUrl` → your App Store URL.
   - `androidUrl` → your Play Store URL (replace the package ID).
   - `androidAvailable` → `false` until the Android app is live on Google Play; flip to `true` after launch.
2. Replace `icon.png` with your real 512×512 app icon (PNG, rounded optional).
3. Host the folder on any static host — GitHub Pages, Netlify, Vercel, Cloudflare Pages, or your own domain.
4. Generate the QR code pointing at the hosted URL:
   ```bash
   python ../qr_generator.py "https://your-domain.example/adaptive/" \
       --logo icon.png -o gsg_qr.png
   ```

The QR code itself is static and permanent. To toggle Android availability later, edit `CONFIG.androidAvailable` and redeploy — the QR never has to change.

## Why not auto-detect "app missing on Play Store"?

Browsers block cross-origin checks against `play.google.com`, and Google doesn't expose a public availability API. The clean, reliable option is the manual `androidAvailable` flag. If you later add a backend, you can replace it with a real server-side check.
