#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site';HTML=SITE/'complete.html';MD=ROOT/'claude-code-blog-slide-integrated.md'
MANIFEST=ROOT/'slide_integration_manifest.json';SKILL=ROOT/'hands-on/skill/textbook-chapter-lab';PDF_META=ROOT/'SOURCE_PDF_METADATA.json'
EXPECTED_KEYS=[f'{i:02d}' for i in range(39)]+['final']

def target_ch(target:str)->str|None:
    m=re.match(r'(?:ch|chapter|story)-(\d+)',target)
    if m:return f'{int(m.group(1)):02d}'
    if target in ('chapter-final','公式確認先'):return 'final'
    return None

def strip_image_directives(md:str)->list[str]:
    lines=md.splitlines();out=[];i=0
    while i<len(lines):
        if lines[i].startswith('> **画像制作指示：'):
            while i<len(lines) and (lines[i].startswith('>') or not lines[i].strip()):i+=1
            continue
        if lines[i].strip()=='## 補助図の制作指示':
            i+=1
            while i<len(lines) and not lines[i].startswith('## 体験ミッション'):i+=1
            continue
        if i==0 and lines[i].startswith('# '):i+=1;continue
        out.append(lines[i]);i+=1
    return [x for x in out if x.strip()]

def ordered_subsequence(source:list[str],target:list[str])->tuple[bool,str|None]:
    j=0
    for line in source:
        while j<len(target) and target[j]!=line:j+=1
        if j>=len(target):return False,line[:160]
        j+=1
    return True,None

def local_links(path:Path,errors:list[str]):
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser');own={x.get('id') for x in soup.find_all(id=True)}
    for a in soup.find_all('a',href=True):
        href=a['href'];u=urlparse(href)
        if u.scheme or href.startswith(('mailto:','javascript:')):continue
        target=path
        if u.path:
            target=(path.parent/unquote(u.path)).resolve()
            if not target.exists():errors.append(f'Broken link {path.relative_to(ROOT)} -> {href}');continue
        if u.fragment:
            ts=soup if target==path.resolve() else BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            ids=own if target==path.resolve() else {x.get('id') for x in ts.find_all(id=True)}
            if u.fragment not in ids:errors.append(f'Broken anchor {path.relative_to(ROOT)} -> {href}')

def run_cli(script:Path,*args:str,ok=True,cwd:Path|None=None):
    p=subprocess.run([sys.executable,str(script),*args],cwd=cwd,capture_output=True,text=True)
    if ok and p.returncode!=0:raise AssertionError(p.stderr+p.stdout)
    if not ok and p.returncode==0:raise AssertionError('Expected failure')
    return p

