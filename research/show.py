import json,sys,os
n=int(sys.argv[2]) if len(sys.argv)>2 else 40
for tid in sys.argv[1].split(','):
    fn=f'research/reddit/threads/{tid}.json'
    if not os.path.exists(fn): print('MISSING',tid); continue
    d=json.load(open(fn)); p=d['post']
    print('='*100); print(p['title'],'| score',p['score'],'| ncom',p['num_comments'],'|',p['id']); print((p['selftext'] or '')[:1200]); print('-'*50)
    cs=sorted(d['comments'],key=lambda c:-(c['score'] or 0))
    for c in cs[:n]:
        b=(c['body'] or '').replace('\n',' ')
        if len(b)>15 and c['author']!='AutoModerator': print(f"[{c['score']}] {b[:380]}")
