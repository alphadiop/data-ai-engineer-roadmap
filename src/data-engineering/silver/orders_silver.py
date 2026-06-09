from common.pipeline_step import PipelineStep

class OrdersSilver(PipelineStep):

    def run(self):
        bronze_df = self.spark.table("training.bronze.orders_raw")

        silver_df = (
            bronze_df
            .filter("amount IS NOT NULL")
            .filter("amount > 0")
            .dropDuplicates(["order_id"])
        )

        silver_df.write \
            .format("delta") \
            .mode("overwrite") \
            .saveAsTable(
                "training.silver.orders_clean"
            )

        self.logger.info(
            f"Silver rows : {silver_df.count()}"
        )