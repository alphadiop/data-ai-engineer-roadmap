from nyc_taxi.src.common.catalog_manager import CatalogManager

from pyspark.sql import Row
import logging
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

class MetadataExplorer:

    def __init__(
            self,
            spark,
            env="local",
            logger=None
    ):
        self.spark = spark
        self.env = env
        self.logger = logger

        self.catalog_manager = CatalogManager(
            spark=spark,
            env=env,
            logger=logger
        )
        #self.catalog_manager.repair_local_metastore()

    def run(self):
        if self.env == "local":
            self.show_local()
        else:
            self.show_databricks()


    def show_local(self):

        print("\n" + "=" * 100)
        print("DATABASES")
        print("=" * 100)

        databases = self.spark.sql(
            "SHOW DATABASES"
        )

        databases.show(truncate=False)

        for row in databases.collect():

            schema_name = row.namespace

            self.logger.info("\n" + "=" * 100)
            self.logger.info(f"SCHEMA : {schema_name}")
            self.logger.info("=" * 100)

            self.spark.sql(
                f"SHOW TABLES IN {schema_name}"
            ).show(truncate=False)


    def show_databricks(self):

        self.logger.info("\n" + "=" * 100)
        self.logger.info("CATALOGS")
        self.logger.info("=" * 100)

        catalogs = self.spark.sql(
            "SHOW CATALOGS"
        )

        catalogs.show(truncate=False)

        for catalog in catalogs.collect():

            catalog_name = catalog.catalog

            print("\n" + "=" * 100)
            print(f"CATALOG : {catalog_name}")
            print("=" * 100)

            schemas = self.spark.sql(
                f"SHOW SCHEMAS IN {catalog_name}"
            )

            schemas.show(truncate=False)

            for schema in schemas.collect():

                schema_name = schema.databaseName

                self.logger.info("\n" + "-" * 100)
                self.logger.info(
                    f"{catalog_name}.{schema_name}"
                )
                self.logger.info("-" * 100)

                self.spark.sql(
                    f"SHOW TABLES IN {catalog_name}.{schema_name}"
                ).show(truncate=False)

    def show_table_details(
            self,
            schema_name,
            table_name
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name=schema_name,
                table_name=table_name
            )
        )

        self.logger.info("\n" + "=" * 100)
        self.logger.info(full_table_name)
        self.logger.info("=" * 100)

        self.spark.sql(
            f"DESCRIBE TABLE {full_table_name}"
        ).show(truncate=False)

    def show_row_count(
            self,
            schema_name,
            table_name
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name=schema_name,
                table_name=table_name
            )
        )

        count = (
            self.spark.table(
                full_table_name
            ).count()
        )

        self.logger.info(
            f"{full_table_name} : {count:,} rows"
        )


    def get_all_row_counts3(self):
        """
        Retourne le nombre de lignes de toutes les tables
        présentes dans les schémas de l'environnement.

        Attention :
        - count() déclenche une lecture complète de la table.
        - Cette méthode peut donc être coûteuse sur de grosses tables.
        - Elle est destinée principalement au diagnostic local.
        """

        rows = []

        schemas = [
            "audit",
            "silver",
            "gold",
            "ref"
        ]

        for schema_name in schemas:

            try:
                tables = self.spark.sql(
                    f"SHOW TABLES IN {schema_name}"
                ).collect()

            except Exception as e:

                if self.logger:
                    self.logger.warning(
                        f"Impossible de lire le schéma "
                        f"{schema_name} : {e}"
                    )

                continue

            for table in tables:

                table_name = table.tableName

                full_table_name = (
                    self.catalog_manager.get_table_name(
                        schema_name=schema_name,
                        table_name=table_name
                    )
                )

                if self.logger:
                    self.logger.info(
                        f"Calcul row count : {full_table_name}"
                    )

                try:
                    row_count = (
                        self.spark
                        .table(full_table_name)
                        .count()
                    )

                    rows.append(
                        Row(
                            schema_name=schema_name,
                            table_name=table_name,
                            row_count=row_count,
                            status="OK"
                        )
                    )

                except Exception as e:

                    if self.logger:
                        self.logger.error(
                            f"Erreur count {full_table_name} : {e}"
                        )

                    rows.append(
                        Row(
                            schema_name=schema_name,
                            table_name=table_name,
                            row_count=None,
                            status="ERROR"
                        )
                    )
        return self.spark.createDataFrame(rows)


    def get_real_row_counts(self):
        """
        garder get_real_row_counts() uniquement comme outil de contrôle qualité permettant de comparer :

        """
        rows = []
        schemas = [
            "audit",
            "silver",
            "gold",
            "ref"
        ]

        for schema_name in schemas:
            tables = self.spark.sql(
                f"SHOW TABLES IN {schema_name}"
            ).collect()

            for table in tables:
                table_name = table.tableName

                full_table_name = (
                    self.catalog_manager.get_table_name(
                        schema_name=schema_name,
                        table_name=table_name
                    )
                )

                self.logger.info(
                    f"COUNT(*) : {full_table_name}"
                )

                count = (
                    self.spark
                    .table(full_table_name)
                    .count()
                )

                rows.append(
                    Row(
                        schema_name=schema_name,
                        table_name=table_name,
                        row_count=count
                    )
                )

        return self.spark.createDataFrame(rows)



    def get_all_row_counts(self):
        return (
            self.spark.table("audit.audit_row_count")
            .orderBy(
                "periode",
                "table_name"
            )
        )

    def show_all_row_counts(self):
        df = self.get_all_row_counts()
        df.show(
            truncate=False
        )
        return df

