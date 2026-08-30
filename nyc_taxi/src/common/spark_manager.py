import sys
import logging

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from nyc_taxi.src.common.catalog_manager import CatalogManager

class SparkManager:
    """
    """
    def __init__(
            self,
            app_name="nyc_taxi",
            env="local",
            logger=None
    ):
        self.app_name = app_name
        self.env = env
        self.logger = logger or logging.getLogger(__name__)
        self.nombre_coeur = 2

    def get_spark(self):

        if self.env == "databricks":
            return SparkSession.getActiveSession()

        builder = (
            SparkSession.builder
            .appName(self.app_name)
            .master(f"local[{self.nombre_coeur}]")
            .config(
                "spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension"
            )
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            )
            .config(
                "spark.sql.warehouse.dir",
                "D:/data-ai-engineer-roadmap/spark-warehouse"
            )
            .config(
                "javax.jdo.option.ConnectionURL",
                "jdbc:derby:D:/data-ai-engineer-roadmap/metastore_db;create=true"
            )
            .config(
                "spark.pyspark.python",
                sys.executable
            )
            .config(
                "spark.pyspark.driver.python",
                sys.executable
            )
            .config("spark.driver.memory", "8g")
            .config("spark.executor.memory", "8g")
        )
        spark = (
            configure_spark_with_delta_pip(builder)
            .enableHiveSupport()
            .getOrCreate()
        )

        CatalogManager(
            spark=spark,
            env="local",
            logger=self.logger
        ).repair_local_metastore()

        return spark