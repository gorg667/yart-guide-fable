# PROGRESS LOG — Toronto Live Resin/Rosin Cartridge Guide

> **READ THIS FIRST if you are a fresh instance after context compaction / account switch.**
> This file is the single source of truth for what has been done, what's in flight, and what's next.
> Update it after every meaningful step and `git push origin main` immediately. No branches, no PRs — commit straight to `main`.

## Task (verbatim intent)
- Research the **best live resin / live rosin 510 cartridges available in Toronto (Ontario, OCS legal market)**.
- **Primary source MUST be r/TheOCS** (reddit). Find a way to access it (old.reddit, .json endpoints, redlib/libreddit mirrors, pullpush.io archive, Google cache, etc.).
- Deliverable: a **static website** (pragmatic, functional design), **hostable on GitHub Pages**, with a detailed, comprehensive guide/review of the best carts.
- Git: **commit straight to `main`, no branches, no PRs.** Push incrementally.
- Document reasoning in this file so a compacted-context instance can continue.

## Repo
- GitHub: https://github.com/gorg667/yart-guide-fable (user gorg667)
- Local: /home/user/webapp
- Site will live in repo root (index.html etc.) so GitHub Pages can serve from `main` / root.

## Plan
1. [x] Set up repo + this progress file
2. [ ] Access r/TheOCS — test methods (old.reddit .json, redlib mirrors, pullpush.io, web_search)
3. [ ] Gather raw reddit data → save to `research/reddit/*.json|md` (commit raw data so it's never lost)
4. [ ] Identify candidate brands/products (live resin + live rosin 510 carts on OCS)
5. [ ] Per-product deep dive: reddit sentiment, effects, hardware, price, availability at OCS/Toronto stores
6. [ ] Cross-check with OCS.ca product pages, Leafly/Weedmaps CA, other review sites
7. [ ] Write structured data file `data/carts.json`
8. [ ] Build static site (index.html, css, js) — reads data, sortable/filterable table + detailed cards + methodology + FAQ
9. [ ] Add `.nojekyll`, verify Pages-compatible, push
10. [ ] Final QA

## Research notes (append as you go)

### r/TheOCS ACCESS METHOD (SOLVED)
- reddit.com / old.reddit / api.reddit / .json → 403 from sandbox AND from crawler tool. r.jina.ai → 403. pullpush.io → 429 (blocks agents). redlib mirrors → Anubis bot challenge or 403.
- **WORKING: Arctic Shift API** (Pushshift successor, full archive incl. recent posts):
  - Posts: `https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=TheOCS&title=live%20resin&limit=100`
    - params: subreddit, title, body (or query), author, after/before (unix), limit (max 100), sort=desc, link_id for comments
  - Comments: `https://arctic-shift.photon-reddit.com/api/comments/search?subreddit=TheOCS&link_id=<post_id>&limit=100`
  - Rate-limited: returns 422 "Timeout. Maybe slow down" → sleep 2-5s between requests, retry.
  - Docs: https://arctic-shift.photon-reddit.com/api
- Script: `research/fetch_reddit.py` saves raw JSON to `research/reddit/`.


## Status log
- 2026-09-06 01:05 — Fresh start. Repo empty. Created PROGRESS.md.

### OCS catalog (DONE)
- OCS.ca is Shopify; `https://ocs.ca/collections/510-thread-cartridges/products.json?limit=250&page=N` works directly (needs browser UA).
- `research/fetch_ocs.py` → `research/ocs/products.json` (793 vape products incl. disposables).
- Filtered 510 live/resin/rosin candidates → `research/ocs/candidates_510_resin_rosin.{json,csv}` (316 rows). Key tags: `subsubcategory` ∈ {Live Cartridges(101), Resin Cartridges(97), Rosin Cartridges(7), Distillate(225), CO2(25)}; `extraction_process`, `drying_method` (Fresh Frozen = true "live"), `availability` (online/in-store), `assortment` (Shared = sold online on OCS.ca; "Wholesale Only" = only via retail stores).
- NOTE: OCS tagging is noisy (e.g. some liquid-diamond distillate tagged "Live"). Verify by product description text + reddit.
- NOTE: Rosin 510 carts are RARE on OCS: only 7 tagged (Connoisseur Culture Hash Rosin, Contraband Live Rosin Guava CKE, Frootyhooty Live Rosin+diamonds x2, + others - check csv).
- OCS official collection `https://ocs.ca/collections/live-carts/products.json` → `research/ocs/collection_live_carts.json` (153 products; 84 are 510 carts). This is the authoritative universe of "live" 510 carts on OCS. Brands: Tribal(11 SKUs), IRIS Labs(5, incl ZODA), EastCann(4), Carmel(4), Lord Jones(4 LD x live resin), Purple Hills(4), Shed Boyz(4), VERO(4), The Loud Plug(4), Frootyhooty(3 rosin+LD), FOUR54(2), Lune Rise(2), Redecan Amped(2), Sherbinskis(2), Jonny Chronic(2), DEBUNK(2), Pura Vida(2), Syrup(2), (GAS)(2); singles: Ambr, Roilty, Qwest, Pepe, Fume, GREAZY, Kolab Liquid Live Resin, Weed Me Max, Vape Breton, Endgame Acai Blxst, JAYS, Contraband Live Rosin, Sauce Rosin Labs, PURE ROSIN, The Goo! rosin, Port North rosin syrup, Connoisseur Culture hash rosin (not in live collection but rosin-tagged), Countryside Live Terp Sauce, Orchid CBD, Bleuh, Queen of the Underground.
- Reddit full dump strategy changed: dump ALL r/TheOCS posts (limit=auto ≈500/page) to `research/reddit/posts_chunks/`, then filter locally & fetch comments to `research/reddit/threads/`. Resumable via `research/reddit/state.json`. Log: research/fetch_posts.log

## RESUME CHECKLIST (after compaction / account switch)
1. `cd /home/user/webapp && git status && git log --oneline -3`
2. Background fetchers DIE on account switch. Restart both (both are resumable/idempotent):
   - `nohup python3 research/fetch_reddit.py posts >> research/fetch_posts.log 2>&1 &`  (full post dump; done when log says "DONE full dump")
   - `nohup python3 research/fetch_priority_threads.py >> research/fetch_priority.log 2>&1 &` (comments for cart-relevant threads, biggest first → research/reddit/threads/)
3. Read threads with `python3 research/show.py <id>[,<id>...] [n_comments]`; append findings to `research/reddit_findings.md`; commit+push often.
4. Steps done so far: OCS catalog ✔, reddit access ✔, ~25 key threads read & noted. NEXT: keep reading (esp. rosin carts, Purple Hills, Tribal, Kolab, Lune Rise, Wildcard, Woody Nelson, Sherbinskis, Lord Jones, brand-specific threads), then quantitative brand-mention analysis (`research/analyze.py` — TODO), then data/carts.json, then site.

## Status update
- Reddit corpus: 81,698 posts (full sub dump), ~760 threads with comments (~36k comments). `research/reddit_findings.md` = curated qualitative notes (~90 threads read in depth). `research/brand_stats.json` (analyze.py) and `research/sku_stats.json` (sku_mentions.py) = quantitative mention/sentiment counts (CAVEAT: SKU regexes also match flower of the same strain name e.g. Gas Face, Permanent Marker, Rainbow Driver, Comatose — treat as indicative; note in methodology).
- Priority comment fetcher still running in background (resumable). Not required to finish before building site.
- NEXT STEP: build `data/carts.json` (structured per-product entries with tier, verdict, pros/cons, effects, flavour, hardware, price, OCS availability, reddit citations) then the static site. Then final QA + push.
- 2026-09-06: data/carts.json COMPLETE (43 products, 14 also_consider, guide sections). NEXT: build static site (index.html + assets/style.css + assets/app.js) reading data/carts.json; .nojekyll; README. Then QA via GetServiceUrl, push.

## 2026-09-06 — SITE BUILT
- index.html, assets/style.css, assets/app.js, data/carts.json (43 products, 10 brand cards, 14 also-consider, guide), .nojekyll, README.md — all committed to main.
- QA: renders with zero console errors; filters/search/sort verified with Playwright; desktop + mobile screenshots OK.
- Remaining optional polish: keep reading new threads and refine scores; add per-strain effect tags; nothing blocking.
- GitHub Pages: user must enable in repo Settings → Pages → Deploy from branch `main` / `/ (root)`.
