from pyspark.sql import SparkSession, DataFrameReader
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

df = df.withColumn("timestamp", F.to_timestamp("timestamp"))
# Define a window specification to order the data by timestamp within each group
window_spec = Window().partitionBy("trackable_object").orderBy("timestamp")

# Calculate the Euclidean distance
df = df.withColumn("lag_x", F.lag("x").over(window_spec)) \
       .withColumn("lag_y", F.lag("y").over(window_spec))

df = df.withColumn("distance", F.sqrt((df["x"] - df["lag_x"])**2 + (df["y"] - df["lag_y"])**2))

# Calculate the time difference
df = df.withColumn("time_diff", (F.unix_timestamp("timestamp") - F.unix_timestamp("lag_timestamp")))

# Calculate the speed (distance / time_diff)
df = df.withColumn("speed", df["distance"] / df["time_diff"])

# Show the resulting DataFrame
df.select("timestamp", "x", "y", "distance", "speed").show()
