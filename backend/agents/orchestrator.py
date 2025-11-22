from agents.summarizer_agent import run_summarizer
from agents.qa_agent import run_qa
from services.vector_store import retrieve_chunks

class Orchestrator:

    @staticmethod
    def summarize(doc_id: str, style: str):
        retrieved = retrieve_chunks(doc_id, "summary", k=5)
        combined = "\n".join([r["chunk"] for r in retrieved])
        result = run_summarizer(combined, style)
        return result

    @staticmethod
    def answer(doc_id: str, question: str):
        retrieved = retrieve_chunks(doc_id, question, k=3)
        context = "\n".join([r["chunk"] for r in retrieved])
        answer = run_qa(question, context)
        return answer, retrieved
