from flask import Flask, session, request
from dotenv import load_dotenv
from app.src.services import gcp
from app.src.services import logger
import os
import secrets
import datetime
from urllib.parse import quote, unquote
import time

app = Flask(__name__)
logger_instance = logger.MyLogger(__name__).get_logger()
app.secret_key = secrets.token_hex(16)

@app.route('/home')
def home():
    return 'home src ftbl project data processing'

@app.route('/send_file_to_gcs/<path:local_file_path>')
def file_to_gcs(local_file_path):
    # Decode the URL-encoded path parameter
    start = time.time()
    step_id = 10
    step_name = 'extracting data to gcs'
    decoded_local_file_path = unquote(local_file_path)

    folder = local_file_path.split('/')[1].split('_')[1].split('.')[0]
    remote_file_path = f'{folder}/{decoded_local_file_path.split("/")[1]}'
    gcp.send_file_to_gcs(local_file_path=decoded_local_file_path,bucket_name=bucket_name,
                         remote_file_path=remote_file_path)

    app.config['remote_file_path'] = remote_file_path
    end = time.time()
    total_time = str(end-start)
    query =f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)
    return(f'file {local_file_path} sent to gcs')

@app.route('/loading_into_bq')
def load_to_bq():
    start = time.time()
    step_id = 20
    step_name = 'loading to staging zone'

    remote_file_path = app.config.get('remote_file_path')
    game_id = remote_file_path.split('/')[1].split('_')[0]
    app.config['game_id'] = game_id
    table = remote_file_path.split("/")[0]

    gcp.gcs_to_bq(project_id=project_id,gcs_bucket_name=bucket_name,
                  gcs_file_path=remote_file_path,bq_dataset_name=f'{dataset_name}_staging',
                  bq_table_name=table)
    end = time.time()
    total_time = str(end-start)
    query =f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)

    return(f'file {remote_file_path} loaded to bq for the game {game_id}')

@app.route('/transformed_tables')
def transforming_data():
    start = time.time()
    step_id = 30
    step_name = 'transforming data'

    game_id = app.config.get('game_id')
    remote_file_path = app.config.get('remote_file_path')
    if remote_file_path.split('/')[0]=='metadata':
        gcp.loading_data(query_file='app/src/queries/gameheaders.toml',id=game_id, technical_id=technical_id, technical_date=technical_date)
        gcp.loading_data(query_file='app/src/queries/game_players_details.toml',id=game_id, technical_id=technical_id, technical_date=technical_date)
    else:
        gcp.loading_data(query_file='app/src/queries/game_tracking.toml',id=game_id, technical_id=technical_id,technical_date=technical_date)

    end = time.time()
    total_time = str(end-start)
    query =f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)

    return 'data sent to tables'

@app.route('/creating_backup')
def loading_backup():
    start = time.time()
    step_id = 40
    step_name = 'back up raw dataset'

    remote_file_path = app.config.get('remote_file_path')
    game_id = remote_file_path.split('/')[1].split('_')[0]
    app.config['game_id'] = game_id
    table = remote_file_path.split("/")[0]

    gcp.gcs_to_bq(project_id=project_id,gcs_bucket_name=bucket_name,
                  gcs_file_path=remote_file_path,bq_dataset_name=f'{dataset_name}_raw',
                  bq_table_name=table)

    end = time.time()
    total_time = str(end-start)
    query =f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)

    return 'backup data inserted'

@app.route('/truncating_staging')
def truncate_staging():
    start = time.time()
    step_id = 50
    step_name = 'truncating staging area'

    remote_file_path = app.config.get('remote_file_path')
    game_id = remote_file_path.split('/')[1].split('_')[0]
    app.config['game_id'] = game_id
    query = """truncate table src_ftbl_staging.metadata;
                truncate table src_ftbl_staging.tracking;"""
    gcp.job_to_bq(query=query)

    end = time.time()
    total_time = str(end - start)
    query = f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)

    return f'staging table truncated '

@app.route('/moving_raw_files')
def gcs_to_gcs():
    start = time.time()
    step_id = 60
    step_name = 'moving raw files to processed gcs bucket'
    remote_file_path = app.config.get('remote_file_path')
    gcp.copy_file(source_bucket_name=bucket_name,source_blob_name=remote_file_path,
                  destination_bucket_name=f'{bucket_name}-processed',
                  destination_blob_name=remote_file_path)

    end = time.time()
    total_time = str(end - start)
    query = f"""
        insert into monitoring.step_execution 
        select '{technical_id}' as tec_id, timestamp('{technical_date}') as tec_date, '{step_name}' as step_name, {step_id} as step_id, 'success' as status, '{total_time}' as execution_time, '{remote_file_path}' as filename_source;
           """
    gcp.job_to_bq(query=query)
    return 'files moved'

if __name__ == '__main__':
    load_dotenv()
    project_id = 'dev-' + os.environ['GCP_PROJECT_ID']
    bucket_name = os.environ['BUCKET_NAME']
    dataset_name = os.environ['DATASET_NAME']
    technical_id = secrets.token_hex(10)
    technical_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#    local_file_path='src_de_sample_data/10000_metadata.json'
#    remote_file_path='metadata/10000_metadata.json'
    app.run(port=int(os.environ.get("PORT",8080)),host="0.0.0.0", debug=True)