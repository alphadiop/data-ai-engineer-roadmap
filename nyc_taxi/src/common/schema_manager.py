from pyspark.sql.functions import col


class SchemaManager:

    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger

    def validate_columns(self, df, schema_json):
        """Vérifie la conformité des colonnes avec le schéma JSON."""

        json_columns = set(schema_json.keys())
        df_columns = set(df.columns)

        missing_cols = json_columns - df_columns
        extra_cols = df_columns - json_columns

        if self.logger:
            self.logger.info(
                f"Missing columns: {sorted(missing_cols)}"
            )
            self.logger.info(
                f"Unexpected columns: {sorted(extra_cols)}"
            )

        if missing_cols:
            raise ValueError(
                f"Missing columns in DataFrame: {sorted(missing_cols)}"
            )

        if extra_cols:
            raise ValueError(
                f"Unexpected columns in DataFrame: {sorted(extra_cols)}"
            )

    def apply_schema(self, df, schema_json):
        """Vérifie les colonnes puis applique les types du schéma JSON."""

        self.validate_columns(
            df=df,
            schema_json=schema_json
        )

        for column_name, metadata in schema_json.items():

            sql_type = metadata["sql_type"]

            df = df.withColumn(
                column_name,
                col(column_name).cast(sql_type)
            )

        return df
