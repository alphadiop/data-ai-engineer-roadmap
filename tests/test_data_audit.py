
from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.audit.audit_manager import AuditManager
from nyc_taxi.src.common.logger import PipelineLogger

table_name = "silver_nyc_taxi"
taxi_type = "yellow"

logger = PipelineLogger(
    name="test_get_next_period",
    env='local'
)

spark = SparkManager(
    app_name="test_get_next_period",
    env="local",
    logger=logger
).get_spark()

audit_manager = AuditManager(
    spark=spark,
    logger=logger
)

spark.sql("""
    SELECT
        run_id,
        periode,
        table_name,
        taxi_type,
        status
    FROM audit.audit_load
    ORDER BY periode
""").show(truncate=False)