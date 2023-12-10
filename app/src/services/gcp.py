from google.cloud import storage
from google.cloud import bigquery
import os
import json
import toml

def gcs_to_bq(project_id, gcs_bucket_name, gcs_file_path, bq_dataset_name, bq_table_name):
    # Set up the BigQuery client
    client = bigquery.Client(project=project_id)

    # Create a load job configuration
    load_job_config = bigquery.LoadJobConfig()
    load_job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    load_job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

    #load_job_config.source_format =bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
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

def send_file_to_gcs(local_file_path, bucket_name, remote_file_path):
    # Initialize the storage client
    storage_client = storage.Client()

    # Get the reference to the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the reference to the blob
    blob = bucket.blob(remote_file_path)

    ## For slow upload speed
    storage.blob._DEFAULT_CHUNKSIZE = 2097152 # 1024 * 1024 B * 2 = 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 2097152 # 2 MB

    # Upload the file to the blob
    blob.upload_from_filename(local_file_path)

    return f'file {local_file_path} sent to gcs as {remote_file_path}'

def loading_data(query_file,id, technical_id, technical_date):
    with open(query_file, "r") as toml_file:
        queries = toml.load(toml_file)

    query = queries["idQuery"][0]['query']
    query = query.format(game_id=id, technical_id=technical_id,technical_date=technical_date)
    client = bigquery.Client()
    # Construct the query job
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = False  # Use standard SQL
    query_job = client.query(query, job_config=job_config)
    # Wait for the query to complete
    query_job.result()

    return query_job.result()

def copy_file(source_bucket_name, source_blob_name, destination_bucket_name, destination_blob_name):
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    # Get source and destination bucket references
    source_bucket = storage_client.bucket(source_bucket_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    # Get the source blob
    source_blob = source_bucket.blob(source_blob_name)
    # Create a new blob in the destination bucket
    destination_blob = destination_bucket.blob(destination_blob_name)
    # copy to new destination
    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name)
    # delete in old destination
    source_blob.delete()

    print(f"File {source_blob_name} copied from {source_bucket_name} to {destination_bucket_name}/{destination_blob_name}")

    return destination_blob

def job_to_bq(query):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = False  # Use standard SQL
    query_job = client.query(query, job_config=job_config)
    result = query_job.result()
    return result.to_dataframe()

def df_to_bq(df,project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    table_id = f'{dataset_id}.{table_id}'
    load_job_config = bigquery.LoadJobConfig()
    load_job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job = client.load_table_from_dataframe(df, table_id, job_config=load_job_config)
    job.result()
    table = client.get_table(table_id)
    return print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

def object_to_gcs(data, bucket_name,file_name):
    """
      :type file_name: object
    """
    client=storage.Client()
    csv_content = data.to_csv(index=False, encoding='UTF-8', sep=',',header=True, mode='a')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_content, content_type='text/csv')

    print(f'Object saved to gs://{bucket_name}/{file_name}')