#!/usr/bin/env python3
"""Harvest full OCS.ca 510-cart catalog (Shopify products.json) -> research/ocs/products.json"""
import json, urllib.request, time, os
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
OUT=os.path.join(os.path.dirname(__file__),"ocs","products.json")
all_p={}
for coll in ["510-thread-cartridges","vapes"]:
    page=1
    while True:
        url=f"https://ocs.ca/collections/{coll}/products.json?limit=250&page={page}"
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        d=json.load(urllib.request.urlopen(req,timeout=60))
        ps=d.get("products",[])
        for p in ps: all_p[p["id"]]=p
        print(coll,page,len(ps),"total",len(all_p),flush=True)
        if len(ps)<250: break
        page+=1; time.sleep(1)
json.dump(list(all_p.values()),open(OUT,"w"),ensure_ascii=False)
print("saved",len(all_p))
