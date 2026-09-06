#!/usr/bin/env python3
"""
Harvest r/TheOCS via Arctic Shift API (Pushshift successor).
STRATEGY: full dump of ALL posts (paginated by `before`, ~500/page with limit=auto), slimmed,
saved in chunk files research/reddit/posts_chunks/NNNN.json so interruption never loses work.
Then filter locally for cart-relevant posts and fetch their comments -> research/reddit/threads/<id>.json.

Usage:
  python3 research/fetch_reddit.py posts      # full post dump (resumable)
  python3 research/fetch_reddit.py comments   # comments for relevant posts (resumable)
  python3 research/fetch_reddit.py all
"""
import json, os, re, sys, time, glob, urllib.parse, urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reddit")
CHUNKS = os.path.join(OUT, "posts_chunks")
THREADS = os.path.join(OUT, "threads")
STATE = os.path.join(OUT, "state.json")
for d in (CHUNKS, THREADS): os.makedirs(d, exist_ok=True)

def get(url, tries=10):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ocs-cart-research/1.0 (personal research)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read()[:120]
            wait = 5 + 5 * i
            print(f"  HTTP {e.code} -> sleep {wait}s ({body})", flush=True)
            time.sleep(wait)
        except Exception as e:
            wait = 5 + 5 * i
            print(f"  ERR {e} -> sleep {wait}s", flush=True)
            time.sleep(wait)
    return None

KEEP = ["id","title","selftext","author","created_utc","score","upvote_ratio","num_comments","permalink","url","link_flair_text","author_flair_text"]
def slim(p): return {k: p.get(k) for k in KEEP}

def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"before": None, "chunk": 0, "done": False}
def save_state(s):
    json.dump(s, open(STATE + ".tmp", "w")); os.replace(STATE + ".tmp", STATE)

def do_posts():
    s = load_state()
    if s.get("done"):
        print("posts already complete"); return
    while True:
        qs = {"subreddit": "TheOCS", "limit": "auto", "sort": "desc"}
        if s["before"]: qs["before"] = s["before"]
        d = get(f"{BASE}/posts/search?" + urllib.parse.urlencode(qs))
        if d is None:
            print("giving up this round; rerun to resume"); return
        data = d.get("data") or []
        if not data:
            s["done"] = True; save_state(s); print("DONE full dump"); return
        rows = [slim(p) for p in data]
        fn = os.path.join(CHUNKS, f"{s['chunk']:04d}.json")
        json.dump(rows, open(fn, "w"), ensure_ascii=False)
        s["chunk"] += 1
        s["before"] = data[-1]["created_utc"] - 1
        save_state(s)
        print(f"chunk {s['chunk']-1}: {len(rows)} posts, oldest {time.strftime('%Y-%m-%d', time.gmtime(data[-1]['created_utc']))}", flush=True)
        time.sleep(3)

def all_posts():
    out = {}
    for fn in sorted(glob.glob(os.path.join(CHUNKS, "*.json"))):
        for p in json.load(open(fn)): out[p["id"]] = p
    return out

# relevance filter for cart-related posts
REL = re.compile(r"\b(cart|carts|cartridge|cartridges|510|vape|vapes|live resin|live rosin|rosin|resin|liquid diamond|diamonds|fse|htfse|full spectrum|solventless|distillate|disty|pen|pens|aio|all[- ]in[- ]one|disposable)\b", re.I)
def relevant(p):
    return bool(REL.search((p.get("title") or "") + " " + (p.get("selftext") or "")[:2000]))

CKEEP = ["id","parent_id","link_id","author","body","score","created_utc","author_flair_text"]

def do_comments(min_comments=1):
    posts = all_posts()
    todo = [p for p in posts.values() if relevant(p) and (p.get("num_comments") or 0) >= min_comments
            and not os.path.exists(os.path.join(THREADS, p["id"] + ".json"))]
    todo.sort(key=lambda p: -(p.get("num_comments") or 0))
    print(f"{len(posts)} total posts; {len(todo)} relevant threads need comments", flush=True)
    for n, p in enumerate(todo):
        comments, before = [], None
        while True:
            qs = {"link_id": p["id"], "limit": "auto", "sort": "desc"}
            if before: qs["before"] = before
            d = get(f"{BASE}/comments/search?" + urllib.parse.urlencode(qs))
            if d is None: break
            data = d.get("data") or []
            if not data: break
            comments.extend({k: c.get(k) for k in CKEEP} for c in data)
            if len(data) < 100: break
            before = data[-1]["created_utc"] - 1
            time.sleep(2)
        json.dump({"post": p, "comments": comments}, open(os.path.join(THREADS, p["id"] + ".json"), "w"), ensure_ascii=False)
        if n % 20 == 0:
            print(f"[{n+1}/{len(todo)}] {p['id']} {len(comments)}c | {p['title'][:70]}", flush=True)
        time.sleep(1.2)
    print("comments DONE")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("posts", "all"): do_posts()
    if mode in ("comments", "all"): do_comments()
