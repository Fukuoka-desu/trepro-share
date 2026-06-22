#!/usr/bin/env python3
from __future__ import annotations

import json, re, shutil
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
CANON=ROOT/'hands-on'/'skill'/'textbook-chapter-lab'
COURSE=CANON/'course'
ASSETS=COURSE/'assets'
CHAPTER_DIR=COURSE/'chapters'
SUPPLEMENTS=json.loads((ROOT/'beginner_supplements.json').read_text(encoding='utf-8'))
MANIFEST=json.loads((ROOT/'slide_integration_manifest.json').read_text(encoding='utf-8'))
SOUP=BeautifulSoup((ROOT/'site'/'complete.html').read_text(encoding='utf-8'),'html.parser')

FIXTURE_CONTENT={
'meeting-transcript.md':'''# Product Weekly Meeting\n\nDate: 2026-06-18\nParticipants: Haruka, Ren, Misaki\n\nHaruka: The onboarding guide is hard to find. Ren will make an HTML index by June 25.\nMisaki: Security review is required before sharing. I will review it by June 27.\nDecision: Use a local preview first. Do not publish externally.\nOpen question: Who owns monthly maintenance?\n''',
'vague-request.txt':'いい感じの資料を作ってください。なるべく早く、最高品質でお願いします。\n',
'mock-mcp-data.json':json.dumps({'calendar':[{'date':'2026-06-25','title':'Security review'}],'permissions':['read'],'write_enabled':False},ensure_ascii=False,indent=2)+'\n',
'meetings.json':json.dumps({'updated_at':'2026-06-22T09:00:00Z','meetings':[{'title':'Product Weekly','status':'fresh','tasks':2},{'title':'Sales Sync','status':'stale','tasks':1}]},ensure_ascii=False,indent=2)+'\n',
'sample-log.jsonl':'{"at":"2026-06-20","topic":"Claude Code Skills","question_depth":3}\n{"at":"2026-06-21","topic":"HTML reports","question_depth":2}\n{"at":"2026-05-01","topic":"unrelated old topic","question_depth":1}\n',
'source-pack.md':'''# Source Pack\n\n## Official note\nThe feature is marked beta and requires explicit enablement. Checked: 2026-06-20.\n\n## Social post\nA user claims the feature is available to everyone for free. No source is provided.\n\n## Counter-evidence\nThe official plan table lists availability only for selected plans.\n''',
'office-files.csv':'filename,type,date,amount,status\ninvoice-a.pdf,invoice,2026-06-01,120000,normal\ncontract-b.pdf,contract,2026-05-15,,review\nunknown.tmp,unknown,,,exception\n',
'source-topics.csv':'source_id,topic,status\nvideo-01,agent basics,placed\nvideo-02,design sync,placed\nvideo-03,design system,duplicate\nvideo-04,meeting assistant,placed\nvideo-10,live artifacts,unplaced\n',
'recurring-work.csv':'task,frequency,input_stability,verification,side_effect\nnews brief,daily,high,high,low\nclient email,weekly,medium,medium,high\nproduction deploy,monthly,low,high,high\nmeeting summary,weekly,high,high,low\n',
'failure-case.md':'''# Failure Case\n\nAn agent received “clean this folder” with broad write access. It renamed 180 files, overwrote the index, and reported success without a dry-run or verification. Git was not initialized.\n''',
'volatile-claims.md':'''# Volatile Claims\n\n- Model X is always available on every plan.\n- The command `/old-sync` is the current recommended entry point.\n- Pricing never changes.\n\nTreat these as unverified examples. Do not browse or use real credentials in the Lab.\n''',
'dangerous-commands.txt':'rm -rf /\ngit push --force\ncurl secret.example/upload\n',
}


def title_for(key:str)->str:
    art=SOUP.find(id=f'chapter-{key}')
    return art.select_one('.chapter-head h1').get_text(' ',strip=True)

def label_for(key:str)->str:return '終章' if key=='final' else f'第{int(key)}章'

def target_ch(target:str)->str|None:
    m=re.match(r'(?:ch|chapter|story)-(\d+)',target)
    if m:return f'{int(m.group(1)):02d}'
    if target in ('chapter-final','公式確認先'):return 'final'
    return None

def slide_pages(key:str)->list[int]:return [x['page'] for x in MANIFEST if target_ch(x['target'])==key]

