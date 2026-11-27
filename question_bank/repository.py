"""Validate local bank and import text-only eligible questions into private Supabase tables."""
import argparse, hashlib, json, os, uuid
from pathlib import Path
from collections import Counter
LANGS=set('en sk uk cs de es fr pl hu it ru zh ja pt ar'.split())
def load(folder,name):
    return json.loads((folder/name).read_text(encoding='utf-8'))
def prepare(folder):
    records=load(folder,'questions_formulas.json'); translations=load(folder,'translations.json'); classes=load(folder,'classifications.json')
    ready=[]; skipped=[]; seen=set()
    for r in records:
        key=r['source']+':'+r['source_question_number']
        if key in seen: raise ValueError('Duplicate source key: '+key)
        seen.add(key)
        fp=hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        t=translations.get(key,{}); c=classes.get(key,{}); d=c.get('classification',{}); reasons=[]
        if t.get('fingerprint')!=fp or c.get('fingerprint')!=fp: reasons.append('missing_or_stale_processing')
        if d.get('scope')!='in_scope' or d.get('level') not in ('BOTH','HL','SL'): reasons.append('scope_not_confirmed')
        if d.get('issues'): reasons.append('classification_issues')
        items=[r['question'],*r['options']]; ids=[i['id'] for i in r['options']]
        if len(ids)<2 or len(set(ids))!=len(ids) or len(r['correct_answer'])!=1 or not set(r['correct_answer'])<=set(ids): reasons.append('invalid_options_or_key')
        if any(i.get('assets') or i.get('display_assets') or i.get('formula_errors') or '[IMAGE]' in i['math_text'] or '[FORMULA_UNRESOLVED]' in i['math_text'] or not i['math_text'].strip() for i in items): reasons.append('visual_or_unresolved_content')
        if set(r.get('issues',[]))-{'embedded_content_requires_conversion','empty_content'}: reasons.append('source_issues')
        versions=t.get('translations',{})
        if not LANGS<=set(versions): reasons.append('missing_languages')
        else:
            for lang in LANGS:
                v=versions[lang]
                if [o['id'] for o in v['options']]!=ids or not v['question_text'].strip() or any(not o['text'].strip() for o in v['options']): reasons.append('invalid_translation'); break
        if reasons: skipped.append({'source_key':key,'reasons':reasons}); continue
        qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'sciencehub:question:'+key))
        original=versions[r['source_language']]
        row=dict(id=qid,topic=d['topic'],subtopic=d['subtopic'],level=d['level'],question_text=original['question_text'],question_type='multiple_choice',options=original['options'],correct_answer=r['correct_answer'],difficulty=d['difficulty'],skills=d['skills'],concepts=d['concepts'],source=r['source'],source_question_number=r['source_question_number'],import_status='imported')
        localized=[dict(question_id=qid,language=lang,question_text=versions[lang]['question_text'],options=versions[lang]['options']) for lang in sorted(LANGS)]
        ready.append((row,localized))
    return ready,skipped

def main():
    p=argparse.ArgumentParser(); p.add_argument('folder',type=Path); mode=p.add_mutually_exclusive_group(required=True); mode.add_argument('--dry-run',action='store_true'); mode.add_argument('--apply',action='store_true'); p.add_argument('--limit',type=int); a=p.parse_args()
    ready,skipped=prepare(a.folder); selected=ready[:a.limit]; report={'eligible':len(ready),'selected':len(selected),'skipped':len(skipped),'reasons':dict(Counter(reason for s in skipped for reason in s['reasons'])),'details':skipped,'uploaded':0}
    path=a.folder/'repository_report.json'
    def save(): path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    save(); print({k:v for k,v in report.items() if k!='details'})
    if a.apply and selected:
        from supabase import create_client
        client=create_client(os.environ['SUPABASE_URL'],os.environ['SUPABASE_SERVICE_ROLE_KEY'])
        for row,localized in selected:
            # Keep incomplete imports hidden from future student retrieval.
            client.table('question_bank').upsert({**row,'import_status':'needs_attention'},on_conflict='id').execute()
            client.table('question_translations').upsert(localized,on_conflict='question_id,language').execute()
            client.table('question_bank').update({'import_status':'imported'}).eq('id',row['id']).execute()
            report['uploaded']+=1; save(); print('Uploaded',row['source_question_number'],flush=True)
if __name__=='__main__': main()
