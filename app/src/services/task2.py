from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def write_to_bigquery(result_df, project_id, dataset_id, table_id, mode='append'):
    result_df.write \
        .format('bigquery') \
        .mode(mode) \
        .option('table', f'{project_id}.{dataset_id}.{table_id}') \
        .save()

def calculate_distance_spark(df, game_id, player_col, timestamp_col='timestamp', x_col='x', y_col='y'):
    # Convert timestamp column to timestamp type
    df = df.withColumn(timestamp_col, F.col(timestamp_col).cast('timestamp'))

    # Sort the DataFrame by player_id, timestamp, and team_id
    window_spec = Window().partitionBy(game_id,player_col).orderBy(timestamp_col)
    df = df.withColumn('dx', F.col(x_col) - F.lag(F.col(x_col)).over(window_spec)).fillna(0)
    df = df.withColumn('dy', F.col(y_col) - F.lag(F.col(y_col)).over(window_spec)).fillna(0)

    # Calculate distance using Pythagorean theorem
    df = df.withColumn('distance', F.sqrt(F.col('dx')**2 + F.col('dy')**2))

    # Calculate time difference in seconds with microseconds
    time_diff_col = (F.col(timestamp_col).cast('long') - F.lag(F.col(timestamp_col).cast('long')).over(window_spec))
    df = df.withColumn('time_diff', time_diff_col.cast('double')).fillna(0)

    # Calculate speed (sqrt(dx^2 + dy^2) / time_diff) and convert to m/s
    df = df.withColumn('speed', (F.sqrt(F.col('dx')**2 + F.col('dy')**2) / F.col('time_diff')).cast('double'))

    # Convert speed to km/h
    df = df.withColumn('speed', F.col('speed') * 3.6)

    # Calculate acceleration (change in speed / change in time)
    df = df.withColumn('acceleration', (F.col('speed') - F.lag(F.col('speed')).over(window_spec)) / F.col('time_diff'))

    # Drop intermediate columns
    df = df.drop('dx', 'dy', 'time_diff')

    return df


required_jars = [
    "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.34.0",
    "com.google.cloud.bigdataoss:gcs-connector-hadoop2-2.1.1"
    #,"./jar-dependencies/gcs-connector-hadoop2-latest.jar"
]

spark = SparkSession.builder \
    .appName("task2-src_ftbl_project") \
    .config("spark.jars.packages", ",".join(required_jars)) \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
    .getOrCreate()

bucket = "src-ftbl"
spark.conf.set('temporaryGcsBucket', bucket)
spark._jsc.hadoopConfiguration().set('fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
spark._jsc.hadoopConfiguration().set('fs.AbstractFileSystem.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS')


df = spark.read \
  .format("bigquery") \
  .load("dev-src-ftbl-home-project.src_ftbl.game_tracking")

result_df = calculate_distance_spark(df, 'game_id', 'trackable_object', 'timestamp', 'x', 'y')

write_to_bigquery(result_df, project_id='dev-src-ftbl-home-project', dataset_id='src_ftbl', table_id='task_1')


############ spread
import pandas as pd
from scipy.spatial.distance import pdist, squareform,euclidean
import math
from app.src.services import gcp

group = df[df.trackable_object!=55].groupby(["trackable_object", 'timestamp'])[["x", "y"]]

def player_dist(player_a, player_b):
    return [euclidean(player_a.iloc[i], player_b.iloc[i])
            for i in range(len(player_a))]

ball = df[df.trackable_object==55][["x", "y"]]

ball_dist = group.apply(player_dist, player_b=(ball))