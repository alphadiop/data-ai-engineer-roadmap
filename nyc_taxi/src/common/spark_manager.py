import sys

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

class SparkManager:

    def __init__(
            self,
            app_name="nyc_taxi",
            env="local",
            logger=None
    ):
        self.app_name = app_name
        self.env = env
        self.logger = logger

    def get_spark(self):

        if self.env == "databricks":
            return SparkSession.getActiveSession()

        builder = (
            SparkSession.builder
            .appName(self.app_name)
            .master("local[*]")
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
        )

        return (
            configure_spark_with_delta_pip(builder)
            .enableHiveSupport()
            .getOrCreate()
        )



