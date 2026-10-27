import os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from index import num, D
syn = {}
rx = re.compile(r'^[\s\-*•]*（([〇○一二三四五六七八九十百]{1,5})）\s*《([^》]+)》[^：:]{0,40}[：:](.+)$')
for f in sorted(os.listdir(D)):
    for line in open(os.path.join(D, f), encoding='utf-8'):
        m = rx.match(line.strip())
        if not m: continue
        n = num(m.group(1))
        if not n or n in syn: continue
        s = re.sub(r'\s*passage[\s\d,]+', '', m.group(3))
        s = re.sub(r'對應巴利南傳[^。；]*?[。；]', '', s).replace('**', '').strip()
        syn[n] = s
print(len(syn), [n for n in range(1, 223) if n not in syn])
json.dump(syn, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_work', 'syn.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for n in (1, 31, 98, 189, 222): print(n, syn.get(n, '')[:200])
