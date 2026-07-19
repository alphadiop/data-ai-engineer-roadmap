import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.pipeline_step import PipelineStep
from common.logger import PipelineLogger
from common.decorators import log_execution 
from common.schema_manager import SchemaManager
from utils.load_json import load_json

class Cheick:
    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger


    def get_partition_columns(self):
        """Return the list of columns to partition the data."""
        for table in [
            "nyc_taxi.silver.silver_nyc_taxi",
            "nyc_taxi.gold.gold_fact_trips",
            "nyc_taxi.gold.gold_dim_date",
            "nyc_taxi.gold.gold_kpi_daily"
        ]:
            self.logger.info(table)

            spark.sql(
                f"DESCRIBE DETAIL {table}"
            ).select("partitionColumns").show(truncate=False)


    def cheick_if_partition_exists(self):

        """Return True if the table exists."""
        for table in [
            "nyc_taxi.silver.silver_nyc_taxi",
            "nyc_taxi.gold.gold_fact_trips",
            "nyc_taxi.gold.gold_dim_date",
            "nyc_taxi.gold.gold_kpi_daily"
        ]:
            detail = self.spark.sql(f""" DESCRIBE DETAIL {table} """).collect()[0]

            self.logger.info(
                f"{table} has {detail.partitionColumns}"
            )


    def get_detail(self):
        return self.spark.sql("""
                DESCRIBE DETAIL nyc_taxi.silver.silver_nyc_taxi
            """).show(truncate=False)
        
    def get_verifi(self):
        self.logger.info(f"{'=' * 12} DEBUT DEBUG {'=' * 12} ")
        self.spark.table("nyc_taxi.silver.silver_nyc_taxi").printSchema()

        self.logger.info(f"{'=' * 12} FIN DEBUG {'=' * 12} ")
        
if __name__ == "__main__":
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("Cheick").getOrCreate()
    logger = PipelineLogger("Cheick")
    cheick = Cheick(spark, logger)
    ## cheick.get_partition_columns()
    cheick.cheick_if_partition_exists()




