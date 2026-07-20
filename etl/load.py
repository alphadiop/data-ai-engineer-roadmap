from pyspark.sql import DataFrame


class Load:
    def sauvegarde_tables_df(
        self,
        df: DataFrame,
        schema_name: str,
        table_name: str
    ):

        (
            df.write
            .format("delta")
            .mode("append")
            .option("mergeSchema", "true")
            .partitionBy("periode")
            .saveAsTable(
                f"nyc_taxi.{schema_name}.{table_name}"
            )
        )
