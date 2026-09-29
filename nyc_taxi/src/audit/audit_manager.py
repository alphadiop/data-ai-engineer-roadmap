from decimal import Decimal
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.decorators import log_execution
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import col
from datetime import datetime

from nyc_taxi.src.common.pipeline_context import PipelineContext


class AuditManager:

    def __init__(self, spark, logger: PipelineLogger):
        self.spark = spark
        self.logger = logger

    def is_period_loaded(self, context: 'PipelineContext'):

        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )

        audit_table = catalog_manager.audit_load()

        self.logger.separator("AUDIT PERIOD CHECK")
        self.logger.metric("Audit table", audit_table)
        self.logger.metric("Period", context.periode)
        self.logger.metric("Table", context.table_name)
        self.logger.metric("Taxi type", context.taxi_type)

        if not self.spark.catalog.tableExists(audit_table):
            self.logger.info(
                f"Audit table inexistante : {audit_table}"
            )
            self.logger.info(
                "Aucune période chargée précédemment"
            )
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

        if result > 0:
            self.logger.success(
                f"Période {context.periode} déjà chargée"
            )
            return True

        self.logger.info(
            f"Période {context.periode} non trouvée dans l'audit"
        )

        return False

    def insert_audit(self, context):

        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )

        audit_table = catalog_manager.audit_load()

        run_id = int(context.run_id)
        periode = int(context.periode)

        table_name = str(context.table_name)
        taxi_type = str(context.taxi_type)
        status = str(context.status)

        start_time = context.start_time
        end_time = context.end_time

        duration_seconds = (
            Decimal(str(round(float(context.duration_seconds), 2)))
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

        self.logger.separator("AUDIT INSERT")
        self.logger.metric("Run ID", run_id)
        self.logger.metric("Period", periode)
        self.logger.metric("Table", table_name)
        self.logger.metric("Taxi type", taxi_type)
        self.logger.metric("Status", status)
        self.logger.metric("Audit table", audit_table)

        query = f"""
        SELECT
            CAST({context.run_id} AS BIGINT)                        AS run_id,
            CAST({context.periode} AS INT)                          AS periode,
            CAST('{context.table_name}' AS STRING)                  AS table_name,
            CAST('{context.taxi_type}' AS STRING)                   AS taxi_type,
            CAST('{context.status}' AS STRING)                      AS status,
            CAST('{context.start_time}' AS TIMESTAMP)               AS start_time,
            CAST('{context.end_time}' AS TIMESTAMP)                 AS end_time,
            CAST({context.duration_seconds} AS DECIMAL(18,2))       AS duration_seconds,
            CAST('{error_step}' AS STRING)                          AS error_step,
            CAST('{message}' AS STRING)                             AS message
        """

        df_audit = self.spark.sql(query)

        (
            df_audit.write
            .format("delta")
            .mode("append")
            .saveAsTable(audit_table)
        )

        self.logger.success(
            f"Audit enregistré dans {audit_table}"
        )

    @log_execution
    def delete_period(
        self,
        table_name,
        periode
    ):

        self.logger.info(
            f"Suppression de la période {periode} "
            f"dans {table_name}"
        )

        self.spark.sql(
            f"""
                DELETE FROM {table_name}
                WHERE periode = {periode}
            """
        )

        self.logger.success(
            f"Période {periode} supprimée de {table_name}"
        )

    def insert_row_counts(self, context):

        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=context.env
        )

        audit_row_table = catalog_manager.audit_row_count()

        run_id = int(context.run_id)
        periode = int(context.periode)

        self.logger.separator("AUDIT ROW COUNTS")
        self.logger.metric("Audit table", audit_row_table)
        self.logger.metric("Run ID", run_id)
        self.logger.metric("Period", periode)

        for table_name, row_count in context.row_count.items():

            self.logger.metric(
                table_name,
                f"{row_count:,}".replace(",", " ")
            )

            table_name_sql = str(table_name).replace("'", "''")
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            query = f"""
                INSERT INTO {audit_row_table}
                (
                    run_id,
                    periode,
                    table_name,
                    row_count,
                    created_at
                )
                VALUES
                (
                    CAST({run_id} AS BIGINT),
                    CAST({periode} AS INT),
                    '{table_name_sql}',
                    CAST({int(row_count)} AS BIGINT),
                    CAST('{created_at}' AS TIMESTAMP)
                )
            """

            self.spark.sql(query)

        self.logger.success(
            "Row counts enregistrés dans l'audit"
        )

    def get_next_period(
            self,
            table_name: str,
            taxi_type: str,
            env: str = 'local'
    ) -> int:

        catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=env
        )

        audit_table = catalog_manager.audit_load()

        self.logger.separator("NEXT PERIOD")
        self.logger.metric("Audit table", audit_table)
        self.logger.metric("Table", table_name)
        self.logger.metric("Taxi type", taxi_type)

        try:

            row = (
                self.spark.table(audit_table)
                .filter(col("table_name") == table_name)
                .filter(col("taxi_type") == taxi_type)
                .filter(col("status") == "SUCCESS")
                .select(
                    spark_max("periode").alias("periode")
                )
                .first()
            )

            max_period = row["periode"] if row else None

            if max_period is None:
                self.logger.info(
                    "Aucune période SUCCESS trouvée -> 202501"
                )
                return 202501

            year = max_period // 100
            month = max_period % 100

            if month == 12:
                next_period = (year + 1) * 100 + 1
            else:
                next_period = year * 100 + (month + 1)

            self.logger.metric(
                "Dernière période",
                max_period
            )
            self.logger.metric(
                "Prochaine période",
                next_period
            )

            return next_period

        except Exception as e:

            self.logger.warning(
                f"Impossible de lire {audit_table}: {e}"
            )

            return 202501


