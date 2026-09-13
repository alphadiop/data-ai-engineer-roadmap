from datetime import datetime
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager

from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    IntegerType,
    StringType,
    TimestampType,
)

logger = PipelineLogger("uber_pipeline", env='local')

spark = SparkManager(
    app_name="serialisation",
    env="local",
    logger=logger
).get_spark()

# from pyspark.sql import SparkSession
# spark = (
#     SparkSession.builder
#     .appName("test_row_count_serialization")
#     .master("local[2]")
#     .getOrCreate()
# )

data = [
    (
        1788099035,
        202504,
        "bronze",
        3970553,
        datetime.now()
    ),
    (
        1788099035,
        202504,
        "silver",
        3776318,
        datetime.now()
    ),
]

schema = StructType([
    StructField("run_id", LongType(), False),
    StructField("periode", IntegerType(), False),
    StructField("table_name", StringType(), False),
    StructField("row_count", LongType(), False),
    StructField("created_at", TimestampType(), False),
])

print("=" * 60)
print("TEST SERIALIZATION ROW COUNT")
print("=" * 60)

print("Python :", __import__("sys").version)
print("Spark  :", spark.version)

df = spark.createDataFrame(
    data=data,
    schema=schema
)

df.printSchema()
df.show()

spark.stop()