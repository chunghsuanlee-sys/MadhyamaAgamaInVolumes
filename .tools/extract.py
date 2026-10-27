import sys, os, re, zipfile, json
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo 根目錄
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_work", "txt")
os.makedirs(OUT, exist_ok=True)
CN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn2i(s):
    if s == '六十': return 60
    n = 0
    if '十' in s:
        a, b = s.split('十')
        n = (CN[a] if a else 1) * 10 + (CN[b] if b else 0)
    else:
        n = CN[s]
    return n
for f in os.listdir(SRC):
    m = re.match(r'中阿含經卷第(.+)\.docx$', f)
    if not m: continue
    v = cn2i(m.group(1))
    with zipfile.ZipFile(os.path.join(SRC, f)) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    paras = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, flags=re.S):
        t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
        if t.strip(): paras.append(t)
    with open(os.path.join(OUT, f"{v:02d}.txt"), 'w', encoding='utf-8') as o:
        o.write('\n'.join(paras))
print('done')
