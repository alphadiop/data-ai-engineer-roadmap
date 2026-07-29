
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager
import os

def main():
    logger = PipelineLogger("uber_pipeline")

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    )
    spark = spark_manager.get_spark()

    logger.info("WAREHOUSE")
    logger.info(
        spark.conf.get(
            "spark.sql.warehouse.dir"
        )
    )

    logger.info("METASTORE")
    logger.info(
        spark.conf.get(
            "javax.jdo.option.ConnectionURL",
            "absent"
        )
    )

    logger.info("CATALOG")
    spark.sql(
        "SELECT current_catalog()"
    ).show()

    logger.info("DATABASES")
    spark.sql(
        "SHOW DATABASES"
    ).show()

if __name__ == "__main__":
    main()