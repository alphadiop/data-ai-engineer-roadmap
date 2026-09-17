from pathlib import Path

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


warehouse = "/mnt/d/data-ai-engineer-roadmap/test-delta-warehouse"

builder = (
    SparkSession.builder
    .appName("test_delta_basic")
    .master("local[2]")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
    .config(
        "spark.sql.warehouse.dir",
        warehouse
    )
)

spark = (
    configure_spark_with_delta_pip(builder)
    .getOrCreate()
)

print("=" * 60)
print("TEST DELTA")
print("=" * 60)

print("Python :", __import__("sys").version)
print("Spark  :", spark.version)

df = spark.createDataFrame(
    [
        (1, "bronze"),
        (2, "silver"),
        (3, "gold"),
    ],
    ["id", "layer"]
)

print("\nDATAFRAME")
df.show()

delta_path = "/mnt/d/data-ai-engineer-roadmap/test-delta-table"

print("\nWRITE DELTA")
df.write.format("delta").mode("overwrite").save(delta_path)

print("\nREAD DELTA")
df_read = (
    spark.read
    .format("delta")
    .load(delta_path)
)

df_read.show()

print("\nCOUNT =", df_read.count())

print("\nDELTA LOG")
print(Path(delta_path, "_delta_log").exists())

spark.stop()