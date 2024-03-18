import requests
import io
import PyPDF2

def load_document_from_link(link:str):
    try:
        data = requests.get(link)
        if data.status_code == 200:
            pdf_reader =  PyPDF2.PdfReader(io.BytesIO(data.content))
            document = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                document += page.extract_text()
            return document
        else:
            print(f"Gagal memuat data dari link")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# print(load_document_from_link("https://pdfobject.com/pdf/sample.pdf"))
print(load_document_from_link("https://media.pragprog.com/titles/ktuk/excerpts.pdf"))