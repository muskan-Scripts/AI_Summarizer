# ✨ Agentic AI Summarizer  
**RAG + Multi-Agent + Embeddings | Smart Document Understanding System**

A modern AI-powered system that lets you:

- Upload & index PDF/TXT documents  
- Generate summaries (concise / detailed / bullets)  
- Ask deep semantic questions from documents  
- Uses **FAISS Vector Store + HuggingFace Embeddings**  
- Multi-Agent workflow (Summarizer Agent + Retrieval Agent)  
- Beautiful pastel UI with gradients, animations & light/dark mode  

---

##  Features

### Document Upload & Indexing
- Supports PDF and TXT
- Automatic chunking + embedding
- Generates a unique `doc_id`

### Retrieval-Augmented Generation (RAG)
- Fast semantic search using FAISS
- Context-aware answers for Q&A

### Multi-Agent Pipeline
- **Retrieval Agent** → fetches top chunks  
- **Summarizer Agent** → generates summaries and answers  

### Smart Summaries
- `concise`
- `detailed`
- `bullets`

### Ask Anything
Ask any question from the document and get LLM-powered responses.

### Modern Streamlit UI
- Pastel color gradients
- Animated buttons
- Section-based cards
- Light/Dark Mode toggle
- Sidebar controls

---

## Architecture

```text
                ┌────────────────────────────┐
                │        Streamlit UI        │
                └──────────────┬─────────────┘
                               │  REST API
                               ▼
                     ┌───────────────────────┐
                     │        FastAPI        │
                     ├────────────┬──────────┤
                     │ Summarizer Agent      │
                     │ Retrieval Agent       │
                     └────────────┬──────────┘
                                  │
                                  ▼
                ┌──────────────────────────────────┐
                │   Vector Store (FAISS)           │
                │   HuggingFace Embeddings         │
                └──────────────────────────────────┘

```

## 📦 Tech Stack

### Frontend
- Streamlit  
- Custom CSS  
- Light/Dark theme toggle  

### Backend
- FastAPI  
- Python  
- LangChain  
- FAISS  
- HuggingFace Sentence Transformers  
