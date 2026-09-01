import sys
from pyspark.sql import SparkSession

print("Python :", sys.version)

spark = (
    SparkSession.builder
    .appName("test_pyspark_basic")
    .master("local[2]")
    .getOrCreate()
)

print("Spark :", spark.version)

df = spark.createDataFrame(
    [
        (1, "test"),
        (2, "spark"),
    ],
    ["id", "name"]
)

df.show()
spark.stop()



# from datetime import datetime
# from nyc_taxi.src.common.logger import PipelineLogger
# from nyc_taxi.src.common.spark_manager import SparkManager
#
# logger = PipelineLogger("uber_pipeline", env='local')
#
# spark = SparkManager(
#     app_name="serialisation",
#     env="local",
#     logger=logger
# ).get_spark()
#
#
# spark.createDataFrame(
#     [(1, "test")],
#     ["id", "name"]
# ).show()