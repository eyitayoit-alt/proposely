from PyPDF2 import PdfReader

def read_cv(file):
    # For Streamlit: Read directly from file-like object
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    print(text)
    return text