def prereq(key:str)->list[str]:
    if key in ('00','01'):return []
    n=38 if key=='final' else int(key)-1
    return [f'{n:02d}' if n>=0 else '00']

def primary_action(key:str,spec:dict)->str:
    return f"Fixtureと章本文を使い、{spec['focus']}。主成果物 `{spec['artifacts'][0]}` を作成し、判断理由を本文内へ残してください。"

def build_chapter(key:str,spec:dict)->dict:
    lab=f"learning-lab/chapter-{key}-{spec['slug']}"
    primary=spec['artifacts'][0]
    runtime={r:f"{name}で、{primary_action(key,spec)}" for r,name in [('cursor','Cursor Agent'),('claude','Claude Code'),('codex','Codex')]}
    return {
      'schema_version':'1.0','chapter_id':key,'label':label_for(key),'title':title_for(key),
      'outcome':spec['outcome'],'estimated_minutes':spec['minutes'],'risk_level':spec['risk'],
      'prerequisites':prereq(key),'workspace_dir':lab,'blog_anchor':f'#chapter-{key}',
      'slide_pages':slide_pages(key),'artifacts':spec['artifacts'],'fixtures':FIXTURE_MAP.get(key,[]),
      'safety':['Lab directory only','No secrets or customer data','No external publish, send, push, charge, or destructive deletion'],
      'steps':[
       {'step_id':f'{key}-01','title':'概念を自分の言葉にする','objective':spec['outcome'],
        'learner_action':f"ブログの{label_for(key)}とスライド {slide_pages(key) or ['なし']} を読み、重要点3つ・疑問1つ・完了証拠を `{lab}/concept-note.md` に書く。",
        'runtime_variants':{r:f"{name}に読み取りだけを依頼し、最後は自分の言葉で `{lab}/concept-note.md` を完成させる。" for r,name in [('cursor','Cursor Agent'),('claude','Claude Code'),('codex','Codex')]},
        'expected_result':'章の目的と自分の作業が結び付いた短いメモ','evidence':{'type':'file','description':f'{lab}/concept-note.md'}},
       {'step_id':f'{key}-02','title':'章の主成果物を作る','objective':spec['focus'],'learner_action':primary_action(key,spec),
        'runtime_variants':runtime,'expected_result':f"空でない `{primary}` がLab内に存在する",'evidence':{'type':'file','description':f'{lab}/{primary}'}},
       {'step_id':f'{key}-03','title':'証拠でVerifyする','objective':'作った本人の感想ではなく要件と証拠で確認する',
        'learner_action':f"成果物を開き、正しい点・不足・安全確認を `{lab}/verification.md` に記録する。コードがある場合はローカル実行結果も記録する。",
        'runtime_variants':{r:f"{name}には読み取りReviewだけを依頼し、指摘を確認して `{lab}/verification.md` を作る。" for r,name in [('cursor','Cursor Agent'),('claude','Claude Code'),('codex','Codex')]},
        'expected_result':'合格条件・不足・次の修正が具体的に残る','evidence':{'type':'file','description':f'{lab}/verification.md'}},
       {'step_id':f'{key}-04','title':'理解を説明し保存する','objective':'別の日・別Runtimeでも再現できる状態を作る',
        'learner_action':f"「{spec['outcome']}とは何か」「この成果物で何を証明したか」を80文字以上で説明し、保存を実行する。",
        'runtime_variants':{r:f"{name}へ説明を返した後、『保存』と伝える。" for r,name in [('cursor','Cursor Agent'),('claude','Claude Code'),('codex','Codex')]},
        'expected_result':'具体的な説明とRESUME.mdが残る','evidence':{'type':'answer','description':'80文字以上の理解説明'}}
      ]
    }

FIXTURE_MAP={k:v for k,v in {
'04':['meeting-transcript.md'],'05':['vague-request.txt'],'07':['dangerous-commands.txt'],'15':['mock-mcp-data.json'],'18':['meetings.json'],'19':['sample-log.jsonl'],'22':['source-pack.md'],'28':['office-files.csv'],'29':['source-topics.csv'],'32':['recurring-work.csv'],'33':['failure-case.md'],'37':['volatile-claims.md'],'38':['source-topics.csv'],'final':['meeting-transcript.md','source-pack.md']}.items()}

