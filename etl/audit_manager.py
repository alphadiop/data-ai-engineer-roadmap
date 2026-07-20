from pyspark.sql.functions import col
from datetime import datetime

class AuditManager:
    def __init__(self, spark):
        self.spark = spark

    def is_period_loaded(
        self,
        table_name:str,
        taxi_type:str,
        periode:int
    ):

        query = f"""
            SELECT COUNT(*) as cnt
            FROM nyc_taxi.audit.audit_load
            WHERE table_name = '{table_name}'
            AND taxi_type = '{taxi_type}'
            AND periode = '{periode}'
            AND status = 'SUCCESS'
        """
        result = self.spark.sql(query).collect()[0]["cnt"]
        return result > 0
    

    def insert_audit(
        self,
        periode,
        table_name,
        taxi_type,
        nb_rows,
        status,
        start_time=None,
        end_time=None,
        duration_seconds=None,
        message=""
    ):

        data = [
            (
                periode,
                table_name,
                taxi_type,
                nb_rows,
                status,
                datetime.now(),
                datetime.now(),
                duration_seconds,
                message
            )
        ]

        df = self.spark.createDataFrame(
            data,
            [
                "periode",
                "table_name",
                "taxi_type",
                "nb_rows",
                "status",
                "start_time",
                "end_time",
                "duration_seconds",
                "message"
            ]
        )

        (
            df.write
            .format("delta")
            .mode("append")
            .saveAsTable(
                "nyc_taxi.audit.audit_load"
            )
        )

    ## nyc_taxi.audit.audit_load
    def delete_period(
        self,
        catalogue,
        schema,
        table_name,
        periode
    ):
        self.spark.sql(f"""
            DELETE FROM {catalogue}.{schema}.{table_name}
            WHERE periode = {periode}
        """)
                                                 
                                            