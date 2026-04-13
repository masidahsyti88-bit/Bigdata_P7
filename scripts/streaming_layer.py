from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType

# buat Spark Session
spark = SparkSession.builder \
    .appName("Streaming Processing") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# schema data (HARUS sesuai dengan generator)
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("city", StringType()) \
    .add("product", StringType()) \
    .add("price", IntegerType()) \
    .add("quantity", IntegerType())

# baca streaming dari folder stream_data
df = spark.readStream \
    .schema(schema) \
    .json("stream_data")

# optional: hitung total revenue
df_transformed = df.withColumn(
    "revenue", df["price"] * df["quantity"]
)

# tulis ke Parquet (Serving Layer)
query = df_transformed.writeStream \
    .format("parquet") \
    .option("path", "data/serving/stream") \
    .option("checkpointLocation", "data/checkpoints/stream") \
    .outputMode("append") \
    .start()

print("🚀 Spark Streaming Started...")

query.awaitTermination()