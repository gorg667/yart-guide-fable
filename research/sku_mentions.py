#!/usr/bin/env python3
"""Count SKU-level mentions across all fetched comments+posts (2025-01 onward) → research/sku_stats.json"""
import glob,json,re,time,os
HERE=os.path.dirname(os.path.abspath(__file__))
SKUS={
 # Atlanticann
 "Iris Labs Fantasm":r"fantasm|phantasm|fantasam",
 "Iris Labs Blackwater":r"black ?water",
 "Iris Labs Purple Sundaze":r"purple sundaze|sundaze|sundance cart|sundaz",
 "Iris Labs Cherry Bang Bang":r"cherry bang",
 "Iris Labs ZODA":r"\bzoda\b",
 "EastCann Gastro Pop":r"eastcann?.{0,25}gastro|gastro ?pop.{0,25}eastcann?",
 "FOUR54 Emerald Triangle (Gastro Pop)":r"emerald triangle|four ?54.{0,25}gastro|gastro.{0,25}four ?54|454.{0,10}gastro",
 "FOUR54 Papaya Bomb":r"papaya bomb",
 "FOUR54 Route 66":r"route 66|rte ?66",
 "EastCann Mango Sour":r"mango sour|sour mango",
 "EastCann Frozen Lemons":r"frozen lemons?",
 "EastCann Purple Kush":r"eastcann?.{0,20}purple kush|purple kush.{0,20}eastcann?|p ?kush from eastcann",
 # Tribal
 "Tribal Triple Burger":r"triple burger|tripple burger",
 "Tribal Bubble Up":r"bubble ?up",
 "Tribal Galactic Runtz":r"galactic r+u?ntz|galactic rants",
 "Tribal Cuban Linx":r"cuban lin[xk]s?|cuban lynx",
 "Tribal Neon Sunshine":r"neon sunshine|neon s\.",
 "Tribal Porto Leche":r"porto leche|porto",
 "Tribal Power Sherb":r"power sherb",
 "Tribal G Mint":r"g[- ]?mint\b",
 "Tribal Drip Station":r"drip station",
 "Tribal Jigglers":r"jigglers?",
 "Tribal Terple":r"\bterple\b",
 "Tribal GT / Gran Turismo":r"gran turismo|\bgt (cart|live|tribal)|tribal gt|gt live resin",
 # Purple Hills
 "Purple Hills Gorilla Z / Zkittlez":r"gorilla z\b|gorilla zk|gorilla skittle|gorilla zkit|gorilla xl",
 "Purple Hills Orangeade":r"orangeade|orange gaede|orangeaid",
 "Purple Hills Lemon Pepper":r"lemon pepper",
 "Purple Hills Big White Dawg":r"big white dawg|big white dog",
 "Purple Hills Creemore Valley Kush":r"creemore",
 "Purple Hills Shishka Dawg":r"shishka ?daw?g",
 # 1964
 "1964 Comatose":r"comatose",
 "1964 Stinky Pinky":r"stinky pinky|stinky pink\b|pinky cart",
 "1964 Blue Dream (cart)":r"1964.{0,20}blue dream|blue dream.{0,20}1964|blue dream (cart|510|fse|lr)",
 "1964 Gelato 41":r"gelato ?#?41|glto ?41|g41\b",
 "1964 Lemon Diesel":r"lemon diesel",
 # Carmel
 "Carmel Animal Face":r"animal face",
 "Carmel Slurty3":r"slurty ?3",
 "Carmel Jungle J":r"jungle j\b",
 "Carmel Big Apple":r"big apple",
 "Carmel Zebra Stripes":r"zebra stripes?",
 "Carmel Permanent Cherries":r"permanent cherr",
 "Carmel Flamingo":r"flamingo",
 # others
 "Kolab Motorbreath":r"motorbreath|motor breath",
 "Woody Nelson Rainbow Driver":r"rainbow driver",
 "Woody Nelson Country Club Gastro Pop":r"country club.{0,20}gastro|gastro.{0,20}country club",
 "Wildcard G-Wagon":r"g[- ]?wagon",
 "Wildcard Forbidden Pie":r"forbidden pie",
 "Sauce Rosin Labs Mob Pie":r"mob pie",
 "Sauce Rosin Labs GovernMint Oasis":r"govern?mint oasis",
 "Sauce Rosin Labs Grease Bucket":r"grease bucket",
 "Sauce Rosin Labs Black Maple":r"black maple",
 "Sauce Rosin Labs Chilly Willy":r"chilly willy",
 "Sauce Rosin Labs Strawberry Guava":r"strawberry guava",
 "Sauce Rosin Labs Point Break":r"point break",
 "Redecan Animal Runtz AIO":r"animal r+u?ntz",
 "Redecan Purple Churro AIO":r"purple churro",
 "Redecan Amped":r"\bamped\b",
 "Lune Rise Pink Tsunami":r"pink tsunami",
 "Lune Rise Lollipopz":r"lollipopz",
 "Lord Jones Deadhead OG":r"deadhead|dead head og",
 "Lord Jones Orange Velvet":r"orange velvet",
 "Sherbinskis Pink Sherb":r"pink sherbs?",
 "Sherbinskis True GLTO 33":r"tru(e)? glto|glto ?33|gelato 33",
 "Sherbinskis Zauce":r"\bzauce\b",
 "Jays Pink Cherry":r"pink cherry",
 "Greazy RNB Belts":r"rnb belts|r&b belts",
 "Greazy Super Lemon Haze":r"greazy.{0,20}super lemon|super lemon haze.{0,20}greazy|greazy slh",
 "Orchid CBD RNTZ":r"cbd r+u?ntz|orchid",
 "67 Sins Gas Face":r"gas face",
 "Pure Sunfarms Pink Kush cart":r"(psf|pure sunfarms).{0,25}pink kush|pink kush.{0,25}(psf|pure sunfarms)",
 "1Above Juice Bar":r"juice bar",
 "Versus BC Purple Kush":r"versus.{0,20}purple kush|bc purple kush",
 "Port North rosin cart":r"port north|point north",
 "Connoisseur's Culture hash rosin":r"connoisseur",
 "Bleuh Wildberry":r"bleuh|wildberry",
 "Northern Canna Permanent Marker AIO":r"permanent marker",
 "Contraband Live Rosin":r"contraband",
 "Frootyhooty rosin":r"frooty ?hooty",
 "Kolab Liquid Live Resin":r"liquid live resin",
 "Weed Me Pai Gow":r"pai gow",
 "MTL Sage n Sour":r"sage n.? ?sour",
}
RX={k:re.compile(v,re.I) for k,v in SKUS.items()}
POS=re.compile(r"\b(best|fire|🔥|slaps|smacks|amazing|love|loved|great|excellent|favou?rite|goat|banger|solid|smooth|delicious|tasty|potent|strong|hits hard|10/10|9/10|9\.5/10|rebuy|re-buy|recommend|never clog|no clog|reliable|consistent|incredible|phenomenal|fantastic)\b",re.I)
NEG=re.compile(r"\b(clog|clogs|clogged|clogging|leak|leaks|leaking|leaked|burnt|burning|harsh|trash|garbage|mid|meh|disappoint\w*|overpriced|avoid|worst|bad|weak|muted|fake|scam|misleading|inconsistent|hate|terrible|horrible|dud|defective|stopped working|not worth|underwhelm\w*|5/10|6/10)\b",re.I)
cut=time.mktime((2025,1,1,0,0,0,0,0,0))
texts=[]
for fn in glob.glob(os.path.join(HERE,"reddit/posts_chunks/*.json")):
    for p in json.load(open(fn)):
        if p["created_utc"]>=cut: texts.append(((p.get("title") or "")+" "+(p.get("selftext") or ""),p.get("score") or 0,"post"))
for fn in glob.glob(os.path.join(HERE,"reddit/threads/*.json")):
    d=json.load(open(fn))
    for c in d["comments"]:
        if (c.get("created_utc") or 0)>=cut and c.get("body"): texts.append((c["body"],c.get("score") or 0,"comment"))
stats={k:{"mentions":0,"score_sum":0,"pos":0,"neg":0} for k in SKUS}
for t,s,kind in texts:
    for k,rx in RX.items():
        if rx.search(t):
            st=stats[k]; st["mentions"]+=1; st["score_sum"]+=s; st["pos"]+=len(POS.findall(t)); st["neg"]+=len(NEG.findall(t))
for k,st in stats.items(): st["sentiment"]=round((st["pos"]-st["neg"])/max(1,st["pos"]+st["neg"]),2)
json.dump({"generated":time.strftime("%Y-%m-%d"),"n_texts":len(texts),"skus":stats},open(os.path.join(HERE,"sku_stats.json"),"w"),indent=1)
print(len(texts),"texts since 2025-01")
for k,st in sorted(stats.items(),key=lambda kv:-kv[1]["mentions"]):
    print(f"{k:42} {st['mentions']:5} {st['score_sum']:6} {st['pos']:4} {st['neg']:4} {st['sentiment']:5}")
