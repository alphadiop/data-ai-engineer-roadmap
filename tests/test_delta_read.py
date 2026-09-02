from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("delta_test")
    .master("local[2]")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)

spark = (
    configure_spark_with_delta_pip(builder)
    .getOrCreate()
)

df = spark.read.format("delta").load(
    "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load"
)

print("COUNT =", df.count())
df.show(truncate=False)