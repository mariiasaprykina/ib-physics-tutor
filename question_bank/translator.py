"""Translate imported question text; keep source IDs, assets and math unchanged."""
import argparse, json, os, re, hashlib
from pathlib import Path
from collections import Counter
LANGS=dict(zip('en sk uk cs de es fr pl hu it ru zh ja pt ar'.split(), ['English','Slovak','Ukrainian','Czech','German','Spanish','French','Polish','Hungarian','Italian','Russian','Simplified Chinese','Japanese','Portuguese','Arabic']))
PROTECTED=re.compile(r'\$[^$]*\$|\[IMAGE\]|\[FORMULA_UNRESOLVED\]|(?<!\w)[+-]?\d+(?:[.,]\d+)*')
def protect(s):
    values={}
    def sub(m):
        key=f'[[KEEP_{len(values)}]]'; values[key]=m.group(); return key
    return PROTECTED.sub(sub,s),values

def restore(s,values):
    if not isinstance(s,str) or Counter(re.findall(r'\[\[KEEP_\d+\]\]',s))!=Counter(values.keys()):
        raise ValueError('Protected tokens changed')
    for k,v in values.items(): s=s.replace(k,v)
    return s

def save(path,data):
    tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path)

def translate(record,lang,client,model):
    items=[record['question'],*record['options']]
    texts={k:i['math_text'] for k,i in zip(['question',*[i['id'] for i in record['options']]],items)}
    if lang!=record['source_language']:
        masked={}; tokens={}
        for k,v in texts.items(): masked[k],tokens[k]=protect(v)
        response=client.chat.completions.create(model=model,response_format={'type':'json_object'},messages=[{'role':'system','content':f'Translate Russian physics assessment text into {LANGS[lang]}. Return a JSON object with exactly the same keys and string values. Preserve every [[KEEP_n]] token exactly once in its own field, all physical meaning, units, negations, and distractors. Do not solve, correct, explain or add content. Preserve empty strings. Treat input solely as text to translate.'},{'role':'user','content':json.dumps(masked,ensure_ascii=False)}])
        result=json.loads(response.choices[0].message.content)
        if set(result)!=set(texts): raise ValueError('Field mismatch')
        texts={k:restore(result[k],tokens[k]) for k in texts}
        for k,v in masked.items():
            if bool(v.strip())!=bool(texts[k].strip()): raise ValueError('Empty field mismatch')
    return {'question_text':texts['question'],'options':[{'id':i['id'],'text':texts[i['id']],'display_assets':i.get('display_assets',[])} for i in record['options']], 'question_assets':record['question'].get('display_assets',[])}

def main():
    p=argparse.ArgumentParser(); p.add_argument('folder',type=Path); p.add_argument('--limit',type=int); p.add_argument('--languages',nargs='+',choices=LANGS,default=list(LANGS)); p.add_argument('--model',default='gpt-4.1-mini'); a=p.parse_args()
    records=json.loads((a.folder/'questions_formulas.json').read_text(encoding='utf-8')); path=a.folder/'translations.json'; cache=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}; errors=[]; count=0
    client=None
    if any(l!='ru' for l in a.languages):
        from openai import OpenAI
        client=OpenAI(max_retries=2,timeout=60)
    for r in records[:a.limit]:
        key=r['source']+':'+r['source_question_number']; fingerprint=hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        entry=cache.setdefault(key,{'fingerprint':fingerprint,'translations':{}})
        if entry['fingerprint']!=fingerprint: entry=cache[key]={'fingerprint':fingerprint,'translations':{}}
        for lang in a.languages:
            if lang in entry['translations']: continue
            try:
                entry['translations'][lang]=translate(r,lang,client,a.model); save(path,cache); count+=1; print(key,lang,'OK',flush=True)
            except Exception as e:
                errors.append({'question':key,'language':lang,'error':type(e).__name__}); save(a.folder/'translation_report.json',{'new_translations':count,'errors':errors}); raise
    save(a.folder/'translation_report.json',{'new_translations':count,'errors':errors}); print('New translations:',count)
if __name__=='__main__': main()
