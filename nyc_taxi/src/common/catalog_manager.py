import os
import sys
from nyc_taxi.src.common.logger import PipelineLogger

class CatalogManager:
    """ 
    un catalog sert à isoler et organiser les données dans un espace de travail
    le schema est un sous dossier du catalog, il contient des :
    """

    def __init__(self,spark, logger: PipelineLogger, env: str = "local"):
        self.spark = spark
        self.logger = logger,
        self.env = env

    # ============================================================================
    # ============Catalogs========================================================
    # ============================================================================

    def get_table_name(
            self,
            schema_name: str,
            table_name: str,
            catalog_name: str = "nyc_taxi"
    ) -> str:

        if self.env == "local":
            return f"{schema_name}.{table_name}"
        return f"{catalog_name}.{schema_name}.{table_name}"


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


    def create_catalog(self, catalog_name: str):
        self.spark.sql(
            f"CREATE CATALOG IF NOT EXISTS {catalog_name}"
        )

        self.logger.info(
            f"Catalog {catalog_name} created"
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
        catalog_name: str,
        schema_name: str
    ):

        self.spark.sql(
            f"""
            CREATE SCHEMA IF NOT EXISTS
            {catalog_name}.{schema_name}
            """
        )

        self.logger.info(
            f"Schema {catalog_name}.{schema_name} created"
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
        

    def catalog_exists(self, catalog_name: str) -> bool:

        df = self.spark.sql("SHOW CATALOGS")

        return (
            df.filter(
                f"catalog = '{catalog_name}'"
            ).count() > 0
        )


    def show_catalogs(self):
        return self.spark.sql(
            "SHOW CATALOGS"
        )


    def schema_exists(
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
        catalog_name: str,
        schema_name: str
    ):

        return self.spark.sql(
            f"""
            SHOW TABLES IN
            {catalog_name}.{schema_name}
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

        if not self.table_exists(
            catalog_name,
            schema_name,
            old_table_name
        ):
            raise ValueError(
                f"La table "
                f"'{catalog_name}.{schema_name}.{old_table_name}' "
                f"n'existe pas."
            )

        if self.table_exists(
            catalog_name,
            schema_name,
            new_table_name
        ):
            raise ValueError(
                f"La table "
                f"'{catalog_name}.{schema_name}.{new_table_name}' "
                f"existe déjà."
            )

        self.spark.sql(
            f"""
            ALTER TABLE
            {catalog_name}.{schema_name}.{old_table_name}
            RENAME TO
            {catalog_name}.{schema_name}.{new_table_name}
            """
        )
        self.spark.catalog.refreshTable(
            f"{catalog_name}.{schema_name}.{new_table_name}"
        )

        self.logger.info(
            f"Table renommée : "
            f"{catalog_name}.{schema_name}.{old_table_name} "
            f"-> "
            f"{catalog_name}.{schema_name}.{new_table_name}"
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
        catalog_name: str,
        schema_name: str,
        table_name: str
    ):

        return self.spark.sql(
            f"""
            DESCRIBE
            {catalog_name}.{schema_name}.{table_name}
            """
        )



if __name__ == "__main__":
    from pyspark.sql import SparkSession
    logger = PipelineLogger("CatalogManager")

    catalog_manager = CatalogManager(
        spark=spark, 
        logger=logger
    )
    catalog_manager.show_catalogs().show()
    catalog_manager.show_schemas("nyc_taxi").show()
    catalog_manager.show_tables("nyc_taxi","gold").show()
    catalog_manager.describe_table_columns("nyc_taxi","audit", "audit_load").show()
    #catalog_manager.create_catalog("test_catalog")
    #catalog_manager.create_schema("test_catalog", "test_schema")
    #catalog_manager.drop_schema("test_catalog", "test_schema")
    #catalog_manager.drop_catalog("test_catalog")


