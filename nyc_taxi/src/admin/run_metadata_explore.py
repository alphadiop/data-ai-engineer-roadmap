from nyc_taxi.src.logger.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.admin.metadata_explore import MetadataExplorer


if __name__ == "__main__":

    # ============================================================
    # Logger
    # ============================================================
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

    catalog_manager = CatalogManager(
        spark=spark,
        env="local",
        logger=logger
    )
    catalog_manager.repair_local_metastore()
    print("=" * 80)
    print("Warehouse")
    print("=" * 80)

    print("Warehouse:",spark.conf.get("spark.sql.warehouse.dir"))
    print("Catalog implementation:",spark.conf.get("spark.sql.catalogImplementation"))


    print("=" * 80)
    print("TEST METASTORE")
    print("=" * 80)

    # spark.sql("SHOW DATABASES").show(
    #     truncate=False
    # )

    # MetadataExplorer(
    #     spark=spark,
    #     env="local",
    #     logger=logger
    # ).run()

    # MetadataExplorer(
    #     spark=spark,
    #     env="local"
    # ).show_table_details(
    #     schema_name="gold",
    #     table_name="gold_fact_trips"
    # )
    #
    # MetadataExplorer(
    #     spark=spark,
    #     env="local"
    # ).show_row_count(
    #     "silver",
    #     "silver_nyc_taxi"
    # )

    # MetadataExplorer(
    #     spark=spark,
    #     env="local",
    #     logger=logger
    # ).show_all_row_counts()