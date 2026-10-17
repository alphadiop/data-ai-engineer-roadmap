from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from nyc_taxi.src.spark.spark_manager import SparkManager
from nyc_taxi.src.logger.logger import PipelineLogger


if __name__ == "__main__":

    periode = 202506

    taxi_type = "yellow"
    env = "local"
    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type,
    )

    # ============================================================
    # Spark
    # ============================================================
    spark_manager = SparkManager(
        env=env,
        app_name="NYC_Taxi_Pipeline",
        logger=logger,
    )

    spark = spark_manager.get_spark()

    #path = r"D:\data-ai-engineer-roadmap\nyc_taxi\spark-warehouse\silver.db\silver_nyc_taxi"
    path = r"D:\data-ai-engineer-roadmap\nyc_taxi\data\bronze\raw_files\yellow\2025\yellow_tripdata_2025-06.parquet"
    df = spark.read.parquet(path)


    df_silver = df.filter(
        col("fare_amount") >= 0
    )

    # df_silver.write.mode("overwrite").parquet(
    #     "data/silver/yellow_trips"
    # )

    df_silver.cache()

    print(df_silver.limit(10).collect())

    # Plusieurs traitements réutilisant df
    df_silver.count()
    df_silver.groupBy("PULocationID").count().show()

    # Libérer le cache
    df_silver.unpersist()

    spark.stop()