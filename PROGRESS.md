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
(nothing yet)

## Status log
- 2026-09-06 01:05 — Fresh start. Repo empty. Created PROGRESS.md.
