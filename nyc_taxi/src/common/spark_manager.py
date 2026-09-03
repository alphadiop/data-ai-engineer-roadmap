import sys
import logging
from pathlib import Path

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.utils.config.load_config import load_config
import logging

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
            "variable_environnement",
            self.logger or logging.getLogger(__name__)
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
                self.config["local"]["warehouse_dir"]
            )

            # ------------------------------------------------------
            # Hive Metastore Derby
            # ------------------------------------------------------
            .config(
                "javax.jdo.option.ConnectionURL",
                f"jdbc:derby:{self.config['local']['metastore_dir']};create=true"
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
            # Ressources
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
            .getOrCreate()
        )

        # ==========================================================
        # LOG CONFIGURATION
        # ==========================================================
        self.logger.info("=" * 120)
        self.logger.info("SPARK CONFIGURATION")
        self.logger.info("=" * 120)

        self.logger.info(
            f"cwd             = {Path.cwd()}"
        )

        self.logger.info(
            f"python          = {sys.executable}"
        )

        self.logger.info(
            f"spark_version   = {spark.version}"
        )

        self.logger.info(
            f"warehouse       = "
            f"{spark.conf.get('spark.sql.warehouse.dir')}"
        )

        self.logger.info(
            f"warehouse_dir   = "
            f"{self.config['local']['warehouse_dir']}"
        )

        self.logger.info(
            f"metastore_dir   = "
            f"{self.config['local']['metastore_dir']}"
        )

        self.logger.info(
            f"bronze_path     = "
            f"{self.config['local']['bronze_path']}"
        )

        self.logger.info("=" * 120)

        # ==========================================================
        # REPAIR DU METASTORE LOCAL
        # ==========================================================
        if self.env == "local":

            self.logger.info(
                "Checking local metastore..."
            )

            CatalogManager(
                spark=spark,
                env=self.env,
                logger=self.logger
            ).repair_local_metastore()

        return spark


if __name__ == "__main__":
    pass