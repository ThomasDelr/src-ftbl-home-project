from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("example") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.34.0") \
    .getOrCreate()

# Read data from BigQuery into a PySpark DataFrame
df = spark.read \
  .format("bigquery") \
  .load("dev-src-ftbl-home-project.src_ftbl.tracking")

def calculate_distance_spark(df, game_id, team_col, player_col, timestamp_col='timestamp', x_col='x', y_col='y'):
    # Convert timestamp column to timestamp type
    df = df.withColumn(timestamp_col, F.col(timestamp_col).cast('timestamp'))

    # Sort the DataFrame by player_id, timestamp, and team_id
    window_spec = Window().partitionBy(game_id, team_col, player_col).orderBy(timestamp_col)
    df = df.withColumn('dx', F.col(x_col) - F.lag(F.col(x_col)).over(window_spec)).fillna(0)
    df = df.withColumn('dy', F.col(y_col) - F.lag(F.col(y_col)).over(window_spec)).fillna(0)

    # Calculate distance using Pythagorean theorem
    df = df.withColumn('distance', F.sqrt(F.col('dx')**2 + F.col('dy')**2))

    # Calculate time difference in seconds with microseconds
    df = df.withColumn('time_diff', (F.col(timestamp_col) - F.lag(F.col(timestamp_col)).over(window_spec)).cast('double')).fillna(0)

    # Calculate speed (sqrt(dx^2 + dy^2) / time_diff) and convert to m/s
    df = df.withColumn('speed', (F.sqrt(F.col('dx')**2 + F.col('dy')**2) / F.col('time_diff')).cast('double'))

    # Convert speed to km/h
    df = df.withColumn('speed', F.col('speed') * 3.6)

    # Calculate acceleration (change in speed / change in time)
    df = df.withColumn('acceleration', (F.col('speed') - F.lag(F.col('speed')).over(window_spec)) / F.col('time_diff'))

    # Drop intermediate columns
    df = df.drop('dx', 'dy', 'time_diff')

    return df
