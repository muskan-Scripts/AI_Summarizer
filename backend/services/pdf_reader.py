import PyPDF2
import io

def read_pdf(file_bytes):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        t = page.extract_text()
        if t:
            text += t
    return text