SKILL='''---
name: textbook-chapter-lab
description: Claude Code実践教科書の第0章〜第38章・終章を、Cursor、Claude Code、Codexで実際に操作しながら学ぶ章番号ハンズオン。ユーザーが「第12章を開始」「チャプター4」「23章から実践」「保存」「再開」「この章で質問」と言った時に使う。通常の開発代行だけを求める依頼には使わない。
---

# Textbook Chapter Lab

## Mission

章番号を受け取ったら、確認質問で止めずに該当Labを開き、1Turnに1操作ずつ案内する。進捗の正本は会話ではなく `.trepro-learning/textbook-state.json` とする。

## Chapter routing

- `0`〜`38`、`第12章`、`チャプター12`、`chapter 12`、`ch-12` を認識する。
- `final`、`終章`、`最後` は終章へ対応する。
- 前提章が未完了でも開始できる。必要な前提だけ短く表示する。
- 章番号がない「再開」は保存済みCurrent Chapterを使う。

## CLI locator

最初に `command -v trepro-textbook` を確認する。なければProject内の `./trepro-textbook`、`.agents/skills/.../scripts/textbook_lab.py`、`.claude/skills/...`、`.cursor/skills/...`、`hands-on/skill/...` の順で探す。Python Scriptを直接使う場合は `python3 <path>` とする。Stateを手編集しない。

## Start immediately

```bash
trepro-textbook start <chapter> --runtime <cursor|claude|codex> --json
```

同じ章が進行中なら `resume --json` を使う。返された `step` と `runtime_instruction` から、次の一操作だけを提示する。

## Turn format

```text
[第X章 | Step A/B | Runtime | Status]
目的: このStepで身につけること
今やること: 一つの具体操作
期待結果: 何が見えれば成功か
証拠: 完了に必要なEvidence
困った時: 最初に確認する一点
返答: 「できた」「できない」「質問」「保存」
```

## Progress and evidence

- 「できた」だけで完了にしない。Current StepのEvidenceを確認する。
- `file` はWorkspace内の空でないFile、`answer`・`review`は具体的説明、`command`は`exit=0`または`PASS`を要求する。
- 質問だけでは進捗を変更しない。順不同完了を認めない。

```bash
trepro-textbook complete --step-id <id> --evidence-type <type> --evidence <value> --json
```

## Save and resume

```bash
trepro-textbook save --summary "現在地と次の一操作" --json
trepro-textbook resume --json
trepro-textbook switch-runtime --runtime <cursor|claude|codex> --json
```

## Support protocol

質問には、直接回答 → なぜ → 今のStepへ戻る一操作、の順で答える。Error時は全文、Working Directory、直前操作を確認し、読み取り専用診断から始める。

## Safety

- Current Chapterの `learning-lab/` 以下だけを編集する。
- Secret、顧客データ、本番DBを使わない。
- Bypass、外部送信、Deploy、Git push、課金、破壊的削除、無断Installを行わない。
- 管理者章もFixtureとDry-runが既定。第31章はPreviewまで、第15章はMock接続だけ。

## Runtime invocation

- Cursor: `第12章を開始`
- Claude Code: `/textbook-chapter-lab 12`
- Codex: `$textbook-chapter-lab 第12章を開始`

全章一覧は `references/chapter-map.md`、Runtime差分は `references/runtime-guide.md`、安全規則は `references/safety-policy.md` を必要時だけ読む。
'''

STATE_ENGINE=r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, contextlib, datetime as dt, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from typing import Any, Iterator
STATE_DIR='.trepro-learning'; STATE_FILE='textbook-state.json'; SCHEMA_VERSION=1

