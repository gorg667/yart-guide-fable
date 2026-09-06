# Best Live Resin & Live Rosin 510 Carts in Toronto — r/TheOCS Community Guide

A static, dependency-free website ranking every live resin / live rosin 510 cartridge sold on the Ontario legal market (OCS.ca + Toronto retailers), built from a full-archive analysis of **r/TheOCS** (81,698 posts, ~850 cart threads / 36,000+ comments read) cross-referenced with the live **OCS.ca** catalogue.

**Live site:** enable GitHub Pages on this repo (Settings → Pages → Source: `main` / root). No build step; `.nojekyll` is included.

## What's on the site
- **Quick picks** — best overall / indica / sativa / flavour / rosin / budget / balanced / skip
- **Brand report cards** — 2026 trend, hardware, oil, price, customer service for each producer
- **Full rankings** — 43 products & product families with tier (S/A/B/C/AVOID), 0–10 community score, verdict, pros/cons, flavour, effects, hardware, THC/terps, OCS price vs street price, availability, verbatim r/TheOCS quotes with thread links, OCS product link, hibuddy store finder
- **Comparison table** — sortable by tier, score, price, $/g, THC, hardware, online availability
- **Also consider** — AIOs, cured resin and balanced/CBD carts the community recommends alongside 510 LR
- **How to vape live resin** — voltage, batteries, no-preheat, draw technique, storage, returns
- **Glossary** — live resin vs cured vs rosin vs liquid diamonds vs distillate, CRC, "amplified" rosin, Shared vs Wholesale-Only, etc.
- **Where to buy in Toronto**, **FAQ**, **Methodology**

## Repo layout
```
index.html            single-page site
assets/style.css      styles (light/dark, mobile, print)
assets/app.js         renders data/carts.json; filters, search, sortable table
data/carts.json       ALL content: products, tiers, brands, also_consider, guide (tldr/glossary/howto/where/faq/methodology)
research/
  fetch_reddit.py     full r/TheOCS post dump via Arctic Shift API (resumable) → reddit/posts_chunks/
  fetch_priority_threads.py / fetch_ids.py   comment fetchers → reddit/threads/<id>.json
  fetch_ocs.py        OCS.ca Shopify catalogue scrape → ocs/products.json (+ live-carts & rosin collections)
  analyze.py          brand mention/sentiment stats → brand_stats.json
  sku_mentions.py     SKU-level stats → sku_stats.json
  show.py             print a thread's top comments
  reddit_findings.md  ~100 threads of curated qualitative notes (the editorial source for carts.json)
  secondary/notes.md  non-reddit sources
PROGRESS.md           work log / resume instructions
```

## Updating
1. `python3 research/fetch_ocs.py` — refresh prices/availability.
2. `python3 research/fetch_reddit.py posts` then `python3 research/fetch_priority_threads.py` — pull new threads (resumable).
3. Read new threads (`python3 research/show.py <id>`), update `research/reddit_findings.md`, then edit `data/carts.json`.
4. `python3 -m http.server` to preview; commit to `main`.

## Disclaimer
Independent and unaffiliated. Opinions are synthesized from public Reddit discussion and may not reflect current lots. Prices are OCS.ca list prices (pre-tax) as of the `updated` date in `data/carts.json`. Cannabis is legal for adults 19+ in Ontario; buy only from OCS.ca or licensed retailers.
