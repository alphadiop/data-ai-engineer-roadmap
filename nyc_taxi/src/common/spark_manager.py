import sys

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


class SparkManager:
    """
    Gestionnaire de SparkSession.

    Supporte :
    - Local Spark
    - Databricks
    - Delta Lake
    """

    def __init__(
            self,
            app_name: str = "nyc_taxi",
            env: str = "local",
            logger=None
    ):

        self.app_name = app_name
        self.env = env
        self.logger = logger


    def get_spark(self) -> SparkSession:
        """
        Création ou récupération d'une SparkSession.
        """

        builder = (
            SparkSession.builder
            .appName(self.app_name)

            # Delta Lake
            .config(
                "spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension"
            )

            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            )
        )


        # Configuration spécifique local
        if self.env == "local":
            builder = (
                builder
                .master("local[*]")

                # utilise le Python de ton environnement conda
                .config(
                    "spark.pyspark.python",
                    sys.executable
                )
                .config(
                    "spark.pyspark.driver.python",
                    sys.executable
                )
            )


        spark = (
            configure_spark_with_delta_pip(builder)
            .getOrCreate()
        )


        # Réduction des logs Spark
        spark.sparkContext.setLogLevel(
            "ERROR"
        )


        if self.logger:
            self.logger.info(
                f"SparkSession created "
                f"(env={self.env})"
            )

            self.logger.info(
                f"Spark version : {spark.version}"
            )


        return spark

