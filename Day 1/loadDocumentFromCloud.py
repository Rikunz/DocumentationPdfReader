import os
from google.cloud import storage
import io
import PyPDF2

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "project-thoriq-8f4af9a7330f.json"

bucket_name = "zettatask"

def load_document_from_gcs(bucket_name, blob_name):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        document_content = blob.download_as_string() #binary
        pdf_reader =  PyPDF2.PdfReader(io.BytesIO(document_content))
        metadata = pdf_reader.metadata
        print(metadata)
        document = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            document += page.extract_text()
        return document
    except Exception as e:
        print(f"Terjadi error: {e}")
        return None
    

print(load_document_from_gcs(bucket_name, "SSRN-id3589962.pdf"))