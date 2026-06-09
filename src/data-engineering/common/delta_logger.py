from pyspark.sql import Row
from datetime import datetime

class DeltaLogger:

    def __init__(self, spark):
        self.spark = spark

    def log(self, run_id, step, status, row_count, message):
        row = Row(
            run_timestamp=datetime.now(),
            run_id=run_id,
            step=step,
            status=status,
            row_count=row_count,
            message=message
        )

        self.spark.createDataFrame([row]) \
            .write \
            .mode("append") \
            .saveAsTable("training.monitoring.pipeline_logs")