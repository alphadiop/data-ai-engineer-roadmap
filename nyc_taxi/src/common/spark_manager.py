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
        # =======================================
        # DATABRICKS
        # ==========================
        if self.env == "databricks":
            spark = SparkSession.getActiveSession()
            if spark is None:
                spark = SparkSession.builder.getOrCreate()
            return spark

    # =======================================
        # LOCAL
        # ======================================
        builder = (
            SparkSession.builder
            .appName(self.app_name)
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
        )

        if self.env == "local":
            builder = (
                builder
                .master("local[*]")
                .config(
                    "spark.pyspark.python",
                    sys.executable
                )
                .config(
                    "spark.pyspark.driver.python",
                    sys.executable
                )
                .config(
                    "javax.jdo.option.ConnectionURL",
                    "jdbc:derby:D:/data-ai-engineer-roadmap/metastore_db;create=true"
                )
            )

        spark = (
            configure_spark_with_delta_pip(builder)
            .enableHiveSupport()
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        if self.logger:
            self.logger.info(
                f"SparkSession created env={self.env}"
            )
            self.logger.info(
                f"warehouse={spark.conf.get('spark.sql.warehouse.dir')}"
            )
        return spark


