from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

from pyspark.sql import functions as F
from pyspark.sql.functions import (
    unix_timestamp,
    year,
    month,
    dayofmonth,
    hour,
    dayofweek,
    sum,
    avg,
    count,
    col,
    round,
    when
)

from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.schema_manager import SchemaManager
from nyc_taxi.src.common.path_manager import PathManager
from nyc_taxi.src.utils.load_json import load_json


class UberSilver(PipelineStep):

    path_sql_schema = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/schema/"

    def __init__(self, spark: SparkSession, logger: PipelineLogger):
        super().__init__(spark, self.__class__.__name__)
        self.spark = spark
        self.logger = logger
        self.spark.conf.set(
            "spark.sql.legacy.timeParserPolicy",
            "LEGACY"
        )

    @log_execution
    def add_trip_duration(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "trip_duration_minute",
            F.round(
                (
                    unix_timestamp("tpep_dropoff_datetime")
                    - unix_timestamp("tpep_pickup_datetime")
                ) / 60,
                3
            )
        )

    @log_execution
    def add_date_key(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "trip_date",
            year("tpep_pickup_datetime") * 10000 +
            month("tpep_pickup_datetime") * 100 +
            dayofmonth("tpep_pickup_datetime")
        )

    @log_execution
    def add_trip_date(self, df: DataFrame) -> DataFrame:
        return (
            df
            .withColumn(
                "date",
                col("tpep_pickup_datetime").cast("date")
            )
            .withColumn(
                "trip_date",
                year("date") * 10000
                + month("date") * 100
                + dayofmonth("date")
            )
        )

    @log_execution
    def add_average_speed(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "average_speed",
            round(
                when(
                    col("trip_duration_minute") > 0,
                    col("trip_distance")
                    / (col("trip_duration_minute") / 60)
                ),
                2
            )
        )

    @log_execution
    def add_tip_percent(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "tip_percent",
            round(
                when(
                    col("fare_amount") > 0,
                    col("tip_amount")
                    / col("fare_amount")
                    * 100
                ),
                2
            )
        )

    @log_execution
    def apply_quality_rules(self, df: DataFrame) -> DataFrame:
        ### 1400 minutes = 23h20 minutes
        return (
            df
            .filter((col("trip_duration_minute") > 0))
            .filter((col("trip_duration_minute") < 1400))
            .filter((col("trip_distance") > 0))
            .filter((col("total_amount") > 0))
        )

    @log_execution
    def add_date_features(self, df_silver: DataFrame) -> DataFrame:
        return (
            df_silver
            .withColumn(
                "pickup_hour",
                hour("tpep_pickup_datetime")
            )
            .withColumn(
                "pickup_day_of_week",
                dayofweek("tpep_pickup_datetime")
            )
            .withColumn(
                "pickup_month",
                month("tpep_pickup_datetime")
            )
            .withColumn(
                "pickup_year",
                year("tpep_pickup_datetime")
            )
        )

    @log_execution
    def cast_columns(self, df: DataFrame) -> DataFrame:
        return (
            df
            .withColumn(
                "tpep_pickup_datetime",
                col("tpep_pickup_datetime").cast("timestamp")
            )
            .withColumn(
                "passenger_count",
                col("passenger_count").cast("bigint")
            )
            .withColumn(
                "payment_type",
                col("payment_type").cast("TINYINT")
            )
            .withColumn(
                "tpep_dropoff_datetime",
                col("tpep_dropoff_datetime").cast("timestamp")
            )
            .withColumn(
                "trip_distance",
                col("trip_distance").cast("decimal(19,5)")
            )
            .withColumn(
                "fare_amount",
                col("fare_amount").cast("decimal(19,5)")
            )
            .withColumn(
                "tip_amount",
                col("tip_amount").cast("decimal(19,5)")
            )
            .withColumn(
                "total_amount",
                col("total_amount").cast("decimal(19,5)")
            )
        )

    @log_execution
    def run(self, context):

        self.logger.subsection(
            "SILVER TRANSFORMATION"
        )

        df_bronze = context.df_bronze

        rows_before = df_bronze.count()

        self.logger.metric(
            "Input rows",
            f"{rows_before:,}".replace(",", " ")
        )

        self.logger.info(
            f"Columns before schema: {len(df_bronze.columns)}"
        )

        df_silver = (
            df_bronze
            .transform(self.add_trip_duration)
            .transform(self.add_date_key)
            .transform(self.add_tip_percent)
            .transform(self.add_average_speed)
            .transform(self.add_date_features)
            .transform(self.cast_columns)
            .transform(self.apply_quality_rules)
        )

        rows_after = df_silver.count()

        rejected = rows_before - rows_after

        self.logger.separator(
            "SILVER QUALITY REPORT"
        )

        self.logger.metric(
            "Rows before quality rules",
            f"{rows_before:,}".replace(",", " ")
        )

        self.logger.metric(
            "Rows after quality rules",
            f"{rows_after:,}".replace(",", " ")
        )

        self.logger.metric(
            "Rejected rows",
            f"{rejected:,}".replace(",", " ")
        )

        if rows_before > 0:

            rejection_rate = (
                rejected / rows_before
            ) * 100

            self.logger.metric(
                "Rejection rate",
                f"{rejection_rate:.2f}%"
            )

        self.logger.success(
            "Silver quality rules completed"
        )

        path_manager = PathManager(
            context=context
        )

        schema_file = path_manager.schema_path(
            taxi_type=context.taxi_type,
            table_name="silver_nyc_taxi"
        )

        schema_json = load_json(schema_file)

        self.logger.info(
            "Applying Silver schema"
        )

        df_silver = SchemaManager.apply_schema(
            df=df_silver,
            schema_json=schema_json
        )

        context.df_silver = df_silver
        context.row_count["silver"] = df_silver.count()

        self.logger.info(
            f"Columns after schema: {len(df_silver.columns)}"
        )

        self.logger.metric(
            "Final Silver rows",
            f"{context.row_count['silver']:,}".replace(",", " ")
        )

        self.logger.success(
            "Silver transformation completed"
        )

        return df_silver

    def add_flag(self, df):
        from pyspark.sql import functions as F

        return df.withColumn(
            "is_positive",
            F.col("amount") > 0
        )


if __name__ == "__main__":
    spark = SparkSession.builder.appName("NYC Taxi").getOrCreate()

    logger = PipelineLogger('Silver')

    silver = UberSilver(
        spark,
        logger
    )

    df = (
        spark.table("nyc_taxi.silver.silver_nyc_taxi")
        .where("Periode = 202411")
    )

    logger.info(
        f"silver : {df.count():,}".replace(",", " ")
    )

    df = silver.run(df)

    logger.info(
        f"gold : {df.count():,}".replace(",", " ")
    )
