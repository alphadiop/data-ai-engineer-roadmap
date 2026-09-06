from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.decorators import log_execution
import logging

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import expr

from pyspark.sql.functions import (
    col, count, sum, avg, round
)

from pyspark.sql.types import DecimalType
from pyspark.sql.functions import (
    col,
    lit,
    year,
    month,
    dayofmonth,
    quarter,
    dayofweek,
    date_format,
    to_date,
    concat,
    lpad,
    avg,
    count
)

from pyspark.sql.types import (
    ByteType,
    ShortType
)


class UberGold(PipelineStep):
    """
    Après chaque chargement reussi, faire optimize_period
    Puis chaque semaine ou mois faire vacuum
    Attention : vacuum est dans le module maintenace_job dans jobs
    """


    def __init__(self, spark: SparkSession, logger: PipelineLogger):
        super().__init__(spark, self.__class__.__name__)
        self.spark = spark
        self.logger = logger or logging.getLogger(__name__)

        #self.config_table = load_config("pilotage_tables", self.logger)


    @log_execution
    def run(self, context):
        """ 
            attention : ["nyc_taxi.gold.gold_dim_date", "nyc_taxi.ref.gold_dim_location"]
            ne sont pas des tables optimisables par période
        """
        self.ref_path = context.config["ref_path"]

        df_silver = context.df_silver
        self.logger.info(
            f"{'=' * 12} Construction des DataFrames Gold {'=' * 12}"
        )

        context.df_fact_trips = self.get_fact_trips(df_silver)
        context.df_dim_date = self.get_dim_date(df_silver,context.periode)
        context.df_kpi_daily = self.get_kpi_daily(df_silver)

        context.tables_to_load = [
            (
                "silver",
                "silver_nyc_taxi",
                context.df_silver
            ),
            (
                "gold",
                "gold_fact_trips",
                context.df_fact_trips
            ),
            (
                "ref",
                "dim_date",
                context.df_dim_date
            ),
            (
                "gold",
                "gold_kpi_daily",
                context.df_kpi_daily
            )
        ]

        self.logger.info(
            f"{'=' * 12} Fin Construction Gold {'=' * 12}"
        )

    @log_execution
    def get_dim_date(self, df_silver: DataFrame, periode: int) -> DataFrame:

        annee = str(periode)[:4]

        return (
            df_silver
            .select(
                col("tpep_pickup_datetime")
                .cast("date")
                .alias("date")
            )
            .distinct()
            .withColumn("periode",lit(periode).cast("int"))
            .withColumn("year", year("date").cast(ShortType()))
            .withColumn("quarter", quarter("date").cast(ByteType()))
            .withColumn("month", month("date").cast(ByteType()))
            .withColumn("day", dayofmonth("date").cast(ByteType()))
            .withColumn("day_of_week", dayofweek("date").cast(ByteType()))
            .withColumn("day_name", date_format("date", "EEEE"))
            .withColumn("month_name", date_format("date", "MMMM"))
            .withColumn(
                "trip_date",
                (
                        year(col("date")) * 10000
                        + month(col("date")) * 100
                        + dayofmonth(col("date"))
                ).cast("int")
            )
            .filter(
                (year(col("date")) == periode // 100)
                &
                (month(col("date")) == periode % 100)
            )
        )

    # "gold_dim_date", "gold_kpi_daily", "gold_fact_trips", "dim_location"

    @log_execution
    def get_fact_trips(self, df_silver: DataFrame) -> DataFrame:

        return (
            df_silver
                .withColumn(
                    "date",
                    to_date("tpep_pickup_datetime")
                )
            .select(
                "periode",
                "trip_date",
                "date",
                "PULocationID",
                "DOLocationID",
                "trip_duration_minute",
                "trip_distance",
                "passenger_count",
                "fare_amount",
                "tip_amount",
                "total_amount",
                "payment_type"
            )
        )





    @log_execution
    def get_kpi_daily(self, df_silver: DataFrame) -> DataFrame:
        from pyspark.sql.types import DecimalType
        return (
            df_silver
            .groupBy(
                col("periode").cast("int").alias("periode"),
                col("trip_date").cast("int").alias("trip_date")
            )
            .agg(
                count("*").alias("nb_trips"),
                round(sum("total_amount"), 2).alias("revenue"),
                round(avg("trip_distance"), 2).alias("avg_distance"),
                round(avg("tip_amount"), 2).alias("avg_tip"),
                round(avg("total_amount"), 2).alias("avg_revenue_per_trip"),
                round(sum("tip_amount"), 2).alias("total_tips"),
                round(sum("trip_distance"), 2).alias("total_distance"),
                round((sum("total_amount") / sum("trip_distance")), 2).alias("revenue_per_distance"),
                round(avg("passenger_count"), 2).alias("avg_passengers_per_trip"),
                round(avg("trip_duration_minute"), 2).alias("avg_trip_duration"),
                round(avg("tip_percent"), 2).alias("avg_tip_percent"),
                round(avg("average_speed"), 2).alias("avg_speed")
            )
            .withColumn("revenue", col("revenue").cast(DecimalType(19,2)))
            .withColumn("avg_distance", col("avg_distance").cast(DecimalType(19,2)))
            .withColumn("avg_tip", col("avg_tip").cast(DecimalType(19,2)))
            .withColumn("avg_revenue_per_trip", col("avg_revenue_per_trip").cast(DecimalType(19,2)))
            .withColumn("total_tips", col("total_tips").cast(DecimalType(19,2)))
            .withColumn("total_distance", col("total_distance").cast(DecimalType(19,2)))
            .withColumn("revenue_per_distance", col("revenue_per_distance").cast(DecimalType(19,2)))
            .withColumn("avg_passengers_per_trip", col("avg_passengers_per_trip").cast(DecimalType(19,2)))
            .withColumn("avg_trip_duration", col("avg_trip_duration").cast(DecimalType(19,2)))
            .withColumn("avg_tip_percent", col("avg_tip_percent").cast(DecimalType(19,2)))
            .withColumn("avg_speed", col("avg_speed").cast(DecimalType(19,2)))
        )


    def get_dim_location(self)-> DataFrame:
        return (

            self.spark.read.csv(self.ref_path, header=True)
            .withColumn(
                "location_id", col("LocationID").cast("int")
            )
            .select(
                "location_id",
                "Borough",
                "Zone",
                "service_zone"
            )
        )


    @log_execution
    def drop_tables_uber(self):
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.silver.silver_nyc_taxi")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_fact_trips")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_kpi_daily")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.ref.dim_date")


    @log_execution
    def purges_tables(self):
        self.spark.sql("TRUNCATE TABLE nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
        self.spark.sql("TRUNCATE TABLE nyc_taxi.ref.dim_date").show(truncate=False)
        self.spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_kpi_daily").show(truncate=False)
        self.spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_fact_trips").show(truncate=False)

        ### "gold_dim_date", "gold_kpi_daily", "gold_fact_trips", "dim_location"




if __name__ == "__main__":
    import sys
    from nyc_taxi.src.common.spark_manager import SparkManager
    from nyc_taxi.src.utils.config import load_config

    taxi_type = "yellow"
    # #taxi_type = "green"
    # #taxi_type = "fhv"
    logger = PipelineLogger('Gold')

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    ).get_spark()

    gold = UberGold(
        spark = spark_manager,
        logger = PipelineLogger('Gold')
    )
    spark_manager.sql(
        """
        DESCRIBE DETAIL silver.silver_nyc_taxi
        """
    ).show(truncate=False)

    spark_manager.sql(
        """
        DESCRIBE DETAIL silver.silver_nyc_taxi
        """
    ).select(
        "partitionColumns"
    ).show()
