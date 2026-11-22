
import base64
import streamlit as st
from openai import OpenAI
from prompts import TUTOR_PROMPT

st.set_page_config(
    page_title="IB Physics AI Tutor",
    page_icon="⚛️",
    layout="centered"
)

st.title("⚛️ IB Physics AI Tutor")
st.caption("Learn physics through guided problem solving")

import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"].strip())
# Learning modes
mode = st.selectbox(
    "Choose your learning mode",
    [
        "Solve my problem",
        "Review a topic",
        "Practise similar problems"
    ]
)

# Upload physics problem
uploaded_file = st.file_uploader(
    "Upload a physics problem",
    type=["png", "jpg", "jpeg", "pdf"]
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_signature" not in st.session_state:
    st.session_state.file_signature = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Enter your problem or answer the tutor..."
)

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add current mode to the user message
    content = [
        {
            "type": "input_text",
            "text": f"Learning mode: {mode}\n{prompt}"
        }
    ]

    # Attach uploaded file once per chat
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        signature = (
            uploaded_file.name,
            len(file_bytes),
            hash(file_bytes)
        )

        if signature != st.session_state.file_signature:
            encoded = base64.b64encode(
                file_bytes
            ).decode("utf-8")

            if uploaded_file.type == "application/pdf":
                content.append({
                    "type": "input_file",
                    "filename": uploaded_file.name,
                    "file_data": (
                        "data:application/pdf;base64,"
                        + encoded
                    )
                })
            else:
                content.append({
                    "type": "input_image",
                    "image_url": (
                        f"data:{uploaded_file.type};base64,"
                        + encoded
                    )
                })

    st.session_state.messages.append({
        "role": "user",
        "content": content
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=TUTOR_PROMPT,
                    input=st.session_state.messages
                )

                answer = response.output_text
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                if uploaded_file is not None:
                    st.session_state.file_signature = signature
            except Exception as e:
                st.error(f"API error: {type(e).__name__}")
                st.code(str(e))
if st.button("Start new conversation"):
    st.session_state.messages = []
    st.session_state.file_signature = None
    st.rerun()
