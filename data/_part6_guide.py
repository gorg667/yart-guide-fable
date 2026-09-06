import json
d=json.load(open('data/carts.json'))

d["guide"]={
 "tldr":[
  {"label":"Best overall","pick":"FOUR54 Emerald Triangle (rotating strain)","why":"Atlanticann resin in the best ceramic XL hardware for $39.95 — the sub's most repeated recommendation in 2026.","id":"four54-emerald-triangle"},
  {"label":"Best flavour + reliability","pick":"Iris Labs Fantasm","why":"Orange-creamsicle live resin in bulletproof ceramic hardware; 'never clogged, never burnt'.","id":"iris-fantasm"},
  {"label":"Best indica / night","pick":"Iris Labs Blackwater","why":"OG-kush gas, sleep-mode heavy; the hardest-hitting Iris.","id":"iris-blackwater"},
  {"label":"Best sativa / daytime","pick":"EastCann Mango Sour (or Iris Cherry Bang Bang)","why":"Clean functional uplift with no crash at $39.95; CBB is the newer, more energetic alternative.","id":"eastcann-mango-sour"},
  {"label":"Best flavour, period","pick":"EastCann Frozen Lemons","why":"'Like eating candy'; social, clear-headed.","id":"eastcann-frozen-lemons"},
  {"label":"Hardest hitter","pick":"Tribal Triple Burger (or Kolab Motorbreath)","why":"GMO gas that 'sends people to a coffin'; Motorbreath for a faster head rush in tank hardware.","id":"tribal-triple-burger"},
  {"label":"Best Tribal all-rounder","pick":"Tribal Bubble Up / Neon Sunshine","why":"The two Tribal SKUs with the most consistent love; Bubble Up heavier, Neon Sunshine brighter.","id":"tribal-bubble-up"},
  {"label":"Best live rosin 510","pick":"Sauce Rosin Labs Solventless Live Rosin (0.5g)","why":"The only rosin cart with a sustained top reputation; ceramic hardware now improved.","id":"sauce-rosin-labs"},
  {"label":"Best value rosin","pick":"Connoisseur Culture Hash Rosin 1g (~$40) / Port North Syrup 0.5g (~$30)","why":"Full gram of real hash rosin in great ceramic hardware; Port North for cheapest entry.","id":"connoisseur-culture"},
  {"label":"Best budget live resin","pick":"Jonny Chronic Acapulco Gold ($37.65) / Debunk on sale ($33–38)","why":"Confirmed 100% LR at 20–25% below Tribal; Debunk if your store takes returns.","id":"jonny-chronic"},
  {"label":"Best cured resin","pick":"1964 Comatose (or 67 Sins Gas Face)","why":"'A veil of happiness'; heavy OG effects despite low terp numbers.","id":"1964-comatose"},
  {"label":"Best balanced / CBD","pick":"Orchid CBD RNTZ (60% THC) or Bleuh Wildberry (30% THC / 48% CBD)","why":"Pure live resin with CBD for anxiety-free daytime use.","id":null},
  {"label":"Skip","pick":"Lord Jones LD x LR, The Loud Plug, Coterie, -ness, Ambr Papaya, Qwest, Roilty, Frootyhooty 'Amp'd', any 'liquid diamonds' cart","why":"Mostly distillate / botanical terps sold at live-resin prices, or chronic hardware + service failures.","id":"lord-jones"}
 ],
 "glossary":[
  {"term":"Live resin","def":"Hydrocarbon (butane/propane) extract made from FRESH-FROZEN plants — never dried or cured — so volatile terpenes survive. 'Pure' or '100%' live resin carts contain only that extract (ingredients: 'cannabis extract'). Typical THC 70–85%, terps 8–20%."},
  {"term":"Cured resin / FSE","def":"Same hydrocarbon process but from dried, cured flower. Slightly fewer volatile terps; many users find the effect heavier. 1964, 67 Sins, Pure Sunfarms, Wildcard Small Batch and 3Saints are cured. 'FSE' (full-spectrum extract) is a marketing term for any un-distilled resin; 1964 uses it for cured resin that stores often mislabel as 'live'."},
  {"term":"Live rosin","def":"Solventless: fresh-frozen flower → ice-water hash → pressed with heat and pressure. Lower yield, higher cost (usually 0.5g carts at the price of 1g resin), thicker oil that is hard on hardware. 'Cured hash rosin' uses dried flower. Rosin can't be CRC'd or hide bad inputs."},
  {"term":"Liquid diamonds","def":"THCa crystals melted/decarboxylated into liquid, usually with terpenes added back. Community consensus: functionally distillate-grade THC (90–99%) with none of the minor cannabinoids of resin — 'a marketing term for distillate'. Many 'live resin x liquid diamonds' carts are mostly diamonds."},
  {"term":"Distillate ('disty')","def":"THC purified to 85–99%, flavourless, then re-flavoured with botanical or cannabis-derived terpenes. One-dimensional head spike, quick fade, throat scratch for many. r/TheOCS rule #1: 'never distillate'."},
  {"term":"Botanical terpenes","def":"Terpenes sourced from non-cannabis plants and added for flavour. If 'terpenes' or 'botanical terpenes' appear in the ingredients, the cart is not pure live resin — even if the front says 'Pure Live Resin' (e.g., Ambr Papaya)."},
  {"term":"CRC (colour remediation column)","def":"Filtration that removes lipids, waxes and dark colour from resin, yielding lighter, thinner oil that wicks better and clogs less in 510 hardware. Tribal, Iris, Jonny Chronic and Pepe CRC their carts; Carmel does not (darker oil). Purists argue it strips character; pragmatists accept it as a hardware trade-off."},
  {"term":"Amplified / Amp'd rosin","def":"A little rosin cut with distillate and flavouring so a 1g cart can be sold as 'rosin'. Frootyhooty's line is the main example. Not the same thing as a pure rosin cart."},
  {"term":"AIO","def":"All-in-one disposable with built-in battery. Not a 510 cart, but several AIOs (67 Sins Gas Face, Redecan Legit LR, 1Above Juice Bar, Northern Canna Permanent Marker) are among the community's favourite vapes."},
  {"term":"Rotating SKU","def":"A product name that stays the same while the strain inside changes by lot (FOUR54 Emerald Triangle / Route 66, Lune Rise Farmers' Market, Sauce Rosin Labs, Woody Nelson Country Club, Wildcard Small Batch). Always check the strain and package date."},
  {"term":"Active / EZCP hardware","def":"The postless full-ceramic 1.2Ω cartridge platform used by FOUR54, EastCann, Iris (branded 'Active EZCP'), Greazy, Bleuh and now Carmel. Wide airflow, low-voltage friendly, very low failure rate. The community's 2026 hardware benchmark."},
  {"term":"Shared vs Wholesale Only","def":"OCS.ca sells 'Shared' SKUs online; 'Wholesale Only' SKUs are shipped only to retail stores. Many top carts (Tribal GT, Kolab Motorbreath, Lune Rise, Sauce Rosin Labs, Purple Hills XL) are store-only — use hibuddy.ca to locate them."}
 ],
 "howto":[
  {"h":"Use a variable-voltage battery","p":"Stick pens with 3 colour settings run too hot for live resin even on 'low'. Buy a Yocan Kodo Pro (~$15–20), Yocan Uni Pro / Tribal Uni Pro Arc (~$30–40, tougher, retracting cart) or similar with a voltage display. Note: the Kodo Pro's small air intakes can be partly blocked by wide FOUR54/Greazy carts — the Uni Pro is safer for XL carts."},
  {"h":"Run 1.8–2.2 V (2.4 V max)","p":"The single most repeated piece of advice on the sub. Start at 1.8 V for flavour; most settle at 2.0–2.2 V; going above 2.4 V tastes 'muddy', burns terps and darkens the coil. Packaging often lists a recommendation (Tribal 2.4 V; 1964 2.4 V; Debunk 2.5 V) — enthusiasts run lower."},
  {"h":"Do NOT preheat live resin","p":"Live resin is already fluid. Preheating cooks the oil and is a leading cause of clogs and burnt cotton. Instead, hold the button 1–2 s before drawing if the room is cold. Rosin carts are the exception — a short preheat can help thick rosin."},
  {"h":"Short, gentle draws","p":"3–5 second pulls, inhale, exhale right away (holding does nothing but cook your lungs), wait 20–30 s between hits. 'Sip, don't rip.' Hauling hard pulls oil into the airway → gurgle → clog → leak. This fixes 90% of 'this cart sucks' complaints."},
  {"h":"Store upright, cool, capped","p":"Leaving carts on their side, in a hot car, or in a pocket uncapped is behind most leaks and the 'coffee-coloured resin' photos. Remove the cart while charging the battery. Re-cap the mouthpiece (it also cuts smell)."},
  {"h":"Check the label before paying","p":"Ingredients should read only 'cannabis extract'. THC above ~88% means diamonds/distillate, not resin. Look for a package date under ~6 months. For rotating SKUs check which strain is inside."},
  {"h":"Returns are easy for vapes","p":"Defective (clogged, leaking, burnt) carts are the easiest OCS credit for retailers to get — return to the store with the packaging. Brands with good direct CS per the sub: Iris Labs, Tribal, Sauce Rosin Labs, Kolab, Carmel (recent), Purple Hills; poor: Woody Nelson, Debunk, Greazy, Lord Jones, The Loud Plug."},
  {"h":"Tolerance","p":"If nothing 'hits' anymore, no cart will fix it. Live resin builds slower and steadier than distillate — heavy distillate users often need a T-break or a week on flower before LR feels strong again."}
 ],
 "where":[
  {"name":"OCS.ca","note":"Every 'Shared' SKU at list price, delivered. Good for Iris/EastCann/FOUR54/Tribal/1964/Carmel/Jonny Chronic. Vape returns handled via CS."},
  {"name":"hibuddy.ca","note":"Live inventory + price comparison across Ontario stores. The sub's standard tool for finding store-only carts (Kolab Motorbreath, Sauce Rosin Labs, Lune Rise, Tribal GT, Purple Hills XL) and the cheapest price on the same cart ($34–50 spread is common)."},
  {"name":"Toronto stores mentioned positively on r/TheOCS","note":"Cannabis Hut (Coxwell) — carries Iris Labs & Sauce Rosin Labs; Premium Cannabis (Danforth) — good prices; Vege Cannabis (Dundas W) — rosin selection; Cookies Toronto — Sauce Rosin Labs; Greenline Cannabis — FOUR54/Iris ~$37; chains (Canna Cabana, Value Buds, Tokyo Smoke) carry Tribal/Redecan/Lord Jones and accept returns, but the sub is critical of chain staff and pricing."}
 ],
 "faq":[
  {"q":"Is live resin really better than distillate?","a":"For most of r/TheOCS, yes: fuller, longer, more 'like flower' effects, far less throat irritation, and real strain flavour. A minority with high tolerance still prefer distillate's hard spike. Live resin costs $5–15 more per gram."},
  {"q":"Live resin vs live rosin in a cart?","a":"Rosin is solventless and often described as a more 'submerged', well-rounded high, but it comes in 0.5g at the price of 1g resin and historically vaped poorly in 510s. Sauce Rosin Labs and Connoisseur Culture are the exceptions worth buying; many rosin fans prefer AIOs (1Above, Invader, SUGR)."},
  {"q":"Why do Tribal carts clog?","a":"Tribal uses a Yocan-made metal/cotton cart with a narrow mouthpiece. It performs well with fresh, high-terp lots at ≤2.3 V and short draws, but the last third often gets sticky. Iris/FOUR54/EastCann ceramic carts clog far less — that hardware gap is the main reason the sub has shifted to Atlanticann since 2025."},
  {"q":"Are Iris Labs, EastCann and FOUR54 the same?","a":"All three are Atlanticann brands (Nova Scotia); Iris Labs does the extraction. Same resin quality, different hardware and pricing: FOUR54 = wide 'Active' XL ceramic, $39.95; EastCann = ceramic, $39.95–44.95; Iris = longer ceramic with orange tip, $44.95. Buy whichever has the strain/price you want."},
  {"q":"Why is my cart only 3/4 full?","a":"Normal. A 1g fill sits below the top of a 1.2g-capacity cart. Carmel, Debunk and others have had to explain this repeatedly."},
  {"q":"Why did my Purple Hills / Tribal cart taste different from last time?","a":"Live resin varies lot to lot — terpene profiles shift with each grow (Blackwater lost its myrcene between Jul and Sep 2025; Orangeade's dominant terp changed). Check package dates and lot numbers; the sub's batch-specific threads are searchable."},
  {"q":"Does THC % matter?","a":"Barely, for resin. 1964 Comatose lists ~2.7% terps and 75–84% THC yet is one of the heaviest carts on the market; Kolab Motorbreath at 66–69% THC 'hits harder than anything'. Terp content, strain and freshness matter more. THC above 90% signals distillate/diamonds."},
  {"q":"What voltage for rosin carts?","a":"1.8–2.2 V, short 3–5 s draws, 30 s between, keep under 25 °C. Some rosin carts need a brief button press to loosen the oil. Never above 2.4 V."}
 ],
 "methodology":[
  "Primary source: r/TheOCS. We pulled the complete post archive (81,698 posts, Oct 2018 – Sep 2026) via the Arctic Shift Reddit archive API, plus full comment trees for ~850 cart-relevant threads (~36,000 comments). Direct reddit.com access is blocked for scrapers, so the archive mirror was used; content is identical.",
  "We read every high-engagement 'best cart' / 'favourite live resin' / 'best rosin cart' thread from 2025–2026 (and the major 2024 ones for trajectory), every brand-specific review thread with ≥5 comments for the shortlisted brands, and the label-controversy threads (Coterie, -ness, Ambr, Qwest, Lord Jones).",
  "Product universe: OCS.ca catalogue scraped 2026-09-06 (793 vape SKUs; 84 live-resin/rosin 510 carts in the official 'live carts' collection; 9 rosin carts). Prices, THC ranges, extraction/drying tags and online availability come from OCS.ca.",
  "Tiers and scores are editorial syntheses of (a) how often and how positively a product is recommended in 'best' threads, weighted toward 2026, (b) hardware reliability reports, (c) label honesty, (d) price. Quantitative mention/sentiment counts (research/brand_stats.json, research/sku_stats.json) informed but did not determine rankings — strain names collide with flower posts, and Reddit voting is noisy.",
  "Quotes are verbatim (lightly trimmed) with the thread ID; open any thread at reddit.com/r/TheOCS/comments/<id>/. Upvote counts are as archived.",
  "Limitations: Reddit skews toward enthusiasts and heavy users; brand reps and possible astroturfing exist (the sub's own bots warn about this); lot-to-lot variance is large; prices change weekly; rotating SKUs change strain. Treat this as a well-informed starting point, not gospel."
 ]
}
json.dump(d,open('data/carts.json','w'),indent=1,ensure_ascii=False)
print("ok", len(d['guide']['glossary']), len(d['guide']['faq']))
