import os
import sys



from nyc_taxi.src.common.logger import PipelineLogger 



class CatalogManager:
    """ 
    un catalog sert à isoler et organiser les données dans un espace de travail
    le schema est un sous dossier du catalog, il contient des :
    """

    def __init__(self, spark, logger: PipelineLogger):
        self.spark = spark
        self.logger = logger

    # ============================================================================
    # ============Catalogs========================================================
    # ============================================================================

    def create_catalog(self, catalog_name: str):

        self.spark.sql(
            f"CREATE CATALOG IF NOT EXISTS {catalog_name}"
        )

        self.logger.info(
            f"Catalog {catalog_name} created"
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

    def rename_schema(
        self,
        catalog_name: str,
        old_schema: str,
        new_schema: str
    ):

        self.spark.sql(
            f"""
            ALTER SCHEMA
            {catalog_name}.{old_schema}
            RENAME TO {catalog_name}.{new_schema}
            """
        )

        self.logger.info(
            f"Schema {old_schema} renamed to {new_schema}"
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

        return self.spark.catalog.tableExists(
            f"{catalog_name}.{schema_name}.{table_name}"
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

        return self.spark.sql(
            f"""
            DESCRIBE DETAIL
            {catalog_name}.{schema_name}.{table_name}
            """
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


