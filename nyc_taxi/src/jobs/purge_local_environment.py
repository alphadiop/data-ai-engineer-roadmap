from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.common.logger import PipelineLogger
from purge_delta_storage import PurgeDeltaStorage

logger = PipelineLogger("PURGE")

spark = SparkManager(
    app_name="purge_local",
    env="local",
    logger=logger
).get_spark()

PurgeDeltaStorage(
    spark=spark,
    logger=logger,
    env="local"
).run()

# EnvironmentSetup(
#     spark=spark,
#     env="local",
#     logger=logger
# ).run(
#     path_sql_schema="D:/data-ai-engineer-roadmap/nyc_taxi/schema",
#     taxi_type="yellow"
# )

### lancement en console : python -m nyc_taxi.src.jobs.purge_local_environment