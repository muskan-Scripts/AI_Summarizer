import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnableSequence
import uvicorn
import PyPDF2
import io

# Load env variables
load_dotenv()

# FastAPI
app = FastAPI(
    title="Agentic AI Summarizer API",
    description="API backend using Google Gemini to summarize documents",
    version="1.0.0"
)

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0.5,
    max_retries=2,
    # This setting helps avoid the "deprecated" warning you saw
    convert_system_message_to_human=True 
)

# PDF Reader
def read_pdf(file_bytes):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


@app.get("/")
def read_root():
    return {"message": "Server running. Visit /docs"}


@app.post("/summarize")
async def summarize_document(file: UploadFile = File(...)):
    filename = file.filename
    content_type = file.content_type

    try:
        file_content = await file.read()

        # Extract text
        if "pdf" in content_type:
            text_data = read_pdf(file_content)
        else:
            text_data = file_content.decode("utf-8")

        if not text_data:
            raise HTTPException(status_code=400, detail="Could not extract text")

        # Prompt
        template = """
        Provide a detailed, clear and concise summary of the following content:

        {text}

        SUMMARY:
        """

        prompt = PromptTemplate(
            template=template,
            input_variables=["text"]
        )

        # Create runnable chain
        chain = (
            {"text": lambda x: x["doc"].page_content}
            | prompt
            | llm
        )

        doc = Document(page_content=text_data)

        summary = chain.invoke({"doc": doc})

        return {"filename": filename, "summary": summary.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
