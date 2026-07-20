import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/src"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import uuid


from common.pipeline_step import PipelineStep
from common.logger import PipelineLogger
from common.decorators import log_execution


from pyspark.sql.functions import col
from datetime import datetime


class AuditManager:
    def __init__(self, spark, logger:PipelineLogger):
        self.spark = spark
        self.logger = logger

    def is_period_loaded(self,context):
        if not self.spark.catalog.tableExists("nyc_taxi.audit.audit_load"):
            return False

        query = f"""
            SELECT COUNT(*) as cnt
            FROM nyc_taxi.audit.audit_load
            WHERE table_name = '{context.table_name}'
            AND taxi_type = '{context.taxi_type}'
            AND periode = {context.periode}
            AND status = 'SUCCESS'
        """
        result = self.spark.sql(query).collect()[0]["cnt"]
        return result > 0
    
        ## context.run_id = str(uuid.uuid4())

    def insert_audit(self, context):
        data = [(
            context.run_id,
            int(context.periode),
            context.table_name,
            context.taxi_type,
            context.status,
            context.start_time,
            context.end_time,
            context.duration_seconds,
            context.error_step,
            context.message
        )]

        df = self.spark.createDataFrame(
            data,
            schema=[
                "run_id",
                "periode",
                "table_name",
                "taxi_type",
                "status",
                "start_time",
                "end_time",
                "duration_seconds",
                "error_step",
                "message"
            ]
        )

        (
        df.write
            .format("delta")
            .mode("append")
            .saveAsTable("nyc_taxi.audit.audit_load")
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
        for table_name, row_count in context.row_count.items():

            data.append(
                (
                    context.run_id,
                    int(context.periode),
                    table_name,
                    int(row_count),
                    datetime.now()
                )
            )

        df = self.spark.createDataFrame(
            data,
            schema=[
                "run_id",
                "periode",
                "table_name",
                "row_count",
                "created_at"
            ]
        )

        (
            df.write
            .format("delta")
            .mode("append")
            .saveAsTable("nyc_taxi.audit.audit_row_count")
        )