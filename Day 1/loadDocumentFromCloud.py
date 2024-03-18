import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "project-thoriq-8f4af9a7330f.json"

bucket_name = "zettatask"

def load_document_from_gcs(bucket_name, blob_name):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        document_content = blob.download_as_string().decode("utf-8")

        return document_content
    except Exception as e:
        print(f"Terjadi error: {e}")
        return None
    

print(load_document_from_gcs(bucket_name, "us_counties_pop_est_2019.csv"))