from flask import Flask
from dotenv import load_dotenv
from app.src.services import gcp
from app.src.services import logger
import os
from app.src.services import util

app = Flask(__name__)
logger_instance = logger.MyLogger(__name__).get_logger()


@app.route('/home')
def home():
    return 'home src ftbl project data processing'

@app.route('/send_file_to_gcs')
def file_to_gcs():
    gcp.send_file_to_gcs(local_file_path=local_file_path,bucket_name=bucket_name,
                         remote_file_path=remote_file_path)
    return('file sent to gcs')

@app.route('/loading_into_bq')
def load_to_bq():
    gcp.gcs_to_bq(project_id=project_id,
                  gcs_bucket_name=bucket_name,
                  gcs_file_path=remote_file_path,
                  bq_dataset_name=f'{dataset_name}_staging',
                  bq_table_name='metadata')
    return('file loaded to bq')

@app.route('/transformed_metadata_table'):
def transformed_data():
    ### add game id that we are pushing


if __name__ == '__main__':
    load_dotenv()
    project_id = 'dev-' + os.environ['GCP_PROJECT_ID']
    bucket_name = os.environ['BUCKET_NAME']
    dataset_name = os.environ['DATASET_NAME']
    local_file_path='src_de_sample_data/10000_metadata.json'
    remote_file_path='tracking/10000_metadata.json'
    app.run(port=int(os.environ.get("PORT",8080)),host="0.0.0.0", debug=True)