import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import uuid
from datetime import datetime

from setup.create_tables import CreateTables
from setup.create_catalog import CreateCatalog

from bronze.uber_bronze import UberBronze
from silver.uber_silver import UberSilver
from gold.uber_gold import UberGold

from common.logger import PipelineLogger
from common.pipeline_context import PipelineContext
from common.decorators import log_execution
from common.delta_manager import DeltaManager

from jobs.maintenance_job import MaintenanceJob

from audit.audit_manager import AuditManager

from pyspark.sql import SparkSession
from datetime import datetime

class PipelineRunner:

    path_sql_schema = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc/schema/"

    def __init__(self, spark,logger,steps):
        self.spark = spark
        self.logger = logger
        self.steps = steps


    def run(self):

        #### CreateTables(spark=self.spark, logger=self.logger).run() ## A faire une fois

        context = PipelineContext()

        ### context.run_id = str(uuid.uuid4())
        context.run_id = int(datetime.now().timestamp())
        context.start_time = datetime.now()
        context.type_taxi = "yellow"

        bronze_step = self.steps[0]

        context.periode = bronze_step.periode

        self.logger.info(
            f"periode = {context.periode}, type = {type(context.periode)}"
        )
        
        context.taxi_type = bronze_step.taxi_type
        context.table_name = "silver_nyc_taxi"

        self.logger.info(f"{'*' * 25} periode = {context.periode} {'*' * 25} ")
        self.logger.info(f"{'*' * 25} table_name = {context.table_name} {'*' * 25} ")
        self.logger.info(f"{'*' * 25} taxi_type = {context.taxi_type} {'*' * 25} ")

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
                context.current_step = step.__class__.__name__
                self.logger.info(f"{'*' * 55} Starting {context.current_step} {'*' * 55}")

                step.run(context)
                
                self.logger.info(f"{'*' * 55} Finished {context.current_step} {'*' * 55}")
                self.logger.info(f"{'='*120}")

            context.status = "SUCCESS"
            context.message = "OK"
            context.error_step = ""

            MaintenanceJob(
                spark=self.spark,
                logger=self.logger
            ).run()
            
        except Exception as e:
            context.status = "ERROR"
            context.error_step = context.current_step
            context.message = str(e)

            self.logger.error(
                f"Error in pipeline : {e}"
            )

            raise

        finally:
            context.end_time = datetime.now()
            context.duration_seconds = (context.end_time - context.start_time).total_seconds()

            audit_manager.insert_audit(context)
            audit_manager.insert_row_counts(context)
            
        return context


if __name__ == "__main__":
    path_volume = "/Volumes/nyc_taxi/bronze/raw_files"
    taxi_type = "yellow"
    #taxi_type = "green"
    #taxi_type = "fhv"
    ### spark = SparkSession.builder.appName("MyDatabricksApp").getOrCreate()

    logger = PipelineLogger("uber_pipeline")
    
    runner = PipelineRunner(
        spark=spark,
        logger=logger,
        steps=[
            UberBronze(
                spark=spark, 
                path_volume=path_volume, 
                taxi_type=taxi_type, 
                periode=202505, 
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
