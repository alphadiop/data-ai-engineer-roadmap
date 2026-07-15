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


class Transformation:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")


    def add_trip_duration(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
                "trip_duration_minute",
                F.round(
                    ( 
                     unix_timestamp("tpep_dropoff_datetime")- unix_timestamp("tpep_pickup_datetime")
                     ) / 60, 
                3)
        )

    def add_date_key(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
                "trip_date",
                year("tpep_pickup_datetime") * 10000 +
                month("tpep_pickup_datetime") * 100 +
                dayofmonth("tpep_pickup_datetime")
        )



    def add_trip_date(self, df: DataFrame) -> DataFrame:
        df.select(col("tpep_pickup_datetime").cast("date").alias("date"))
        return df.withColumn(
                "trip_date",year(col("date")) * 10000 + 
                  month(col("date")) * 100 + dayofmonth(col("date"))
            )

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
        

    def apply_quality_rules(self, df: DataFrame) -> DataFrame:
        ### 1400 minutes = 23h20 minutes
        return (
            df
            .filter(col("trip_duration_minute") > 0)
            .filter(col("trip_duration_minute") < 1400)
            .filter(col("trip_distance") > 0)
            .filter(col("total_amount") > 0)
        )

    
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


    def get_silver_transformation(self, df_bronze: DataFrame) -> DataFrame:
        df = self.add_trip_duration(df_bronze)
        df = self.add_date_key(df)
        df = self.add_tip_percent(df)
        df = self.add_average_speed(df)
        df = self.add_date_features(df)
        df = self.apply_quality_rules(df)
        return df


    def get_dimdate(self, df_silver: DataFrame) -> DataFrame:
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

        def sauvegarde(self, df):
            (
                df.write
            .format("delta")
            #.mode("append")
            .mode("overwrite")
            .option("mergeSchema", "true")
            .partitionBy("period")
            .saveAsTable("bronze_nyc_taxi")
            )

