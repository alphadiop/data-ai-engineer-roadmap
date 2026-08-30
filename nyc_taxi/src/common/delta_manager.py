import os
import sys
from nyc_taxi.src.utils.sql_schema.build_schema import build_schema
from nyc_taxi.src.utils.sql_schema.get_columns_from_schema import get_columns_from_schema
from nyc_taxi.src.utils.load_json import load_json

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union,Tuple
import shutil
from pathlib import Path
from nyc_taxi.src.common.logger import PipelineLogger
from pyspark.sql import DataFrame


from nyc_taxi.src.common.spark_manager import SparkManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

class DeltaManager:

    def __init__(self, spark, catalog_manager, logger: PipelineLogger):
        self.spark = spark
        self.catalog_manager = catalog_manager
        self.logger = logger
        self.nombre_partition = 8


    def create_table(
            self,
            schema_name: str,
            table_name: str,
            schema: list[tuple[str, str, str]],
            partition_by: str | None = None,
            drop_table: bool = False
    ) -> None:

        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )

        exists = self.spark.catalog.tableExists(
            full_table_name
        )

        self.logger.info(
            f"Table exists {full_table_name} = {exists}"
        )

        if exists and not drop_table:

            self.logger.info(
                f"Table already exists : {full_table_name}"
            )
            return

        if drop_table and exists:

            self.logger.info(
                f"Dropping table : {full_table_name}"
            )

            self.drop_table(
                schema_name=schema_name,
                table_name=table_name
            )

        columns_sql = ",\n".join(
            [
                " ".join(
                    filter(
                        None,
                        column
                    )
                )
                for column in schema
            ]
        )

        partition_clause = ""

        if partition_by:
            partition_clause = (
                f"PARTITIONED BY ({partition_by})"
            )

        ddl = f"""
        CREATE TABLE IF NOT EXISTS {full_table_name}
        (
            {columns_sql}
        )
        USING DELTA
        {partition_clause}
        """

        self.logger.info(
            f"Creating table : {full_table_name}"
        )

        self.logger.info(ddl)

        self.spark.sql(ddl)

        self.logger.info(
            f"Table created : {full_table_name}"
        )



    def create_table2(
            self,
            schema_name: str,
            table_name: str,
            schema: List[Tuple[str, str, str]],
            partition_by=None,
            drop_table: bool = True
    ) -> None:

        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )

        partition_clause = (
            f"PARTITIONED BY ({partition_by})"
            if partition_by
            else ""
        )

        exists = self.spark.catalog.tableExists(
            full_table_name
        )
        self.logger.info(
            f"Table exists {full_table_name} = {exists}"
        )

        if drop_table:
            self.logger.info(
                f"Dropping table {full_table_name}"
            )

            self.drop_table(
                schema_name=schema_name,
                table_name=table_name
            )

        str_schema = ", ".join(
            [
                " ".join(tp)
                for tp in schema
            ]
        )

        self.spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {full_table_name}
            (
                {str_schema}
            )
            USING DELTA
            {partition_clause}
            """
        )

        self.logger.info(
            f"Table created : {full_table_name}"
        )



    def drop_table(
            self,
            schema_name,
            table_name,
            delete_files=True
    ):
        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )
        self.spark.sql(
            f"DROP TABLE IF EXISTS {full_table_name}"
        )
        if (self.catalog_manager.env == "local" and delete_files):

            warehouse_dir = self.spark.conf.get(
                "spark.sql.warehouse.dir"
            )

            warehouse_path = (
                    Path(warehouse_dir)
                    / f"{schema_name}.db"
                    / table_name
            )

            if warehouse_path.exists():

                self.logger.info(
                    f"Deleting {warehouse_path}"
                )
                shutil.rmtree(
                    warehouse_path
                )


    def rename_table(
        self,
        schema_name: str,
        old_name: str,
        new_name: str
    ):

        self.spark.sql(
            f"""
            ALTER TABLE
            nyc_taxi.{schema_name}.{old_name}
            RENAME TO
            nyc_taxi.{schema_name}.{new_name}
            """
        )

    def table_exists(
            self,
            schema_name: str,
            table_name: str
    ) -> bool:

        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )

        return self.spark.catalog.tableExists(
            full_table_name
        )


    def show_tables(
            self,
            schema_name: str):

        schema_full_name = self.catalog_manager.get_schema_name(
            schema_name
        )

        return self.spark.sql(
            f"""
            SHOW TABLES IN
            {schema_full_name}
            """
        )


    def truncate_table(
            self,
            schema_name: str,
            table_name: str
    ):
        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )
        self.spark.sql(
            f"""
            TRUNCATE TABLE
            {full_table_name}
            """
        )
        if self.logger:
            self.logger.info(
                f"Table truncated : {full_table_name}"
            )


    def restore_version(
        self,
        table_name: str,
        version: int
    ):
        self.spark.sql(
            f"""
            RESTORE TABLE {table_name}
            TO VERSION AS OF {version}
            """
        )


    def optimize_table(
            self,
            schema_name:str,
            table_name:str
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )
        self.spark.sql(
            f"""
            OPTIMIZE {full_table_name}
            """
        )

    def optimize_period(
            self,
            schema_name: str,
            table_name: str,
            periode: int
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        detail = self.spark.sql(
            f"""
            DESCRIBE DETAIL {full_table_name}
            """
        ).collect()[0]
        partition_columns = detail["partitionColumns"]
        if "periode" in partition_columns:

            self.spark.sql(
                f"""
                OPTIMIZE {full_table_name}
                WHERE periode = {periode}
                """
            )
        else:
            self.spark.sql(
                f"""
                OPTIMIZE {full_table_name}
                """
            )


    def vacuum(
            self,
            schema_name: str,
            table_name: str,
            retain_hours: int = 168
    ):
        try:
            full_table_name = (
                self.catalog_manager.get_table_name(
                    schema_name,
                    table_name
                )
            )
            self.spark.sql(
                f"""
                VACUUM {full_table_name}
                RETAIN {retain_hours} HOURS
                """
            )
            if self.logger:
                self.logger.info(
                    f"VACUUM completed on {full_table_name}"
                )
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Vacuum failed on {table_name} : {e}"
                )
            raise

    def vacuum_dry_run(
            self,
            schema_name: str,
            table_name: str
    ):

        full_table_name = self.catalog_manager.get_table_name(
            schema_name,
            table_name
        )

        self.logger.info(
            f"VACUUM DRY RUN on {full_table_name}"
        )

        return self.spark.sql(
            f"""
            VACUUM {full_table_name}
            DRY RUN
            """
        )


    def history(
            self,
            schema_name: str,
            table_name: str
    ) -> DataFrame:

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Historique {full_table_name} {'=' * 12}"
            )

        return self.spark.sql(
            f"""
            DESCRIBE HISTORY {full_table_name}
            """
        )


    def describe_detail(
            self,
            schema_name: str,
            table_name: str
    ) -> DataFrame:

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Detail {full_table_name} {'=' * 12}"
            )

        return self.spark.sql(
            f"""
            DESCRIBE DETAIL {full_table_name}
            """
        )



    def delete_period(
            self,
            schema_name: str,
            table_name: str,
            periode: int):

        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )

        self.spark.sql(
            f"""
            DELETE FROM {full_table_name}
            WHERE periode = {periode}
            """
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Suppression d'une période {'=' * 12}"
            )
            self.logger.info(
                f"Period {periode} deleted from {full_table_name}"
            )

    def sauvegarde_tables_delta(
        self,
        df: DataFrame,
        schema_name: str,
        table_name: str,
        periode:int,
        replace:bool=False
    ):
        full_table_name = self.catalog_manager.get_table_name(
            schema_name=schema_name,
            table_name=table_name
        )
        self.logger.info(
            f"Table TO SAVE : {full_table_name}"
        )

        if replace:
            (
                df.write
                .format("delta")
                .mode("overwrite")
                .option("replaceWhere", f"periode = {periode}")
                .saveAsTable(full_table_name)
            )
            self.logger.info(
                f"Table {full_table_name} replaced"
            )

        else:
            (
            df.coalesce(self.nombre_partition)
                .write
                .format("delta")
                .mode("append")
                .saveAsTable(full_table_name)
            )
            self.logger.info(
                f"Table {full_table_name} saved"
            )


    def count_period(
            self,
            schema_name: str,
            table_name: str,
            periode: int
    ) -> int:

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        count = (
            self.spark.sql(
                f"""
                SELECT COUNT(*) cnt
                FROM {full_table_name}
                WHERE periode = {periode}
                """
            )
            .collect()[0]["cnt"]
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Vérification {'=' * 12}"
            )
            self.logger.info(
                f"{full_table_name} -> "
                f"Period {periode} has {count} records"
            )

        return count



    def time_travel(
            self,
            schema_name: str,
            table_name: str,
            version: int
    ) -> DataFrame:

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Time Travel {full_table_name} {'=' * 12}"
            )

        return (
            self.spark.read
            .format("delta")
            .option(
                "versionAsOf",
                version
            )
            .table(full_table_name)
        )

    def read_delta(
            self,
            schema_name: str,
            table_name: str
    ) -> DataFrame:

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        if self.logger:
            self.logger.info(
                f"Reading Delta table {full_table_name}"
            )

        return (
            self.spark.read
            .format("delta")
            .table(full_table_name)
        )

    def write_delta(
            self,
            df: DataFrame,
            schema_name: str,
            table_name: str,
            mode: str = "overwrite"
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        (
            df.write
            .format("delta")
            .mode(mode)
            .saveAsTable(full_table_name)
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Write Delta {'=' * 12}"
            )
            self.logger.info(
                f"Delta written to {full_table_name}"
            )


    def read_stream(self) -> DataFrame:
        path_volume = "/Volumes/nyc_taxi/bronze/raw_files/yellow"
        if self.logger:
            self.logger.info(f"{'=' * 12} Lecture Auto Loader{'=' * 12} ")
        return (
            self.spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format","parquet")
                .load(path_volume)
            )


    def write_stream(
            self,
            df: DataFrame,
            path_volume: str,
            schema_name: str,
            table_name: str
    ):

        full_table_name = (
            self.catalog_manager.get_table_name(
                schema_name,
                table_name
            )
        )

        checkpoint_path = (
            f"{path_volume}/_checkpoints/{table_name}"
        )

        (
            df.writeStream
            .format("delta")
            .option(
                "checkpointLocation",
                checkpoint_path
            )
            .trigger(
                availableNow=True
            )
            .toTable(
                full_table_name
            )
        )

        if self.logger:
            self.logger.info(
                f"{'=' * 12} Write Stream {'=' * 12}"
            )
            self.logger.info(
                f"Stream written to {full_table_name}"
            )

    def register_table(
            self,
            schema_name: str,
            table_name: str,
            location: str
    ):

        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS
            {schema_name}.{table_name}
            USING DELTA
            LOCATION '{location}'
        """)


