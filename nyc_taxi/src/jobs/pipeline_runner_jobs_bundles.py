
import os

from pathlib import Path

import uuid
from datetime import datetime
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.delta_manager import DeltaManager
from pyspark.sql import SparkSession

import sys
from nyc_taxi.src.setup.create_tables import CreateTables
from nyc_taxi.src.setup.create_catalog import CreateCatalog

from nyc_taxi.src.bronze.uber_bronze import UberBronze
from nyc_taxi.src.silver.uber_silver import UberSilver
from nyc_taxi.src.gold.uber_gold import UberGold
from nyc_taxi.src.loader.data_loader import DataLoader

from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.pipeline_context import PipelineContext

from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.jobs.maintenance_job import MaintenanceJob

from nyc_taxi.src.utils.config.load_config import load_config

from nyc_taxi.src.common.spark_manager import SparkManager

from nyc_taxi.src.audit.audit_manager import AuditManager
from nyc_taxi.src.exception.exception_handler import DataNotAvailableError
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger


class PipelineRunner:
    """
    PipelineRunner
        ↓
    PipelineContext
        ↓
    Bronze
        ↓
    Silver
        ↓
    Gold
    """

    def __init__(self, spark, env, taxi_type, periode, catalog_name, logger, steps):
        self.spark = spark
        self.env = env
        self.taxi_type = taxi_type
        self.periode = periode
        self.catalog_name=catalog_name
        self.logger = logger
        self.steps = steps
        self.config = load_config('variable_environnement', self.logger)


    # def set_row_count(self,layer,count):
    #     self.row_count[layer] = count


    def run(self):

        context = PipelineContext(
            env=self.env,
            catalog_name=self.catalog_name,
            taxi_type=self.taxi_type
        )
        context.spark = self.spark
        context.logger = self.logger
        context.config = self.config[context.env]

        context.env = self.env
        context.taxi_type = self.taxi_type
        context.catalog_name = self.catalog_name
        context.periode = int(self.periode)

        catalog_manager = CatalogManager(
            spark = self.spark,
            logger=self.logger,
            env=context.env
        )

        self.logger.info(
            f"context.env = {context.env}"
        )

        self.logger.info(
            f"CATALOG : {context.config['catalog_name']}"
        )

        catalog_manager.create_catalog(
            catalog_name=context.config["catalog_name"]
        )
        catalog_manager.create_environment_schemas()

        audit_manager = AuditManager(
            spark=self.spark, 
            logger=self.logger
        )

        context.run_id = int(datetime.now().timestamp())
        context.start_time = datetime.now()
        context.table_name = "silver_nyc_taxi"

        self.logger.info(f"liste steps : {self.steps}")


        self.logger.info(f"{'='*120}")
        self.logger.info(
            f"context.row_count = {context.row_count}"
        )

        # self.logger.info(f"{'='*120}")
        # self.logger.info(
        #     f"Run pipeline {'='*12}"
        #     f"periode={context.periode}"
        #     f"taxi_type={context.taxi_type}"
        #     f"taxi_type={context.table_name}"
        # )

        self.logger.info(f"{'='*120}")
        self.logger.info(
            f"{'*' * 25} periode : {context.periode}, type = {type(context.periode)}"
        )
        self.logger.info(f"{'*' * 20} taxi_type : {context.taxi_type} {'*' * 20} ")
        self.logger.info(f"{'*' * 20} periode : {context.periode} {'*' * 20} ")
        self.logger.info(f"{'*' * 20} table_name : {context.table_name} {'*' * 20} ")
        self.logger.info(f"{'='*120}")

        if audit_manager.is_period_loaded(context):

            context.status = "ALREADY_LOADED"
            context.message = f"Period {context.periode} already loaded"
            self.logger.info(
                f"Period {context.periode} already loaded {'=' * 85 }"
            )
            self.logger.info(f"{'='*120}")
            return
        
        try:

            for step in self.steps:
                context.current_step = step.__class__.__name__
                self.logger.info(f"{'*' * 45} Starting {context.current_step} {'*' * 45}")

                step.run(context)
                
                self.logger.info(f"{'*' * 45} Finished {context.current_step} {'*' * 45}")
                self.logger.info(f"{'='*120}")

            context.status = "SUCCESS"
            context.message = "OK"
            context.error_step = ""

            MaintenanceJob(
                spark=self.spark,
                logger=self.logger).run(context)
            
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
            try:
                audit_manager.insert_audit(context)
            except Exception as e:
                self.logger.error(
                    f"Audit insert failed: {e}"
                )
            try:
                audit_manager.insert_row_counts(context)
            except Exception as e:
                self.logger.error(
                    f"Row count insert failed: {e}"
                )
        return context

if __name__ == "__main__":
    # Je rend le paramètre periode optionnel car il est renseigné automatiquement à partir de la table audit
    from pyspark.sql import SparkSession
    from delta import configure_spark_with_delta_pip
    #spark = SparkManager.get_spark()

    import argparse

    catalog_name = "nyc_taxi"
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["local", "databricks"],default='local')
    parser.add_argument("--periode", type=int, required=True)
    parser.add_argument("--taxi_type", type=str, default="yellow")


    args = parser.parse_args()

    env = args.env
    periode = args.periode
    taxi_type = args.taxi_type

    logger = PipelineLogger("uber_pipeline")
    logger.info(f"env = {env}")

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        env=env,
        logger=logger
    )

    spark = spark_manager.get_spark()

    logger.info(f"sys.argv  : {sys.argv}")
    logger.info(f"env       : {env}")
    logger.info(f"args      : {args}")
    logger.info(f"periode   : {periode}")
    logger.info(f"taxi_type : {taxi_type}")

    runner = PipelineRunner(
        spark=spark,
        env= env,
        taxi_type = taxi_type,
        periode = periode,
        catalog_name = catalog_name,
        logger=logger,
        steps=[
            CreateCatalog(
                spark=spark,
                logger=logger
            ),
            CreateTables(
                spark=spark,
                logger=logger
            ),
            UberBronze(
                spark=spark,
                logger=logger,
            ),
            UberSilver(
                spark=spark,
                logger=logger
            ),
            UberGold(
                spark=spark,
                logger=logger
            ),
            DataLoader(
                spark=spark,
                logger=logger
            )
        ]
    )

    runner.run()
    
    ## bash : python pipeline_runner.py --taxi_type yellow --periode 202603
