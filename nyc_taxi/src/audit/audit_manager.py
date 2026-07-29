import os
import sys
import uuid
from pyspark.sql import DataFrame
from nyc_taxi.src.common.pipeline_step import PipelineStep
from decimal import Decimal
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.decorators import log_execution
from pyspark.sql.functions import max as spark_max

from pyspark.sql.functions import col
from datetime import datetime

from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    IntegerType,
    StringType,
    TimestampType,
    DecimalType
)

class AuditManager:
    def __init__(self, spark, logger:PipelineLogger):
        self.spark = spark
        self.logger = logger


    def is_period_loaded(self,context):
        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )
        audit_table = catalog_manager.audit_load()

        self.logger.info(f"audit_table : {audit_table}")

        if not self.spark.catalog.tableExists(audit_table):
            return False

        query = f"""
            SELECT COUNT(*) as cnt
            FROM {audit_table}
            WHERE table_name = '{context.table_name}'
            AND taxi_type = '{context.taxi_type}'
            AND periode = {context.periode}
            AND status = 'SUCCESS'
        """
        result = self.spark.sql(query).collect()[0]["cnt"]
        return result > 0
    
        ## context.run_id = str(uuid.uuid4())

    def insert_audit(self, context):
        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )
        audit_table = catalog_manager.audit_load()

        data = [(
            context.run_id,
            int(context.periode),
            context.table_name,
            context.taxi_type,
            context.status,
            context.start_time,
            context.end_time,
            Decimal(str(context.duration_seconds))
            if context.duration_seconds is not None
            else None,
            context.error_step,
            context.message
        )]

        schema = StructType([
            StructField("run_id", LongType(), False),
            StructField("periode", IntegerType(), False),
            StructField("table_name", StringType(), False),
            StructField("taxi_type", StringType(), False),
            StructField("status", StringType(), False),
            StructField("start_time", TimestampType(), False),
            StructField("end_time", TimestampType(), False),
            StructField("duration_seconds", DecimalType(18, 2), True),
            StructField("error_step", StringType(), True),
            StructField("message", StringType(), True)
        ])

        df_audit = self.spark.createDataFrame(
            data=data,
            schema=schema
        )

        (
        df_audit.write
            .format("delta")
            .mode("append")
            .saveAsTable(audit_table)
        )


    ## table audit : nyc_taxi.audit.audit_load
    @log_execution
    def delete_period(
        self,
        catalog_name,
        schema_name,
        table_name,
        periode
    ):
        self.spark.sql(
        f"""
            DELETE FROM {catalog_name}.{schema_name}.{table_name}
            WHERE periode = {periode}
        """
        )
        self.logger.info(
            f"Deleting period {periode} "
            f"from {catalog_name}.{schema_name}.{table_name}"
        )
        

    def insert_row_counts(self, context):
        data = []
        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )
        audit_row_table = catalog_manager.audit_row_count()
        for table_name, row_count in context.row_count.items():
            self.logger.info(
                f"Inserting row count for {table_name} with {row_count} rows"
            )
            data.append(
                (
                    context.run_id,
                    int(context.periode),
                    table_name,
                    int(row_count),
                    datetime.now()
                )
            )

        schema = StructType([
            StructField("run_id", LongType(), False),
            StructField("periode", IntegerType(), False),
            StructField("table_name", StringType(), False),
            StructField("row_count", LongType(), False),
            StructField("created_at", TimestampType(), False),
        ])

        df = self.spark.createDataFrame(
            data,
            schema=schema
        )

        (
            df.write
            .format("delta")
            .mode("append")
            .saveAsTable(audit_row_table)
        )

    def get_next_period(self,table_name:str,taxi_type:str) -> int:
        try:
            row = (
                self.spark.table("nyc_taxi.audit.audit_load")
                    .filter(col("table_name") == table_name)
                    .filter(col("taxi_type") == taxi_type)
                    .filter(col("status") == "SUCCESS")
                    .select(spark_max("periode").alias("periode"))
                    .first()["periode"]
                    )

            max_period = row["periode"] if row else None

            if max_period is None:
                return 202401

            year = max_period // 100
            month = max_period % 100

            if month == 12:
                return (year + 1) * 100 + 1

            return year * 100 + (month + 1)

        except Exception:
            # Première exécution du projet
            return 202401

if __name__ == "__main__":
    logger = PipelineLogger("uber_pipeline")
    audit_manager = AuditManager(
        spark=spark,
        logger=logger
    )
    logger.info(f"Periode choisie : {audit_manager.get_next_period()}")


    