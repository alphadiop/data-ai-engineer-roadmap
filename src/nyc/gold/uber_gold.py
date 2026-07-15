import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.pipeline_step import PipelineStep
from common.logger import PipelineLogger
from silver.uber_silver import UberSilver
from common.decorators import log_execution


from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import re
from pyspark.sql.functions import lit
from pyspark.sql import functions as F
from pyspark.sql.functions import (
    unix_timestamp,
    year,
    month,
    dayofmonth,
    hour, dayofweek,
    sum,
    avg,
    count,
    col,
    round,
    when
)


class UberGold(PipelineStep):
    def __init__(self, spark: SparkSession, logger: PipelineLogger):
        super().__init__(spark, self.__class__.__name__)
        self.spark = spark
        self.logger = logger
        ##self.spark = SparkSession.getActiveSession()
        #self.df_silver = (
            #spark.table("nyc_taxi.silver.silver_nyc_taxi")
            #.where("Periode = 202411")
        #)

    @log_execution
    def run(self, context):

        df_silver = context.df_silver

        context.df_fact_trips = self.get_fact_trips(df_silver)
        context.df_dim_date = self.get_dim_date(df_silver)
        context.df_kpi_daily = self.get_kpi_daily(df_silver)
        context.dim_location = self.get_dim_location()

        context.row_count["fact_trips"] = context.df_fact_trips.count()
        context.row_count["dim_date"] = context.df_dim_date.count()
        context.row_count["kpi_daily"] = context.df_kpi_daily.count()
        context.row_count["dim_location"] = context.dim_location.count()

        self.sauvegarde_tables_df(
            context.df_silver,
            "silver",
            "silver_nyc_taxi"
        )
                
        self.sauvegarde_tables_df(
            context.df_fact_trips,
            "gold",
            "gold_fact_trips"
        )

        self.sauvegarde_tables_df(
            context.df_dim_date,
            "gold",
            "gold_dim_date"
        )

        self.sauvegarde_tables_df(
            context.df_kpi_daily,
            "gold",
            "gold_kpi_daily"
        )


    @log_execution   
    def get_dim_date(self, df_silver: DataFrame) -> DataFrame:
        from pyspark.sql.functions import (
                col,
                year,
                month,
                dayofmonth,
                quarter,
                dayofweek,
                date_format
            )

        return (
            df_silver
            .select(
                col("periode"),
                col("tpep_pickup_datetime").cast("date").alias("date")
            )
            .distinct()
            .withColumn("year", year("date"))
            .withColumn("quarter", quarter("date"))
            .withColumn("month", month("date"))
            .withColumn("day", dayofmonth("date"))
            .withColumn("day_of_week", dayofweek("date"))
            .withColumn("day_name", date_format("date", "EEEE"))
            .withColumn("month_name", date_format("date", "MMMM"))
            .withColumn(
                "trip_date",
                year(col("date")) * 10000 
                 + month(col("date")) * 100 
                 + dayofmonth(col("date"))
            )
        )

    # "gold_dimdate", "gold_kpi_daily", "gold_fact_trips", "gold_dim_location"

    @log_execution
    def get_fact_trips(self, df_silver: DataFrame) -> DataFrame:
        from pyspark.sql.functions import to_date
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
        return (
            df_silver
            .groupBy(
                col("periode").cast("string"),
                col("trip_date").cast("int")
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
        )

    def get_dim_location(self):
        catalog = "nyc_taxi"
        schema = "ref"
        voulume = "ref_files"
        return (
            self.spark.read.csv("/Volumes/nyc_taxi/ref/ref_files/taxi_zone_lookup.csv", header=True)
            .withColumn(
                "location_id",
                col("LocationID").cast("int")
            )
            .select(
                "location_id",
                "Borough",
                "Zone",
                "service_zone"
            )
        )

    @log_execution
    def sauvegarde_tables_df(
        self,
        df: DataFrame,
        schema_name: str,
        table_name: str
    ):
        ### self.spark.sql("DROP TABLE IF EXISTS {0}".format(table_name))
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
        self.logger.info(
            f"Table nyc_taxi.{schema_name}.{table_name} saved"
        )


    @log_execution
    def drop_tables_uber(self):
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.silver.silver_nyc_taxi")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_fact_trips")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_kpi_daily")
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_dimdate")

    @log_execution
    def purges_tables(self):
        spark.sql("TRUNCATE TABLE nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_dimdate").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_kpi_daily").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_fact_trips").show(truncate=False)

        ### "gold_dimdate", "gold_kpi_daily", "gold_fact_trips", "gold_dim_location"




if __name__ == "__main__":
    
    spark = SparkSession.builder.appName("NYC Taxi").getOrCreate()
    silver = UberSilver(
        spark = spark, 
        logger = PipelineLogger('Silver')
    )

    df = (
        spark.table("nyc_taxi.silver.silver_nyc_taxi")
        .where("periode = 202411")
    )
        
    df_silver = silver.run(df)

    gold = UberGold(
        spark=spark,
        logger=PipelineLogger('Gold')
    )

    df_fact_trips =gold.get_fact_trips(df_silver),
    df_dim_date=gold.get_dim_date(df_silver),
    df_kpi_daily=gold.get_kpi_daily(df_silver),
    df_dim_location=gold.get_dim_location() 

    display(df_fact_trips)







