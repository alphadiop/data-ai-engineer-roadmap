from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


WAREHOUSE = "/mnt/d/data-ai-engineer-roadmap/spark-warehouse"

builder = (
    SparkSession.builder
    .appName("test_audit_exists")
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
        WAREHOUSE
    )
)

spark = (
    configure_spark_with_delta_pip(builder)
    .enableHiveSupport()
    .getOrCreate()
)

audit_table = "audit.audit_load"

print()
print("=" * 50)
print("AUDIT TABLE TEST")
print("=" * 50)

print("Table :", audit_table)

print(
    "tableExists =",
    spark.catalog.tableExists(audit_table)
)

print()
print("COUNT")

spark.sql(
    f"SELECT COUNT(*) AS cnt FROM {audit_table}"
).show()

spark.stop()