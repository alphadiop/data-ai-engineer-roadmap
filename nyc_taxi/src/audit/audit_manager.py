

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
        self.logger.info(
            f"DEBUG context.env = {context.env}"
        )
        audit_table = catalog_manager.audit_load()

        self.logger.info(f"audit_table : {audit_table}")

        if not self.spark.catalog.tableExists(audit_table):
            return False

        self.logger.info(
            f"Tables disponibles dans le catalogue : "
            f"{self.spark.catalog.listTables()}"
        )

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

        ## transforme explicitement les valeurs avant de les donner à Spark
        run_id = int(context.run_id)
        periode = int(context.periode)

        table_name = str(context.table_name)
        taxi_type = str(context.taxi_type)
        status = str(context.status)

        start_time = context.start_time
        end_time = context.end_time

        duration_seconds = (
            Decimal(str(round(float(context.duration_seconds),2)))
            if context.duration_seconds is not None
            else None
        )

        error_step = (
            str(context.error_step)
            if context.error_step is not None
            else None
        )

        message = (
            str(context.message)
            if context.message is not None
            else None
        )

        self.logger.info(
            f"AUDIT | run_id={run_id} | periode={periode} | "
            f"table={table_name} | taxi_type={taxi_type} | "
            f"status={status}"
        )

        data = [(
            run_id,
            periode,
            table_name,
            taxi_type,
            status,
            start_time,
            end_time,
            duration_seconds,
            error_step,
            message
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

        # print("================================")
        # print("AUDIT DEBUG")
        # print("================================")
        # print("run_id       :", repr(context.run_id), type(context.run_id))
        # print("periode      :", repr(context.periode), type(context.periode))
        # print("table_name   :", repr(context.table_name), type(context.table_name))
        # print("taxi_type    :", repr(context.taxi_type), type(context.taxi_type))
        # print("status       :", repr(context.status), type(context.status))
        # print("start_time   :", repr(context.start_time), type(context.start_time))
        # print("end_time     :", repr(context.end_time), type(context.end_time))
        # print("duration     :", repr(context.duration_seconds), type(context.duration_seconds))
        # print("error_step   :", repr(context.error_step), type(context.error_step))
        # print("message      :", repr(context.message), type(context.message))
        # print("================================")

        df_audit = self.spark.createDataFrame(
            data=data,
            schema=schema
        )

        self.logger.info(f"audit_table = {audit_table}")
        ## df_audit.printSchema()
        df_audit.show(truncate=False)

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

        run_id = int(context.run_id)
        periode = int(context.periode)

        for table_name, row_count in context.row_count.items():
            self.logger.info(
                f"Inserting row count for "
                f"{table_name} with {row_count} rows"
            )
            data.append(
                (
                    run_id,
                    periode,
                    str(table_name),
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

        df.show(truncate=False)

        (
            df.write
            .format("delta")
            .mode("append")
            .saveAsTable(audit_row_table)
        )

    def get_next_period(
            self,
            table_name: str,
            taxi_type: str,
            env:str='local'
    ) -> int:

        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=env
        )
        audit_table = catalog_manager.audit_load()

        self.logger.info(
            f"audit_table  : {audit_table}"
        )

        try:

            row = (
                self.spark.table(audit_table)
                .filter(col("table_name") == table_name)
                .filter(col("taxi_type") == taxi_type)
                .filter(col("status") == "SUCCESS")
                .select(spark_max("periode").alias("periode"))
                .first()
            )

            max_period = row["periode"] if row else None

            if max_period is None:
                self.logger.info(
                    "Aucune période SUCCESS trouvée -> 202401"
                )
                return 202501

            year = max_period // 100
            month = max_period % 100

            if month == 12:
                next_period = (year + 1) * 100 + 1
            else:
                next_period = year * 100 + (month + 1)

            self.logger.info(
                f"Dernière période : {max_period} "
                f"-> prochaine période : {next_period}"
            )
            return next_period

        except Exception as e:

            self.logger.warning(
                f"Impossible de lire {audit_table}: {e}"
            )

            return 202501


if __name__ == "__main__":
    logger = PipelineLogger("uber_pipeline", env='local')
    # audit_manager = AuditManager(
    #     spark=spark,
    #     logger=logger
    # )
    # periode = audit_manager.get_next_period(
    #     table_name=context.table_name,
    #     taxi_type=context.taxi_type,
    #     env=context.env
    # )
    # logger.info(f"Periode choisie : {audit_manager.get_next_period()}")


    