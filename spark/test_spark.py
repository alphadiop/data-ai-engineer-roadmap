from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.utils.config import load_config
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.bronze.uber_bronze import UberBronze
from nyc_taxi.src.common.pipeline_context import PipelineContext
from pyspark.sql.functions import (
            sum,
            col
)

if __name__ == "__main__":

    taxi_type = "yellow"
    # #taxi_type = "green"
    # #taxi_type = "fhv"
    env = 'local'
    year = 2025
    month = 6

    logger = PipelineLogger('Bronze')

    config_all = load_config("variable_environnement", logger)
    config = config_all[env]

    context = PipelineContext(
        env=env,
        taxi_type=taxi_type
    )

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    )

    bronze = UberBronze(
        spark = spark_manager.get_spark(),
        logger=logger
    )

    file_name = bronze.get_file_name(
        taxi_type, year, month
    )
    context.periode = bronze.get_period(file_name)

    context.config = config

    df = bronze.run(context)

    df.groupBy("PULocationID").agg(sum("total_amount")).show()
    df.filter(col("PULocationID").isNull()).count()
