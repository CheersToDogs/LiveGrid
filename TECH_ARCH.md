# LiveGrid — Technical Architecture

## Overview
Single static HTML file. No framework, no build step, no backend. Deployed to Cloudflare Pages via GitHub auto-deploy.

## File Structure
```
livegrid/
├── index.html          # Entire app — HTML + CSS + JS
├── PROJECT.md          # Project context, roadmap, rules
├── TECH_ARCH.md        # This file
├── README.md           # Public-facing docs
└── .github/
    └── workflows/
        ├── deploy.yml      # GitHub Pages (unused — private repo)
        └── staging.yml     # Netlify staging preview
```

## Data Flow
```
Browser
  → fetch() Stripchat API (CORS-open)
  → filter public models with stream.urls
  → build tile DOM nodes
  → HLS.js loads m3u8 from saawsedge.com CDN
  → video plays in <video> element
  → hover CTA links to stripchat.com/?campaign=ID
```

## Stripchat Affiliate API
```
GET https://go.stripchat.com/api/models
Params:
  limit     int       number of models to return
  sortBy    string    viewersCount | onlineTime | new
  gender    string    female | male | couple | trans
  tag       string    free text (latina, bbw, etc.)

Response:
  models[].username
  models[].status          "public" = free cam
  models[].viewersCount
  models[].broadcastHD     bool
  models[].snapshotUrl     thumbnail
  models[].widgetPreviewUrl fallback thumbnail
  models[].stream.urls     { original, 480p, 240p, 160p }
```

## HLS Video Pipeline
- CDN: edge-hls.saawsedge.com (master playlist)
- Segments: media-hls.saawsedge.com
- CORS: access-control-allow-origin: * on all endpoints
- Proprietary tag: #EXT-X-MOUFLON in master playlist
  → handled by strictManifestParsing: false in HLS.js
- Quality levels: 160p / 240p / 480p / original (adaptive)

## HLS.js Config
```javascript
{
  maxBufferLength: 15,
  maxMaxBufferLength: 30,
  enableWorker: true,
  strictManifestParsing: false,  // handles EXT-X-MOUFLON
  manifestLoadingMaxRetry: 4,
  manifestLoadingRetryDelay: 1000,
  levelLoadingMaxRetry: 4,
  fragLoadingMaxRetry: 4
}
```

## Layout Architecture
```
body (100vh, flex column, overflow hidden)
├── #gate (fixed overlay, z-index 9999)
└── #app (flex column, 100vh, display:none until auth)
    ├── header (flex, shrink 0)
    └── #grid-wrapper (flex:1, overflow-y:auto)
        └── #grid (CSS grid, repeat(N, 1fr))
            └── .tile (aspect-ratio:16/9, position:relative)
                ├── video (position:absolute, inset:0)
                ├── .tile-snapshot (absolute, z-index:1)
                ├── .tile-top (absolute, z-index:2)
                ├── .tile-bottom (absolute, z-index:2)
                └── .tile-cta (absolute, z-index:3, opacity:0)
```

## Critical CSS Rules
- `body` must be `height: 100vh` + `overflow: hidden` — do not change
- `#app` must be `height: 100vh` — do not change
- `#grid-wrapper` must be `flex: 1` + `overflow-y: auto` — this is where scroll happens
- `.tile` uses `aspect-ratio: 16/9` — requires parent width to be defined
- Changing any of the above breaks tile sizing

## Password Gate
- Client-side only — JavaScript comparison
- Session-based: `sessionStorage.setItem('lg_auth', '1')`
- Clears on tab/browser close
- NOT secure against inspection — sufficient for obscurity only
- Future: replace with Cloudflare Worker cookie-based auth

## Deployment
- Push to `main` → GitHub webhook → Cloudflare Pages build
- Build command: none
- Output directory: none (root)
- Deploy time: ~30 seconds
- Rollback: `git checkout <commit> -- index.html && git push`

## Dependencies (CDN)
- HLS.js: https://cdn.jsdelivr.net/npm/hls.js@latest
- Fonts: Google Fonts (Space Mono, Syne)

## Browser Compatibility
- Chrome/Edge: full support via HLS.js
- Firefox: full support via HLS.js
- Safari: native HLS via video.canPlayType('application/vnd.apple.mpegurl')
- Mobile: playsInline attribute set, webkit-playsinline set

## Known Issues
- banemedia.com MDM profile blocks saawsedge.com — not a code issue
- ERR_BLOCKED_BY_CLIENT in managed Chrome = MDM/proxy filtering
- Test in clean Chrome profile or Firefox
