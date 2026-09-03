from nyc_taxi.src.common.spark_manager import SparkManager

spark = SparkManager(app_name="audit_check",env="local").get_spark()
spark.sql(""" DESCRIBE EXTENDED silver.silver_nyc_taxi """).show(200, False)
spark.sql(""" DESCRIBE DETAIL silver.silver_nyc_taxi """).show(truncate=False)