from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.logger.logger import PipelineLogger

if __name__ == "__main__":
    env = 'local'
    periode = 202411
    taxi_type = 'yellow'

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type,
    )
    spark = SparkManager().get_spark()

    audit = spark.read.format("delta").load(
        "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load"
    )
    audit.show(50, False)


#
# tables = {
#     "silver_nyc_taxi":
#         "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/silver.db/silver_nyc_taxi",
#
#     "gold_fact_trips":
#         "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_fact_trips",
#
#     "gold_kpi_daily":
#         "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_kpi_daily",
#
#     "audit_load":
#         "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load",
#
#     "audit_row_count":
#         "/mnt/d/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_row_count"
# }
#
# for name, path in tables.items():
#
#     print("\n" + "=" * 80)
#     print(name)
#     print("=" * 80)
#
#     df = spark.read.format("delta").load(path)
#
#     print(f"Nombre lignes : {df.count()}")
#
#     df.show(20, truncate=False)



### Power Shell
### wsl
### cd D:\data-ai-engineer-roadmap
### source ~/spark4_env/bin/activate
## python -m nyc_taxi.src.admin.check_delta_tables