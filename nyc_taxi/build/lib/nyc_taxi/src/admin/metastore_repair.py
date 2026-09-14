import os
from pathlib import Path
from urllib.parse import urlparse
import platform


class MetastoreRepair:
    """
        C'est une opération de maintenance/réparation de l'environnement local.
        # recherche du warehouse
        # détection des tables Delta
        # création des schemas
        # enregistrement des tables
    """

    def __init__(self, spark, env="local", logger=None):
        self.spark = spark
        self.env = env
        self.logger = logger


    def repair(self):
        if self.env != "local":
            self._log(
                "Metastore repair skipped: environment is not local."
            )
            return

        self._log("=" * 100)
        self._log("METASTORE REPAIR")
        self._log("=" * 100)

        warehouse = self.get_warehouse_path()

        self._log(
            f"Warehouse Spark : "
            f"{self.spark.conf.get('spark.sql.warehouse.dir')}"
        )

        self._log(
            f"Warehouse path  : {warehouse}"
        )

        if not warehouse.exists():
            self._log(
                f"Warehouse does not exist : {warehouse}",
                level="warning"
            )
            return

        registered = 0
        already_registered = 0
        errors = 0

        # Recherche des tables Delta
        for root, dirs, files in os.walk(warehouse):

            if "_delta_log" not in dirs:
                continue

            table_path = Path(root)
            schema_dir = table_path.parent
            schema_name = schema_dir.name.replace(
                ".db",
                ""
            )

            table_name = table_path.name

            full_table_name = (
                f"{schema_name}.{table_name}"
            )

            self._log(
                f"Delta table found : {full_table_name}"
            )

            self._log(
                f"Location          : {table_path}"
            )

            try:

                # -------------------------------------------------
                # 1. Créer le schema s'il n'existe pas
                # -------------------------------------------------

                self.spark.sql(
                    f"""
                        CREATE DATABASE IF NOT EXISTS
                        `{schema_name}`
                        """
                )

                # -------------------------------------------------
                # 2. Vérifier si la table existe déjà
                # -------------------------------------------------

                exists = self.spark.catalog.tableExists(
                    full_table_name
                )

                if exists:

                    self._log(
                        f"Already registered : "
                        f"{full_table_name}"
                    )

                    already_registered += 1

                    continue

                # -------------------------------------------------
                # 3. Enregistrer la table Delta
                # -------------------------------------------------

                self.spark.sql(
                    f"""
                        CREATE TABLE
                        `{schema_name}`.`{table_name}`
                        USING DELTA
                        LOCATION '{table_path.as_posix()}'
                        """
                )

                self._log(
                    f"Registered : {full_table_name}"
                )

                registered += 1

            except Exception as e:

                errors += 1

                self._log(
                    f"Error repairing "
                    f"{full_table_name} : {e}",
                    level="error"
                )

        # ---------------------------------------------------------
        # Résumé
        # ---------------------------------------------------------

        self._log("=" * 100)
        self._log("METASTORE REPAIR SUMMARY")
        self._log("=" * 100)

        self._log(
            f"Registered          : {registered}"
        )

        self._log(
            f"Already registered  : {already_registered}"
        )

        self._log(
            f"Errors              : {errors}"
        )

        self._log("=" * 100)

    def get_warehouse_path(self) -> Path:

        warehouse_uri = self.spark.conf.get(
            "spark.sql.warehouse.dir"
        )

        if warehouse_uri.startswith("file:"):

            parsed = urlparse(
                warehouse_uri
            )

            if platform.system() == "Windows":

                warehouse_path = Path(
                    parsed.path.lstrip("/")
                )

            else:

                warehouse_path = Path(
                    parsed.path
                )

        else:

            warehouse_path = Path(
                warehouse_uri
            )

        return warehouse_path

    def _log(
            self,
            message,
            level="info"
    ):

        if self.logger:
            if level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)
            else:
                self.logger.info(message)
        else:
            print(message)