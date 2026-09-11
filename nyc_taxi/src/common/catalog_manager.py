
import os
from urllib.parse import urlparse
import platform
from pathlib import Path
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger


class CatalogManager:
    """ 
    un catalog sert à isoler et organiser les données dans un espace de travail
    le schema est un sous dossier du catalog, il contient des :
    """
    def __init__(self,spark, logger: 'PipelineLogger', env: str = "local"):
        self.spark = spark
        self.logger = logger or logging.getLogger(__name__)
        self.env = env

    # ============================================================================
    # ============Catalogs========================================================
    # ============================================================================
    def create_environment_schemas(self):
        schemas = [
            "bronze",
            "silver",
            "gold",
            "audit",
            "ref"
        ]

        for schema in schemas:
            if self.env in ["local", "docker"]:
                self.spark.sql(
                    f"CREATE DATABASE IF NOT EXISTS {schema}"
                )
            else:
                self.spark.sql(
                    f"""
                    CREATE SCHEMA IF NOT EXISTS
                    nyc_taxi.{schema}
                    """
                )

    def get_table_name(
            self,
            schema_name: str,
            table_name: str,
            catalog_name: str = "nyc_taxi"
    ) -> str:
        """
        le nom d'une table Delta est structurée différemment en local ou sur databricks
        """

        if self.env == "databricks":
            return f"{catalog_name}.{schema_name}.{table_name}"
            # 'local','docker'
        return f"{schema_name}.{table_name}"




    def audit_row_count(self):
        return self.get_table_name(
            schema_name="audit",
            table_name="audit_row_count"
        )

    def audit_load(self):
        return self.get_table_name(
            schema_name="audit",
            table_name="audit_load"
        )

    def silver_nyc_taxi(self):
        return self.get_table_name(
            schema_name="silver",
            table_name="silver_nyc_taxi"
        )

    def gold_fact_trips(self):
        return self.get_table_name(
            schema_name="gold",
            table_name="gold_fact_trips"
        )

    def get_schema_name(
            self,
            schema_name: str,
            catalog_name: str = "nyc_taxi"
    ):

        if self.env in ("local", "docker"):
            return schema_name
        return f"{catalog_name}.{schema_name}"


    def create_catalog(self, catalog_name: str):
        self.logger.info(f"ENV = {self.env}")

        if self.env in ("local", "docker"):

            self.logger.info(
                f"Mode local : catalog {catalog_name} ignoré"
            )
            return

        self.spark.sql(
            f"CREATE CATALOG IF NOT EXISTS {catalog_name}"
        )



    def catalog_exists(self, catalog_name: str) -> bool:
        catalogs = [
            row.catalog
            for row in self.spark.sql("SHOW CATALOGS").collect()
        ]
        return catalog_name in catalogs


    def rename_catalog(self, old_catalog: str, new_catalog: str):
        """
        Renomme un catalog Unity Catalog.
        """
        catalogs = [
            row.catalog
            for row in self.spark.sql("SHOW CATALOGS").collect()
        ]

        if old_catalog not in catalogs:
            raise ValueError(
                f"Le catalog '{old_catalog}' n'existe pas."
            ) 

        if new_catalog in catalogs:
            raise ValueError(
                f"Le catalog '{new_catalog}' existe déjà."
            )

        self.spark.sql(
            f"""
            ALTER CATALOG {old_catalog}
            RENAME TO {new_catalog}
            """
        )
        self.logger.info(
            f"Catalog '{old_catalog}' renommé en '{new_catalog}'"
        )


    def drop_catalog(
        self,
        catalog_name: str,
        cascade: bool = False
    ):

        cascade_clause = "CASCADE" if cascade else "RESTRICT"

        self.spark.sql(
            f"""
            DROP CATALOG IF EXISTS {catalog_name}
            {cascade_clause}
            """
        )

        self.logger.info(
            f"Catalog {catalog_name} dropped"
        )

    # ====================================================================================================
    # ====================Schemas============================================================
    # ====================================================================================================

    def create_schema(
            self,
            schema_name: str,
            env:str
    ):

        if env in ("local", "docker"):
            self.spark.sql(
                f"""
                CREATE DATABASE IF NOT EXISTS
                {schema_name}
                """
            )
        else:
            self.spark.sql(
                f"""
                CREATE SCHEMA IF NOT EXISTS
                nyc_taxi.{schema_name}
                """
            )


    def drop_schema(
        self,
        catalog_name: str,
        schema_name: str,
        cascade: bool = False
    ):

        cascade_clause = "CASCADE" if cascade else "RESTRICT"

        self.spark.sql(
            f"""
            DROP SCHEMA IF EXISTS
            {catalog_name}.{schema_name}
            {cascade_clause}
            """
        )

        self.logger.info(
            f"Schema {catalog_name}.{schema_name} dropped"
        )

    def schema_exists(
        self,
        catalog_name: str,
        schema_name: str
    ) -> bool:

        schemas = self.spark.sql(
            f"SHOW SCHEMAS IN {catalog_name}"
        ).collect()

        return any(
            row.namespace == schema_name
            for row in schemas
        )

        
    def rename_schema(
        self,
        catalog_name: str,
        old_schema: str,
        new_schema: str
    ):
        """
        Databricks ne supporte pas
        ALTER SCHEMA ... RENAME TO ...

        On recrée donc le schéma puis
        on déplace les tables.
        """

        if not self.schema_exists(
            catalog_name,
            old_schema
        ):
            raise ValueError(
                f"Schema '{old_schema}' introuvable"
            )

        if self.schema_exists(
            catalog_name,
            new_schema
        ):
            raise ValueError(
                f"Schema '{new_schema}' existe déjà"
            )

        self.spark.sql(
            f"""
            CREATE SCHEMA
            {catalog_name}.{new_schema}
            """
        )

        tables = self.spark.sql(
            f"""
            SHOW TABLES IN
            {catalog_name}.{old_schema}
            """
        ).collect()

        for table in tables:

            old_name = (
                f"{catalog_name}."
                f"{old_schema}."
                f"{table.tableName}"
            )

            new_name = (
                f"{catalog_name}."
                f"{new_schema}."
                f"{table.tableName}"
            )

            self.spark.sql(
                f"""
                ALTER TABLE
                {old_name}
                RENAME TO
                {new_name}
                """
            )

        self.spark.sql(
            f"""
            DROP SCHEMA
            {catalog_name}.{old_schema}
            """
        )

        self.logger.info(
            f"Schema '{old_schema}' "
            f"renamed to '{new_schema}'"
        )


    def show_catalogs(self):
        return self.spark.sql(
            "SHOW CATALOGS"
        )


    def schema_exists2(
        self,
        catalog_name: str,
        schema_name: str
    ) -> bool:

        df = self.spark.sql(
            f"SHOW SCHEMAS IN {catalog_name}"
        )
        return (
            df.filter(
                f"databaseName = '{schema_name}'"
            ).count() > 0
        )


    def show_schemas(
        self,
        catalog_name: str
    ):

        return self.spark.sql(
            f"SHOW SCHEMAS IN {catalog_name}"
        )


    # ==================================================
    # Tables
    # ==================================================

    def show_tables(
            self,
            schema_name: str,
            catalog_name: str = "nyc_taxi"
    ):
        schema_full_name = self.get_schema_name(
            schema_name=schema_name,
            catalog_name=catalog_name
        )
        return self.spark.sql(
            f"""
            SHOW TABLES IN {schema_full_name}
            """
        )


    def table_exists(
        self,
        catalog_name: str,
        schema_name: str,
        table_name: str
    ) -> bool:
        full_name = self.get_table_name(
            schema_name=schema_name,
            table_name=table_name,
            catalog_name=catalog_name
        )
        return self.spark.catalog.tableExists(
            full_name
        )


    def rename_table(
        self,
        catalog_name: str,
        schema_name: str,
        old_table_name: str,
        new_table_name: str
    ):
        """
            Renomme une table Databricks.
        """

        old_name = self.get_table_name(
            schema_name,
            old_table_name,
            catalog_name
        )

        new_name = self.get_table_name(
            schema_name,
            new_table_name,
            catalog_name
        )

        self.spark.sql(
            f"""
            ALTER TABLE {old_name}
            RENAME TO {new_name}
            """
        )

    # ==================================================
    # Description
    # ==================================================

    def describe_schema(
        self,
        catalog_name: str,
        schema_name: str
    ):

        return self.spark.sql(
            f"""
            DESCRIBE SCHEMA EXTENDED
            {catalog_name}.{schema_name}
            """
        )


    def describe_table(
            self,
            catalog_name: str,
            schema_name: str,
            table_name: str
    ):

        full_name = self.get_table_name(
            schema_name=schema_name,
            table_name=table_name,
            catalog_name=catalog_name
        )

        return self.spark.sql(
            f"DESCRIBE DETAIL {full_name}"
        )


    def describe_table_columns(
            self,
            catalog_name,
            schema_name,
            table_name
    ):

        full_name = self.get_table_name(
            schema_name,
            table_name,
            catalog_name
        )

        return self.spark.sql(
            f"""
            DESCRIBE {full_name}
            """
        )

    def repair_local_metastore(self):

        if self.env not in ("local", "docker"):
            self.logger.info(
                "repair_local_metastore skipped (not local)"
            )
            return

        warehouse = self.get_warehouse_path()

        self.logger.info(
            f"Warehouse Spark : "
            f"{self.spark.conf.get('spark.sql.warehouse.dir')}"
        )

        self.logger.info(
            f"Scanning warehouse : {warehouse}"
        )

        if not warehouse.exists():
            self.logger.warning(
                f"Warehouse does not exist : {warehouse}"
            )
            return

        for root, dirs, files in os.walk(warehouse):

            # On cherche uniquement les répertoires Delta
            if "_delta_log" not in dirs:
                continue

            table_path = Path(root)

            schema_dir = table_path.parent

            schema_name = schema_dir.name.replace(".db", "")
            table_name = table_path.name

            full_table_name = (
                f"`{schema_name}`.`{table_name}`"
            )

            self.logger.info(
                f"Delta table found : {full_table_name}"
            )
            self.logger.info(
                f"Location          : {table_path}"
            )

            try:

                # 1. Créer le schema s'il n'existe pas
                self.spark.sql(
                    f"""
                    CREATE DATABASE IF NOT EXISTS
                    `{schema_name}`
                    """
                )

                # 2. Vérifier si la table est déjà enregistrée
                exists = self.spark.catalog.tableExists(
                    f"{schema_name}.{table_name}"
                )

                if exists:
                    self.logger.info(
                        f"Already registered : "
                        f"{schema_name}.{table_name}"
                    )
                    continue

                # 3. Enregistrer la table Delta
                self.spark.sql(
                    f"""
                    CREATE TABLE {full_table_name}
                    USING DELTA
                    LOCATION '{table_path.as_posix()}'
                    """
                )

                self.logger.info(
                    f"Registered : "
                    f"{schema_name}.{table_name}"
                )

            except Exception as e:

                self.logger.error(
                    f"Error repairing "
                    f"{schema_name}.{table_name} : {e}"
                )



    def get_warehouse_path(self) -> Path:

        warehouse_uri = self.spark.conf.get(
            "spark.sql.warehouse.dir"
        )
        self.logger.info(
            f"Warehouse URI       : {warehouse_uri}"
        )
        if warehouse_uri.startswith("file:"):

            parsed = urlparse(warehouse_uri)

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

        self.logger.info(
            f"Warehouse path      : {warehouse_path}"
        )

        self.logger.info(
            f"Warehouse exists     : {warehouse_path.exists()}"
        )

        return warehouse_path




    #catalog_manager.show_catalogs().show()
    #catalog_manager.show_schemas("nyc_taxi").show()
    #catalog_manager.show_tables("nyc_taxi","gold").show()
    #catalog_manager.describe_table_columns("nyc_taxi","audit", "audit_load").show()
    #catalog_manager.create_catalog("test_catalog")
    #catalog_manager.create_schema("test_catalog", "test_schema")
    #catalog_manager.drop_schema("test_catalog", "test_schema")
    #catalog_manager.drop_catalog("test_catalog")


