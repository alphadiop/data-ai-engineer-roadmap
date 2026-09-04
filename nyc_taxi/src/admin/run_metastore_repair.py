from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.admin.metastore_repair import MetastoreRepair


if __name__ == "__main__":

    logger = PipelineLogger(
        "MetastoreRepair",
        env="local"
    )

    spark = SparkManager(
        app_name="metastore_repair",
        env="local",
        logger=logger
    ).get_spark()

    repair = MetastoreRepair(
        spark=spark,
        env="local",
        logger=logger
    )

    repair.repair()


### python -m nyc_taxi.src.admin.run_metastore_repair