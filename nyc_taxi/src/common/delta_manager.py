import os
import sys
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union,Tuple



from nyc_taxi.src.common.logger import PipelineLogger
from pyspark.sql import DataFrame

from utils.sql_schema.build_schema import build_schema
from utils.sql_schema.get_columns_from_schema import get_columns_from_schema
from utils.load_json import load_json


class DeltaManager:
    def __init__(self, spark, logger: PipelineLogger):
        self.spark = spark
        self.logger = logger


    def create_table(self, 
                     schema_name:str,
                     table_name:str, 
                     schema:List[Tuple[str, str, str]], 
                     partition_by=None,
                     drop_table:bool = True) -> None:
        
        partition_clause = (
            f"PARTITIONED BY ({partition_by})" if partition_by else ""
        )

        exists = self.spark.catalog.tableExists(
                f"nyc_taxi.{schema_name}.{table_name}"
            )
        
        self.logger.info(f"Exists after drop = {exists}")

        if drop_table:
            self.logger.info(
                f"Dropping table nyc_taxi.{schema_name}.{table_name}"
            )
            self.drop_table(
                schema_name=schema_name, 
                table_name=table_name
            )
            
        str_schema = ", ".join(list(map(lambda tp:" ".join(tp), schema)))

        self.spark.sql(f"""
                CREATE TABLE IF NOT EXISTS nyc_taxi.{schema_name}.{table_name} 
                ({str_schema})
                USING DELTA
                {partition_clause}
              """
         )


    def drop_table(
        self,
        schema_name: str,
        table_name: str
    ):

        self.spark.sql(
            f"""
            DROP TABLE IF EXISTS
            nyc_taxi.{schema_name}.{table_name}
            """
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
    ):
        return self.spark.catalog.tableExists(
            f"nyc_taxi.{schema_name}.{table_name}"
        )
    

    def show_tables(
        self,
        schema_name: str
    ):
        return self.spark.sql(
            f"""
            SHOW TABLES IN
            nyc_taxi.{schema_name}
            """
        )


    def truncate_table(
        self,
        schema_name: str,
        table_name: str
    ):

        self.spark.sql(
            f"""
            TRUNCATE TABLE
            nyc_taxi.{schema_name}.{table_name}
            """
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



    def optimize_table(self, table_name:str):
        self.spark.sql(f"OPTIMIZE {table_name}")
        if self.logger:
            self.logger.info(f"{'=' * 12} OPTIMIZE completed {'=' * 12} ")
            self.logger.info(f"OPTIMIZE completed {table_name}")



    def optimize_period(self, table_name: str, periode: int):
        """ attention : OPTIMISER que lorsque la table est partionnée par periode
            sinon pas d'optimisation
        """

        if self.logger:
            self.logger.info(f"{'=' * 12} OPTIMIZE period {'=' * 12} ")
        
        detail = self.spark.sql(
            f"DESCRIBE DETAIL {table_name}"
        ).collect()[0]

        partition_columns = detail["partitionColumns"]

        if "periode" not in partition_columns:
            if self.logger:
                self.logger.warning(
                    f"Table {table_name} is not partitioned by period"
                    f"Partitions found: {partition_columns}"
                )
            return

        self.spark.sql(
            f"""
            OPTIMIZE {table_name}
            WHERE periode = {periode}
            """
        )

        if self.logger:
            self.logger.info(f"{'=' * 12} Optimisation {'=' * 12} ")
            self.logger.info(
                f"OPTIMIZE completed on {table_name} "
                f"for period {periode}"
            )


    def vacuum(self,table_name: str,retain_hours: int = 168):
        """ Conserver les versions des 7 derniers jours -> retention 168h """
        self.spark.sql(
            f"""
            VACUUM {table_name}
            RETAIN {retain_hours} HOURS
            """
        )
        if self.logger:
            self.logger.info(f"VACUUM completed on {table_name}")


    def vacuum_dry_run(self, table_name: str) -> DataFrame:
        return self.spark.sql(
            f"""
            VACUUM {table_name}
            DRY RUN
            """
        )

    def history(
        self,
        table_name: str
    ) -> DataFrame:

        self.logger.info(f"{'=' * 12} Historique {'=' * 12} ")
        return self.spark.sql(
            f"""
            DESCRIBE HISTORY {table_name}
            """
        )

    def describe_detail(
        self,
        table_name: str
    ) -> DataFrame:
        
        if self.logger:
            self.logger.info(f"{'=' * 12} Historique {'=' * 12} ")

        return self.spark.sql(
            f"""
            DESCRIBE DETAIL {table_name}
            """
        )


    def delete_period(
        self,
        schema_name: str,
        table_name: str,
        periode: int
    ):

        self.spark.sql(
            f"""
            DELETE FROM nyc_taxi.{schema_name}.{table_name}
            WHERE periode = {periode}
            """
        )

        if self.logger:
            self.logger.info(f"{'=' * 12} Suppression d'une période {'=' * 12} ")
            self.logger.info(f"{'=' * 120}")
            self.logger.info(
                f"Period {periode} deleted "
                f"from {table_name}"
            )


    def sauvegarde_tables_delta(
        self,
        df: DataFrame,
        schema_name: str,
        table_name: str,
        periode:int
    ):
        self.delete_period(
            schema_name = schema_name,
            table_name=table_name,
            periode=periode
        )

        (
            df.write
            .format("delta")
            .mode("append")
            .saveAsTable(
                f"nyc_taxi.{schema_name}.{table_name}"
            )
        )
        self.logger.info(
            f"Table nyc_taxi.{schema_name}.{table_name} saved"
        )



    def count_period(self,table_name: str,periode: int) -> int:
        count = (
            self.spark.sql(
                f"""
                SELECT COUNT(*) cnt
                FROM {table_name}
                WHERE periode = {periode}
                """
            )
            .collect()[0]["cnt"]
        )
        if self.logger:
            self.logger.info(f"{'=' * 12} Vérification {'=' * 12} ")
            self.logger.info(f"{'=' * 120}")
            self.logger.info(f"{table_name} -> Period {periode} has {count} records {'=' * 40}")
            self.logger.info(f"{'=' * 120}")
        return count



    def time_travel(self,table_name: str, version: int) -> DataFrame:
        if self.logger:
            self.logger.info(f"{'=' * 12} Time Travel {'=' * 12} ")
        return (
            self.spark.read
                .format("delta")
                .option("versionAsOf",version)
                .table(table_name)
            )


    def read_delta(self,table_name:str) -> DataFrame:
        return self.spark.read.format("delta").table(table_name)
    

    def write_delta(self, df: DataFrame, table_name:str):
        (
            df.write
                .format("delta")
                .mode("overwrite")
                .saveAsTable(table_name)
            )
        if self.logger:
            self.logger.info(f"{'=' * 12} Write Delta {'=' * 12} ")
            self.logger.info(f"{'=' * 120}")
            self.logger.info(f"Delta written to {table_name} {'=' * 40}")
            self.logger.info(f"{'=' * 120}")


    def read_stream(self,path_volume:str) -> DataFrame:
        path_volume = "/Volumes/nyc_taxi/bronze/raw_files/yellow"
        if self.logger:
            self.logger.info(f"{'=' * 12} Lecture Auto Loader{'=' * 12} ")
        return (
            spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format","parquet")
                .load(path_volume)
            )




    def write_stream(self, df: DataFrame, path_volume:str, table_name:str):
        ## "nyc_taxi.bronze.bronze_nyc_taxi"
        (
            df.writeStream
                .format("delta")
                .option("checkpointLocation", f"{path_volume}/_checkpoints/{table_name}")
                .trigger(availableNow=True)
                .toTable(table_name)
            )
        if self.logger:
            self.logger.info(f"{'=' * 12} Write Stream {'=' * 12} ")
            self.logger.info(f"{'=' * 120}")
            self.logger.info(f"Stream written to {table_name} {'=' * 40}")
            self.logger.info(f"{'=' * 120}")




if __name__ == "__main__":
    logger=PipelineLogger('DeltaManager')
    delta_manager = DeltaManager(
        spark=spark,
        logger=logger
    )
    path = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc/schema/yellow/audit_load.json"
    load_json = load_json(path)
    schema = build_schema(load_json)
    colums = get_columns_from_schema(schema)

    delta_manager.create_table(
        schema_name="audit",
        table_name="audit_load",
        schema=schema, 
        partition_by = None,
        drop_table=True
    ) 
    print(f"schema : {schema} \n")
    print(f"colums : {colums} \n ")



    ## delta_manager.history("nyc_taxi.silver.silver_nyc_taxi").show()
    #delta_manager.describe_detail("nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
    # delta_manager.delete_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    #delta_manager.count_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    #delta_manager.optimize_period("nyc_taxi.silver.silver_nyc_taxi",202507)
    #df = delta_manager.time_travel("nyc_taxi.silver.silver_nyc_taxi", version=5)
    #display(df.limit(10))
    









    