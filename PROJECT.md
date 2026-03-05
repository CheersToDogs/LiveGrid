# LiveGrid — Project Master Doc
**Last Updated:** 2026-03-04  
**Commit:** 37368f0  
**Live URL:** https://livegrid.pages.dev  
**Repo:** https://github.com/CheersToDogs/LiveGrid (PUBLIC — never commit secrets)  
**Local:** C:\Users\kb\projects\livegrid\index.html  
**Deploy:** Cloudflare Pages — auto-deploys on push to `main` (~60s)

---

## What It Is
Single static HTML file. Multi-stream viewer for Stripchat affiliate revenue.  
HLS streams rendered via hls.js. No backend, no build step, no framework.  
Affiliate links include campaign ID → monetize every click to model rooms.

---

## Architecture
- **File:** `index.html` — everything in one file (CSS, JS, HTML)
- **HLS:** hls.js from CDN, `strictManifestParsing: false` required (EXT-X-MOUFLON tag)
- **API:** `https://go.stripchat.com/api/models` — public, no auth required
- **Deploy:** GitHub push → Cloudflare Pages CI (~60s)
- **Auth:** Cloudflare Worker ready, needs custom domain. See AUTH section.

---

## Features Complete
- Grid selector 1×1 to 6×6
- Gender filter (double-enforced: API param + client-side filter)
- Sort: Most Viewers / Longest Online / Newest
- Tag text filter (Enter to apply)
- Country filter (populated dynamically from API, with flags)
- Quality selector: Original(Max) / 720p / 480p / 240p / 160p
- Affiliate CTA with campaign ID field
- HLS playback, snapshot preload while loading
- Auto-refresh every 60s with progress bar
- Pause/Play All toggle
- Active audio tile → snaps to position [0,0], cyan glow, mutes all others
- Metadata overlay on hover (bottom drawer, JS mouseenter/mouseleave — NOT CSS :hover)
  - Shows: viewers, online time, country (flag), language, toy (lovense etc), favorites, features (VR/Mobile/New), quality badges, clickable tags
- Infinite scroll: fetches 1500 models (3x parallel requests), renders in batches of 16
- Country filter populated from live API data
- Arrow D-pad navigator in header + keyboard arrow keys
- Stats modal (📊): KPIs, gender breakdown, top countries, quality availability, live tag cloud
- Fullscreen pauses others, resumes on exit; HLS recovers from buffer stalls instead of dying
- Parallel fetch: 3 simultaneous API calls (offset 0/500/1000) merged + deduped

---

## Known Issues / Next Chat TODO
- [ ] **Gender filter unreliable** — API sometimes ignores `gender` param; client-side filter is safety net
- [ ] **Language param ignored** — `language=es` on API does nothing server-side; no reliable language filter available
- [ ] **Filter Modal** — replace scattered header filters with a proper modal; full tag browser, quality checkboxes, multi-select tags
- [ ] **People count filter** — solo / couple / group selector if API supports it
- [ ] **Auth** — Cloudflare Worker deployed, needs custom domain to wire up
- [ ] **Custom domain** — separate chat in progress
- [ ] **Stats not live** — stats modal reads from already-fetched `allModels` array, not a separate live query

---

## API Notes — VERIFIED 2026-03-04
**Endpoint:** `https://go.stripchat.com/api/models`

**Confirmed params:**
- `limit` — hard server cap of **500** regardless of what you ask for; default unclear
- `offset` — **works** for pagination; tested 0/500/1000, no meaningful overlap
- `sortBy` — `viewersCount` | `onlineTime` | `new`
- `gender` — `female` | `male` | `couple` | `trans` (unreliable server-side, always filter client-side too)
- `tag` — single tag string
- `language` — **IGNORED** server-side, does not filter results
- `status=public` — filter in code, not param

**Real totals (female, 2026-03-04):** ~7,700 live models. We fetch top 1,500.  
**Pagination strategy:** 3× parallel fetch at offset 0/500/1000, merge+dedup by username.

