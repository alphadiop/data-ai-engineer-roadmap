import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.logger import PipelineLogger
from pyspark.sql import DataFrame

class DeltaManager:
    def __init__(self, spark, logger: PipelineLogger):
        self.spark = spark
        self.logger = logger

    def optimize(self, table_name:str):
        self.spark.sql(f"OPTIMIZE {table_name}")
        if self.logger:
            self.logger.info(f"{'=' * 12} OPTIMIZE completed {'=' * 12} ")
            self.logger.info("OPTIMIZE completed {table_name}")


    def optimize_period(self, table_name: str, periode: int):
        if self.logger:
            self.logger.info(f"{'=' * 12} OPTIMIZE period {'=' * 12} ")
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
        table_name: str,
        periode: int
    ):

        self.spark.sql(
            f"""
            DELETE FROM {table_name}
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



    def time_travel(
        self,
        table_name: str,
        version: int
    ) -> DataFrame:
        
        if self.logger:
            self.logger.info(f"{'=' * 12} Time Travel {'=' * 12} ")
        return (
            self.spark.read
            .format("delta")
            .option("versionAsOf",version)
            .table(table_name)
        )
    


if __name__ == "__main__":
    delta_manager = DeltaManager(
        spark=spark,
        logger=PipelineLogger('DeltaManager')
    )

    ## delta_manager.history("nyc_taxi.silver.silver_nyc_taxi").show()
    #delta_manager.describe_detail("nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
    # delta_manager.delete_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    delta_manager.count_period("nyc_taxi.silver.silver_nyc_taxi", 202507)
    #delta_manager.optimize_period("nyc_taxi.silver.silver_nyc_taxi",202507)
    df = delta_manager.time_travel("nyc_taxi.silver.silver_nyc_taxi", version=5)
    display(df.limit(10))
    









    