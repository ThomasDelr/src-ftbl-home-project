from dotenv import load_dotenv
from app.src.services import gcp
import os
import pandas as pd
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
              bq_table_name='metadata')

gcp.gcs_to_bq(project_id=project_id,
              gcs_bucket_name=bucket_name,
              gcs_file_path='tracking/10000_tracking.txt',
              bq_dataset_name=f'{dataset_name}_staging',
              bq_table_name='tracking')

query = """
with ball as (
SELECT 10000 as game_id,
      tr.timestamp,cast(FORMAT_TIME("%H:%M:%E*S",timestamp) as string) as t,
      tr.frame, 
      tr.period, 
      d.*
 FROM `dev-src-ftbl-home-project.src_ftbl_staging.tracking` tr
 , unnest(data) as d
 where trackable_object = 55
),
players as (
SELECT 10000 as game_id,
      tr.timestamp,cast(FORMAT_TIME("%H:%M:%E*S",timestamp)as string) as t,
      tr.frame, 
      tr.period, 
      d.*
 FROM `dev-src-ftbl-home-project.src_ftbl_staging.tracking` tr
 , unnest(data) as d
 where trackable_object != 55
)
select p.*, b.z as ball_z, b.y as ball_y, b.x as ball_x, b.trackable_object as ball_id  
from  players p
left join ball as b on b.timestamp=p.timestamp
order by trackable_object, timestamp

"""

tracking = gcp.job_to_bq(query=query)

df = tracking.to_dataframe()
def convert_to_seconds(timedelta_obj):
    # Convert timedelta to seconds
    return timedelta_obj.total_seconds()

df['x'].diff()
df['timestamp2'] =pd.to_timedelta(df['t'])



def calculate_player_acceleration(df):
    # Convert 'time' to timedelta using the custom function
    df['delta_t'] = df.groupby('trackable_object')['timestamp2'].diff()

    # Sort the DataFrame by player and time
    df = df.sort_values(by=['trackable_object', 'timestamp2'])

    # Calculate time differences and velocities within each player group
    df['delta_t'] = df.groupby('trackable_object')['timestamp2'].diff()
    df['delta_t_seconds'] = df['delta_t'].apply(convert_to_seconds)
    df['delta_vx'] = df.groupby('trackable_object')['x'].diff() / df['delta_t_seconds']
    df['delta_vy'] = df.groupby('trackable_object')['y'].diff() / df['delta_t_seconds']

    return df['delta_vx'], df['delta_vy']

acceleration_x, acceleration_y = calculate_player_acceleration(df)
df['acceleration_x'] = acceleration_x
df['acceleration_y'] = acceleration_y

print(df)