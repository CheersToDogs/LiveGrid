# LiveGrid — Next Chat Rotation Prompt
**Session hash:** `4a2adad1fb6eec628be39bcc9442ed9127eea4615331ceb3cff8a7d94e7bebdc`
**Generated:** 2026-03-04

## Session Start Protocol
1. Load hash above via KBMCP:hash_project_save_session_v2
2. Read C:\Users\kb\projects\livegrid\PROJECT.md
3. git log --oneline -5
4. Confirm live URL matches commit before touching anything

## All Bugs Fixed — Do Not Re-Fix
- Meta overlay: JS mouseenter/mouseleave, z-index:12, bottom:44px
- Unmute: explicit btn ref via unmuteTile(tile, explicitBtn)
- Country: model.modelsCountry normalized to model.country on ingest
- Fetch: 3x parallel offset 0/500/1000 = 1500 models
- Fullscreen: HLS fatal error recovery, buffer 30/60s

## Build Order This Session
1. Viewport pause/resume (IntersectionObserver per tile, 2s debounce)
2. Diff-based auto-refresh (no more destroyAll on 60s tick)
3. Favorites + offline tracking (localStorage, 5min watcher, pattern detection)
4. Load All 7700 (paginate until response.count < 500, batch 5 at a time)
5. Vision scanner (Python/AWS/SQLite — separate from app, design in session hash)

## See NEXT_CHAT asset in hash store for full specs.
