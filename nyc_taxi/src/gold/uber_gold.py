import os
import sys


from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.common.schema_manager import SchemaManager
from nyc_taxi.src.utils.load_json import load_json

from silver.uber_silver import UberSilver


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
    """
    Après chaque chargement reussi, faire optimize_period
    Puis chaque semaine ou mois faire vacuum
    Attention : vacuum est dans le module maintenace_job dans jobs
    """

    path_sql_schema = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/schema/"

    def __init__(self, spark: SparkSession, logger: PipelineLogger):
        super().__init__(spark, self.__class__.__name__)
        self.spark = spark
        self.logger = logger


    @log_execution
    def run(self, context):

        """ 
            attention : ["nyc_taxi.gold.gold_dim_date", "nyc_taxi.ref.gold_dim_location"]
            ne sont pas des tables optimisable par période
        """
        df_silver = context.df_silver

        context.df_fact_trips = self.get_fact_trips(df_silver)
        context.df_dim_date = self.get_dim_date(df_silver)
        context.df_kpi_daily = self.get_kpi_daily(df_silver)
        
        delta_manager = DeltaManager(
            spark=self.spark,
            logger=self.logger
        )
       
        schema_manager = SchemaManager(
            spark=self.spark,
            logger=self.logger
        )
         
        if self.logger:
            self.logger.info(f"{'=' * 12} Début Validation des schemas {'=' * 12} ")

        schema_json = self.get_schema_json(
                type_taxi=context.type_taxi, 
                table_name="silver_nyc_taxi"
        )
        
        schema_manager.validate_columns(
            df=context.df_silver, 
            schema_json=schema_json
        )

        if self.logger:
            self.logger.info(f"{'=' * 12} Fin Validation des schemas {'=' * 12} ")


        if self.logger:
            self.logger.info(f"{'=' * 12} Chargement des données dans Delta {'=' * 12} ")

        tables = [
            ("silver", "silver_nyc_taxi", context.df_silver),
            ("gold", "gold_fact_trips", context.df_fact_trips),
            ("gold", "gold_dim_date", context.df_dim_date),
            ("gold", "gold_kpi_daily", context.df_kpi_daily),
        ]

        for schema_name, table_name, df in tables:

            delta_manager.sauvegarde_tables_delta(
                df=df,
                schema_name=schema_name,
                table_name=table_name,
                periode=context.periode
            )

        if self.logger:
            self.logger.info(f"{'=' * 12} Optimisation des tables Delta {'=' * 12} ")

        tables_to_optimize = [
            "nyc_taxi.silver.silver_nyc_taxi",
            "nyc_taxi.gold.gold_fact_trips",
            "nyc_taxi.gold.gold_kpi_daily"
        ]
        
        for table in tables_to_optimize:

            delta_manager.optimize_period(
                table_name=table,
                periode=context.periode
            )


    def get_schema_json(self, type_taxi, table_name: str) -> dict:
        path = os.path.join(
            self.path_sql_schema,
            type_taxi,
            f"{table_name}.json"
        )
        return load_json(path)
    


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

    # "gold_dim_date", "gold_kpi_daily", "gold_fact_trips", "gold_dim_location"

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
        self.spark.sql("DROP TABLE IF EXISTS nyc_taxi.gold.gold_dim_date")

    @log_execution
    def purges_tables(self):
        spark.sql("TRUNCATE TABLE nyc_taxi.silver.silver_nyc_taxi").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_dim_date").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_kpi_daily").show(truncate=False)
        spark.sql("TRUNCATE TABLE nyc_taxi.gold.gold_fact_trips").show(truncate=False)

        ### "gold_dim_date", "gold_kpi_daily", "gold_fact_trips", "gold_dim_location"




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







