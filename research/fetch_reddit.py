#!/usr/bin/env python3
"""
Harvest r/TheOCS posts + comments about live resin / live rosin 510 carts via Arctic Shift API.
Idempotent & incremental: saves each post + its comments to research/reddit/posts/<id>.json.
Re-running skips already-fetched posts. Safe to interrupt at any time.

Usage:
  python3 research/fetch_reddit.py posts     # fetch post listings for all queries -> research/reddit/index.json
  python3 research/fetch_reddit.py comments  # fetch comments for indexed posts (skips done)
  python3 research/fetch_reddit.py all
"""
import json, os, sys, time, urllib.parse, urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api"
OUT = os.path.join(os.path.dirname(__file__), "reddit")
POSTS_DIR = os.path.join(OUT, "posts")
INDEX = os.path.join(OUT, "index.json")
os.makedirs(POSTS_DIR, exist_ok=True)

# Title / body search terms. Arctic Shift supports 'title' and 'body' and 'query' params.
TITLE_QUERIES = [
    "live resin", "live rosin", "rosin cart", "rosin 510", "resin cart", "resin 510",
    "510 cart", "510 vape", "cartridge", "carts", "best cart", "best carts", "best vape",
    "liquid diamonds", "diamonds cart", "full spectrum", "FSE", "HTFSE",
    "hash rosin", "solventless", "cured resin",
    # brands commonly associated with live resin/rosin carts on OCS
    "Eastcann", "Four54", "FOUR54", "Tribal", "Lune Rise", "Tribal cuban linx",
    "General Admission", "Back Forty", "Good Supply", "Roilty", "Sticky Greens",
    "Boxhot", "BOXHOT", "Endgame", "Debunk", "Redecan", "Ambr", "AMBR", "Jays", "Weed Me",
    "Fresh Coast", "Wildcard", "Spinach", "Broken Coast", "Simply Bare", "Rubicon",
    "Kolab", "KOLAB", "Dab Bods", "Dabbods", "Greybeard", "Greybeard vape", "Astrolab", "Astro Lab",
    "Beurre Blanc", "Beurre", "Divvy", "Versus", "Contraband", "Adults Only", "Pure Sunfarms",
    "Lord Jones", "Zoda", "ZODA", "Iris Labs", "MTL Cannabis", "Cruuzy", "Ghost Drops", "Ghost Drops vape",
    "Carmel", "Woody Nelson", "Tenzo", "Shred", "SHRED", "Shred X", "Bzam", "BZAM", "Pistol and Paris",
    "Highly Dutch", "Gage", "Cookies", "Alien Labs", "Connected", "Homestead", "Homestead Cannabis",
    "Joints cannabis", "Sitka", "Cannabis Cousins", "Dymond", "Dymond Concentrates", "Fume", "FUME",
    "Marley", "Dunn Cannabis", "Twd", "TWD", "Trailblazer", "Hexo", "HEXO", "Aurora", "San Rafael",
    "Bhang", "Riff", "RIFF", "Solei", "Wagners", "Wana", "Glacial Gold", "Kingsway", "Kinloch",
    "Nuance", "Farmhouse", "Purple Hills", "Muskoka Grown", "Ness", "Edison", "Northern Harvest",
    "Foray", "Weed Pool", "Station House", "1964", "Qwest", "Thumbs Up", "Loosh", "Nith & Grand", "Nith and Grand",
    "Origami", "Kush Kraft", "Level Up", "Motif", "Tilray", "Flowr", "Ontario Cannabis Store vape",
]
BODY_QUERIES = [
    "live resin cart", "live rosin cart", "rosin 510", "best live resin", "best live rosin",
    "best 510", "best cart", "favourite cart", "favorite cart", "cart recommendation",
    "liquid diamonds", "hash rosin cart", "solventless cart", "fse cart", "htfse cart",
]

def get(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ocs-cart-research/1.0 (personal research)"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read()[:200]
            wait = 4 + 4 * i
            print(f"  HTTP {e.code} -> sleep {wait}s ({body[:80]})", flush=True)
            time.sleep(wait)
        except Exception as e:
            wait = 4 + 4 * i
            print(f"  ERR {e} -> sleep {wait}s", flush=True)
            time.sleep(wait)
    return None

def search_posts(param, q, after=None):
    """Paginate backwards through time using 'before' cursor."""
    results = []
    before = None
    while True:
        qs = {"subreddit": "TheOCS", param: q, "limit": 100, "sort": "desc"}
        if before: qs["before"] = before
        if after: qs["after"] = after
        url = f"{BASE}/posts/search?" + urllib.parse.urlencode(qs)
        d = get(url)
        if not d or not d.get("data"):
            break
        data = d["data"]
        results.extend(data)
        print(f"  [{param}={q!r}] +{len(data)} (total {len(results)}) oldest={data[-1]['created_utc']}", flush=True)
        if len(data) < 100:
            break
        before = data[-1]["created_utc"] - 1
        time.sleep(2.5)
    return results

def load_index():
    if os.path.exists(INDEX):
        return json.load(open(INDEX))
    return {}

def save_index(idx):
    tmp = INDEX + ".tmp"
    json.dump(idx, open(tmp, "w"), indent=0, ensure_ascii=False)
    os.replace(tmp, INDEX)

KEEP = ["id","title","selftext","author","created_utc","score","upvote_ratio","num_comments","permalink","url","link_flair_text","author_flair_text"]

def slim(p):
    return {k: p.get(k) for k in KEEP}

def do_posts():
    idx = load_index()
    done_q = set(idx.get("_queries_done", []))
    posts = idx.setdefault("posts", {})
    for param, qlist in (("title", TITLE_QUERIES), ("body", BODY_QUERIES)):
        for q in qlist:
            key = f"{param}:{q}"
            if key in done_q:
                continue
            print(f"Query {key}", flush=True)
            res = search_posts(param, q)
            for p in res:
                posts[p["id"]] = slim(p)
            done_q.add(key)
            idx["_queries_done"] = sorted(done_q)
            save_index(idx)
            time.sleep(2.5)
    print(f"Index has {len(posts)} unique posts")

CKEEP = ["id","parent_id","link_id","author","body","score","created_utc","author_flair_text"]

def do_comments(min_comments=1):
    idx = load_index()
    posts = idx.get("posts", {})
    todo = [p for p in posts.values() if (p.get("num_comments") or 0) >= min_comments
            and not os.path.exists(os.path.join(POSTS_DIR, p["id"] + ".json"))]
    # highest engagement first so most valuable data lands early
    todo.sort(key=lambda p: -(p.get("num_comments") or 0))
    print(f"{len(todo)} posts need comments")
    for n, p in enumerate(todo):
        comments = []
        before = None
        while True:
            qs = {"link_id": p["id"], "limit": 100, "sort": "desc"}
            if before: qs["before"] = before
            d = get(f"{BASE}/comments/search?" + urllib.parse.urlencode(qs))
            if not d or not d.get("data"):
                break
            comments.extend({k: c.get(k) for k in CKEEP} for c in d["data"])
            if len(d["data"]) < 100:
                break
            before = d["data"][-1]["created_utc"] - 1
            time.sleep(2)
        out = {"post": p, "comments": comments}
        json.dump(out, open(os.path.join(POSTS_DIR, p["id"] + ".json"), "w"), ensure_ascii=False)
        print(f"[{n+1}/{len(todo)}] {p['id']} {len(comments)}c | {p['title'][:70]}", flush=True)
        time.sleep(1.5)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("posts", "all"): do_posts()
    if mode in ("comments", "all"): do_comments()
