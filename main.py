import datetime

from flask import Flask, session, request
from dotenv import load_dotenv
from app.src.services import gcp
from app.src.services import logger
import os
import secrets
import datetime
from app.src.services import util

app = Flask(__name__)
logger_instance = logger.MyLogger(__name__).get_logger()
app.secret_key = secrets.token_hex(16)

@app.route('/home')
def home():
    #session['user_id'] = 1
    return 'home src ftbl project data processing'

@app.route('/send_file_to_gcs/<local_file_path>')
def file_to_gcs(local_file_path):
    remote_file_path = f'{local_file_path.split("/")[0]}/{local_file_path.split("/")[1]}'
    gcp.send_file_to_gcs(local_file_path=local_file_path,bucket_name=bucket_name,
                         remote_file_path=remote_file_path)
    #session['user_id']=remote_file_path
    return('file sent to gcs')

@app.route('/loading_into_bq')
def load_to_bq():
    table = remote_file_path.split("/")[0]
    gcp.gcs_to_bq(project_id=project_id,
                  gcs_bucket_name=bucket_name,
                  gcs_file_path=remote_file_path,
                  bq_dataset_name=f'{dataset_name}_staging',
                  bq_table_name=table)
    return('file loaded to bq')

@app.route('/transformed_metadata_table')
def transformed_data():
    ### add game id that we are pushing
    gcp.loading_data(query_file='app/src/queries/gameheaders.toml',id=10000, technical_id=technical_id, technical_date=technical_date)
    gcp.loading_data(query_file='app/src/queries/players_game_details.toml', id=10000, technical_id=technical_id,technical_date=technical_date)
    gcp.loading_data(query_file='app/src/queries/tracking.toml', id=10000, technical_id=technical_id,technical_date=technical_date)

    return 'data sent to table'

if __name__ == '__main__':
    load_dotenv()
    project_id = 'dev-' + os.environ['GCP_PROJECT_ID']
    bucket_name = os.environ['BUCKET_NAME']
    dataset_name = os.environ['DATASET_NAME']
    technical_id = secrets.token_hex(10)
    technical_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    local_file_path='src_de_sample_data/10000_metadata.json'
    remote_file_path='metadata/10000_metadata.json'
    app.run(port=int(os.environ.get("PORT",8080)),host="0.0.0.0", debug=True)