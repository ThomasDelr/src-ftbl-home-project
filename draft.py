from dotenv import load_dotenv
from app.src.services import gcp,util
import os
import pandas as pd
load_dotenv()

project_id = 'dev-'+ os.environ['GCP_PROJECT_ID']
bucket_name = os.environ['BUCKET_NAME']
dataset_name = os.environ['DATASET_NAME']

query = """
select * from src_ftbl_staging.temp_metadata
"""

df = gcp.job_to_bq(query)
df2= util.calculate_distance(df=df, game_id='game_id', team_col='team_id',player_col='trackable_object')


df['distance'].max()