def main()->int:
    errors=[];checks={}
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'));checks['manifest_entries']=len(manifest)
    if len(manifest)!=147:errors.append('Manifest must have 147 entries')
    pages=[x['page'] for x in manifest]
    if sorted(pages)!=list(range(1,148)) or len(set(pages))!=147:errors.append('PDF page coverage mismatch')
    meta=json.loads(PDF_META.read_text(encoding='utf-8'));checks['source_pdf_pages']=meta['pages']
    if meta['pages']!=147:errors.append('Source PDF metadata page count mismatch')
    # Slide files and hashes.
    bad_images=[]
    for item in manifest:
        p=ROOT/'assets/slides'/item['filename']
        if not p.exists():errors.append(f'Missing slide {p.name}');continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:errors.append(f'Hash mismatch {p.name}')
        try:
            with Image.open(p) as im:
                if im.size!=(1920,1072):bad_images.append((p.name,im.size))
                im.verify()
        except Exception as e:bad_images.append((p.name,str(e)))
    checks['slide_files']=len(list((ROOT/'assets/slides').glob('slide-*.webp')))
    if bad_images:errors.append(f'Bad slide images: {bad_images[:5]}')
    # HTML.
    soup=BeautifulSoup(HTML.read_text(encoding='utf-8'),'html.parser');figs=soup.select('figure.lesson-slide')
    checks['html_slides']=len(figs);checks['html_beginner_sections']=len(soup.select('.beginner-primer'));checks['html_hands_on_launchers']=len(soup.select('.hands-on-launcher'));checks['html_chapters']=len(soup.select('article.chapter[id^="chapter-"]'))
    if len(figs)!=147:errors.append(f'HTML slide count {len(figs)}')
    if len(soup.select('.beginner-primer'))!=40:errors.append('HTML beginner sections != 40')
    if len(soup.select('.hands-on-launcher'))!=40:errors.append('HTML hands-on launchers != 40')
    html_pages=[int(x.get('data-slide-page')) for x in figs]
    if sorted(html_pages)!=list(range(1,148)):errors.append('HTML page coverage mismatch')
    ids=[x.get('id') for x in soup.find_all(id=True)];checks['duplicate_html_ids']=len(ids)-len(set(ids))
    if len(ids)!=len(set(ids)):errors.append('Duplicate HTML IDs')
    for item in manifest:
        f=soup.find('figure',attrs={'data-slide-page':str(item['page'])})
        if not f:continue
        art=f.find_parent('article',class_='chapter');actual=art.get('id').removeprefix('chapter-') if art else None;expected=target_ch(item['target'])
        if actual!=expected:errors.append(f"HTML semantic placement p{item['page']}: expected {expected}, got {actual}")
        img=f.find('img');src=(HTML.parent/img['src']).resolve()
        if not src.exists():errors.append(f'Missing HTML image source p{item["page"]}: {img["src"]}')
    # Markdown.
    text=MD.read_text(encoding='utf-8');checks['markdown_slides']=text.count('class="lesson-slide');checks['markdown_beginner_sections']=text.count('## 完全初心者のための準備');checks['markdown_hands_on_sections']=text.count('## この章をハンズオンで開始する')
    if checks['markdown_slides']!=147:errors.append('Markdown slides != 147')
    if checks['markdown_beginner_sections']!=40:errors.append('Markdown beginner sections != 40')
    if checks['markdown_hands_on_sections']!=40:errors.append('Markdown hands-on sections != 40')
    current=None;seen=[]
    for line in text.splitlines():
        m=re.match(r'^# 第(\d+)章',line)
        if m:current=f'{int(m.group(1)):02d}'
        elif line.startswith('# 終章'):current='final'
        m=re.search(r'id="slide-page-(\d+)"',line)
        if m:seen.append((int(m.group(1)),current))
    if sorted(x[0] for x in seen)!=list(range(1,148)):errors.append('Markdown page coverage mismatch')
    by_page={x['page']:x for x in manifest}
    for page,actual in seen:
        expected=target_ch(by_page[page]['target'])
        if actual!=expected:errors.append(f'Markdown semantic placement p{page}: expected {expected}, got {actual}')
    # Original technical content and code retained after removing visual directives.
    original=(ROOT/'claude-code-blog-complete-beginner-original.md').read_text(encoding='utf-8')
    src=strip_image_directives(original);tgt=[x for x in text.splitlines() if x.strip()]
    ok,missing=ordered_subsequence(src,tgt);checks['original_content_ordered']=ok
    if not ok:errors.append(f'Original content not preserved near: {missing}')
    checks['original_code_fences']=original.count('```');checks['integrated_code_fences']=text.count('```')
    if text.count('```')<original.count('```'):errors.append('Code fences lost')
    # Local site links.
    for p in SITE.glob('*.html'):local_links(p,errors)
    # Course structure and state engine.
    index=json.loads((SKILL/'course/chapter-index.json').read_text(encoding='utf-8'));checks['course_chapters']=len(index['chapters'])
    if [x['chapter_id'] for x in index['chapters']]!=EXPECTED_KEYS:errors.append('Course chapter order mismatch')
    total_steps=0
    for item in index['chapters']:
        ch=json.loads((SKILL/f"course/chapters/chapter-{item['chapter_id']}.json").read_text(encoding='utf-8'));total_steps+=len(ch['steps'])
        if len(ch['steps'])!=4:errors.append(f"Chapter {item['chapter_id']} steps != 4")
        if ch['blog_anchor']!=f"#chapter-{item['chapter_id']}":errors.append(f"Chapter {item['chapter_id']} blog anchor")
        for f in ch.get('fixtures',[]):
            if not (SKILL/'course/assets'/f).exists():errors.append(f'Missing fixture {f}')
    checks['course_steps']=total_steps
    script=SKILL/'scripts/textbook_lab.py'
    try:
        j=json.loads(run_cli(script,'validate-course','--json').stdout);checks['course_validator']=j['status']
        if j['status']!='PASS':errors.append('Course validator failed')
        with tempfile.TemporaryDirectory() as td:
            w=Path(td)
            out=json.loads(run_cli(script,'start','12','--runtime','cursor','--workspace',td,'--json').stdout)
            if out['chapter_id']!='12' or out['step']['step_id']!='12-01':errors.append('Start routing failed')
            # Out-of-order guard.
            p=run_cli(script,'complete','--step-id','12-02','--evidence-type','file','--evidence','x','--workspace',td,'--json',ok=False)
            if 'Out-of-order' not in (p.stderr+p.stdout):errors.append('Out-of-order guard message missing')
            lab=w/'learning-lab/chapter-12-skills';note=lab/'concept-note.md';note.write_text('目的、入力、成果物、証拠を整理しました。',encoding='utf-8')
            run_cli(script,'complete','--evidence-type','file','--evidence',str(note),'--workspace',td,'--json')
            skill=lab/'my-first-skill/SKILL.md';skill.parent.mkdir(parents=True,exist_ok=True);skill.write_text('---\nname: demo\ndescription: demo\n---\n\n# Workflow\n',encoding='utf-8')
            run_cli(script,'complete','--evidence-type','file','--evidence',str(skill),'--workspace',td,'--json')
            ver=lab/'verification.md';ver.write_text('入力、Workflow、出力契約、安全、品質確認をレビューしました。',encoding='utf-8')
            run_cli(script,'complete','--evidence-type','file','--evidence',str(ver),'--workspace',td,'--json')
            end=json.loads(run_cli(script,'complete','--evidence-type','answer','--evidence','Skillは成功手順を別の入力でも再現するための業務パッケージであり、成果物と品質確認を契約として持ちます。','--workspace',td,'--json').stdout)
            if end['status']!='verified':errors.append('Chapter completion failed')
            run_cli(script,'save','--summary','api_key=supersecret123 第12章完了','--workspace',td,'--json')
            state=json.loads((w/'.trepro-learning/textbook-state.json').read_text())
            if 'supersecret' in json.dumps(state):errors.append('Secret masking failed')
            res=json.loads(run_cli(script,'resume','--workspace',td,'--json').stdout)
            if res['chapter_id']!='12':errors.append('Resume failed')
            run_cli(script,'switch-runtime','--runtime','codex','--workspace',td,'--json')
            sw=json.loads(run_cli(script,'current','--workspace',td,'--json').stdout)
            if sw['runtime']!='codex':errors.append('Runtime switch failed')
            outside=Path(td).parent/'outside-evidence.txt';outside.write_text('outside')
            run_cli(script,'start','4','--workspace',td,'--json')
            p=run_cli(script,'complete','--evidence-type','file','--evidence',str(outside),'--workspace',td,'--json',ok=False)
            if 'inside workspace' not in (p.stderr+p.stdout):errors.append('Outside evidence guard failed')
    except Exception as e:errors.append(f'State engine test: {e}')
    # Installer dry-run and real project install.
    try:
        inst=ROOT/'hands-on/install.sh'
        p=subprocess.run([str(inst),'--runtime','all','--scope','project','--target','/tmp/trepro-installer-dry','--dry-run'],capture_output=True,text=True)
        if p.returncode or p.stdout.count('Would install')!=3:errors.append('Installer dry-run failed')
        with tempfile.TemporaryDirectory() as td:
            p=subprocess.run([str(inst),'--runtime','all','--scope','project','--target',td],capture_output=True,text=True)
            if p.returncode:errors.append('Installer project run failed')
            for rel in ['.cursor/skills/textbook-chapter-lab/SKILL.md','.claude/skills/textbook-chapter-lab/SKILL.md','.agents/skills/textbook-chapter-lab/SKILL.md','trepro-textbook']:
                if not (Path(td)/rel).exists():errors.append(f'Installer missing {rel}')
    except Exception as e:errors.append(f'Installer test: {e}')
    status='PASS' if not errors else 'FAIL'
    report=['# Experiential Edition Validation Report','',f'- Status: **{status}**','', '## Checks','']+[f'- **{k}**: {v}' for k,v in checks.items()]+['','## Failures','']+([f'- {e}' for e in errors] if errors else ['- None'])
    out='\n'.join(report)+'\n';(ROOT/'EXPERIENTIAL_VALIDATION_REPORT.md').write_text(out,encoding='utf-8');print(out);return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
