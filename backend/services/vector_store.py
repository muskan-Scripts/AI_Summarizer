import os
import google.generativeai as genai
import numpy as np
import faiss

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Stores doc_id → {index, chunks}
VECTOR_DB = {}

# TEXT SPLITTING
def split_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start += chunk_size - overlap
    return chunks


# EMBEDDINGS

def embed(text: str):
    res = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return res["embedding"]

# STORE DOCUMENT

def store_document(text: str):
    chunks = split_text(text)

    embeddings = [embed(c) for c in chunks]
    dim = len(embeddings[0])

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    doc_id = f"doc_{len(VECTOR_DB)+1}"

    VECTOR_DB[doc_id] = {
        "index": index,
        "chunks": chunks,
        "embeddings": embeddings
    }

    return doc_id

# RETRIEVE CHUNKS
def retrieve_chunks(doc_id: str, query: str, k=3):
    if doc_id not in VECTOR_DB:
        return []

    store = VECTOR_DB[doc_id]

    qvec = np.array(embed(query)).astype("float32")
    D, I = store["index"].search(np.array([qvec]), k)

    results = []

    for idx, score in zip(I[0], D[0]):
        if 0 <= idx < len(store["chunks"]):
            results.append({
                "chunk": store["chunks"][idx],
                "score": float(score)
            })

    return results
