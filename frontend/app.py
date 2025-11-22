# frontend/app.py
import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Agentic AI Summarizer", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align:center'>✨ Agentic AI Summarizer</h1>", unsafe_allow_html=True)
st.write("Upload PDF/TXT → Index → Summarize or Ask questions from the document.")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083267.png", width=100)
    st.markdown("**Controls**")
    st.write("Backend: " + API_BASE)

# Upload + Index
st.header("Upload & Index Document")
uploaded = st.file_uploader("Choose a PDF or TXT", type=["pdf", "txt"])
if uploaded is not None:
    if st.button("Upload & Index"):
        files = {"file": (uploaded.name, uploaded, uploaded.type)}
        resp = requests.post(f"{API_BASE}/upload", files=files)
        if resp.ok:
            data = resp.json()
            st.success(f"Uploaded. doc_id: {data['doc_id']}")
            st.session_state["doc_id"] = data["doc_id"]
        else:
            st.error(resp.text)

# If we've already uploaded before
doc_id = st.text_input("Or paste an existing doc_id", value=st.session_state.get("doc_id",""))
if doc_id:
    st.write("Working with doc_id:", doc_id)

# Summarize
st.header("Summarize Document")
style = st.selectbox("Summary style", ["concise","detailed","bullets"])
if st.button("Generate Summary"):
    if not doc_id:
        st.error("Provide a doc_id (upload first).")
    else:
        resp = requests.post(f"{API_BASE}/summarize", params={"doc_id": doc_id, "style": style})
        if resp.ok:
            out = resp.json()
            st.success("Summary ready")
            st.subheader("Summary")
            st.markdown(out["summary"])
        else:
            st.error(resp.text)

# Ask-from-doc
st.header("Ask from Document")
question = st.text_input("Ask a question about the document")
if st.button("Ask"):
    if not doc_id:
        st.error("Provide a doc_id")
    elif not question.strip():
        st.error("Enter a question")
    else:
        payload = {"doc_id": doc_id, "question": question}
        resp = requests.post(f"{API_BASE}/ask", json=payload)
        if resp.ok:
            out = resp.json()
            st.success("Answer")
            st.write(out["answer"])
            # st.write("Retrieved chunks (index & score):")
            # st.json(out.get("retrieved", []))
        else:
            st.error(resp.text)