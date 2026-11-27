"""Convert imported vector assets without changing the source question or key."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET


def process(folder):
    folder = folder.resolve()
    records = json.loads((folder / 'questions.json').read_text(encoding='utf-8'))
    out = folder / 'graphics'
    out.mkdir(exist_ok=True)
    results = {}
    for record in records:
        for item in [record['question'], *record['options']]:
            item['display_assets'] = []
            for name in item['assets']:
                if name not in results:
                    source = (folder / name).resolve()
                    try:
                        if not source.is_relative_to(folder / 'assets'):
                            raise ValueError('Invalid asset path')
                        if source.suffix.lower() in {'.wmf', '.emf'}:
                            target = out / (source.stem + '.svg')
                            subprocess.run(['inkscape', str(source), '--export-text-to-path', '--export-plain-svg', f'--export-filename={target}'], check=True, capture_output=True, timeout=60)
                            if ET.parse(target).getroot().tag != '{http://www.w3.org/2000/svg}svg':
                                raise ValueError('Invalid SVG')
                        elif source.suffix.lower() in {'.png', '.jpg', '.jpeg', '.svg', '.webp'}:
                            target = out / source.name
                            shutil.copyfile(source, target)
                        else:
                            raise ValueError('Unsupported format')
                        results[name] = {'status':'converted', 'path':str(target.relative_to(folder))}
                    except (OSError, ValueError, subprocess.SubprocessError, ET.ParseError) as exc:
                        results[name] = {'status':'failed', 'error':str(exc)}
                result = results[name]
                if result['status'] == 'converted':
                    item['display_assets'].append(result['path'])
            if item['embedded'] and not item['assets']:
                item['graphics_status'] = 'missing_embedded_object'
            elif len(item['display_assets']) != len(item['assets']):
                item['graphics_status'] = 'conversion_failed'
            elif item['assets']:
                item['graphics_status'] = 'converted_needs_visual_check'
            else:
                item['graphics_status'] = 'not_required'
    report = {'assets_converted':sum(v['status']=='converted' for v in results.values()), 'assets_failed':sum(v['status']=='failed' for v in results.values()), 'questions_with_missing_objects':sum(any(i['graphics_status']=='missing_embedded_object' for i in [r['question'],*r['options']]) for r in records), 'assets':results}
    for name,data in [('questions_graphics.json',records),('graphics_report.json',report)]:
        (folder/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='assets'},indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder',type=Path)
    process(parser.parse_args().folder)
