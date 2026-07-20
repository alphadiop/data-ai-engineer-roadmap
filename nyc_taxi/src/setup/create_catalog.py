
import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/src"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.catalog_manager import CatalogManager
from common.logger import PipelineLogger 


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
    logger = PipelineLogger("Cretate Catalog")
    create_catalog = CreateCatalog(spark=spark, logger=logger)
    create_catalog.run()
   