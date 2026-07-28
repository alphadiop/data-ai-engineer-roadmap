
import os
import sys


from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.logger import PipelineLogger 


class CreateCatalog:
    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger

    def run(self, context):
        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env,
        )

        catalog_manager.create_catalog("nyc_taxi")

        for schema in [
            "audit",
            "silver",
            "gold",
            "ref",
            "audit"
        ]:
            catalog_manager.create_schema(schema, context.env)

if __name__ == "__main__":
    from pyspark.sql import SparkSession
    import sys