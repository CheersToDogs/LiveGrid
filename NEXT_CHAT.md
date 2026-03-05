
# NEXT CHAT ROTATION — LiveGrid Phase 4
**Date:** 2026-03-05 | **Commit:** a1911c6 | **Hash:** edfab5019bbf1fc3ab60235f46c38fbe64a2816228fde50db5f21d61cffcd800

## Status
- 3 AWS services running: livegrid-scanner, livegrid-api (port 8765 localhost), livegrid-cam
- CAMS tab live in frontend but showing "API unavailable" — port 8765 not exposed yet
- All emoji/symbol bugs fixed, unmute snapshot bleed fixed
- **ENCODING RULE (DO NOT BREAK):** All file edits use Python string ops. Never PowerShell Set-Content on unicode files.

## Task 1 — Cloudflare Tunnel (do first, 5 min)
Expose port 8765 to livegrid.pages.dev frontend.
```
# On AWS:
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb
cloudflared tunnel login
cloudflared tunnel create livegrid-api
cloudflared tunnel route dns livegrid-api api.livegrid.pages.dev  # or whatever domain
# Create config, run as service
```
Then update `VISION_API` const in index.html from `http://98.95.155.84:8765` to the tunnel URL.

## Task 2 — Fullscreen Priority + Buffer Management
**Goal:** Fullscreen tile monopolizes bandwidth. Others freeze (not destroy).

**Implementation:**
```javascript
// Per-tile: wire to video element
video.addEventListener('fullscreenchange', () => {
  if (document.fullscreenElement === video) {
    setFullscreenPriority(hls);
  } else {
    clearFullscreenPriority();
  }
});

function setFullscreenPriority(activeHls) {
  // Freeze all other HLS instances
  hlsInstances.forEach(h => {
    if (h !== activeHls) h.stopLoad();
  });
  // Boost active tile buffer
  activeHls.config.maxBufferLength = 30;
  activeHls.config.maxMaxBufferLength = 60;
}

function clearFullscreenPriority() {
  // Restore all visible tiles
  hlsInstances.forEach(h => h.startLoad());
  // Re-run viewport observer to re-pause out-of-view tiles
  setupViewportObserver();
}
```
**HLS config tiers:**
- Normal: maxBufferLength:10, maxMaxBufferLength:20
- Active audio: maxBufferLength:15, maxMaxBufferLength:30  
- Fullscreen: maxBufferLength:30, maxMaxBufferLength:60
- Background (viewport): stopLoad() — resumes on startLoad(), no stream loss

## Task 3 — Security Audit
Review in this order:

1. **AWS security groups** — `aws ec2 describe-security-groups` or check console. Should be 22+443 only. Port 8765 must NOT be open to 0.0.0.0/0.
2. **API auth** — /cams and /vision have zero auth. Add CF-Access or static `X-API-Key` header check in FastAPI before tunnel goes live.
3. **SSRF** — cam_scanner.py fetches `snapshot_url` from insecam HTML directly. Attacker who injects a URL into the DB gets server-side fetch. Mitigate: allowlist URL patterns (must match `http://{ip}:{port}/...`, block RFC1918 ranges).
4. **CORS** — `allow_origins=["*"]` in api.py. Lock to `["https://livegrid.pages.dev"]`.
5. **Rate limiting** — add `slowapi` or simple in-memory counter to FastAPI.
6. **Secrets hygiene** — verify `vision/.env` not in git: `git log --all -- vision/.env`
7. **Snapshot proxy SSRF** — `/cams/{id}/snapshot` serves whatever is in `snapshot_url` column. Same SSRF risk as above if DB tampered.
8. **CSP** — add `_headers` file to CF Pages repo with Content-Security-Policy.
9. **Affiliate links** — `buildAffUrl` appends user-supplied `affId` to URL. Sanitize.

## File Edit Rule
```python
# ALWAYS edit index.html like this:
with open(r'C:\Users\kb\projects\livegrid\index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8')
text = text.replace('OLD', 'NEW')
with open(r'C:\Users\kb\projects\livegrid\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
# Then: git add index.html && git commit && git push
```

## Context
- Repo: https://github.com/CheersToDogs/LiveGrid
- Live: https://livegrid.pages.dev  
- AWS: 98.95.155.84 (ubuntu)
- Vision API: http://98.95.155.84:8765 (localhost only until tunnel)
- DB: ~/projects/livegrid/vision/vision.db
- Session hash: edfab5019bbf1fc3ab60235f46c38fbe64a2816228fde50db5f21d61cffcd800
