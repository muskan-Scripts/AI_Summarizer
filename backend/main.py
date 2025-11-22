import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv

from services.pdf_reader import read_pdf
from services.vector_store import store_document
from agents.orchestrator import Orchestrator

load_dotenv()

app = FastAPI(title="Agentic AI Backend", version="1.0")


@app.get("/")
def root():
    return {"message": "Backend running"}


# ------------------------ UPLOAD ------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    raw = await file.read()

    if "pdf" in file.content_type:
        text = read_pdf(raw)
    else:
        text = raw.decode("utf-8")

    if not text:
        raise HTTPException(400, "No readable text in file")

    doc_id = store_document(text)
    return {"doc_id": doc_id}


# ------------------------ SUMMARIZE ------------------------
@app.post("/summarize")
def summarize(doc_id: str, style: str = "concise"):
    result = Orchestrator.summarize(doc_id, style)
    return {"summary": result}


# ------------------------ ASK ------------------------
@app.post("/ask")
def ask(payload: dict):
    doc_id = payload.get("doc_id")
    question = payload.get("question")

    if not doc_id or not question:
        raise HTTPException(400, "doc_id and question required")

    answer, retrieved = Orchestrator.answer(doc_id, question)

    return {"answer": answer, "retrieved": retrieved}


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
