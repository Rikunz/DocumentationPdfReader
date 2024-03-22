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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
nlp = spacy.load('en_core_web_sm')
load_dotenv()
bucket_name = os.getenv("BUCKET_NAME")
vectorizer = TfidfVectorizer()
webhook_url = os.getenv("WEBHOOK_URL")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def callWebhook(result, is_success):
    import requests
    payload = {}
    if(is_success):
        payload['result'] = result # Replace with your Data
    else:
        payload['error'] = result
    response = requests.post(webhook_url, json=payload)
    print('Webhook response: ', response)

def load_document_from_link(link:str, is_called:bool = True):
    import requests
    try:
        data = requests.get(link)
        if data.status_code == 200:
            pdf_reader =  PyPDF2.PdfReader(io.BytesIO(data.content))
            document = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                document += page.extract_text()
            if(not is_called):
                callWebhook(document, True)
            return document
        else:
            print(f"Failed to loaded the document in the link")
            callWebhook("Failed to loaded the document in the link", False)
    except Exception as e:
        print(f"TError happen: {e}")
        callWebhook(f"Error happen: {e}", False)


#Funcsi untuk load document sekaligus menjadikan teks
def load_document_from_gcs(bucket_name, blob_name, is_called:bool = True):
    try:
        client = storage.Client()
        print(blob_name)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        document_content = blob.download_as_string() #binary
        pdf_reader =  PyPDF2.PdfReader(io.BytesIO(document_content))
        document = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            document += page.extract_text()
        if(not is_called):
            callWebhook(document, True)
        return document
    except Exception as e:
        print(f"Terjadi error: {e}")
        callWebhook(f"Terjadi error: {e}", False)
        return None

#Mengecek similaritas dalam dua text menggunakan skicit learns cosine_similarity
#   - Cosine simmilarity ini digunakan untuk mencari perbedaan angle dari kedua text document yang sudah di translasikan
def calculate_similarity(vector1, vector2):
    similarity_score = cosine_similarity(vector1, vector2)
    return similarity_score.diagonal()

def translate_to_french(text, is_called:bool = True):
    translated_text = GoogleTranslator(source='auto', target='fr').translate(text)
    if(not is_called):
        callWebhook(translated_text, True)
    return translated_text

def similarity_to_fr_language(bucket_name, filename, platform):
    try:
        if(platform == "cloud"):
            document = load_document_from_gcs(bucket_name, filename)
        else:
            document = load_document_from_link(filename)
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
        callWebhook(result, True)
    except Exception as e:
        print(f"An Error Occur: {e}")
        callWebhook(f"An Error Occur: {e}", False)
