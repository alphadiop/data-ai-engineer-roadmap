from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager
import os

if __name__ == "__main__":

    tab = "gold.gold_kpi_daily"
    logger = PipelineLogger("uber_pipeline")

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        logger=logger
    )
    spark = spark_manager.get_spark()

    logger.info(spark.conf.get("spark.sql.warehouse.dir"))
    logger.info(spark.conf.get("javax.jdo.option.ConnectionURL", "no hive metastore"))
    logger.info(spark.conf.get("spark.sql.warehouse.dir"))
    logger.info(spark.catalog.currentDatabase())
    logger.info(spark.catalog.listDatabases())

    spark.sql(""" CREATE DATABASE IF NOT EXISTS gold """)


    for root, dirs, files in os.walk(
            "D:/data-ai-engineer-roadmap/spark-warehouse"
    ):
        if "_delta_log" in dirs:
            logger.info(root)

    # spark.read.table("audit.audit_load").limit(4).show(truncate=False)
    # spark.read.table("audit.audit_row_count").limit(4).show(truncate=False)
    # spark.read.table("silver.silver_nyc_taxi").limit(4).show(truncate=False)
    # spark.read.table("gold.gold_fact_trips").limit(4).show(truncate=False)
    # spark.read.table("gold.gold_dim_date").limit(4).show(truncate=False)
    # spark.read.table("gold.gold_kpi_daily").limit(4).show(truncate=False)

    df = spark.sql("SELECT periode, count(*) as Count FROM silver.silver_nyc_taxi group by periode order by periode desc")
    df.show(truncate=False)

    # df_dim_date = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date"
    # )
    # spark.sql("""
    #     CREATE TABLE gold.gold_dim_date
    #     USING DELTA
    #     LOCATION 'D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date'
    # """)


    # logger.info(f"{15*'='} Pour voir toutes les tables du projet {15*'='} ")
    # for db in ["audit", "bronze", "silver", "gold"]:
    #     try:
    #         logger.info(f"{15*'='}  {db.upper()} {15*'='}")
    #         spark.sql(f"SHOW TABLES IN {db}").show(truncate=False)
    #     except Exception as e:
    #         logger.info(e)
    # logger.info(f"{15*'='} Fin {15*'='} ")
    #
    # spark.read.table("gold.gold_dim_date").show()


    # logger.info(f"{15*'='}  Voir le chemin physique {db.upper()} {15*'='}")
    # spark.sql(""" DESCRIBE DETAIL gold.gold_dim_date """).show(truncate=False)
    #
    # logger.info(f"{15*'='}  Où est stocké ton metastore local ? {db.upper()} {15*'='}")
    # spark.sql(""" DESCRIBE EXTENDED gold.gold_dim_date """).show(200, truncate=False)
    #
    # logger.info(f"{15*'='} gold_kpi_daily {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_kpi_daily"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} gold_fact_trips {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_fact_trips"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} gold_kpi_daily {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_kpi_daily"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} gold_dim_date {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} silver_nyc_taxi {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/silver.db/silver_nyc_taxi"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} audit_load {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} audit_row_count {15*'='} ")
    # df = spark.read.format("delta").load(
    #     "D:/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_row_count"
    # )
    # df.show(truncate=False)
    #
    # logger.info(f"{15*'='} Entree Metastore {15*'='} ")
    # spark.sql("SHOW DATABASES").show(truncate=False)



    # df_dim_date.show()
    #
    # spark.sql("SHOW TABLES IN gold").show(truncate=False)
    # logger.info(spark.conf.get("spark.sql.warehouse.dir"))
    # logger.info(spark.sql("SELECT current_database()").collect())
    #
    # df = spark.read.table("gold.gold_dim_date")
    # df.show()
    # spark.table("gold.gold_dim_date").printSchema()
    # spark.sql("SHOW TABLES IN gold").show()
    # spark.sql(""" DESCRIBE TABLE gold.gold_dim_date """).show(truncate=False)
    # spark.sql(""" DESCRIBE DETAIL gold.gold_dim_date """).show(truncate=False)
    #
    # spark.sql("SHOW TABLES IN gold").show(truncate=False)
    # logger.info("=== DATABASES ===")
    # spark.sql("SHOW DATABASES").show()
    #
    # logger.info("=== TABLES GOLD ===")
    # spark.sql("SHOW TABLES IN gold").show()

    #df = spark.read.table(tab)
    #df.show()