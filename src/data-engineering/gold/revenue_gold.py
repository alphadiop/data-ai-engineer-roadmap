from pyspark.sql.functions import sum
from common.pipeline_step import PipelineStep


class RevenueGold(PipelineStep):

    def run(self):

        silver_df = self.spark.table(
            "training.silver.orders_clean"
        )

        gold_df = (
            silver_df
            .groupBy("country")
            .agg(
                sum("amount").alias("revenue")
            )
        )

        gold_df.write \
            .format("delta") \
            .mode("overwrite") \
            .saveAsTable(
                "training.gold.revenue_by_country"
            )

        self.logger.info(
            f"Gold rows : {gold_df.count()}"
        )