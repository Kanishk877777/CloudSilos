import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "D:/CloudSilos/cloudbucketproject-496408-9572105fe7ab.json"
)

client = storage.Client()

bucket = client.bucket("cloud_silo_mvp")

print(bucket)


def upload_to_gcs(file_name, file_data):
    blob = bucket.blob(file_name)

    blob.upload_from_string(file_data)

    return blob.name


def download_from_gcs(blob_name):
    blob = bucket.blob(blob_name)
    return blob.download_as_bytes()


def delete_from_gcs(blob_name):
    blob = bucket.blob(blob_name)
    blob.delete()
