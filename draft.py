from dotenv import load_dotenv
from app.src.services import gcp
import os
load_dotenv()

project_id = 'dev-'+ os.environ['GCP_PROJECT_ID']
bucket_name = os.environ['BUCKET_NAME']
dataset_name = os.environ['DATASET_NAME']

gcp.send_file_to_gcs(local_file_path='src_de_sample_data/10000_tracking.txt',
                     bucket_name=bucket_name,
                     remote_file_path='tracking/10000_tracking.txt'
                      )

gcp.send_file_to_gcs(local_file_path='src_de_sample_data/10000_metadata.json',
                     bucket_name=bucket_name,
                     remote_file_path='metadata/10000_metadata.json'
                      )

gcp.gcs_to_bq(project_id=project_id,
              gcs_bucket_name=bucket_name,
              gcs_file_path='metadata/10000_metadata.json',
              bq_dataset_name=f'{dataset_name}_staging',
              bq_table_name='metadata',
              type='json')

gcp.gcs_to_bq(project_id=project_id,
              gcs_bucket_name=bucket_name,
              gcs_file_path='tracking/10000_tracking.txt',
              bq_dataset_name=f'{dataset_name}_staging',
              bq_table_name='tracking',
              type='nljson')

tracking = gcp.job_to_bq(query=f'select * from {project_id}.{dataset_name}_staging.tracking')

df = tracking.to_dataframe()
