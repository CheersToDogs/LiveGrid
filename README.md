# LiveGrid — Multi-Stream Viewer

Live at: **https://livegrid.pages.dev** (password protected)

## What It Does
Multi-stream viewer for Stripchat free cams with affiliate revenue tracking. Displays a configurable grid of live HLS streams with viewer counts, HD badges, and affiliate CTAs.

## Features
- Grid sizes: 1x1 through 8x8
- Filters: gender, sort, tag, quality
- Solo audio: unmuting one stream mutes all others
- Affiliate CTA on hover → stamps links with campaign ID
- Auto-refresh every 60 seconds with countdown bar
- Password gate (session-based)
- Snapshot fallback while video loads

## Architecture
- Single static HTML file, no build step
- HLS.js for video playback
- Stripchat public affiliate API: `https://go.stripchat.com/api/models`
- Cloudflare Pages for hosting (auto-deploys on push to `main`)

## API
```
GET https://go.stripchat.com/api/models
  ?limit=N
  &sortBy=viewersCount|onlineTime|new
  &gender=female|male|couple|trans
  &tag=latina|bbw|...
```
Returns models with `status: "public"` and `stream.urls` containing HLS endpoints.

## Deployment
- Repo: https://github.com/CheersToDogs/LiveGrid
- Cloudflare Pages project: `livegrid`
- Branch: `main` → auto-deploys to `livegrid.pages.dev`
- No build command, no output directory needed

## Known Issues
- `kb@banemedia.com` managed Chrome profile blocks `saawsedge.com` via MDM policy — use a clean Chrome profile or another browser
- HLS streams contain proprietary `#EXT-X-MOUFLON` tag — handled by `strictManifestParsing: false` in HLS.js config

## Affiliate Setup
1. Sign up at https://stripchat.com/affiliate
2. Enter your campaign ID in the **Aff. ID** field
3. All hover CTAs auto-stamp with `?campaign=YOUR_ID`

## Roadmap
- Pagination / load more
- Multi-site support (Chaturbate, MyFreeCams)
- Click-through analytics
- PWA / installable app
