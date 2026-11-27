import streamlit as st
from html import escape
from exam_data import COURSE, ASSESSMENT, SYLLABUS, OBJECTIVES, BRIEF_URL, SOURCE
from exam_translations import et, topic_text

st.html('''<style>
.ib-hero{background:#C6F432;color:#202420;border-radius:22px;padding:32px;display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:16px}.ib-hero h1{color:#202420!important;font-size:clamp(1.8rem,4vw,2.7rem);margin:8px 0}.ib-hero p{margin:8px 0}.ib-card{background:#fff;color:#202420;border:1px solid #DCE1D5;border-radius:16px;padding:20px;margin:10px 0;overflow-wrap:anywhere}.ib-card h3{color:#202420!important;margin:0;font-size:1.15rem}.ib-muted{color:#687064;font-size:.9rem}.ib-row{display:flex;align-items:center;justify-content:space-between;gap:12px}.ib-track{background:#E9F3D5;border-radius:20px;height:9px;margin:12px 0}.ib-fill{background:#C6F432;height:100%;border-radius:20px}.ib-grade{background:#202420;color:white;border-radius:16px;padding:24px;margin:16px 0}.ib-stack{display:flex;gap:4px;margin:16px 0}.ib-stack span{padding:12px 0;text-align:center;color:#202420;border-radius:6px;font-weight:700}.ib-topic{padding:12px 0;border-top:1px solid #DCE1D5}.ib-code{background:#E9F3D5;border-radius:8px;padding:8px;font-weight:700}.ib-metric{font-size:2rem;font-weight:700}.ib-hero svg{flex-shrink:0;width:90px}@media(max-width:600px){.ib-hero{padding:20px}.ib-hero svg{display:none}.ib-row{flex-wrap:wrap}}
</style>''')

lang = st.session_state.get('ui_language', 'en')
direction = 'rtl' if lang == 'ar' else 'ltr'
def e(key):
    return escape(et(key))
def render(content):
    st.html(f'<div dir="{direction}">{content}</div>')

def duration(minutes):
    h, m = divmod(minutes, 60)
    return ' '.join(([f'{h} {et("hours")}'] if h else []) + ([f'{m} {et("minutes")}'] if m else []))

render(f'''<div class="ib-hero"><div><small>SCIENCEHUB / IB PHYSICS</small><h1>{e('hero_title')}</h1><p>{e('hero_description')}</p><small>{e('first_assessment')}</small></div><svg viewBox="0 0 100 110" fill="none" stroke="#202420" stroke-width="2"><rect x="15" y="8" width="70" height="94" rx="7"/><path d="M27 25H72 M27 33H58 M28 84V48 M28 84H73 M32 75L44 61L54 67L70 43 M34 92H66"/><circle cx="70" cy="43" r="3" fill="#202420"/></svg></div>''')

st.link_button(et('official_source'), BRIEF_URL)
st.caption(SOURCE)

level = st.session_state.get('physics_level', 'SL')
if level not in COURSE:
    level = 'SL'
course = COURSE[level]
for col, value, label in zip(st.columns(3), [course['teaching_hours'], duration(round(course['exam_hours']*60)), course['topics']], ['teaching_hours','written_exams','topics']):
    with col:
        render(f'<div class="ib-card"><div class="ib-metric">{escape(str(value))}</div><div class="ib-muted">{e(label)}</div></div>')

# Localized assessment descriptions.
formats = {'paper1':et('paper1_format') + ' (Paper 1A + 1B)', 'paper2':et('paper2_format'), 'ia':et('internal_assessment')}
a, s, o = st.tabs([et('assessment'), et('syllabus'), et('objectives')])
with a:
    st.subheader(et('assessment_structure'))
    for item in ASSESSMENT:
        weight = int(item['weight'])
        render(f'''<div class="ib-card"><div class="ib-row"><h3>{escape(et('ia_title') + ' (IA)' if item['id'] == 'ia' else item['title'])}</h3><strong style="font-size:1.6rem">{weight}%</strong></div><div class="ib-muted">{escape(formats[item['id']])}</div><div class="ib-track"><div class="ib-fill" style="width:{weight}%"></div></div><div class="ib-muted">{escape(duration(item['duration'][level]))}</div></div>''')
    render(f'''<div class="ib-grade"><strong>{e('grade_composition')}</strong><div class="ib-stack"><span style="flex:36;background:#C6F432">36%</span><span style="flex:44;background:#A4C92A">44%</span><span style="flex:20;background:#E9F3D5">20%</span></div><div class="ib-row"><small>{e('external_assessment')} · 80%</small><small>{e('internal_assessment')} · 20%</small></div></div>''')
with s:
    for theme in SYLLABUS:
        code = theme['id']
        rows = []
        for topic, name, coverage in theme['topics']:
            if level == 'SL' and coverage == 'hl':
                continue
            label = {'hl':'hl_only','both_hl':'hl_extension','both':'common_content'}[coverage]
            if level == 'SL':
                label = 'common_content'
            translated = topic_text(topic)
            english = topic_text(topic, english=True)
            secondary = f'<div class="ib-muted">{escape(english)}</div>' if translated != english else ''
            rows.append(f'<div class="ib-topic"><div class="ib-row"><strong>{escape(topic)} · {escape(translated)}</strong><small class="ib-muted">{e(label)}</small></div>{secondary}</div>')
        render(f'<div class="ib-card"><div class="ib-row"><h3><span class="ib-code">{escape(code)}</span> {escape(topic_text(code))}</h3><small class="ib-muted">{escape(duration(theme["hours"][level]*60))}</small></div><div style="margin-top:16px">{"".join(rows)}</div></div>')
with o:
    for item in OBJECTIVES:
        render(f'<div class="ib-card"><h3><span class="ib-code">{escape(item["id"])}</span> {escape(et(item["id"] + "_title"))}</h3><p>{escape(et(item["id"] + "_description"))}</p></div>')