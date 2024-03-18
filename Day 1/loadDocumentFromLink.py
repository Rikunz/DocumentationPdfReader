import requests
import PyPDF2

def load_document_from_link(link:str):
    try:
        data = requests.get(link)
        if data.status_code == 200:
            return data.text
        else:
            print(f"Gagal memuat data dari link")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

print(load_document_from_link("https://raw.githubusercontent.com/faprikaa/Scrapper-DaringUINSK-Telethon/main/README"))