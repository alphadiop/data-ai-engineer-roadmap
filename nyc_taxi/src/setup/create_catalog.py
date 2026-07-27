
import os
import sys


from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.logger import PipelineLogger 


class CreateCatalog:
    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger

    def run(self):
        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
        )
        catalog_manager.create_catalog("nyc_taxi")

        catalog_manager.create_schema(
            catalog_name="nyc_taxi",
            schema_name = "bronze"
        )
        catalog_manager.create_schema(
            catalog_name="nyc_taxi",
            schema_name = "silver"
        )
        catalog_manager.create_schema(
            catalog_name="nyc_taxi",
            schema_name = "gold"
        )
        catalog_manager.create_schema(
            catalog_name="nyc_taxi",
            schema_name = "audit"
        )
        catalog_manager.create_schema(
            catalog_name="nyc_taxi",
            schema_name = "ref"
        )
        catalog_manager.drop_schema(
            catalog_name="nyc_taxi",
            schema_name="audit_load",
            cascade=True
        )

        catalog_manager.show_catalogs().show()
        catalog_manager.show_schemas("nyc_taxi").show()
        catalog_manager.show_tables("nyc_taxi", "bronze").show()
        catalog_manager.show_tables("nyc_taxi", "silver").show()
        catalog_manager.show_tables("nyc_taxi", "gold").show()
        catalog_manager.show_tables("nyc_taxi", "ref").show()
        catalog_manager.show_tables("nyc_taxi", "audit").show()


if __name__ == "__main__":
    from pyspark.sql import SparkSession
    import sys

    spark = (
        SparkSession.builder
        .appName("nyc_taxi")
        .config(
            "spark.pyspark.python",
            sys.executable
        )
        .getOrCreate()
    )
    logger = PipelineLogger("Cretate Catalog")
    create_catalog = CreateCatalog(
        spark=spark,
        logger=logger
    )
    create_catalog.run()
   