**Model fields actually returned by API (verified from live response):**
- `id`, `username`, `status`, `gender`
- `modelsCountry` ← **NOT `country`** — normalize on ingest: `m.country = m.modelsCountry`
- `languages` (array, e.g. `["de","en"]`)
- `viewersCount`, `favoritedCount`
- `broadcastHD`, `broadcastVR`, `broadcastMobile`
- `broadcastInteractiveToy` (array, e.g. `["lovense"]`)
- `isNew`, `topBestPlace`
- `stream.urls` — keys: `original`, `480p`, `240p`, `160p` (720p NOT always present)
- `snapshotUrl`, `widgetPreviewUrl`, `popularSnapshotUrl`
- `avatarUrl`, `previewUrl`, `previewUrlThumbBig`, `previewUrlThumbSmall`
- `strict` (boolean)

**Fields that do NOT exist in this API:**
- `country` (use `modelsCountry`)
- `city`, `age`, `ethnicity`, `bodyType`, `hairColor`, `eyeColor`
- `tags`, `categories` (tags come back empty/absent — tag cloud in Stats modal may be sparse)
- `onlineTime`, `liveSince`
- `spokenLanguages`

**Quality keys in stream.urls:** `original`, `480p`, `240p`, `160p`  
`original` = highest available (broadcaster-dependent). `720p` not reliably present.

---

## HLS Notes
- `strictManifestParsing: false` — **required**, Stripchat HLS has non-standard tags
- Buffer: `maxBufferLength: 30`, `maxMaxBufferLength: 60`
- Retries: `manifestLoadingMaxRetry: 4`, `fragLoadingMaxRetry: 6`
- Fatal error recovery: NETWORK → `hls.startLoad()`, MEDIA → `hls.recoverMediaError()`
- `video.waiting` → `hls.startLoad()` to refill buffer proactively
- Fullscreen stall was caused by fatal error handler killing the tile — now recovered gracefully

---

## Auth Status
- **Worker:** `livegrid-gate.kb-a22.workers.dev` — deployed, GATE_PASSWORD secret set
- **Blocker:** Workers cannot intercept `*.pages.dev` — needs custom domain
- **Plan:** When domain acquired → add custom domain to Pages → Worker route intercepts it
- **CF API Token:** in Wrangler env only (not in repo)
- **Do not** re-enable Cloudflare Access (OTP broken on this account)

---

## Critical Rules (DO NOT BREAK)
1. `body` must keep `height: 100vh` — removing breaks tile aspect-ratio
2. `#grid-wrapper` must keep `overflow-y: auto` — removing breaks scroll
3. hls.js config must keep `strictManifestParsing: false`
4. Never commit secrets to repo (repo is public)
5. Always `destroyAll()` HLS instances before re-rendering grid
6. Gender filter must be double-enforced (API param + `.filter(m => m.gender === gender)`)
7. Unmuting one tile must mute ALL others — single audio source only
8. Meta overlay uses JS `mouseenter`/`mouseleave` — do NOT switch back to CSS `:hover` (z-index uncontrollable)
9. `.tile-bottom` z-index: 20, `.tile-top` z-index: 20, `.tile-meta` z-index: 12 — never invert these
10. Always back up before large edits: `copy index.html index.html.bak`

---

## File Structure
```
C:\Users\kb\projects\livegrid\
├── index.html          ← entire app
├── PROJECT.md          ← this file
└── worker\
    ├── index.js        ← Cloudflare Worker password gate
    └── wrangler.toml   ← Worker config (name: livegrid-gate)
```

---

## Cloudflare Account
- **Pages project:** livegrid (livegrid.pages.dev)
- **Worker:** livegrid-gate (livegrid-gate.kb-a22.workers.dev)
- **Zero Trust:** Free plan, team name: livegrid-pages (Access deleted)
- **Account:** Kb@banemedia.com

---

## Commit History (recent)
- `37368f0` — 3x parallel fetch (1500 models), HLS buffer recovery, bigger buffer/retries
- `ea3f976` — meta via JS mouseenter, fix modelsCountry, add toy/favorites/features fields
- `f08c92b` — meta overlay stops above bottom bar, controls z:20, log API fields
- `5a69a1c` — meta overlay bottom drawer, fix unmute btn reference
- `c19a81f` — (baseline this session)
