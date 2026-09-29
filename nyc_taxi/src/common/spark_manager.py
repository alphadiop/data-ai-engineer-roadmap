import sys
import logging
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

from nyc_taxi.src.utils.config.load_config import load_config
from nyc_taxi.src.common.spark_environment_logger import (
    SparkEnvironmentLogger
)

class SparkManager:
    """
    Gestionnaire de SparkSession pour l'environnement local
    et Databricks.
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

        self.config = load_config(
            file_name="variable_environnement",
            env=self.env,
            logger=self.logger or logging.getLogger(__name__)
        )

    def get_spark(self):

        # ==========================================================
        # DATBRICKS
        # ==========================================================
        if self.env == "databricks":
            return SparkSession.getActiveSession()

        # ==========================================================
        # LOCAL
        # ==========================================================
        builder = (
            SparkSession.builder
            .appName(self.app_name)

            # ------------------------------------------------------
            # Spark Master
            # ------------------------------------------------------
            .master(f"local[{self.nombre_coeur}]")

            # ------------------------------------------------------
            # Delta Lake
            # ------------------------------------------------------
            .config(
                "spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension"
            )
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            )

            # ------------------------------------------------------
            # Warehouse
            # ------------------------------------------------------
            .config(
                "spark.sql.warehouse.dir",
                self.config[self.env]["warehouse_dir"]
            )

            # ------------------------------------------------------
            # Hive Metastore Derby  self.config[self.env]["spark_local_dir"] self.config[self.env]["spark_ivy_dir"]
            # ------------------------------------------------------
            # .config(
            #     "spark.hadoop.javax.jdo.option.ConnectionURL",
            #     f"jdbc:derby:{self.config[self.env]['metastore_dir']};create=true"
            # )
            # .config(
            #     "spark.driver.extraJavaOptions",
            #     f"-Dderby.system.home={self.config[self.env]['project_root']}"
            # )

            .config(
                "javax.jdo.option.ConnectionURL",
                f"jdbc:derby:{self.config[self.env]['metastore_dir']};create=true"
            )

            # ------------------------------------------------------
            # Python utilisé par Spark
            # ------------------------------------------------------
            .config(
                "spark.pyspark.python",
                sys.executable
            )
            .config(
                "spark.pyspark.driver.python",
                sys.executable
            )

            # ------------------------------------------------------
            # Ressources : RAM
            # ------------------------------------------------------
            .config(
                "spark.driver.memory",
                "8g"
            )
            .config(
                "spark.executor.memory",
                "8g"
            )
        )

        spark = (
            configure_spark_with_delta_pip(builder)
            .enableHiveSupport()
            .config("spark.jars.ivy", self.config[self.env]["spark_ivy_dir"])
            .config("spark.local.dir",  self.config[self.env]["spark_local_dir"])
            .getOrCreate()
        )

        self.logger.info(
            f"warehouse = {spark.conf.get('spark.sql.warehouse.dir')}"
        )
        self.logger.info(
            f"metastore = {spark.conf.get('javax.jdo.option.ConnectionURL')}"
        )
        self.logger.info(
            f"warehouse_yaml = {self.config[self.env]['warehouse_dir']}"
        )

        self.logger.info(
            f"metastore_yaml = {self.config[self.env]['metastore_dir']}"
        )

        self.logger.info(
            f"Spark local dir = {spark.sparkContext.getConf().get('spark.local.dir')}"
        )


        # ==========================================================
        # LOG CONFIGURATION
        # ==========================================================
        SparkEnvironmentLogger(
            spark=spark,
            config=self.config,
            env=self.env,
            logger=self.logger
        ).log_environment()


        # ==========================================================
        # REPAIR DU METASTORE LOCAL
        # ==========================================================
        if self.env == "local":
            self.logger.info(
                "Checking local metastore..."
            )

        return spark


if __name__ == "__main__":
    pass