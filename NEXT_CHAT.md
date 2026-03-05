# 🔄 CHAT ROTATION - CONTINUATION
**Project:** livegrid | **Phase:** 3 | **Rotation:** #1
**Reason:** Session complete, context limit approaching

## Summary
LiveGrid vision scanner shipped and running on AWS. Two systemd services live: `livegrid-scanner` (50 models/5min, Haiku 4.5, $0.0215/cycle, $2/day cap) and `livegrid-api` (FastAPI port 8765). SQLite DB with scans + spend_log tables. Vision API returns hair_color, hair_length, body_type, apparent_age_range, activity, setting, is_explicit, confidence per username. Ken also had a voice strategy session (see hash) covering vibe-based discovery UI, freemium model, and a SECOND separate frontend concept: insecam-style unsecured live cam grid with motion detection + LLM interest scoring.

## Key Decisions
- Vision scanner: Haiku 4.5, real cost $0.00043/scan, 50 models MVP, expand later
- API endpoint: http://[AWS_IP]:8765 — needs to be wired into LiveGrid frontend
- Insecam grid: SEPARATE frontend, NOT merged with LiveGrid (different product)
- Motion detection first (OpenCV frame diff, cheap) BEFORE LLM vision on cams
- Cam LLM vision LATER — prove motion detection works first
- Vibe clusters: emergent, not hardwired — let LLM discover patterns over time
- Business: aggregator model, freemium, affiliate %, mobile-first, social ads

## Open Questions
- What is the AWS public IP/port exposure for port 8765? (currently localhost only — needs nginx or tunnel for frontend to reach it)
- Shodan API key for cam discovery, or use public insecam-style lists?
- Separate domain for cam grid, or subdomain of livegrid?

## Next Steps (IN ORDER)
1. **Wire vision API into LiveGrid frontend** — on tile hover meta panel, fetch `/vision/{username}`, show hair/body/activity/setting if scanned_at is recent (<30min). Show "scanning…" if no data yet.
2. **Update PROJECT.md on AWS** with vision scanner facts, API endpoint, DB schema
3. **Expose vision API publicly** — nginx reverse proxy or Cloudflare tunnel so livegrid.pages.dev JS can call it (CORS already configured in api.py)
4. **NEW: Insecam-style cam grid frontend** (separate HTML file, separate deployment)
   - Source: start with public insecam directory scraping OR Shodan API
   - Motion detection: Python script, OpenCV frame diff on RTSP/HTTP streams
   - Change detection output: {stream_url, status: live/dead/active, last_activity, interest_score}
   - Simple grid UI: same aesthetic as LiveGrid, show live/dead/active badge
   - NO LLM vision yet — motion detection MVP first
5. **LLM vision on cams** (LATER) — only after motion detection proven, interest scoring pipeline

## Current State
- LiveGrid: https://livegrid.pages.dev (commit 8d83ca1) — all 4 features from this session live
- Vision scanner: running on AWS 98.95.155.84, port 8765 (localhost only)
- vision.db: 50 scans, $0.0215 spent today
- Files: ~/projects/livegrid/vision/scanner.py, api.py, vision.db, .env

## Full Context
`hash_retrieve_content_v2("3cb5216b1099")`

## Session Hash (vision scanner checkpoint)
`hash_retrieve_content_v2("cbc3114401de")`
