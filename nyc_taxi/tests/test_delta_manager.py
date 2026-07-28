from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager


if __name__ == "__main__":

    tab = "gold.gold_kpi_daily"
    logger = PipelineLogger("uber_pipeline")

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    )
    spark = spark_manager.get_spark()

    df = spark.read.table(tab)
    df.show()