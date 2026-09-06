#!/usr/bin/env python3
"""
Quantitative brand-mention analysis over r/TheOCS corpus.
- Counts posts whose title/body mention a brand AND a cart context term.
- Counts comment mentions (within fetched threads) with a crude sentiment lexicon.
- Outputs research/brand_stats.json + prints a table.
"""
import glob, json, re, collections, time, os
HERE = os.path.dirname(os.path.abspath(__file__))

BRANDS = {
 "Iris Labs": r"\biris\b(?!h)|fantasm|phantasm|blackwater|black water|purple sundaze|cherry bang bang|\bzoda\b",
 "EastCann": r"east ?cann?\b|eastcan\b|gastro ?pop|frozen lemons|mango sour|sour mango",
 "FOUR54": r"four ?54|four54|454 cart|area 54|emerald triangle|route 66|papaya bomb",
 "Tribal": r"\btribal\b|cuban lin[xk]s?|triple burger|bubble up|galactic r+u?ntz|neon sunshine|g[- ]?mint\b|power sherb|drip station|jigglers|porto leche|\bterple\b",
 "Purple Hills": r"purple hills?\b|\bph carts?|orangeade|gorilla z\b|gorilla zk|gorilla skittle|lemon pepper|creemore|big white dawg|shishka ?dawg|wedding singer|lake huron haze|frozen bananas",
 "1964": r"\b1964\b|comatose|stinky pinky|la kush cake cart|lemon diesel fse",
 "Carmel": r"\bcarmel\b|caramel cart|animal face|slurty ?3|jungle j\b|big apple (pure|live)|flamingo (cart|live)",
 "Woody Nelson": r"woody nelson|rainbow driver|country club (cart|live|510)",
 "Wildcard": r"wild ?card extracts|wildcard\b.*(cart|resin|vape)|g[- ]wagon|forbidden pie|pumelo skunk|waffle bites",
 "Kolab": r"\bkolab\b|motorbreath|wedding pie (live|rosin|cart)",
 "Sauce Rosin Labs": r"sauce rosin|sauce labs|\bsrl\b",
 "1Above": r"1 ?above|one above|juice bar (aio|live|rosin)|fruit bar (aio|rosin)",
 "Lune Rise Farms": r"lune ?rise|farmers.? market (pure|live|510|aio)|pink tsunami|lollipopz",
 "Redecan": r"\bredecan\b|legit live resin|animal r+u?ntz (live|aio|legit)|purple churro|amped live resin",
 "Lord Jones": r"lord jones",
 "Sherbinskis": r"sherbinski|pink sherbs?|tru(e)? glto|sherbunk",
 "Coterie": r"\bcoterie\b",
 "The Loud Plug": r"loud plug|\btlp\b",
 "Greazy": r"\bgreazy\b|rnb belts",
 "Versus": r"\bversus\b.*(cart|fsr|resin|510)|versus bc purple",
 "Contraband": r"\bcontraband\b.*(rosin|cart|510)",
 "Weed Me": r"weed ?me\b.*(live|resin|cart|510|pai gow)|pai gow",
 "Jonny Chronic": r"jon+y chronic",
 "Pepe": r"\bpepe\b.*(cart|lemon|resin|510)",
 "Jays": r"\bjays\b.*(cart|pink cherry|resin)|pink cherry (live|cart|510)",
 "Roilty": r"\broilty\b",
 "Debunk": r"\bdebunk\b.*(live|resin|cart|510|glto)",
 "Endgame": r"\bendgame\b.*(live|acai|cart|510)",
 "Boxhot": r"box ?hot",
 "Kolab Liquid Diamonds": r"kolab.*diamond",
 "General Admission": r"general admission|\bGA\b.*(diamond|cart)|kootenay fruit",
 "Back Forty": r"back ?40|back forty",
 "Good Supply": r"good supply",
 "Spinach": r"\bspinach\b.*(cart|510|vape|disty|distillate)",
 "Sticky Greens": r"sticky greens",
 "Dymond": r"\bdymond\b",
 "Greybeard": r"grey ?beard",
 "Shred": r"\bshred\b.*(cart|510|vape|x)",
 "Adults Only / NSFW": r"adults only|\bnsfw\b.*(cart|diamond|510)",
 "BLKMKT": r"blk ?mkt|blkmrkt|black market carts?",
 "Polar": r"\bpolar\b.*(cart|rosin|resin|510)|polar black mountain",
 "Msiku": r"\bmsiku\b|starstruck",
 "Pharmabee": r"pharmabee|rozzie",
 "Port North": r"port north|port berry",
 "Brindle": r"\bbrindle\b",
 "SUGR": r"\bsugr\b",
 "Unlicensed Producer": r"unlicensed producer|\bUP rosin|\(UP\)",
 "The Goo!": r"the goo\b|goo[- ]cart",
 "Frootyhooty": r"frooty ?hooty",
 "MTL Cannabis": r"\bmtl\b.*(sage|cart|510|resin)|sage n.? sour",
 "Orchid CBD": r"orchid (cbd|runtz|cart)",
 "Highxotic": r"highxotic|hoghxotic|mr\.? ?c rosin",
 "Bleuh": r"\bbleuh\b",
 "Purple Hills XL": r"purple hills.*xl|xl cart",
 "Fume": r"\bfume\b.*(live|resin|cart)",
 "GAS": r"\(gas\)|\bgas\b (mango|cart|live action)",
 "Nugz": r"\bnugz\b",
 "Slaps": r"\bslaps\b.*(rosin|stick|brand)|slaps -",
 "Ambr": r"\bambr\b",
 "Qwest": r"\bqwest\b.*(live|cart|510|georgia)",
 "Shed Boyz": r"shed boyz",
 "VERO": r"\bvero\b.*(cart|diamond|510|live)",
 "Cabana": r"cabana cannabis|cabana.*(cart|diamond)",
}
BR = {k: re.compile(v, re.I) for k, v in BRANDS.items()}
CART = re.compile(r"\b(cart|carts|cartridge|cartridges|510|vape|vapes|live resin|live rosin|rosin|resin|aio|disposable|pen)\b", re.I)
POS = re.compile(r"\b(best|fire|🔥|slaps|smacks|amazing|love|loved|great|excellent|favou?rite|goat|banger|solid|smooth|delicious|tasty|potent|strong|hits hard|10/10|9/10|rebuy|re-buy|recommend|never clog|no clog|reliable|consistent|top tier|s tier)\b", re.I)
NEG = re.compile(r"\b(clog|clogs|clogged|clogging|leak|leaks|leaking|leaked|burnt|burning|burns|harsh|trash|garbage|mid|mids|meh|disappoint\w*|overpriced|avoid|worst|bad|shit|ass|weak|muted|fake|distillate|disty|scam|misleading|bait|inconsistent|hate|terrible|horrible|dud|defective|stopped working|no taste|not worth)\b", re.I)

