import os
import sys


import uuid
from datetime import datetime

from nyc_taxi.src.setup.create_tables import CreateTables
from nyc_taxi.src.setup.create_catalog import CreateCatalog


from nyc_taxi.src.bronze.uber_bronze import UberBronze
from nyc_taxi.src.silver.uber_silver import UberSilver
from nyc_taxi.src.gold.uber_gold import UberGold

from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.pipeline_context import PipelineContext
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.common.catalog_manager import CatalogManager

from nyc_taxi.src.jobs.maintenance_job import MaintenanceJob

from nyc_taxi.src.audit.audit_manager import AuditManager
from nyc_taxi.src.exception.exception_handler import DataNotAvailableError


from pyspark.sql import SparkSession
from datetime import datetime



class PipelineRunner:

    path_sql_schema = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/schema/"

    def __init__(self, spark,logger,steps):
        self.spark = spark
        self.logger = logger
        self.steps = steps


    def run(self):

        ### CreateCatalog(spark=self.spark, logger=self.logger).run()
        ## CreateTables(spark=self.spark, logger=self.logger).run() ## A faire une fois

        context = PipelineContext()

        audit_manager = AuditManager(
            spark=self.spark, 
            logger=self.logger
        )

        context.run_id = int(datetime.now().timestamp())
        context.start_time = datetime.now()
        bronze_step = self.steps[0]
        context.taxi_type = "yellow"
        context.table_name = "silver_nyc_taxi"
        context.periode = bronze_step.periode

        self.logger.info(
            f"context.row_count = {context.row_count}"
        )
        
        self.logger.info(
            f"{'*' * 25} periode : {context.periode}, type = {type(context.periode)}"
        )
        self.logger.info(f"bronze_step.periode = {bronze_step.periode}")
        self.logger.info(f"{'*' * 25} taxi_type : {context.taxi_type} {'*' * 25} ")
        self.logger.info(f"{'*' * 25} periode : {context.periode} {'*' * 25} ")
        self.logger.info(f"{'*' * 25} table_name : {context.table_name} {'*' * 25} ")
        self.logger.info(f"{'*' * 2} path_schema : {self.path_sql_schema} {'*' * 5} ")


        if audit_manager.is_period_loaded(context):

            context.status = "ALREADY_LOADED"
            context.message = f"Period {context.periode} already loaded"
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
                logger=self.logger).run()
            
        except DataNotAvailableError as e:
            context.status = "NO_DATA"
            context.error_step = context.current_step
            context.message = str(e)
            self.logger.warning(str(e))

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
    # Je rend le parametre periode optionnel car il est renseigné automatiquement à partir de la table audit
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--periode", type=int, required=False)
    parser.add_argument("--taxi_type", type=str, default="yellow")

    args = parser.parse_args()

    periode = args.periode
    taxi_type = args.taxi_type

    logger = PipelineLogger("uber_pipeline")

    logger.info(f"sys.argv : {sys.argv}")
    logger.info(f"args      : {args}")
    logger.info(f"periode   : {periode}")
    logger.info(f"taxi_type : {taxi_type}")

    runner = PipelineRunner(
        spark=spark,
        logger=logger,
        steps=[
            UberBronze(
                spark=spark,
                taxi_type=taxi_type,
                periode=periode,
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
        ]
    )

    runner.run()
    
    ## bash : python pipeline_runner.py --taxi_type yellow --periode 202603
