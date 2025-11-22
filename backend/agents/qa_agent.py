import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Q&A AGENT
def run_qa(question: str, context: str):
    prompt = f"""
You are an assistant that answers questions only from the provided context.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER (based only on the context):
"""

    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return response.text
