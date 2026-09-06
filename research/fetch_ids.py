#!/usr/bin/env python3
"""Fetch comments for specific thread ids right now: python3 research/fetch_ids.py id1,id2"""
import sys,os,json,time,urllib.parse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from fetch_reddit import get,BASE,THREADS,CKEEP,all_posts
posts=all_posts()
for tid in sys.argv[1].split(','):
    fn=os.path.join(THREADS,tid+'.json')
    if os.path.exists(fn): continue
    p=posts.get(tid)
    if not p:
        d=get(f"{BASE}/posts/ids?ids={tid}"); 
        if d and d.get('data'): p={k:d['data'][0].get(k) for k in ["id","title","selftext","author","created_utc","score","upvote_ratio","num_comments","permalink","url","link_flair_text","author_flair_text"]}
        else: print('no post',tid); continue
    comments,before=[],None
    while True:
        qs={"link_id":tid,"limit":"auto","sort":"desc"}
        if before: qs["before"]=before
        d=get(f"{BASE}/comments/search?"+urllib.parse.urlencode(qs))
        if not d or not d.get('data'): break
        comments.extend({k:c.get(k) for k in CKEEP} for c in d['data'])
        if len(d['data'])<100: break
        before=d['data'][-1]['created_utc']-1; time.sleep(2)
    json.dump({"post":p,"comments":comments},open(fn,"w"),ensure_ascii=False)
    print(tid,len(comments),p['title'][:60]); time.sleep(2)
