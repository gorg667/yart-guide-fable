#!/usr/bin/env python3
"""Fetch comments for the highest-value 'best cart' discussion threads first. Resumable."""
import glob,json,re,os,sys,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from fetch_reddit import get, BASE, THREADS, CKEEP, all_posts
import urllib.parse
posts=all_posts()
q=re.compile(r'(best|favou?rite|recommend|top|go[- ]to|tier|ranking|rank|euphoric|potent|strongest|worth|review|first impression|thoughts)\b.*\b(cart|carts|510|vape|live resin|rosin|resin|aio)',re.I)
q2=re.compile(r'\b(live resin|live rosin|rosin|liquid diamond|fse|htfse)\b',re.I)
hits=[p for p in posts.values() if (q.search(p['title'] or '') or q2.search(p['title'] or '')) and (p['num_comments'] or 0)>=3]
hits.sort(key=lambda p:-(p['num_comments'] or 0))
print(len(hits),'priority threads')
for n,p in enumerate(hits):
    fn=os.path.join(THREADS,p['id']+'.json')
    if os.path.exists(fn): continue
    comments,before=[],None
    while True:
        qs={"link_id":p["id"],"limit":"auto","sort":"desc"}
        if before: qs["before"]=before
        d=get(f"{BASE}/comments/search?"+urllib.parse.urlencode(qs))
        if d is None: break
        data=d.get("data") or []
        if not data: break
        comments.extend({k:c.get(k) for k in CKEEP} for c in data)
        if len(data)<100: break
        before=data[-1]["created_utc"]-1; time.sleep(2)
    json.dump({"post":p,"comments":comments},open(fn,"w"),ensure_ascii=False)
    print(f"[{n+1}/{len(hits)}] {p['id']} {len(comments)}c | {p['title'][:70]}",flush=True)
    time.sleep(2.5)
print("priority DONE")
