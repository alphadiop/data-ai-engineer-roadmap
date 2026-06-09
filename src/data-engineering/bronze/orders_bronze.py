from common.pipeline_step import PipelineStep


class OrdersBronze(PipelineStep):

    def run(self):

        df = (
            self.spark.read
                .option("header", True)
                .option("inferSchema", True)
                .csv("/Volumes/training/bronze/sales_volume/orders.csv")
        )

        df = df.toDF(*[
            c.strip().lower()
            for c in df.columns
        ])

        row_count = df.count()

        df.write \
            .format("delta") \
            .mode("overwrite") \
            .saveAsTable("training.bronze.orders_raw")

        self.logger.info(
            f"Bronze loaded : {row_count} rows"
        )