"""Offline staging importer for three-column Word question banks."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from docx import Document


def extract(source, output):
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'assets'
    assets.mkdir(exist_ok=True)
    records = []
    warnings = []
    with tempfile.TemporaryDirectory() as tmp:
        path = source
        if source.suffix.lower() == '.doc':
            subprocess.run(['libreoffice', '--headless', f'-env:UserInstallation={Path(tmp, "profile").as_uri()}', '--convert-to', 'docx', '--outdir', tmp, str(source.resolve())], check=True)
            path = Path(tmp) / (source.stem + '.docx')
        doc = Document(path)
        def cell_data(cell):
            images = []
            for node in cell._tc.xpath('.//*[local-name()="blip" or local-name()="imagedata"]'):
                rid = next((v for k,v in node.attrib.items() if k.endswith('}embed') or k.endswith('}id')), None)
                part = cell.part.related_parts.get(rid)
                if part is None:
                    continue
                blob = part.blob
                name = hashlib.sha256(blob).hexdigest()[:24] + Path(str(part.partname)).suffix
                (assets / name).write_bytes(blob)
                images.append('assets/' + name)
            embedded = bool(cell._tc.xpath('.//w:drawing | .//w:pict | .//w:object | .//m:oMath'))
            return {'text':cell.text.strip(), 'assets':images, 'embedded':embedded}
        current = None
        def finish():
            if current is None:
                return
            issues = []
            if len(current['correct_answer']) != 1: issues.append('unexpected_answer_count')
            if len(current['options']) < 2: issues.append('missing_options')
            for item in [current['question'], *current['options']]:
                if item['embedded']: issues.append('embedded_content_requires_conversion')
                if not item['text'] and not item['assets']: issues.append('empty_content')
            current['issues'] = sorted(set(issues))
            current['import_status'] = 'needs_attention' if issues else 'imported'
            records.append(current)
        for table in doc.tables:
            for row in table.rows:
                cells = row.cells
                if len(cells) != 3:
                    warnings.append('Unexpected column count'); continue
                number, body, mark = cells
                n = number.text.strip()
                if n.isdecimal():
                    finish()
                    current = {'source':source.name,'source_question_number':n,'source_language':'ru','question':cell_data(body),'options':[],'correct_answer':[],'topic':None,'level':None}
                    if mark.text.strip(): warnings.append(f'{n}: mark in question row')
                elif 'ф.ф' in n.lower().replace(' ', ''):
                    finish(); current = None
                elif current is not None:
                    item = cell_data(body)
                    item['id'] = f'option_{len(current["options"])+1}'
                    current['options'].append(item)
                    if mark.text.strip() == '1': current['correct_answer'].append(item['id'])
                    elif mark.text.strip(): warnings.append(f'{current["source_question_number"]}: unknown mark {mark.text!r}')
        finish()
    numbers = [r['source_question_number'] for r in records]
    if numbers and all(n.isdecimal() for n in numbers):
        missing = sorted(set(range(1,max(map(int,numbers))+1))-set(map(int,numbers)))
        if missing: warnings.append(f'Missing question numbers: {missing}')
    if len(set(numbers)) != len(numbers): warnings.append('Duplicate question numbers')
    report = {'questions':len(records),'imported':sum(r['import_status']=='imported' for r in records),'needs_attention':sum(r['import_status']=='needs_attention' for r in records),'assets':len(list(assets.iterdir())),'warnings':warnings}
    for name,data in [('questions.json',records),('report.json',report)]:
        (output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('source',type=Path); p.add_argument('--out',type=Path,required=True); a=p.parse_args(); extract(a.source,a.out)
