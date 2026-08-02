from pathlib import Path
import os
import sys
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager


if __name__ == "__main__":

    logger = PipelineLogger("debug_delta")

    logger.info(sys.version)

    spark = (
        SparkManager(
            app_name="debug_delta",
            env="local",
            logger=logger
        )
        .get_spark()
    )

    logger.info("=" * 120)
    logger.info("WAREHOUSE")
    logger.info(
        spark.conf.get("spark.sql.warehouse.dir")
    )

    logger.info("=" * 120)
    logger.info("METASTORE")
    logger.info(
        spark.conf.get(
            "javax.jdo.option.ConnectionURL",
            "not found"
        )
    )

    logger.info("=" * 120)
    logger.info("DATABASES")
    spark.sql("SHOW DATABASES").show(truncate=False)

    logger.info("=" * 120)
    logger.info("TABLES")

    for db in ["audit", "silver", "gold"]:

        try:
            logger.info(f"=== {db.upper()} ===")

            spark.sql(
                f"SHOW TABLES IN {db}"
            ).show(truncate=False)

        except Exception as e:
            logger.error(str(e))

    logger.info("=" * 120)
    logger.info("DELTA FOLDERS")

    warehouse = Path(
        "D:/data-ai-engineer-roadmap/spark-warehouse"
    )

    for root, dirs, files in os.walk(warehouse):
        if "_delta_log" in dirs:
            logger.info(root)

    logger.info("=" * 120)
    logger.info("READ TABLES")

    tables = [
        "audit.audit_load",
        "audit.audit_row_count",
        "silver.silver_nyc_taxi",
        "gold.gold_dim_date",
        "gold.gold_fact_trips",
        "gold.gold_kpi_daily"
    ]

    for table_name in tables:
        try:

            logger.info(
                f"Lecture {table_name}"
            )
            spark.read.table(
                table_name
            ).show(5,truncate=False)

        except Exception as e:

            logger.error(
                f"{table_name} : {e}"
            )