import os, re, json
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_work", "txt")
DIG = {'〇':0,'○':0,'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def num(s):
    s = s.strip()
    if s.isdigit(): return int(s)
    if '百' in s or '十' in s:
        n = 0; cur = 0
        for ch in s:
            if ch == '百': n += (cur or 1) * 100; cur = 0
            elif ch == '十': n += (cur or 1) * 10; cur = 0
            elif ch in DIG: cur = DIG[ch]
        return n + cur
    v = 0
    for ch in s:
        if ch not in DIG: return None
        v = v * 10 + DIG[ch]
    return v
PIN = ['七法品','業相應品','舍梨子相應品','未曾有法品','習相應品','王相應品','長壽王品','穢品','因品','林品','大品','梵志品','根本分別品','心品','雙品','晡利多品','例品']
pat = re.compile(r'（([〇○一二三四五六七八九十百0-9]{1,5})）\s*(?:中阿含)?\s*(?:大品/)?(' + '|'.join(PIN) + r')\s*([^\s》（）「」，。:：]{1,14}?經)第')
pat2 = re.compile(r'(?:中阿含)?(' + '|'.join(PIN) + r')([^\s》（）「」，。:：、]{1,14}?經)第([一二三四五六七八九十]+)')
res = {}
for f in sorted(os.listdir(D)):
    v = int(f[:2]); t = open(os.path.join(D, f), encoding='utf-8').read()
    for m in pat.finditer(t):
        n = num(m.group(1))
        if n and 1 <= n <= 222:
            res.setdefault(n, {}).setdefault((m.group(2), m.group(3), v), 0)
            res[n][(m.group(2), m.group(3), v)] += 1
out = {}
for n in sorted(res):
    best = max(res[n].items(), key=lambda kv: kv[1])[0]
    out[n] = best
missing = [n for n in range(1, 223) if n not in out]
print(len(out), 'found; missing', missing)
# secondary: list pat2 titles per volume for missing analysis
sec = {}
for f in sorted(os.listdir(D)):
    v = int(f[:2]); t = open(os.path.join(D, f), encoding='utf-8').read()
    for m in pat2.finditer(t):
        sec.setdefault(v, {}).setdefault((m.group(1), m.group(2), num(m.group(3))), 0)
        sec[v][(m.group(1), m.group(2), num(m.group(3)))] += 1
json.dump({'found': {n: list(out[n]) for n in out}, 'sec': {v: [list(k)+[c] for k, c in sorted(d.items(), key=lambda x: x[0][2] or 0)] for v, d in sec.items()}}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_work', 'idx.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
