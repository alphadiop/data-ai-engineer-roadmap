from decimal import Decimal
from nyc_taxi.src.logger.logger import PipelineLogger
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

    def insert_audit(self, context:PipelineContext)-> None:

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

        # Échapper les apostrophes dans les chaînes SQL.
        def sql_string(value: object) -> str:
            if value is None:
                return "NULL"
            return "'" + str(value).replace("'", "''") + "'"

        self.logger.separator("AUDIT INSERT")
        self.logger.metric("Run ID", run_id)
        self.logger.metric("Period", periode)
        self.logger.metric("Table", table_name)
        self.logger.metric("Taxi type", taxi_type)
        self.logger.metric("Status", status)
        self.logger.metric("Audit table", audit_table)

        query = f"""
            SELECT
                CAST({run_id} AS BIGINT) AS run_id,
                CAST({periode} AS INT) AS periode,
                CAST({sql_string(table_name)} AS STRING) AS table_name,
                CAST({sql_string(taxi_type)} AS STRING) AS taxi_type,
                CAST({sql_string(status)} AS STRING) AS status,
                CAST({sql_string(start_time)} AS TIMESTAMP) AS start_time,
                CAST({sql_string(end_time)} AS TIMESTAMP) AS end_time,
                CAST({str(duration_seconds) if duration_seconds is not None else "NULL"} AS DECIMAL(18,2)) AS duration_seconds,
                CAST({sql_string(error_step)} AS STRING) AS error_step,
                CAST({sql_string(message)} AS STRING) AS message
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

    def insert_row_counts(self, context:PipelineContext):

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
                    .select(spark_max("periode").alias("periode"))
                    .first()
            )

            max_period = row["periode"] if row else None

            if max_period is None:
                self.logger.info(
                    "Aucune période SUCCESS trouvée -> 202501"
                )
                return 202501

            year = int(max_period) // 100
            month = int(max_period) % 100

            if month == 12:
                next_period = (year + 1) * 100 + 1
            else:
                next_period = year * 100 + (month + 1)

            self.logger.metric("Dernière période",max_period)
            self.logger.metric("Prochaine période",next_period)

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
