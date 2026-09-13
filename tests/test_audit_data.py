from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager

if __name__=="__main__":

    env = 'local'
    logger = PipelineLogger(
        "periode_insere",
        env=env
    )
    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        env=env,
        logger=logger
    )
    spark = spark_manager.get_spark()

    spark.sql("""
        SELECT *
        FROM audit.audit_load
        ORDER BY end_time DESC
    """).show(truncate=False)