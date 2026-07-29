from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager

def main():
    logger = PipelineLogger("register_delta")
    spark_manager = SparkManager(
        app_name="register_delta_tables",
        logger=logger
    )
    spark = spark_manager.get_spark()

    tables = {
        "audit.audit_load":"D:/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load",
        "audit.audit_row_count":"D:/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_row_count",
        "silver.silver_nyc_taxi":"D:/data-ai-engineer-roadmap/spark-warehouse/silver.db/silver_nyc_taxi",
        "gold.gold_fact_trips":"D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_fact_trips",
        "gold.gold_dim_date":"D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date",
        "gold.gold_kpi_daily":"D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_kpi_daily",
    }
    for table_name, path in tables.items():
        spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            USING DELTA
            LOCATION '{path}'
        """)
    logger.info("=== DATABASES ===")
    spark.sql("SHOW DATABASES").show()

    # logger.info("=== GOLD TABLES ===")
    # spark.sql("SHOW TABLES IN gold").show(truncate=False)
    #
    # logger.info("=== SILVER TABLES ===")
    # spark.sql("SHOW TABLES IN silver").show(truncate=False)
    #
    # logger.info("=== AUDIT TABLES ===")
    # spark.sql("SHOW TABLES IN audit").show(truncate=False)
    #
    # logger.info(f"{15*'='}  Où est stocké ton metastore local ? {'silver'.upper()} {15*'='}")
    # spark.sql(""" DESCRIBE EXTENDED silver.silver_nyc_taxi """).show(200, truncate=False)

if __name__ == "__main__":
    main()