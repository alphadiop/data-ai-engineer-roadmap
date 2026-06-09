from bronze.orders_bronze import OrdersBronze
from silver.orders_silver import OrdersSilver
from gold.revenue_gold import RevenueGold
from common.logger import PipelineLogger


class PipelineRunner:

    def __init__(self, steps):
        self.steps = steps

    def run(self):
        for step in self.steps:
            step.execute()


if __name__ == "__main__":

    logger = PipelineLogger("orders_pipeline")
    spark = spark
    runner = PipelineRunner([
        OrdersBronze(spark, logger),
        OrdersSilver(spark, logger),
        RevenueGold(spark, logger)
    ])

    runner.run()