/* Static, dependency-free renderer for data/carts.json (GitHub Pages friendly). */
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const redd = id => `https://www.reddit.com/r/TheOCS/comments/${id}/`;
  const TIER_ORDER = { S: 0, A: 1, B: 2, C: 3, AVOID: 4 };

  function typeClass(p) {
    const t = (p.type || "").toLowerCase();
    if (/rosin/.test(t) && !/amp/.test(t) && !/mislabel|blend/.test(p.name.toLowerCase())) return "rosin";
    if (/cured|fse/.test(t) && !/live resin/.test(t)) return "cured";
    if (/distillate|diamond|blend|mislabel|botanical/.test(t) || p.tier === "AVOID" && /blend|diamond|distillate/.test(t)) return "blend";
    return "live";
  }
  function leanClass(p) {
    const l = (p.leaning || "").toLowerCase();
    const ind = /indica|night|sleep|sedat/.test(l), sat = /sativa|day|stimul/.test(l);
    if (ind && sat) return "hybrid"; if (ind) return "indica"; if (sat) return "sativa"; return "hybrid";
  }
  function thcMin(p) { const m = String(p.thc || "").match(/(\d+(\.\d+)?)/); return m ? parseFloat(m[1]) : 0; }
  function onlineOCS(p) { return /OCS\.ca online|OCS\.ca \(|OCS\.ca \+|OCS\.ca online/i.test(p.availability || "") && !/Wholesale Only\)?$/.test(p.availability || "") || /^OCS\.ca/.test(p.availability || ""); }

  let DATA, PRODUCTS;

  fetch("data/carts.json").then(r => r.json()).then(d => {
    DATA = d; PRODUCTS = d.products.slice();
    PRODUCTS.forEach(p => { p._type = p.kind || typeClass(p); p._lean = p.lean || leanClass(p); p._thc = thcMin(p); p._online = (p.on_ocs_online != null) ? p.on_ocs_online : onlineOCS(p); });
    renderStats(); renderTldr(); renderBrands(); renderTierKey(); renderCards(); renderTable(); renderAlso(); renderGuide();
    $("#footer-meta").textContent = `Last updated ${d.meta.updated}. ${d.meta.price_note} ${d.meta.disclaimer}`;
    wire();
    if (location.hash) setTimeout(() => { const el = $(location.hash); if (el) el.scrollIntoView(); }, 50);
  }).catch(e => { $("#cards").innerHTML = `<p class="muted">Could not load data/carts.json (${esc(e.message)}). If you opened this file directly, serve it over HTTP (e.g. GitHub Pages or <code>python3 -m http.server</code>).</p>`; });

  function renderStats() {
    const m = DATA.meta;
    $("#stats").innerHTML = [
      [m.reddit_posts_scanned.toLocaleString(), "r/TheOCS posts scanned (full archive)"],
      [m.reddit_threads_read.toLocaleString() + "+", "cart threads with comments read"],
      [m.reddit_comments_indexed.toLocaleString(), "comments indexed"],
      [m.ocs_live_510_skus, "live resin/rosin 510 SKUs on OCS"],
      [DATA.products.length, "products & product families ranked"],
      [m.updated, "last updated"]
    ].map(([b, s]) => `<div class="stat"><b>${esc(b)}</b><span>${esc(s)}</span></div>`).join("");
  }

  function renderTldr() {
    $("#tldr-grid").innerHTML = DATA.guide.tldr.map(t => {
      const cls = /^skip/i.test(t.label) ? " skip-card" : "";
      const link = t.id ? `<a href="#p-${esc(t.id)}">${esc(t.pick)}</a>` : esc(t.pick);
      return `<div class="tldr${cls}"><div class="lbl">${esc(t.label)}</div><div class="pick">${link}</div><div class="why">${esc(t.why)}</div></div>`;
    }).join("");
  }

  function renderBrands() {
    const tb = $("#brand-table tbody"); if (!tb || !DATA.brands) return;
    tb.innerHTML = DATA.brands.map(b => `<tr style="cursor:default"><td><strong>${esc(b.brand)}</strong></td><td>${esc(b.tier).split(/\s*\/\s*/).map(t => { const k = t.match(/^(S|A|B|C|AVOID)/); return k ? `<span class="badge ${k[1]}">${esc(t)}</span>` : esc(t); }).join(" ")}</td><td>${esc(b.trend)}</td><td>${esc(b.hardware)}</td><td>${esc(b.oil)}</td><td>${esc(b.price)}</td><td>${esc(b.cs)}</td><td>${esc(b.summary)}</td></tr>`).join("");
  }
  function renderTierKey() {
    $("#tier-key").innerHTML = Object.entries(DATA.tiers).map(([k, v]) => `<span><span class="badge ${k}">${k}</span>${esc(v)}</span>`).join("");
  }

  function filtered() {
    const q = $("#q").value.trim().toLowerCase(), ty = $("#f-type").value, le = $("#f-lean").value, ti = $("#f-tier").value, on = $("#f-online").checked, so = $("#sort").value;
    let list = PRODUCTS.filter(p => {
      if (ty && p._type !== ty) return false;
      if (le && p._lean !== le && !(le === "hybrid" && p._lean === "hybrid")) return false;
      if (ti && p.tier !== ti) return false;
      if (on && !p._online) return false;
      if (q) { const hay = [p.brand, p.name, p.current_strain, p.flavour, p.effects, p.verdict, p.leaning, p.type, p.parent].join(" ").toLowerCase(); if (!hay.includes(q)) return false; }
      return true;
    });
    const cmp = {
      score: (a, b) => (TIER_ORDER[a.tier] - TIER_ORDER[b.tier]) || (b.score - a.score),
      price: (a, b) => a.price_ocs - b.price_ocs,
      thc: (a, b) => a._thc - b._thc,
      brand: (a, b) => a.brand.localeCompare(b.brand) || b.score - a.score
    }[so];
    return list.sort(cmp);
  }

  function card(p) {
    const quotes = (p.reddit_quotes || []).map(q => `<blockquote class="quote">“${esc(q.q)}”<span class="src">— r/TheOCS${q.s ? `, ${q.s}↑` : ""} · <a href="${redd(q.t)}" rel="noopener" target="_blank">thread ${esc(q.t)}</a></span></blockquote>`).join("");
    const threads = (p.threads || []).map(t => `<a href="${redd(t)}" rel="noopener" target="_blank">${esc(t)}</a>`).join("");
    const tags = [p._type === "live" ? "live resin" : p._type, p._lean, p.size, p._online ? "on OCS.ca" : "store only"].filter(Boolean).map(t => `<span class="tag">${esc(t)}</span>`).join("");
    return `<article class="card ${esc(p.tier)}" id="p-${esc(p.id)}" data-tier="${esc(p.tier)}">
      <div class="card-head">
        <div><div class="brandline">${esc(p.brand)}${p.parent ? " · " + esc(p.parent) : ""}</div><h3>${esc(p.name)}</h3>
        ${p.current_strain ? `<div class="muted">Strain: ${esc(p.current_strain)}</div>` : ""}<div class="tags">${tags}</div></div>
        <div class="score"><span class="badge ${esc(p.tier)}">${esc(p.tier)}</span><b>${p.score.toFixed(1)}</b><small>/10 community score</small></div>
      </div>
      <div class="facts">
        <div><b>Type</b>${esc(p.type)}</div>
        <div><b>OCS price</b>$${p.price_ocs.toFixed(2)} / ${esc(p.size)}${p.street_price ? `<br><span class="muted">stores: ${esc(p.street_price)}</span>` : ""}</div>
        <div><b>THC</b>${esc(p.thc)}</div>
        <div><b>Terps</b>${esc(p.terps)}</div>
        <div><b>Leaning</b>${esc(p.leaning)}</div>
        <div><b>Availability</b>${esc(p.availability)}</div>
        <div style="grid-column:1/-1"><b>Hardware</b>${esc(p.hardware)}</div>
      </div>
      <div class="body">
        <p class="verdict"><strong>Verdict:</strong> ${esc(p.verdict)}</p>
        <p><strong>Flavour:</strong> ${esc(p.flavour)}<br><strong>Effects:</strong> ${esc(p.effects)}</p>
        <div class="pc"><div class="pros"><h4>Pros</h4><ul>${(p.pros || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul></div><div class="cons"><h4>Cons</h4><ul>${(p.cons || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul></div></div>
        <details><summary>What r/TheOCS says (${(p.reddit_quotes || []).length} quotes, ${(p.threads || []).length} threads)</summary>${quotes}<div class="linkrow">${threads}</div></details>
        <div class="linkrow">${p.ocs_url ? `<a href="${esc(p.ocs_url)}" rel="noopener" target="_blank">OCS.ca product page ↗</a>` : ""}<a href="https://hibuddy.ca/search?q=${encodeURIComponent(p.brand + " " + (p.current_strain || "").split(/[(,;]/)[0])}" rel="noopener" target="_blank">Find in Toronto stores (hibuddy) ↗</a><a href="https://www.reddit.com/r/TheOCS/search/?q=${encodeURIComponent(p.brand + " " + p.name.split(/[\/(—]/)[0])}&restrict_sr=1&sort=new" rel="noopener" target="_blank">Latest r/TheOCS posts ↗</a></div>
      </div></article>`;
  }

  function renderCards() {
    const list = filtered();
    $("#cards").innerHTML = list.map(card).join("") || `<p class="muted">No products match.</p>`;
    $("#count").textContent = `(${list.length} of ${PRODUCTS.length})`;
  }

  let tSort = { k: "score", asc: false };
  const COLS = [
    ["tier", "Tier", p => `<span class="badge ${p.tier}">${p.tier}</span>`, p => TIER_ORDER[p.tier]],
    ["score", "Score", p => p.score.toFixed(1), p => p.score],
    ["brand", "Brand", p => esc(p.brand), p => p.brand],
    ["name", "Product", p => esc(p.name), p => p.name],
    ["type", "Type", p => esc(p._type === "live" ? "live resin" : p._type), p => p._type],
    ["lean", "Leaning", p => esc(p._lean), p => p._lean],
    ["price", "OCS $", p => "$" + p.price_ocs.toFixed(2), p => p.price_ocs],
    ["size", "Size", p => esc(p.size), p => parseFloat(p.size) || 0],
    ["ppg", "$ / g", p => "$" + (p.price_ocs / (parseFloat(p.size) || 1)).toFixed(0), p => p.price_ocs / (parseFloat(p.size) || 1)],
    ["thc", "THC", p => esc(p.thc), p => p._thc],
    ["hw", "Hardware (short)", p => esc(String(p.hardware).split(/[;—–]/)[0].slice(0, 70)), p => p.hardware],
    ["online", "OCS.ca", p => p._online ? "✓" : "store", p => p._online ? 0 : 1]
  ];
  function renderTable() {
    const th = COLS.map(([k, l]) => `<th data-k="${k}" class="${tSort.k === k ? "sorted" + (tSort.asc ? " asc" : "") : ""}">${l}</th>`).join("");
    $("#table thead").innerHTML = `<tr>${th}</tr>`;
    const col = COLS.find(c => c[0] === tSort.k);
    const rows = PRODUCTS.slice().sort((a, b) => { const x = col[3](a), y = col[3](b); let r = x < y ? -1 : x > y ? 1 : 0; if (tSort.k === "score" || tSort.k === "tier") r = tSort.k === "tier" ? (r || b.score - a.score) : (r || TIER_ORDER[a.tier] - TIER_ORDER[b.tier]); return tSort.asc ? r : -r; });
    $("#table tbody").innerHTML = rows.map(p => `<tr data-id="${esc(p.id)}">${COLS.map(c => `<td>${c[2](p)}</td>`).join("")}</tr>`).join("");
  }

  function renderAlso() {
    $("#also-grid").innerHTML = DATA.also_consider.map(a => `<div class="also"><div class="cat">${esc(a.category)}</div><h3>${esc(a.name)}</h3><p><strong>${esc(a.price)}</strong></p><p>${esc(a.why)}</p><div class="linkrow">${(a.threads || []).map(t => `<a href="${redd(t)}" rel="noopener" target="_blank">${esc(t)}</a>`).join("")}</div></div>`).join("");
  }

  function renderGuide() {
    const g = DATA.guide;
    $("#howto-grid").innerHTML = g.howto.map((h, i) => `<div class="howto"><h3>${i + 1}. ${esc(h.h)}</h3><p>${esc(h.p)}</p></div>`).join("");
    $("#glossary-list").innerHTML = g.glossary.map(x => `<div><dt>${esc(x.term)}</dt><dd>${esc(x.def)}</dd></div>`).join("");
    $("#where-list").innerHTML = g.where.map(w => `<div class="where"><strong>${esc(w.name)}</strong> — ${esc(w.note)}</div>`).join("");
    $("#faq-list").innerHTML = g.faq.map(f => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join("");
    $("#method-list").innerHTML = g.methodology.map(m => `<li>${esc(m)}</li>`).join("");
  }

  function wire() {
    ["#q", "#f-type", "#f-lean", "#f-tier", "#sort", "#f-online"].forEach(s => $(s).addEventListener("input", renderCards));
    $("#table thead").addEventListener("click", e => { const th = e.target.closest("th"); if (!th) return; const k = th.dataset.k; if (tSort.k === k) tSort.asc = !tSort.asc; else { tSort = { k, asc: !(k === "score" || k === "online") && k !== "tier" ? true : false }; if (k === "tier") tSort.asc = true; } renderTable(); });
    $("#table tbody").addEventListener("click", e => { const tr = e.target.closest("tr"); if (!tr) return; const el = $("#p-" + tr.dataset.id); if (el) { ["#q", "#f-type", "#f-lean", "#f-tier"].forEach(s => $(s).value = ""); $("#f-online").checked = false; renderCards(); $("#p-" + tr.dataset.id).scrollIntoView({ behavior: "smooth", block: "start" }); } });
  }
})();