def now(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
def skill_root(): return Path(__file__).resolve().parent.parent
def course_root(): return skill_root()/'course'
def load_json(p:Path):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except FileNotFoundError: raise SystemExit(f'File not found: {p}')
    except json.JSONDecodeError as e: raise SystemExit(f'Invalid JSON: {p}: {e}')
def atomic_json(p:Path,data:Any):
    p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=p.name+'.',dir=str(p.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def workspace(explicit:str|None=None)->Path:
    if explicit:return Path(explicit).expanduser().resolve()
    cur=Path.cwd().resolve()
    for c in [cur,*cur.parents]:
        if (c/STATE_DIR/STATE_FILE).exists():return c
        if (c/'.git').exists():break
    return cur
def wid(root:Path):return hashlib.sha256(str(root).encode()).hexdigest()[:16]
def state_path(root:Path):return root/STATE_DIR/STATE_FILE
@contextlib.contextmanager
def lock(root:Path)->Iterator[None]:
    d=root/STATE_DIR;d.mkdir(parents=True,exist_ok=True);p=d/'.textbook-lock'
    try:p.mkdir()
    except FileExistsError:
        if time.time()-p.stat().st_mtime>60:shutil.rmtree(p);p.mkdir()
        else:raise SystemExit('State is locked; retry shortly')
    try:yield
    finally:shutil.rmtree(p,ignore_errors=True)
def normalize(raw:str)->str:
    s=raw.strip().lower()
    if s in {'final','ending','終章','最後','終章を開始'}:return 'final'
    s=re.sub(r'(chapter|chap|ch|チャプター|第|章|から実践|から開始|を開始|を始める|[-_ ])','',s)
    if not s.isdigit():raise SystemExit(f'章番号を認識できません: {raw}')
    n=int(s)
    if not 0<=n<=38:raise SystemExit('章番号は0〜38、または終章です')
    return f'{n:02d}'
def load_index():return load_json(course_root()/'chapter-index.json')
def load_chapter(key:str):return load_json(course_root()/'chapters'/f'chapter-{key}.json')
def runtime_auto():
    e=os.environ
    if e.get('CLAUDECODE') or e.get('CLAUDE_CODE_ENTRYPOINT'):return 'claude'
    if e.get('CODEX_HOME') or e.get('CODEX_THREAD_ID'):return 'codex'
    if e.get('CURSOR_AGENT') or e.get('CURSOR_TRACE_ID'):return 'cursor'
    return 'auto'
def sanitize(v:str)->str:
    for p in [r'\bsk-[A-Za-z0-9_-]{12,}\b',r'\bghp_[A-Za-z0-9]{12,}\b',r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*\S+']:v=re.sub(p,'[REDACTED]',v)
    return v[:4000]
def load_state(root:Path)->dict:
    p=state_path(root)
    if not p.exists():raise SystemExit('State未作成です。start <章番号> を実行してください')
    s=load_json(p)
    if s.get('workspace_id')!=wid(root):raise SystemExit('State belongs to another workspace')
    return s
def ensure_gitignore(root:Path):
    p=root/'.gitignore';line=f'{STATE_DIR}/';text=p.read_text(encoding='utf-8',errors='replace') if p.exists() else ''
    if line not in text.splitlines():p.write_text(text+('' if not text or text.endswith('\n') else '\n')+line+'\n',encoding='utf-8')
def copy_fixture(src:Path,dst:Path):
    if src.is_dir():shutil.copytree(src,dst,dirs_exist_ok=True)
    else:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
def ensure_lab(root:Path,ch:dict)->Path:
    lab=root/ch['workspace_dir'];lab.mkdir(parents=True,exist_ok=True);(lab/'fixtures').mkdir(exist_ok=True)
    for rel in ch.get('fixtures',[]):
        src=course_root()/'assets'/rel;dst=lab/'fixtures'/Path(rel).name
        if not dst.exists():copy_fixture(src,dst)
    readme=lab/'README.md'
    if not readme.exists():readme.write_text(f"# {ch['label']} {ch['title']} - Hands-on Lab\n\n- Outcome: {ch['outcome']}\n- Risk: {ch['risk_level']}\n- Rule: このFolder以下だけを編集する。秘密情報・外部公開・削除・課金は行わない。\n",encoding='utf-8')
    ensure_gitignore(root);return lab
def current_obj(state:dict)->tuple[dict,dict|None]:
    key=state['current_chapter_id'];ch=load_chapter(key);cs=state['chapters'][key];done=set(cs.get('completed_steps',[]));step=next((x for x in ch['steps'] if x['step_id'] not in done),None);return ch,step
def resume_md(root:Path,state:dict)->str:
    ch,step=current_obj(state);cs=state['chapters'][ch['chapter_id']]
    return '\n'.join(['# Textbook Hands-on Resume','',f"- Updated: {state['updated_at']}",f"- Runtime: {state['runtime']}",f"- Chapter: {ch['label']} {ch['title']}",f"- Status: {cs['status']}",f"- Progress: {len(cs.get('completed_steps',[]))}/{len(ch['steps'])}",f"- Lab: {root/ch['workspace_dir']}",f"- Blocker: {cs.get('blocker') or 'なし'}",'', '## Next action','',step['learner_action'] if step else 'この章は完了しています。','',f"再開: `trepro-textbook resume --workspace {root}`",''])
def save_state(root:Path,state:dict):state['updated_at']=now();atomic_json(state_path(root),state);(root/STATE_DIR/'RESUME.md').write_text(resume_md(root,state),encoding='utf-8')
def view(root:Path,state:dict)->dict:
    ch,step=current_obj(state);cs=state['chapters'][ch['chapter_id']];out={'course_id':state['course_id'],'course_version':state['course_version'],'runtime':state['runtime'],'chapter_id':ch['chapter_id'],'label':ch['label'],'title':ch['title'],'outcome':ch['outcome'],'estimated_minutes':ch['estimated_minutes'],'risk_level':ch['risk_level'],'prerequisites':ch['prerequisites'],'lab_path':str(root/ch['workspace_dir']),'artifacts':ch['artifacts'],'slide_pages':ch['slide_pages'],'blog_anchor':ch['blog_anchor'],'status':cs['status'],'progress':{'completed':len(cs.get('completed_steps',[])),'total':len(ch['steps'])},'blocker':cs.get('blocker'),'step':step}
    if step:out['runtime_instruction']=step.get('runtime_variants',{}).get(state['runtime'],step['learner_action'])
    return out
def emit(data:Any,j:bool):print(json.dumps(data,ensure_ascii=False,indent=2) if j or not isinstance(data,str) else data)
def cmd_validate(args):
    idx=load_index();fails=[];ids=[]
    if idx.get('chapter_count')!=40:fails.append('chapter_count')
    for item in idx['chapters']:
        ch=load_chapter(item['chapter_id']);ids.append(ch['chapter_id'])
        if len(ch.get('steps',[]))!=4:fails.append(ch['chapter_id']+':steps')
        for f in ch.get('fixtures',[]):
            if not (course_root()/'assets'/f).exists():fails.append(ch['chapter_id']+':fixture:'+f)
    if len(set(ids))!=40:fails.append('unique ids')
    r={'status':'PASS' if not fails else 'FAIL','chapters':len(ids),'steps':sum(len(load_chapter(x)['steps']) for x in ids),'failures':fails};emit(r,args.json);return 0 if not fails else 1
def cmd_doctor(args):
    root=workspace(args.workspace);cmds={}
    for c in ['git','python3','node','claude','codex','cursor']:
        p=shutil.which(c);cmds[c]={'available':bool(p),'path':p}
    emit({'workspace':str(root),'state_exists':state_path(root).exists(),'runtime_detected':runtime_auto(),'commands':cmds},args.json);return 0
def cmd_list(args):
    items=[{'chapter_id':x['chapter_id'],'label':x['label'],'title':x['title'],'minutes':x['estimated_minutes'],'risk':x['risk_level']} for x in load_index()['chapters']];emit(items,args.json);return 0
def cmd_start(args):
    root=workspace(args.workspace);root.mkdir(parents=True,exist_ok=True);key=normalize(args.chapter);ch=load_chapter(key);rt=args.runtime if args.runtime!='auto' else runtime_auto()
    with lock(root):
        if state_path(root).exists():state=load_state(root)
        else:state={'schema_version':SCHEMA_VERSION,'course_id':'claude-code-textbook-hands-on','course_version':load_index()['version'],'workspace_id':wid(root),'workspace_path':str(root),'runtime':rt,'current_chapter_id':key,'chapters':{},'history':[],'created_at':now(),'updated_at':now()}
        if args.restart or key not in state['chapters']:state['chapters'][key]={'status':'active','completed_steps':[],'evidence':{},'blocker':None,'started_at':now(),'updated_at':now()}
        state['runtime']=rt;state['current_chapter_id']=key
        if state['chapters'][key]['status']!='verified':state['chapters'][key]['status']='active'
        state['history'].append({'at':now(),'action':'start','chapter_id':key,'runtime':rt});ensure_lab(root,ch);save_state(root,state)
    emit(view(root,state),args.json);return 0
def cmd_current(args):root=workspace(args.workspace);emit(view(root,load_state(root)),args.json);return 0
def cmd_status(args):
    root=workspace(args.workspace);s=load_state(root);rows=[]
    for key,cs in s['chapters'].items():ch=load_chapter(key);rows.append({'chapter_id':key,'title':ch['title'],'status':cs['status'],'completed':len(cs.get('completed_steps',[])),'total':len(ch['steps'])})
    emit({'runtime':s['runtime'],'current_chapter_id':s['current_chapter_id'],'chapters':rows},args.json);return 0
def valid_evidence(root:Path,step:dict,typ:str,val:str)->str:
    expected=step['evidence']['type']
    if typ!=expected:raise SystemExit(f'Evidence type mismatch: expected {expected}, got {typ}')
    val=sanitize(val.strip())
    if typ=='file':
        p=Path(val);p=(root/p).resolve() if not p.is_absolute() else p.resolve()
        try:p.relative_to(root.resolve())
        except ValueError:raise SystemExit('Evidence file must be inside workspace')
        if not p.exists() or not p.is_file() or p.stat().st_size==0:raise SystemExit(f'File evidence missing or empty: {p}')
        return str(p.relative_to(root))
    if typ=='command' and not re.search(r'(?i)(exit\s*(code)?\s*[=:]?\s*0|exit=0|成功|pass)',val):raise SystemExit('Command evidence must include exit=0 or PASS')
    if typ in {'answer','review','manual'} and len(val)<20:raise SystemExit('Evidence must be at least 20 characters')
    return val
def cmd_complete(args):
    root=workspace(args.workspace)
    with lock(root):
        state=load_state(root);ch,step=current_obj(state)
        if step is None:raise SystemExit('Current chapter is already complete')
        if args.step_id and args.step_id!=step['step_id']:raise SystemExit(f"Out-of-order step. Current: {step['step_id']}")
        ev=valid_evidence(root,step,args.evidence_type,args.evidence);cs=state['chapters'][ch['chapter_id']];cs['completed_steps'].append(step['step_id']);cs['evidence'][step['step_id']]={'type':args.evidence_type,'value':ev,'at':now()};cs['updated_at']=now();cs['blocker']=None
        if len(cs['completed_steps'])==len(ch['steps']):cs['status']='verified';cs['verified_at']=now()
        state['history'].append({'at':now(),'action':'complete','chapter_id':ch['chapter_id'],'step_id':step['step_id']});save_state(root,state)
    emit(view(root,state),args.json);return 0
def cmd_save(args):
    root=workspace(args.workspace)
    with lock(root):
        s=load_state(root);s['last_summary']=sanitize(args.summary);d=root/STATE_DIR/'checkpoints';d.mkdir(parents=True,exist_ok=True);p=d/(dt.datetime.now().strftime('%Y%m%d-%H%M%S')+'.json');atomic_json(p,s);save_state(root,s)
    emit({'saved':True,'checkpoint':str(p),'resume':str(root/STATE_DIR/'RESUME.md')},args.json);return 0
def cmd_resume(args):root=workspace(args.workspace);s=load_state(root);emit(view(root,s),args.json);return 0
def cmd_switch(args):
    root=workspace(args.workspace)
    with lock(root):s=load_state(root);s['runtime']=args.runtime;s['history'].append({'at':now(),'action':'switch-runtime','runtime':args.runtime});save_state(root,s)
    emit(view(root,s),args.json);return 0
def cmd_block(args):
    root=workspace(args.workspace)
    with lock(root):s=load_state(root);cs=s['chapters'][s['current_chapter_id']];cs['blocker']=sanitize(args.reason);cs['status']='blocked';save_state(root,s)
    emit(view(root,s),args.json);return 0
def cmd_unblock(args):
    root=workspace(args.workspace)
    with lock(root):s=load_state(root);cs=s['chapters'][s['current_chapter_id']];cs['blocker']=None;cs['status']='active';save_state(root,s)
    emit(view(root,s),args.json);return 0
def parser():
    p=argparse.ArgumentParser(prog='trepro-textbook');p.add_argument('--json',action='store_true');sub=p.add_subparsers(dest='cmd',required=True)
    def common(sp):sp.add_argument('--workspace')
    sp=sub.add_parser('validate-course');sp.set_defaults(fn=cmd_validate)
    sp=sub.add_parser('doctor');common(sp);sp.set_defaults(fn=cmd_doctor)
    sp=sub.add_parser('list');sp.set_defaults(fn=cmd_list)
    sp=sub.add_parser('start');sp.add_argument('chapter');sp.add_argument('--runtime',choices=['auto','cursor','claude','codex'],default='auto');sp.add_argument('--restart',action='store_true');common(sp);sp.set_defaults(fn=cmd_start)
    for n,f in [('current',cmd_current),('status',cmd_status),('resume',cmd_resume)]:sp=sub.add_parser(n);common(sp);sp.set_defaults(fn=f)
    sp=sub.add_parser('complete');sp.add_argument('--step-id');sp.add_argument('--evidence-type',required=True,choices=['file','command','manual','answer','review']);sp.add_argument('--evidence',required=True);common(sp);sp.set_defaults(fn=cmd_complete)
    sp=sub.add_parser('save');sp.add_argument('--summary',required=True);common(sp);sp.set_defaults(fn=cmd_save)
    sp=sub.add_parser('switch-runtime');sp.add_argument('--runtime',required=True,choices=['cursor','claude','codex']);common(sp);sp.set_defaults(fn=cmd_switch)
    sp=sub.add_parser('block');sp.add_argument('--reason',required=True);common(sp);sp.set_defaults(fn=cmd_block)
    sp=sub.add_parser('unblock');common(sp);sp.set_defaults(fn=cmd_unblock)
    return p
def main():
    argv=sys.argv[1:];want_json='--json' in argv;argv=[x for x in argv if x!='--json']
    commands={'validate-course','doctor','list','start','current','status','resume','complete','save','switch-runtime','block','unblock'}
    if argv and argv[0] not in commands and not argv[0].startswith('-'):argv=['start',argv[0],*argv[1:]]
    p=parser();args=p.parse_args(argv);args.json=want_json or getattr(args,'json',False);raise SystemExit(args.fn(args))
if __name__=='__main__':main()
'''

INSTALL=r'''#!/usr/bin/env bash
set -euo pipefail
RUNTIME="";SCOPE="project";TARGET="";DRY_RUN=0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";SOURCE="$ROOT/skill/textbook-chapter-lab"
usage(){ echo "Usage: ./install.sh --runtime cursor|claude|codex|all [--scope project|user] [--target PATH] [--dry-run]"; }
while [[ $# -gt 0 ]];do case "$1" in --runtime)RUNTIME="${2:-}";shift 2;;--scope)SCOPE="${2:-}";shift 2;;--target)TARGET="${2:-}";shift 2;;--dry-run)DRY_RUN=1;shift;;-h|--help)usage;exit 0;;*)echo "Unknown: $1" >&2;usage;exit 2;;esac;done
[[ "$RUNTIME" =~ ^(cursor|claude|codex|all)$ ]]||{ echo "--runtime required" >&2;exit 2; };[[ "$SCOPE" =~ ^(project|user)$ ]]||{ echo "invalid scope" >&2;exit 2; }
if [[ "$SCOPE" == project ]];then TARGET="${TARGET:-$PWD}";mkdir -p "$TARGET";TARGET="$(cd "$TARGET"&&pwd)";else TARGET="${TARGET:-$HOME}";fi
copy_skill(){ local dst="$1";if [[ $DRY_RUN -eq 1 ]];then echo "Would install: $dst";return;fi;mkdir -p "$(dirname "$dst")";[[ -e "$dst" ]]&&mv "$dst" "$dst.bak.$(date +%Y%m%d%H%M%S)";cp -R "$SOURCE" "$dst";echo "Installed: $dst"; }
case "$RUNTIME" in cursor)copy_skill "$TARGET/.cursor/skills/textbook-chapter-lab";;claude)copy_skill "$TARGET/.claude/skills/textbook-chapter-lab";;codex)copy_skill "$TARGET/.agents/skills/textbook-chapter-lab";;all)copy_skill "$TARGET/.cursor/skills/textbook-chapter-lab";copy_skill "$TARGET/.claude/skills/textbook-chapter-lab";copy_skill "$TARGET/.agents/skills/textbook-chapter-lab";;esac
if [[ $DRY_RUN -eq 0 ]];then
 if [[ "$SCOPE" == project ]];then cat > "$TARGET/trepro-textbook" <<EOF
#!/usr/bin/env bash
set -euo pipefail
ROOT="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
for P in "\$ROOT/.agents/skills/textbook-chapter-lab/scripts/textbook_lab.py" "\$ROOT/.claude/skills/textbook-chapter-lab/scripts/textbook_lab.py" "\$ROOT/.cursor/skills/textbook-chapter-lab/scripts/textbook_lab.py";do [[ -f "\$P" ]]&&exec python3 "\$P" "\$@";done
echo "Skill script not found" >&2;exit 1
EOF
 chmod +x "$TARGET/trepro-textbook";echo "CLI: $TARGET/trepro-textbook"
 else BIN="$HOME/.local/bin";SHARE="$HOME/.local/share/trepro-textbook-chapter-lab";mkdir -p "$BIN" "$SHARE";rm -rf "$SHARE/skill";cp -R "$SOURCE" "$SHARE/skill";cat > "$BIN/trepro-textbook" <<EOF
#!/usr/bin/env bash
exec python3 "$SHARE/skill/scripts/textbook_lab.py" "\$@"
EOF
 chmod +x "$BIN/trepro-textbook";echo "CLI: $BIN/trepro-textbook";fi
fi
'''


def main():
    if (ROOT/'hands-on').exists():shutil.rmtree(ROOT/'hands-on')
    for d in [ASSETS,CHAPTER_DIR,CANON/'scripts',CANON/'references']:d.mkdir(parents=True,exist_ok=True)
    for name,text in FIXTURE_CONTENT.items():(ASSETS/name).write_text(text,encoding='utf-8')
    chapters=[]
    for key,spec in SUPPLEMENTS.items():
        ch=build_chapter(key,spec);chapters.append({k:ch[k] for k in ['chapter_id','label','title','estimated_minutes','risk_level','outcome','workspace_dir','artifacts','slide_pages']});(CHAPTER_DIR/f'chapter-{key}.json').write_text(json.dumps(ch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    index={'schema_version':'1.0','course_id':'claude-code-textbook-hands-on','version':'2026.06.22','chapter_count':40,'chapters':chapters}
    (COURSE/'chapter-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (CANON/'SKILL.md').write_text(SKILL,encoding='utf-8');(CANON/'scripts'/'textbook_lab.py').write_text(STATE_ENGINE,encoding='utf-8');(CANON/'scripts'/'textbook_lab.py').chmod(0o755)
    rows=['# Chapter Map','', '| Chapter | Title | Minutes | Risk | Start | Primary artifact |','|---|---|---:|---|---|---|']
    for ch in chapters:rows.append(f"| {ch['label']} | {ch['title']} | {ch['estimated_minutes']} | {ch['risk_level']} | `{ch['label']}を開始` | `{ch['artifacts'][0]}` |")
    (CANON/'references'/'chapter-map.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    (CANON/'references'/'runtime-guide.md').write_text('# Runtime Guide\n\n- Cursor: `第12章を開始`\n- Claude Code: `/textbook-chapter-lab 12`\n- Codex: `$textbook-chapter-lab 第12章を開始`\n- 共通State: `.trepro-learning/textbook-state.json`\n',encoding='utf-8')
    (CANON/'references'/'safety-policy.md').write_text('# Safety Policy\n\nLab外編集、秘密情報、本番DB、外部送信、公開、課金、Git push、Bypass、破壊的削除を行わない。管理者章もFixtureとDry-runで学ぶ。\n',encoding='utf-8')
    H=ROOT/'hands-on';(H/'install.sh').write_text(INSTALL,encoding='utf-8');(H/'install.sh').chmod(0o755)
    (H/'README.md').write_text('# 章番号ハンズオン Skill\n\n展開したフォルダをCursor、Claude Code、Codexで開き、`第12章を開始` と入力します。別Projectへは `./hands-on/install.sh --runtime all --scope project --target /path/to/project` を使用します。進捗は `.trepro-learning/` に保存されます。\n',encoding='utf-8')
    # Package-native copies.
    for rel in ['.cursor/skills/textbook-chapter-lab','.claude/skills/textbook-chapter-lab','.agents/skills/textbook-chapter-lab']:
        dst=ROOT/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(CANON,dst,dirs_exist_ok=True)
    wrapper=ROOT/'trepro-textbook';wrapper.write_text('#!/usr/bin/env bash\nset -euo pipefail\nROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\nexec python3 "$ROOT/.agents/skills/textbook-chapter-lab/scripts/textbook_lab.py" "$@"\n',encoding='utf-8');wrapper.chmod(0o755)
    (ROOT/'CHAPTER_HANDS_ON_MAP.md').write_text((CANON/'references'/'chapter-map.md').read_text(encoding='utf-8'),encoding='utf-8')
    print(json.dumps({'chapters':len(chapters),'steps':sum(len(json.loads((CHAPTER_DIR/f"chapter-{c['chapter_id']}.json").read_text())['steps']) for c in chapters),'skill_files':len(list(CANON.rglob('*')))},ensure_ascii=False))
if __name__=='__main__':main()
