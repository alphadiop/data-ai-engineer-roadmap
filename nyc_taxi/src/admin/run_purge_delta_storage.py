from nyc_taxi.src.admin.purge_delta_storage import PurgeDeltaStorage

if __name__ == "__main__":
    from nyc_taxi.src.common.spark_manager import SparkManager
    from nyc_taxi.src.common.logger import PipelineLogger

    logger = PipelineLogger("PURGE",env="local")

    spark = SparkManager(
        app_name="purge_local",
        env="local",
        logger=logger
    ).get_spark()

    PurgeDeltaStorage(
        spark=spark,
        logger=logger,
        env="local"
    ).run()