def load_posts():
    out = {}
    for fn in sorted(glob.glob(os.path.join(HERE, "reddit/posts_chunks/*.json"))):
        for p in json.load(open(fn)): out[p["id"]] = p
    return out

def main():
    posts = load_posts()
    threads = {}
    for fn in glob.glob(os.path.join(HERE, "reddit/threads/*.json")):
        d = json.load(open(fn)); threads[d["post"]["id"]] = d
    stats = {b: {"posts": 0, "posts_2025plus": 0, "post_score": 0, "comments": 0, "comment_score": 0, "pos": 0, "neg": 0, "example_posts": []} for b in BRANDS}
    cutoff = time.mktime((2025, 1, 1, 0, 0, 0, 0, 0, 0))
    for p in posts.values():
        text = (p.get("title") or "") + " \n " + (p.get("selftext") or "")
        if not CART.search(text): continue
        for b, rx in BR.items():
            if rx.search(text):
                s = stats[b]; s["posts"] += 1; s["post_score"] += (p.get("score") or 0)
                if p["created_utc"] >= cutoff: s["posts_2025plus"] += 1
                if len(s["example_posts"]) < 8 and (p.get("num_comments") or 0) >= 5:
                    s["example_posts"].append({"id": p["id"], "title": p["title"], "score": p["score"], "n": p["num_comments"], "date": time.strftime("%Y-%m-%d", time.gmtime(p["created_utc"]))})
    for d in threads.values():
        for c in d["comments"]:
            body = c.get("body") or ""
            if len(body) < 8: continue
            for b, rx in BR.items():
                if rx.search(body):
                    s = stats[b]; s["comments"] += 1; s["comment_score"] += (c.get("score") or 0)
                    s["pos"] += len(POS.findall(body)); s["neg"] += len(NEG.findall(body))
    for b, s in stats.items():
        s["sentiment"] = round((s["pos"] - s["neg"]) / max(1, s["pos"] + s["neg"]), 2)
    json.dump({"generated": time.strftime("%Y-%m-%d"), "n_posts_total": len(posts), "n_threads_with_comments": len(threads),
               "n_comments_total": sum(len(d["comments"]) for d in threads.values()), "brands": stats},
              open(os.path.join(HERE, "brand_stats.json"), "w"), indent=1, ensure_ascii=False)
    rows = sorted(stats.items(), key=lambda kv: -(kv[1]["posts"] + kv[1]["comments"]))
    print(f"{len(posts)} posts, {len(threads)} threads, {sum(len(d['comments']) for d in threads.values())} comments")
    print(f"{'brand':22} {'posts':>5} {'p25+':>5} {'pScore':>6} {'cmts':>5} {'cScore':>6} {'pos':>4} {'neg':>4} {'sent':>5}")
    for b, s in rows:
        print(f"{b:22} {s['posts']:5} {s['posts_2025plus']:5} {s['post_score']:6} {s['comments']:5} {s['comment_score']:6} {s['pos']:4} {s['neg']:4} {s['sentiment']:5}")

if __name__ == "__main__":
    main()
