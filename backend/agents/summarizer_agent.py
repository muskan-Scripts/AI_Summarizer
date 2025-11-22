import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# SUMMARY AGENT
def run_summarizer(text: str, style: str = "concise"):
    prompt = f"""
You are a professional summarization agent.
Summarize the following content in a **{style}** manner.

CONTENT:
{text}

SUMMARY:
"""

    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return response.text
