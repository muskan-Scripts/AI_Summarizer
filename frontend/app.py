import streamlit as st
import requests
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Agentic AI Summarizer",
    page_icon="✨",
    layout="centered"
)

# --- CUSTOM CSS FOR COLORFUL UI ---
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(to right bottom, #f0f2f6, #e0eafc);
    }
    
    /* Header Style */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Subheader */
    .sub-header {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Card Style for Summary */
    .summary-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #6a11cb;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
    }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(37, 117, 252, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- UI LAYOUT ---

st.markdown('<div class="main-header">✨ Agentic AI Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Give your documents a brain — AI summaries in seconds using Gemini + FastAPI.</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083267.png", width=100)
    st.title("Controls")
    st.info("Upload a PDF or TXT file to generate a concise summary using AI.")
    st.write("---")
    st.write("backend status: `active` 🟢")

# File Uploader
uploaded_file = st.file_uploader("Choose a document...", type=['pdf', 'txt'])

if uploaded_file is not None:
    st.write("### 📄 File Details")
    file_details = {"Filename": uploaded_file.name, "File size": f"{uploaded_file.size / 1024:.2f} KB"}
    st.json(file_details)

    if st.button("🚀 Generate Summary"):
        with st.spinner('Analyzing document with AI... this might take a moment...'):
            try:
                # Prepare payload for Backend API
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Call the FastAPI Backend
                response = requests.post("http://localhost:8000/summarize", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    summary_text = result.get("summary", "No summary returned.")
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📝 AI Summary")
                    st.markdown(f'<div class="summary-card">{summary_text}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Make sure `main.py` is running!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.write("---")
st.markdown("<div style='text-align: center; color: #888;'>Built for the AgenticAIG Project</div>", unsafe_allow_html=True)