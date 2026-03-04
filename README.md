# LiveGrid

Multi-stream live viewer with affiliate revenue tracking, built on the Stripchat public HLS API.

## Architecture

Single-file static app (`index.html`). No build step, no dependencies beyond CDN-loaded HLS.js.

**API:** `https://go.stripchat.com/api/models` — Stripchat's affiliate/widget API. CORS-open, no auth. Returns live HLS stream URLs, viewer counts, snapshots, HD flags.

**Video:** HLS via `hls.js`. Manifest pre-processed client-side to strip Stripchat's proprietary `#EXT-X-MOUFLON` tag before HLS.js parses it.

**Affiliate tracking:** Append `?campaign=YOUR_ID` to all outbound links via the Aff. ID field in the header.

## Branches

| Branch | Purpose | Deploy target |
|--------|---------|---------------|
| `dev` | Active development | Local only |
| `staging` | Pre-release testing | GitHub Pages (`/staging`) or Netlify preview |
| `main` | Production | GitHub Pages root or custom domain |

## Local dev

```bash
# Serve locally (no build needed)
python -m http.server 8080
# open http://localhost:8080
```

## Deploy

Push to `main` → GitHub Actions auto-deploys to GitHub Pages.

## Affiliate setup

1. Sign up at https://stripchat.com/affiliate
2. Get your campaign ID
3. Enter it in the Aff. ID field — all CTA links auto-stamp it

## API params

| Param | Values | Notes |
|-------|--------|-------|
| `gender` | female, male, couple, trans | Filter by category |
| `sortBy` | viewersCount, onlineTime, new | Sort order |
| `tag` | latina, bbw, asian, etc. | Free-text tag filter |
| `limit` | integer | Max results (fetch extra, slice to grid) |
| `offset` | integer | Pagination |

## Roadmap

- [ ] Pagination / "Next page" button
- [ ] Multi-site support (Chaturbate, MyFreeCams)
- [ ] Click-through analytics dashboard
- [ ] A/B test CTA copy variants
- [ ] PWA / installable app
