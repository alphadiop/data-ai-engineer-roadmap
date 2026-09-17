## find /mnt/d/data-ai-engineer-roadmap -type f -name "_delta_log"

from nyc_taxi.src.logger.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager
from delta.tables import DeltaTable

if __name__ == "__main__":
    """
    spark-warehouse/
     ├── audit.db
     │   ├── audit_load
     │   └── audit_row_count
     │
     ├── silver.db
     │   └── silver_nyc_taxi
     │
     └── gold.db
         ├── gold_fact_trips
         ├── gold_dim_date
         ├── gold_dim_location
         └── gold_kpi_daily
    """
    env = 'local'
    periode = 202411
    taxi_type = 'yellow'

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type
    )

    spark = SparkManager(
        app_name="metadata_explorer",
        env="local",
        logger=logger
    ).get_spark()

    path = "D:/data-ai-engineer-roadmap/spark-warehouse/silver.db/silver_nyc_taxi"
    df = spark.read.format("delta").load(path)
    df.show(5, False)

    spark.read.format("delta").load(
        "D:/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load"
    ).show()


    # spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_fact_trips"
    # ).show()

