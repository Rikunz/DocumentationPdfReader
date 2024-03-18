from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
import os
from google.cloud import storage
import io
import PyPDF2
from dotenv import load_dotenv
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

nlp = spacy.load('en_core_web_sm')

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

bucket_name = "zettatask"

def load_document_from_gcs(bucket_name, blob_name):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        document_content = blob.download_as_string() #binary
        pdf_reader =  PyPDF2.PdfReader(io.BytesIO(document_content))
        document = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            document += page.extract_text()
        return document
    except Exception as e:
        print(f"Terjadi error: {e}")
        return None


def calculate_similarity(text1, text2, vectorizer):
    vectorized_texts = vectorizer.transform([text1, text2])
    similarity_score = cosine_similarity(vectorized_texts)
    return similarity_score[0, 1]

def translate_to_french(text):
    translated_text = GoogleTranslator(source='auto', target='fr').translate(text)
    return translated_text

def main():
    document = load_document_from_gcs(bucket_name, "SSRN-id3589962.pdf")
    tokens = nlp(document)
    print(len(tokens))
    sentences = [token.text for token in tokens.sents]
    vectorizer = TfidfVectorizer()

    # Melakukan vektorisasi pada teks yang telah diproses
    vectorized_text = vectorizer.fit_transform(sentences)
    fr_translated = [translate_to_french(sentence) for sentence in sentences]
    fr_translated_doc = " ".join(fr_translated)
    similarity_score = calculate_similarity(document, fr_translated_doc, vectorizer)
    result = {"content": vectorized_text, "translated": fr_translated_doc, "similarity value": similarity_score}
    logging.info(result)
    
    


main()
