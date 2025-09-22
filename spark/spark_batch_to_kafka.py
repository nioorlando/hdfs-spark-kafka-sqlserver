#!/usr/bin/env python3
from pyspark.sql import SparkSession, functions as F, types as T

# ==== CONFIGURATION ====
USERNAME = "<username>"                                    # ganti sesuai user
SRC_DIR  = f"/uc2/{USERNAME}/uc2_src"                      # lokasi input JSON
TOPIC    = f"usecase2.{USERNAME}"                          # nama Kafka topic
BROKERS  = "broker1.example.internal:9093"                 # Kafka bootstrap server (placeholder)

spark = (SparkSession.builder
         .appName(f"uc2-batch-schemaful-{USERNAME}")
         .getOrCreate())

# Schema sederhana untuk input
schema = T.StructType([
    T.StructField("id",   T.IntegerType(), True),
    T.StructField("name", T.StringType(),  True),
])

# READ & simple TRANSFORM
df = (spark.read.schema(schema).json(SRC_DIR)
        .withColumn("name", F.upper(F.trim("name")))
        .dropna(subset=["id"])
        .coalesce(1))

# ==== Connect envelope: {"schema": {...}, "payload": {...}} ====
connect_schema = F.struct(
    F.lit("struct").alias("type"),
    F.array(
        F.struct(F.lit("id").alias("field"),   F.lit("int32").alias("type"),  F.lit(False).alias("optional")),
        F.struct(F.lit("name").alias("field"), F.lit("string").alias("type"), F.lit(True).alias("optional"))
    ).alias("fields"),
    F.lit(False).alias("optional")
)

payload = F.struct(
    F.col("id").cast("int").alias("id"),
    F.col("name").alias("name")
)

value_connect_json = F.to_json(F.struct(
    connect_schema.alias("schema"),
    payload.alias("payload")
))

out = df.select(
    F.col("id").cast("string").alias("key"),  # Kafka key (bisa diganti PK)
    value_connect_json.alias("value")
)
# ===============================================================

# WRITE ke Kafka
(out.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
   .write
   .format("kafka")
   .option("kafka.bootstrap.servers", BROKERS)
   .option("kafka.security.protocol", "SASL_SSL")
   .option("kafka.sasl.mechanism", "GSSAPI")
   .option("kafka.sasl.kerberos.service.name", "kafka")
   .option("kafka.ssl.truststore.location", "/path/to/kafka-truststore.jks")
   .option("kafka.ssl.truststore.password", "<TRUSTSTORE_PASSWORD>")
   .option("kafka.ssl.endpoint.identification.algorithm", "")
   .option("topic", TOPIC)
   .save())

spark.stop()
