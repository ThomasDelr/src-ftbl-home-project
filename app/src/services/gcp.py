from google.cloud import storage
from google.cloud import bigquery
import os


def send_file_to_gcs(local_file_path, bucket_name, remote_file_path):
    # Initialize the storage client
    storage_client = storage.Client()

    # Get the reference to the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the reference to the blob
    blob = bucket.blob(remote_file_path)

    # Upload the file to the blob
    with open(local_file_path, "rb") as f:
        blob.upload_from_file(f)
    return f'file {local_file_path} sent to gcs as {remote_file_path}'

def gcs_to_bq(gcs_bucket_name, gcs_file_path, bq_dataset_name, bq_table_name):
    # Set up the BigQuery client
    client = bigquery.Client()

    # Create a load job configuration
    load_job_config = bigquery.LoadJobConfig()
    load_job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    # Specify the source URI and destination table
    source_uri = "gs://{}/{}".format(gcs_bucket_name, gcs_file_path)
    destination_table = client.dataset(bq_dataset_name).table(bq_table_name)

    # Load the data from GCS to BigQuery
    load_job = client.load_table_from_uri(
        source_uri,
        destination_table,
        job_config=load_job_config
    )

    # Wait for the load job to complete
    load_job.result()

    return f'file {gcs_file_path} loaded into bq dataset {bq_dataset_name} and table {bq_table_name}'