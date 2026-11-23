import os
import json
import base64
import hashlib
import streamlit as st
from openai import OpenAI
from prompts import TUTOR_PROMPT
from rag import retrieve_knowledge
from problems.problem_search import find_similar_problems, detect_topic, detect_skill
from chat_history import create_conversation, get_conversations, get_messages, save_message


# Chat state is initialized before any UI uses it.
def reset_chat():
    st.session_state.messages = []
    st.session_state.current_topic = None
    st.session_state.current_skill = None
    st.session_state.used_problem_ids = []
    st.session_state.file_signature = None


for key, default in {
    'messages': [],
    'current_topic': None,
    'current_skill': None,
    'used_problem_ids': [],
    'file_signature': None,
    'conversation_id': None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


with st.sidebar:
    st.subheader('💬 Chat history')
    if st.button('➕ New chat', key='new_saved_chat', width='stretch'):
        st.session_state.conversation_id = None
        reset_chat()
        st.rerun()

    try:
        conversations = get_conversations()
        for conversation in conversations:
            conversation_id = conversation['id']
            title = conversation['title']
            if st.button('💬 ' + title, key=f'open_{conversation_id}', width='stretch'):
                st.session_state.messages = get_messages(conversation_id)
                st.session_state.conversation_id = conversation_id
                st.session_state.current_topic = None
                st.session_state.current_skill = None
                st.session_state.used_problem_ids = []
                st.session_state.file_signature = None
                st.rerun()
    except Exception:
        st.error('Could not load chat history. Please check Supabase settings and RLS policies.')


st.title('💬 Practice with AI')
st.caption('Learn physics through guided problem solving')
level = st.session_state.get('physics_level', 'SL')
mode = st.selectbox('Choose your learning mode', [
    'Solve my problem', 'Review a topic', 'Practise similar problems'
])
uploaded_file = st.file_uploader('Upload a physics problem', type=['png', 'jpg', 'jpeg', 'pdf'])


def display_message(message):
    content = message['content']
    with st.chat_message(message['role']):
        if isinstance(content, str):
            st.markdown(content)
        elif isinstance(content, list):
            for block in content:
                if block.get('type') == 'input_text':
                    text = block.get('text', '')
                    if text.startswith('Learning mode: '):
                        text = text.split('\n', 1)[-1] if '\n' in text else text
                    st.markdown(text)
                elif block.get('type') == 'input_image':
                    st.caption('📷 Image attached')
                elif block.get('type') == 'input_file':
                    st.caption('📄 PDF attached: ' + block.get('filename', 'file'))


def safe_history_content(content):
    """Store attachment metadata, not base64 files, in Supabase."""
    if isinstance(content, str):
        return content
    cleaned = []
    for block in content:
        if block.get('type') == 'input_text':
            cleaned.append({'type': 'input_text', 'text': block.get('text', '')})
        elif block.get('type') == 'input_file':
            cleaned.append({'type': 'input_file', 'filename': block.get('filename', 'file')})
        elif block.get('type') == 'input_image':
            cleaned.append({'type': 'input_image'})