from pyspark.sql.functions import col

class SchemaManager:

    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger

    def apply_schema2(self, df, schema_json):

        missing_cols = []

        for column_name, metadata in schema_json.items():

            if column_name not in df.columns:
                missing_cols.append(column_name)
                continue

            sql_type = metadata["sql_type"]

            df = df.withColumn(
                column_name,
                col(column_name).cast(sql_type)
            )

        if missing_cols:
            raise ValueError(
                f"Missing columns in DataFrame: {missing_cols}"
            )

        return df

    @staticmethod
    def apply_schema(df, schema_json):

        json_columns = set(schema_json.keys())
        df_columns = set(df.columns)

        extra_columns = df_columns - json_columns
        missing_cols = json_columns - df_columns

        if missing_cols:
            raise ValueError(
                f"Missing columns in DataFrame: {sorted(missing_cols)}"
            )

        if extra_columns:
            raise ValueError(
                f"Unexpected columns in DataFrame: {sorted(extra_columns)}"
            )

        for column_name, metadata in schema_json.items():

            sql_type = metadata["sql_type"]

            df = df.withColumn(
                column_name,
                col(column_name).cast(sql_type)
            )

        return df

    def validate_columns(self, df, schema_json):

        json_cols = set(schema_json.keys())
        df_cols = set(df.columns)

        missing_cols = json_cols - df_cols
        extra_cols = df_cols - json_cols

        if self.logger:
            self.logger.info(
                f"Missing columns: {missing_cols}"
            )

        if missing_cols:
            raise ValueError(
                f"Missing columns: {sorted(missing_cols)}"
            )

        if extra_cols:
            raise ValueError(
                f"Unexpected columns: {sorted(extra_cols)}"
            )

        # Validation + cast selon le JSON
        for column_name, metadata in schema_json.items():

            sql_type = metadata["sql_type"]

            df = df.withColumn(
                column_name,
                col(column_name).cast(sql_type)
            )

        return df


# from pyspark.sql.functions import col
#
# class SchemaManager:
#     def __init__(self, spark, logger):
#         self.spark = spark
#         self.logger = logger
#
#     def apply_schema2(self, df, schema_json):
#
#         missing_cols = []
#
#         for column_name, metadata in schema_json.items():
#
#             if column_name not in df.columns:
#                 missing_cols.append(column_name)
#                 continue
#
#             sql_type = metadata["sql_type"]
#
#             df = df.withColumn(
#                 column_name,
#                 col(column_name).cast(sql_type)
#             )
#
#         if missing_cols:
#             raise ValueError(
#                 f"Missing columns in DataFrame: {missing_cols}"
#             )
#
#         return df
#
#
#     @staticmethod
#     def apply_schema(df, schema_json):
#
#         json_columns = set(schema_json.keys())
#         df_columns = set(df.columns)
#
#         extra_columns = df_columns - json_columns
#         missing_cols = json_columns - df_columns
#
#         if missing_cols:
#             raise ValueError(
#                 f"Missing columns in DataFrame: {sorted(missing_cols)}"
#             )
#
#         if extra_columns:
#             raise ValueError(
#                 f"Unexpected columns in DataFrame: {sorted(extra_columns)}"
#             )
#
#         for column_name, metadata in schema_json.items():
#
#             sql_type = metadata["sql_type"]
#
#             df = df.withColumn(
#                 column_name,
#                 col(column_name).cast(sql_type)
#             )
#
#         return df
#
#
#     def validate_columns(self, df, schema_json):
#
#         json_cols = set(schema_json.keys())
#         df_cols = set(df.columns)
#
#         missing_cols = json_cols - df_cols
#         extra_cols = df_cols - json_cols
#
#         if self.logger:
#             self.logger.info(f"Missing columns: {missing_cols}")
#
#         if missing_cols:
#             raise ValueError(
#                 f"Missing columns: {sorted(missing_cols)}"
#             )
#
#         if extra_cols:
#             raise ValueError(
#                 f"Unexpected columns: {sorted(extra_cols)}"
#             )
#
#
#
#     def validate_types(self, df, schema_json):
#         spark_types = {
#             field.name: field.dataType.simpleString()
#             for field in df.schema.fields
#         }
#
#         errors = []
#
#         for col_name, metadata in schema_json.items():
#
#             if col_name not in spark_types:
#                 continue
#
#             df_type = spark_types[col_name]
#             expected_type = metadata["sql_type"]
#
#             errors.append(
#                 (
#                     col_name,
#                     df_type,
#                     expected_type
#                 )
#             )
#         return errors

