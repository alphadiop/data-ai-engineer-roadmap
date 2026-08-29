from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.common.logger import PipelineLogger
from pyspark.sql import SparkSession


if __name__ == "__main__":
    logger = PipelineLogger('Bronze')
    spark = SparkManager(env="local", logger=logger).get_spark()
    logger.info(spark)
    spark.sql("SHOW SCHEMAS").show(truncate=False)
    #spark.sql("SHOW TABLES IN audit").show(truncate=False)
    df = spark.read.table("audit.audit_load")
    df.show(truncate=False)

    path_warehouse = spark.conf.get("spark.sql.warehouse.dir")
    logger.info(path_warehouse)