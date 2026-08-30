# src/jobs/purge_delta_storage.py

import shutil
from pathlib import Path

from nyc_taxi.src.utils.config.load_config import load_config

import logging
import shutil
from pathlib import Path

from nyc_taxi.src.utils.config.load_config import load_config


class PurgeDeltaStorage:
    """
    Utilitaire de maintenance local.

    Modes disponibles :
    - truncate() : vide les tables mais conserve le metastore.
    - run()      : supprime schémas, warehouse et metastore.

    A utiliser uniquement en environnement local.
    """

    SCHEMAS = [
        "audit",
        "silver",
        "gold",
        "ref"
    ]

    TABLES = [
        "audit.audit_load",
        "audit.audit_row_count",
        "silver.silver_nyc_taxi",
        "gold.gold_fact_trips",
        "gold.gold_dim_date",
        "gold.gold_kpi_daily"
    ]

    def __init__(
            self,
            spark,
            logger=None,
            env="local"
    ):
        self.spark = spark
        self.env = env
        self.logger = logger or logging.getLogger(__name__)

        self.config = load_config(
            "variable_environnement",
            self.logger
        )

    def run(self):
        """
        Purge complète :
        - DROP DATABASE CASCADE
        - arrêt Spark
        - suppression warehouse
        - suppression metastore
        """

        self._validate_env()

        self.logger.info("=" * 80)
        self.logger.info("DEBUT PURGE COMPLETE")
        self.logger.info("=" * 80)

        self.drop_schemas()

        self.logger.info("Arrêt de Spark")
        self.spark.stop()

        self.delete_local_storage()

        self.logger.info("=" * 80)
        self.logger.info("FIN PURGE COMPLETE")
        self.logger.info("=" * 80)

    def truncate(self):
        """
        Vide les tables mais conserve les schémas.
        """

        self._validate_env()

        self.logger.info("=" * 80)
        self.logger.info("TRUNCATE DES TABLES")
        self.logger.info("=" * 80)

        for table in self.TABLES:

            try:

                self.logger.info(
                    f"TRUNCATE TABLE {table}"
                )

                self.spark.sql(
                    f"TRUNCATE TABLE {table}"
                )

            except Exception as e:

                self.logger.warning(
                    f"Impossible de vider {table} : {e}"
                )

    def drop_schemas(self):

        for schema in self.SCHEMAS:

            try:

                self.logger.info(
                    f"DROP DATABASE IF EXISTS {schema} CASCADE"
                )

                self.spark.sql(
                    f"DROP DATABASE IF EXISTS {schema} CASCADE"
                )

            except Exception as e:

                self.logger.warning(
                    f"Impossible de supprimer {schema} : {e}"
                )

    def delete_local_storage(self):

        paths = [
            Path(self.config["local"]["warehouse_dir"]),
            Path(self.config["local"]["metastore_dir"])
        ]

        for path in paths:

            if not path.exists():

                self.logger.warning(
                    f"Répertoire introuvable : {path}"
                )

                continue

            self.logger.info(
                f"Suppression : {path}"
            )

            shutil.rmtree(
                path,
                ignore_errors=True
            )

    def _validate_env(self):

        if self.env != "local":

            raise ValueError(
                "Cette opération est autorisée uniquement en local"
            )

if __name__ == "__main__":
    from nyc_taxi.src.common.spark_manager import SparkManager
    from nyc_taxi.src.common.logger import PipelineLogger

    logger = PipelineLogger("PURGE")

    spark = SparkManager(
        app_name="purge_local",
        env="local",
        logger=logger
    ).get_spark()

    PurgeDeltaStorage(
        spark=spark,
        logger=logger,
        env="local"
    ).run()

    # PurgeDeltaStorage(
    #     spark=spark,
    #     logger=logger,
    #     env="local"
    # ).truncate()