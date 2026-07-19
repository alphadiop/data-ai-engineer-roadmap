import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from bronze.uber_bronze import UberBronze
from silver.uber_silver import UberSilver
from gold.uber_gold import UberGold

from common.logger import PipelineLogger
from common.pipeline_context import PipelineContext
from common.decorators import log_execution
from common.delta_manager import DeltaManager

from audit.audit_manager import AuditManager

from pyspark.sql import SparkSession
from datetime import datetime

class PipelineRunner:

    def __init__(self, spark,logger,steps):
        self.spark = spark
        self.logger = logger
        self.steps = steps


    def run(self):

        context = PipelineContext()

        context.start_time = datetime.now()

        bronze_step = self.steps[0]
        context.periode = bronze_step.periode
        context.taxi_type = bronze_step.taxi_type
        context.table_name = "silver_nyc_taxi"

        self.logger.info(f"periode = {context.periode}")
        self.logger.info(f"table_name = {context.table_name}")
        self.logger.info(f"taxi_type = {context.taxi_type}")
    
        audit_manager = AuditManager(
            spark=self.spark, 
            logger=self.logger
        )

        if audit_manager.is_period_loaded(context):
            self.logger.info(
                f"Period {context.periode} already loaded {'=' * 85 }"
            )
            return context
        
        try:

            for step in self.steps:
                self.logger.info(f"{'*' * 55} Starting {step.__class__.__name__} {'*' * 55}")

                step.run(context)
                
                self.logger.info(f"{'*' * 55} Finished {step.__class__.__name__} {'*' * 55}")
                self.logger.info(f"{'='*120}")

            context.status = "SUCCESS"
            context.message = "OK"
            
        except Exception as e:
            context.status = "ERROR"
            context.message = str(e)
            context.row_count["silver"] = 0
            self.logger.error(f"{'*' * 12} Error in pipeline : {e} {'*'*12}")

            raise

        finally:

            context.end_time = datetime.now()
            context.duration_seconds = (context.end_time - context.start_time).total_seconds()
            audit_manager.insert_audit(context)
            
            self.logger.info(f"periode = {context.periode}")
            self.logger.info(f"table_name = {context.table_name}")
            self.logger.info(f"taxi_type = {context.taxi_type}")
            self.logger.info(f"row_count = {context.row_count}")
        return context



if __name__ == "__main__":
    path_volume = "/Volumes/nyc_taxi/bronze/raw_files"
    taxi_type = "yellow"
    #taxi_type = "green"
    #taxi_type = "fhv"
    ## spark = SparkSession.builder.appName("MyDatabricksApp").getOrCreate()
    logger = PipelineLogger("uber_pipeline")
    
    runner = PipelineRunner(
        spark=spark,
        logger=logger,
        steps=[
            UberBronze(
                spark=spark, 
                path_volume=path_volume, 
                taxi_type=taxi_type, 
                periode=202508, 
                logger=logger
            ),
            UberSilver(
                spark=spark, 
                logger=logger
            ),
            UberGold(
                spark=spark, 
                logger=logger
            )
        ])
    runner.run()
    
    #context = runner.run()
    #print(context.df_bronze.count())
    #print(context.df_silver.count())
