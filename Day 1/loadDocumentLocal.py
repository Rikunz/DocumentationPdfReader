import os
import PyPDF2

def load_document(filepath):
    assert os.path.exists(filepath), "File tidak ada :()"
    try:
        with open(filepath, "rb") as readFile: 
            pdf_reader =  PyPDF2.PdfReader(readFile)
            document = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]  
                document += page.extract_text()
            return document
    except Exception as e:
        print(f"Terjadi Error: {e}")

print(load_document("SSRN-id3589962.pdf"))
