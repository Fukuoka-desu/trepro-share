#!/usr/bin/env python3
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
