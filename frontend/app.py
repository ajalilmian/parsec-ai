import streamlit as st
import requests
import os

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Parsec AI",
    page_icon="🧠",
    layout="wide"
)

st.title("Parsec AI")
st.markdown("""
Parse documents at light speed! Parsec AI allows you to have a conversation with your files. Simply upload a PDF, such as a marketing brief, a research paper or a legal document, and ask questions in natural language to get instant, context-aware answers.
""")

if 'collection_name' not in st.session_state:
    st.session_state.collection_name = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Upload Your Documents")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing document... This may take a moment."):
                files = {'file': (uploaded_file.name,
                                  uploaded_file.getvalue(), 'application/pdf')}
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/upload/", files=files)
                    if response.status_code == 200:
                        st.session_state.collection_name = response.json().get("collection_name")
                        st.session_state.messages = []
                        st.success(
                            f"Document processed! Collection '{st.session_state.collection_name}' is ready.")
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

st.header("1. Upload Your Brief")
st.markdown("""
Upload a PDF of your marketing brief, and I'll help you find the answers you need.
""")

st.header("2. Ask Your Questions")
st.markdown("""
Ask about KPIs, target audience, campaign goals, and more!
""")

if st.session_state.collection_name:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask something about your brief..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                payload = {"question": prompt,
                           "collection_name": st.session_state.collection_name}
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/query/", json=payload)
                    if response.status_code == 200:
                        answer = response.json().get("answer")
                        st.markdown(answer)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": answer})
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

else:
    st.warning("Please upload and process a document in the sidebar to begin.")
