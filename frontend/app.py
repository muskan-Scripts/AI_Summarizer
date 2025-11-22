import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Agentic AI Summarizer",
    page_icon="✨",
    layout="wide",
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    /* Gradient header */
    .title-gradient {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff4b1f, #ff9068);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
    }
    .sub-section {
        background: rgba(255,255,255,0.5);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-left: 5px solid #ff9068;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ff9068, #ff4b1f);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(255,120,120,0.4);
    }
    .css-1kyxreq { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<div class='title-gradient'>✨ Agentic AI Summarizer</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:17px;'>Upload → Index → Summarize → Ask Anything</p>", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083267.png", width=110)
    st.markdown("### ⚙️ Controls")
    st.info(f"Backend: `{API_BASE}`")
    st.markdown("---")
    st.write("Built with ❤️ using RAG + Multi-Agent Orchestration")

# ------------------ UPLOAD SECTION ------------------
st.markdown("## 📤 Upload & Index Document")
with st.container():
    with st.container():
        st.markdown("<div class='sub-section'>", unsafe_allow_html=True)

        uploaded = st.file_uploader("Choose a PDF or TXT", type=["pdf", "txt"])

        if uploaded is not None:
            if st.button("🚀 Upload & Index"):
                files = {"file": (uploaded.name, uploaded, uploaded.type)}
                resp = requests.post(f"{API_BASE}/upload", files=files)

                if resp.ok:
                    data = resp.json()
                    st.success(f"📄 Uploaded! **doc_id:** `{data['doc_id']}`")
                    st.session_state["doc_id"] = data["doc_id"]
                else:
                    st.error(resp.text)

        doc_id = st.text_input("Paste existing doc_id", value=st.session_state.get("doc_id", ""))

        if doc_id:
            st.info(f"Working with: `{doc_id}`")

        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ SUMMARIZE SECTION ------------------
st.markdown("## 🧠 Generate Summary")
with st.container():
    st.markdown("<div class='sub-section'>", unsafe_allow_html=True)

    style = st.selectbox("Summary Style", ["concise", "detailed", "bullets"])

    if st.button("✨ Generate Summary"):
        if not doc_id:
            st.error("Please upload or enter a doc_id first.")
        else:
            resp = requests.post(f"{API_BASE}/summarize", params={"doc_id": doc_id, "style": style})
            if resp.ok:
                output = resp.json()
                st.success("Summary Ready!")

                st.markdown("### 📌 Summary")
                st.markdown(output["summary"])
            else:
                st.error(resp.text)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ ASK SECTION ------------------
st.markdown("## 💬 Ask Questions")
with st.container():
    st.markdown("<div class='sub-section'>", unsafe_allow_html=True)

    question = st.text_input("Ask anything from the document")

    if st.button("🔍 Ask"):
        if not doc_id:
            st.error("Provide a doc_id first.")
        elif not question.strip():
            st.error("Enter a question.")
        else:
            payload = {"doc_id": doc_id, "question": question}
            resp = requests.post(f"{API_BASE}/ask", json=payload)

            if resp.ok:
                out = resp.json()
                st.success("📥 Answer")
                st.write(out["answer"])
            else:
                st.error(resp.text)

    st.markdown("</div>", unsafe_allow_html=True)
