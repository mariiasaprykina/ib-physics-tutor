"""Recover OMML formulas in their original positions; preserve source answer IDs."""
import argparse, json, subprocess, tempfile
from pathlib import Path
from docx import Document
from lxml import etree
M='http://schemas.openxmlformats.org/officeDocument/2006/math'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def tag(n): return etree.QName(n).localname
def child(n,k): return n.find('{'+M+'}'+k)
def val(n,k,default=''):
    x=child(n,k) if n is not None else None
    return x.get('{'+M+'}val',default) if x is not None else default
symbols={'ω':r'\omega ','ϖ':r'\varpi ','ϕ':r'\phi ','ε':r'\varepsilon ','α':r'\alpha ','τ':r'\tau ','μ':r'\mu ','π':r'\pi ','Δ':r'\Delta ','ℏ':r'\hbar ','≥':r'\ge ','±':r'\pm ','⋅':r'\cdot ','−':'-','х':'x','р':'p','Т':'T','М':'M','з':r'\text{з}'}
def latex(n):
    if n is None: return ''
    k=tag(n)
    def c(key): return latex(child(n,key))
    if k=='t':
        s=n.text or ''
        if s in ('sin','cos','const'): return '\\'+s+' ' if s!='const' else r'\mathrm{const}'
        return ''.join(symbols.get(a,a) for a in s)
    if k in ('oMath','r','e','num','den','sub','sup'): return ''.join(latex(x) for x in n if not tag(x).endswith('Pr'))
    if k=='f': return r'\frac{'+c('num')+'}{'+c('den')+'}'
    if k in ('sSub','sSup','sSubSup'):
        return '{'+c('e')+'}'+('_{'+c('sub')+'}' if k!='sSup' else '')+('^{'+c('sup')+'}' if k!='sSub' else '')
    if k=='acc':
        a=val(child(n,'accPr'),'chr')
        if a!='⃗': raise ValueError('Unknown accent '+a)
        return r'\vec{'+c('e')+'}'
    if k=='d':
        p=child(n,'dPr'); a=val(p,'begChr','('); b=val(p,'endChr',')')
        if a not in ('(','[','|') or b not in (')',']','|'): raise ValueError('Unsupported delimiter')
        return r'\left'+a+c('e')+r'\right'+b
    if k=='nary':
        p=child(n,'naryPr'); op={'∫':r'\int','∑':r'\sum'}.get(val(p,'chr'))
        if not op: raise ValueError('Unknown operator')
        return op+('_{'+c('sub')+'}' if c('sub') else '')+('^{'+c('sup')+'}' if c('sup') else '')+' '+c('e')
    raise ValueError('Unsupported OMML: '+k)
def extract_cell(cell):
    parts=[]; formulas=[]; errors=[]
    def walk(n):
        if n.tag=='{'+M+'}oMath':
            try:
                s=latex(n); formulas.append(s); parts.append('$'+s+'$')
            except ValueError as e: errors.append(str(e)); parts.append('[FORMULA_UNRESOLVED]')
        elif n.tag=='{'+W+'}t': parts.append(n.text or '')
        elif tag(n) in ('object','drawing','pict'): parts.append('[IMAGE]')
        elif tag(n) in ('tab','br'): parts.append(' ')
        else:
            for x in n: walk(x)
            if tag(n)=='p': parts.append('\n')
    walk(cell._tc)
    return {'math_text':''.join(parts).strip(),'formulas_latex':formulas,'formula_errors':errors}
def process(source,folder):
    records=json.loads((folder/'questions_graphics.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        path=source
        if source.suffix.lower()=='.doc':
            subprocess.run(['libreoffice','--headless',f'-env:UserInstallation={Path(tmp,"profile").as_uri()}','--convert-to','docx','--outdir',tmp,str(source.resolve())],check=True)
            path=Path(tmp)/(source.stem+'.docx')
        doc=Document(path); groups=[]; current=None
        for table in doc.tables:
            for row in table.rows:
                if len(row.cells)!=3: continue
                number,body,mark=row.cells; n=number.text.strip()
                if n.isdecimal():
                    current={'number':n,'cells':[extract_cell(body)],'keys':[]}; groups.append(current)
                elif 'ф.ф' in n.lower().replace(' ',''): current=None
                elif current is not None:
                    current['cells'].append(extract_cell(body))
                    if mark.text.strip()=='1': current['keys'].append('option_'+str(len(current['cells'])-1))
        if len(groups)!=len(records): raise ValueError('Question count mismatch; no output written')
        for r,g in zip(records,groups):
            items=[r['question'],*r['options']]
            if r['source_question_number']!=g['number'] or len(items)!=len(g['cells']) or r['correct_answer']!=g['keys']: raise ValueError('Source alignment mismatch: '+g['number'])
            for item,math in zip(items,g['cells']): item.update(math)
    items=[i for r in records for i in [r['question'],*r['options']]]
    report={'questions':len(records),'formulas_converted':sum(len(i['formulas_latex']) for i in items),'formula_errors':sum(len(i['formula_errors']) for i in items),'questions_with_formulas':sum(any(i['formulas_latex'] for i in [r['question'],*r['options']]) for r in records)}
    for name,data in [('questions_formulas.json',records),('formula_report.json',report)]: (folder/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('folder',type=Path); a=p.parse_args(); process(a.source,a.folder)
