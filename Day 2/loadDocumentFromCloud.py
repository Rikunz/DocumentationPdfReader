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

#Setting Inisiasi pada berbagai library dan logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
nlp = spacy.load('en_core_web_sm')
load_dotenv()
bucket_name = os.getenv("BUCKET_NAME")
vectorizer = TfidfVectorizer()


#Funcsi untuk load document sekaligus menjadikan teks
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

#Mengecek similaritas dalam dua text menggunakan skicit learns cosine_similarity
#   - Cosine simmilarity ini digunakan untuk mencari perbedaan angle dari kedua text document yang sudah di translasikan
def calculate_similarity(vector1, vector2):
    similarity_score = cosine_similarity(vector1, vector2)
    return similarity_score.diagonal()

def translate_to_french(text):
    translated_text = GoogleTranslator(source='auto', target='fr').translate(text)
    return translated_text

def main():
    document = load_document_from_gcs(bucket_name, "SSRN-id3589962.pdf")
    tokens = nlp(document) #Tokenisasi setiap kata
    print(f"Banyak token:{len(tokens)}")
    sentences_en = [token.text for token in tokens.sents] #mendapatkan kalimat dari token.sents property


    # Melakukan vektorisasi pada teks yang telah diproses
    vectorized_en = vectorizer.fit_transform(sentences_en) #Vectorisasi setiap text pada sentences
    logging.info(vectorized_en)
    fr_translated = [translate_to_french(sentence) for sentence in sentences_en] # Aku translate menggunakan DeepTranslator
    vectorized_fr = vectorizer.transform(fr_translated)
    similarity_score = calculate_similarity(vectorized_en, vectorized_fr)
    result = []
    for eng_sentence, fr_sentence, similarity_score in zip(sentences_en, fr_translated, similarity_score):
        result.append({"content": eng_sentence, "translated": fr_sentence, "similarity value": similarity_score})
        print(f'"content": {eng_sentence}, "translated": {fr_sentence}, "similarity value": {similarity_score}')
    logging.info(result)
    
    


main()
