# LiveGrid Project

## Status
ACTIVE — v1 deployed, revenue-ready

## URLs
- Production: https://livegrid.pages.dev
- Password: livegrid2026
- Repo: https://github.com/CheersToDogs/LiveGrid
- Cloudflare Pages project: `livegrid`

## Owner
Ken Bane / kb@banemedia.com

## Purpose
Affiliate revenue tool. Displays a grid of live free cams from Stripchat. Users click through to models' rooms via affiliate-stamped links. Revenue via Stripchat affiliate program.

## Affiliate Program
- Sign up: https://stripchat.com/affiliate
- Enter campaign ID in Aff. ID field → all CTA links auto-stamp with `?campaign=YOUR_ID`
- Revenue model: CPA / revshare per signup/token purchase

## Current Features
- Grid sizes: 1x1 through 8x8 (up to 64 simultaneous streams)
- Filters: gender, sort order, tag, quality, affiliate ID
- Solo audio toggle (unmuting one mutes all others)
- Affiliate CTA on tile hover
- Auto-refresh every 60 seconds
- Password gate (session-based, client-side)
- Snapshot fallback while HLS loads

## Known Constraints
- kb@banemedia.com managed Chrome profile blocks saawsedge.com via MDM — use clean Chrome profile or Firefox for personal testing
- Password gate is client-side only — not secure against determined attackers, sufficient for obscurity

## Roadmap
- [ ] Pagination / load more button
- [ ] Multi-site support (Chaturbate, MyFreeCams)
- [ ] Click-through analytics dashboard
- [ ] Server-side password protection (Cloudflare Worker)
- [ ] PWA / installable app
- [ ] Mobile layout optimization
- [ ] A/B test CTA copy

## Git Branches
- `main` → production (Cloudflare Pages auto-deploy)
- `staging` → Netlify preview
- `dev` → active development

## Critical Rules
- DO NOT change body/app height or grid-wrapper overflow — breaks tile aspect-ratio sizing
- Test all CSS changes in clean Chrome profile before pushing to main
- Always revert via `git checkout <good-commit> -- index.html` if broken
