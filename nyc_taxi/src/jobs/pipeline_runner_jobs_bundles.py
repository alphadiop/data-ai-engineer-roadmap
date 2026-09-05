
import logging
from datetime import datetime
from typing import TYPE_CHECKING
import sys

from nyc_taxi.src.setup.environment_setup import EnvironmentSetup

from nyc_taxi.src.bronze.uber_bronze import UberBronze
from nyc_taxi.src.silver.uber_silver import UberSilver
from nyc_taxi.src.gold.uber_gold import UberGold
from nyc_taxi.src.loader.data_loader import DataLoader

from nyc_taxi.src.logger.logger import PipelineLogger
from nyc_taxi.src.common.pipeline_context import PipelineContext
from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.admin.metastore_repair import MetastoreRepair
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.jobs.maintenance_job import MaintenanceJob

from nyc_taxi.src.utils.config.load_config import load_config

from nyc_taxi.src.audit.audit_manager import AuditManager
from nyc_taxi.src.exception.exception_handler import DataNotAvailableError


if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger


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

    def __init__(self, spark, env, taxi_type="yellow", periode=None, logger=None, steps=None):
        self.spark = spark
        self.env = env
        self.taxi_type = taxi_type
        self.periode = periode
        self.logger = logger or logging.getLogger(__name__)
        self.steps = steps

        self.audit_manager = AuditManager(
            spark=self.spark,
            logger=self.logger
        )

        self.config = load_config(
            'variable_environnement', self.logger
        )


    def run(self):

        # ==========================================================
        # DÉTERMINATION DE LA PÉRIODE
        # ==========================================================
        if self.periode is None:

            self.periode = self.audit_manager.get_next_period(
                table_name="silver_nyc_taxi",
                taxi_type=self.taxi_type
            )
            self.logger.info(
                f"Période déterminée automatiquement : "
                f"{self.periode}"
            )
        else:
            self.logger.info(
                f"Période fournie explicitement : "
                f"{self.periode}"
            )

        # ==========================================================
        # CONTEXTE
        # ==========================================================

        context = PipelineContext(
            env=self.env,
            taxi_type=self.taxi_type
        )

        # ==========================================================
        # PIPELINE
        # ==========================================================
        context.spark = self.spark
        context.logger = self.logger

        # Configuration de l'environnement
        context.config = self.config[context.env]

        context.env = self.env
        context.taxi_type = self.taxi_type
        context.periode = int(self.periode)

        self.logger.info(
            f"Période sélectionnée automatiquement : "
            f"{context.periode}"
        )
        self.logger.info(
            f"path_sql_schema : {context.config['path_sql_schema']}"
        )

        self.logger.info(
            f"Environnement = {context.env}"
        )
        self.logger.info(
            f"catalog_name : {context.config['catalog_name']}"
        )

        context.run_id = int(datetime.now().timestamp())
        context.start_time = datetime.now()
        context.table_name = "silver_nyc_taxi"

        ## self.logger.info(f"liste steps : {self.steps}")

        self.logger.info(f"\n {'='*120}")
        self.logger.info(
            f"context.row_count = {context.row_count}"
        )

        self.logger.info(f"\n {'='*120}")
        self.logger.info(
            f"{'*' * 25} periode : {context.periode}"
        )
        self.logger.info(f"{'*' * 20} taxi_type : {context.taxi_type} {'*' * 20} ")
        self.logger.info(f"{'*' * 20} periode : {context.periode} {'*' * 20} ")
        self.logger.info(f"{'*' * 20} table_name : {context.table_name} {'*' * 20} ")
        self.logger.info(f"{'='*120}")

        if self.audit_manager.is_period_loaded(context):

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
            context.duration_seconds = (
                    context.end_time - context.start_time
            ).total_seconds()

            try:
                self.audit_manager.insert_audit(context)
            except Exception as e:
                self.logger.error(
                    f"Audit insert failed: {e}"
                )
            try:
                self.audit_manager.insert_row_counts(context)
            except Exception as e:
                self.logger.error(
                    f"Row count insert failed: {e}"
                )

            # ==========================================================
            # FINALISATION DU FICHIER DE LOG
            # ==========================================================
            self.logger.finalize(
                success=context.status == "SUCCESS"
            )

        return context

if __name__ == "__main__":
    # Je rend le paramètre periode optionnel car il est renseigné automatiquement à partir de la table audit
    from pyspark.sql import SparkSession
    from delta import configure_spark_with_delta_pip
    #spark = SparkManager.get_spark()

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["local", "databricks"],default='local')
    parser.add_argument("--periode", type=int, default=None)
    parser.add_argument("--taxi_type", type=str, default="yellow")


    args = parser.parse_args()

    env = args.env
    periode = args.periode
    taxi_type = args.taxi_type

    logger = PipelineLogger(
        name="pipeline_runner",
        env=args.env,
        periode=args.periode,
        taxi_type=args.taxi_type
    )

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        env=env,
        logger=logger
    )

    spark = spark_manager.get_spark()

    repair = MetastoreRepair(
        spark=spark,
        env=args.env,
        logger=logger
    )
    repair.repair()

    # =====================================================
    # DEBUG METASTORE
    # =====================================================
    logger.info("===============DEBUG METASTORE=============")
    # spark.sql("SHOW DATABASES").show(200, truncate=False)
    # spark.sql("SHOW TABLES IN audit").show(200, truncate=False)


    # =====================================================
    # PIPELINE
    # =====================================================
    logger.info("===============PIPELINE=============")
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
        logger=logger,

        steps=[
            EnvironmentSetup(
                spark=spark,
                env=env,
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
            ),
            MaintenanceJob(
                spark=spark,
                logger=logger
            )
        ]
    )
    runner.run()
    
    ## bash : python pipeline_runner.py --taxi_type yellow --periode 202603
    # next_period = audit_manager.get_next_period(
    #     table_name="silver_nyc_taxi",
    #     taxi_type="yellow"
    # )