if __name__ == "__main__":
    logger = PipelineLogger(
        "uber_pipeline",
        env='local'
    )




# from decimal import Decimal
# from nyc_taxi.src.common.logger import PipelineLogger
# from nyc_taxi.src.common.catalog_manager import CatalogManager
# from nyc_taxi.src.common.decorators import log_execution
# from pyspark.sql.functions import max as spark_max
#
# from pyspark.sql.functions import col
# from datetime import datetime
#
#
#
# from nyc_taxi.src.common.pipeline_context import PipelineContext
# class AuditManager:
#
#     def __init__(self, spark, logger:PipelineLogger):
#         self.spark = spark
#         self.logger = logger
#
#     def is_period_loaded(self,context:'PipelineContext'):
#         catalog_manager = CatalogManager(
#             spark=self.spark,
#             logger=self.logger,
#             env=context.env
#         )
#
#         audit_table = catalog_manager.audit_load()
#
#         self.logger.info(f"audit_table : {audit_table}")
#
#         if not self.spark.catalog.tableExists(audit_table):
#             return False
#
#         self.logger.info(
#             f"Tables disponibles dans le catalogue : "
#             f"{self.spark.catalog.listTables()}"
#         )
#
#         query = f"""
#             SELECT COUNT(*) as cnt
#             FROM {audit_table}
#             WHERE table_name = '{context.table_name}'
#             AND taxi_type = '{context.taxi_type}'
#             AND periode = {context.periode}
#             AND status = 'SUCCESS'
#         """
#
#         result = self.spark.sql(query).collect()[0]["cnt"]
#         return result > 0
#
#         ## context.run_id = str(uuid.uuid4())
#
#     def insert_audit(self, context):
#
#         catalog_manager = CatalogManager(
#             spark=self.spark,
#             logger=self.logger,
#             env=context.env
#         )
#
#         audit_table = catalog_manager.audit_load()
#
#         ## transforme explicitement les valeurs avant de les donner à Spark
#         run_id = int(context.run_id)
#         periode = int(context.periode)
#
#         table_name = str(context.table_name)
#         taxi_type = str(context.taxi_type)
#         status = str(context.status)
#
#         start_time = context.start_time
#         end_time = context.end_time
#
#         duration_seconds = (
#             Decimal(str(round(float(context.duration_seconds),2)))
#             if context.duration_seconds is not None
#             else None
#         )
#
#         error_step = (
#             str(context.error_step)
#             if context.error_step is not None
#             else None
#         )
#
#         message = (
#             str(context.message)
#             if context.message is not None
#             else None
#         )
#
#         self.logger.info(
#             f"AUDIT | run_id={run_id} | periode={periode} | "
#             f"table={table_name} | taxi_type={taxi_type} | "
#             f"status={status}"
#         )
#
#
#         query = f"""
#         SELECT
#             CAST({context.run_id} AS BIGINT)                        AS run_id,
#             CAST({context.periode} AS INT)                          AS periode,
#             CAST('{context.table_name}' AS STRING)                  AS table_name,
#             CAST('{context.taxi_type}' AS STRING)                   AS taxi_type,
#             CAST('{context.status}' AS STRING)                      AS status,
#             CAST('{context.start_time}' AS TIMESTAMP)               AS start_time,
#             CAST('{context.end_time}' AS TIMESTAMP)                 AS end_time,
#             CAST({context.duration_seconds} AS DECIMAL(18,2))       AS duration_seconds,
#             CAST('{error_step}' AS STRING)                          AS error_step,
#             CAST('{message}' AS STRING)                             AS message
#         """
#
#         df_audit = self.spark.sql(query)
#
#         self.logger.info(f"audit_table = {audit_table}")
#         ## df_audit.printSchema()
#         df_audit.show(truncate=False)
#
#         (
#         df_audit.write
#             .format("delta")
#             .mode("append")
#             .saveAsTable(audit_table)
#         )
#
#
#
#     ## table audit : nyc_taxi.audit.audit_load
#     @log_execution
#     def delete_period(
#         self,
#         table_name,
#         periode
#     ):
#         self.spark.sql(
#         f"""
#             DELETE FROM {table_name}
#             WHERE periode = {periode}
#         """
#         )
#         self.logger.info(
#             f"Deleting period {periode} "
#             f"from {table_name}"
#         )
#
#
#     def insert_row_counts(self, context):
#
#         catalog_manager = CatalogManager(
#             spark=self.spark,
#             logger=self.logger,
#             env=context.env
#         )
#
#         audit_row_table = catalog_manager.audit_row_count()
#
#         run_id = int(context.run_id)
#         periode = int(context.periode)
#
#         self.logger.separator(
#             "AUDIT ROW COUNTS"
#         )
#         for table_name, row_count in context.row_count.items():
#
#             self.logger.metric(
#                 table_name,
#                 f"{row_count:.}"
#             )
#
#             table_name_sql = str(table_name).replace("'", "''")
#             created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#             query = f"""
#                 INSERT INTO {audit_row_table}
#                 (
#                     run_id,
#                     periode,
#                     table_name,
#                     row_count,
#                     created_at
#                 )
#                 VALUES
#                 (
#                     CAST({run_id} AS BIGINT),
#                     CAST({periode} AS INT),
#                     '{table_name_sql}',
#                     CAST({int(row_count)} AS BIGINT),
#                     CAST('{created_at}' AS TIMESTAMP)
#                 )
#             """
#             self.spark.sql(query)
#
#         self.logger.success(
#             "Audit completed"
#         )
#
#
#
#
#     def get_next_period(
#             self,
#             table_name: str,
#             taxi_type: str,
#             env:str='local'
#     ) -> int:
#
#         catalog_manager = CatalogManager(
#             spark=self.spark,
#             logger=self.logger,
#             env=env
#         )
#         audit_table = catalog_manager.audit_load()
#
#         self.logger.info(
#             f"audit_table  : {audit_table}"
#         )
#
#         try:
#
#             row = (
#                 self.spark.table(audit_table)
#                 .filter(col("table_name") == table_name)
#                 .filter(col("taxi_type") == taxi_type)
#                 .filter(col("status") == "SUCCESS")
#                 .select(spark_max("periode").alias("periode"))
#                 .first()
#             )
#
#             max_period = row["periode"] if row else None
#
#             if max_period is None:
#                 self.logger.info(
#                     "Aucune période SUCCESS trouvée -> 202401"
#                 )
#                 return 202501
#
#             year = max_period // 100
#             month = max_period % 100
#
#             if month == 12:
#                 next_period = (year + 1) * 100 + 1
#             else:
#                 next_period = year * 100 + (month + 1)
#
#             self.logger.info(
#                 f"Dernière période : {max_period} "
#                 f"-> prochaine période : {next_period}"
#             )
#             return next_period
#
#         except Exception as e:
#
#             self.logger.warning(
#                 f"Impossible de lire {audit_table}: {e}"
#             )
#
#             return 202501
#
#
# if __name__ == "__main__":
#     logger = PipelineLogger("uber_pipeline", env='local')
#     # audit_manager = AuditManager(
#     #     spark=spark,
#     #     logger=logger
#     # )
#     # periode = audit_manager.get_next_period(
#     #     table_name=context.table_name,
#     #     taxi_type=context.taxi_type,
#     #     env=context.env
#     # )
#     # logger.info(f"Periode choisie : {audit_manager.get_next_period()}")


#