from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.setup.environment_setup import EnvironmentSetup


if __name__ == "__main__":
    logger = PipelineLogger("PURGE")

    spark = SparkManager(
        app_name="purge_local",
        env="local",
        logger=logger
    ).get_spark()

    env = 'local'
    setup_env = EnvironmentSetup(
        spark=spark,
        env=env,
        logger=logger
    ),