if __name__ == "__main__":
    from pyspark.sql import SparkSession
    import sys
    import os

    from nyc_taxi.src.common.catalog_manager import CatalogManager
    logger=PipelineLogger('DeltaManager')

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    )
    spark = spark_manager.get_spark()

    catalog_manager = CatalogManager(
        spark=spark,
        logger=logger
    )
    delta_manager = DeltaManager(
        spark=spark,
        catalog_manager = catalog_manager,
        logger=logger
    )

    full_table_name = catalog_manager.get_table_name(
        schema_name="silver",
        table_name='silver_nyc_taxi'
    )

    logger.info(
        f"CREATE TABLE TARGET = {full_table_name}"
    )

    for schema_name in ["audit", "silver", "gold"]:
        catalog_manager.create_schema(
            schema_name=schema_name,
            env='local'
        )
    logger.info(
        spark.conf.get(
            "spark.sql.warehouse.dir"
        )
    )
    spark.sql("SHOW DATABASES").show(truncate=False)

    warehouse = (
        spark.conf.get("spark.sql.warehouse.dir")
        .replace("file:/", "")
    )

    for root, dirs, files in os.walk(warehouse):
        print(root)

    spark.sql("SHOW TABLES IN audit").show()
    spark.sql("SHOW TABLES IN gold").show()
    spark.sql("SHOW TABLES IN silver").show()

    warehouse = Path(
        "D:/data-ai-engineer-roadmap/nyc_taxi/src/common/spark-warehouse"
    )

    for db in warehouse.iterdir():
        print("\n", db)

        if db.is_dir():
            for child in db.iterdir():
                print("   ", child.name)

    spark.conf.get("spark.sql.warehouse.dir")

    tab = "gold.gold_kpi_daily"
    spark.sql("SHOW TABLES IN gold").show()

    if spark.catalog.tableExists(tab):
        df = spark.read.table(tab)
        df.show()
    else:
        print(f"Table {tab} inexistante")
    # df = spark.read.table(tab)
    # print(df.count())
    #spark.sql("DESCRIBE DETAIL audit.audit_load").show(truncate=False)
    #spark.sql("CREATE DATABASE IF NOT EXISTS audit")
    #spark.sql("CREATE DATABASE IF NOT EXISTS silver")
    #spark.sql("CREATE DATABASE IF NOT EXISTS gold")
    #spark.sql("SHOW DATABASES").show(truncate=False)


    # path = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc/schema/yellow/audit_load.json"
    # load_json = load_json(path)
    # schema = build_schema(load_json)
    # colums = get_columns_from_schema(schema)
    #
    # delta_manager.create_table(
    #     schema_name="audit",
    #     table_name="audit_load",
    #     schema=schema,
    #     partition_by = None,
    #     drop_table=True
    # )
    # print(f"schema : {schema} \n")
    # print(f"colums : {colums} \n ")



    ## delta_manager.history("nyc_taxi.silver.silver_nyc_taxi").show()
    #delta_manager.describe_detail("nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
    # delta_manager.delete_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    #delta_manager.count_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    #delta_manager.optimize_period("nyc_taxi.silver.silver_nyc_taxi",202507)
    #df = delta_manager.time_travel("nyc_taxi.silver.silver_nyc_taxi", version=5)
    #display(df.limit(10))
    









    