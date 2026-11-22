import streamlit as st

st.set_page_config(page_title='IB Physics AI Tutor', page_icon='⚛️', layout='wide')

if 'physics_level' not in st.session_state:
    st.session_state.physics_level = 'SL'

with st.sidebar:
    st.title('⚛️ IB Physics Tutor')
    st.radio('IB Physics level', ['SL', 'HL'], key='physics_level', horizontal=True)

pages = [
    st.Page('pages/exam.py', title='About the Exam', icon='📘', default=True),
    st.Page('pages/diagnostic.py', title='Diagnostic Assessment', icon='📝'),
    st.Page('pages/practice.py', title='Practice with AI', icon='💬'),
    st.Page('pages/progress.py', title='My Progress', icon='📈'),
]
st.navigation(pages).run()
