"""將 NL_中阿含經分卷 內各卷 .docx 轉為同名 .md（原 docx 不動）。"""
import os, re, zipfile, html
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo 根目錄
HEAD = {'Heading1': 2, 'Heading2': 2, 'Heading3': 2, 'Heading4': 3, 'Heading5': 4, 'Heading6': 5}

def para_text(p):
    out = []
    for m in re.finditer(r'<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br/>', p):
        out.append(html.unescape(m.group(1)) if m.group(1) is not None else ('\t' if 'tab' in m.group(0) else '  \n'))
    return ''.join(out).strip()

def convert(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    title = os.path.splitext(os.path.basename(path))[0]
    lines = [f'# {title}', '']
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, flags=re.S):
        t = para_text(p)
        if not t:
            continue
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        lv = HEAD.get(st.group(1)) if st else None
        if lv:
            if lines and lines[-1].lstrip().startswith('- '):
                lines.append('')
            t = re.sub(r'^#+\s*', '', t).replace('**', '')
            lines += ['#' * lv + ' ' + t, '']
        elif '<w:numPr>' in p:
            il = re.search(r'<w:ilvl w:val="(\d+)"', p)
            lines.append('  ' * int(il.group(1) if il else 0) + '- ' + t)
        else:
            if lines and lines[-1].lstrip().startswith('- '):
                lines.append('')
            lines += [t, '']
    md = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip() + '\n'
    out = os.path.splitext(path)[0] + '.md'
    with open(out, 'w', encoding='utf-8') as o:
        o.write(md)
    return out, len(md)

n = tot = 0
for f in sorted(os.listdir(SRC)):
    if f.endswith('.docx') and f.startswith('中阿含經卷第'):
        _, size = convert(os.path.join(SRC, f)); n += 1; tot += size
print(f'converted {n} files, {tot/1024/1024:.1f} MB text')
