import logging
from datetime import datetime
import sys
import argparse

from nyc_taxi.src.setup.environment_setup import EnvironmentSetup

from nyc_taxi.src.bronze.uber_bronze import UberBronze
from nyc_taxi.src.silver.uber_silver import UberSilver
from nyc_taxi.src.gold.uber_gold import UberGold
from nyc_taxi.src.loader.data_loader import DataLoader

from nyc_taxi.src.common.pipeline_context import PipelineContext
from nyc_taxi.src.common.spark_manager import SparkManager
from nyc_taxi.src.common.catalog_manager import CatalogManager

from nyc_taxi.src.admin.metastore_repair import MetastoreRepair
from nyc_taxi.src.jobs.maintenance_job import MaintenanceJob

from nyc_taxi.src.utils.config.load_config import load_config

from nyc_taxi.src.audit.audit_manager import AuditManager
from nyc_taxi.src.exception.exception_handler import DataNotAvailableError
from nyc_taxi.src.table_reference.load_tab_ref import ReferenceDataLoader
from nyc_taxi.src.logger.logger import PipelineLogger


class PipelineRunner:
    """
    PipelineRunner
        │
        ├── _determine_period()
        ├── _build_context()
        ├── _check_already_loaded()
        ├── _execute_steps()
        └── run()
    """

    def __init__(
            self,
            spark,
            env,
            taxi_type="yellow",
            periode=None,
            logger=None,
            steps=None
    ):
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
            file_name="variable_environnement",
            env=self.env,
            logger=self.logger
        )

        self.catalog_manager = CatalogManager(
            spark=self.spark,
            logger=self.logger,
            env=self.env
        )

        self.environment_setup = EnvironmentSetup(
            spark=self.spark,
            env=self.env,
            logger=self.logger
        )

    def run(self):

        pipeline_error = None

        # ==========================================================
        # INITIALISATION / VERIFICATION ENVIRONNEMENT
        # ==========================================================

        self.logger.separator(
            "PIPELINE INITIALIZATION"
        )

        context = self._build_context()

        self.environment_setup.run(context)

        self.logger.success(
            "Environment ready"
        )

        self.logger.separator(
            "ENVIRONMENT CHECK"
        )

        self.logger.metric(
            "audit.audit_load",
            self.spark.catalog.tableExists("audit.audit_load")
        )

        self.logger.metric(
            "audit.audit_row_count",
            self.spark.catalog.tableExists("audit.audit_row_count")
        )

        # ==========================================================
        # DÉTERMINATION DE LA PÉRIODE
        # ==========================================================

        self._determine_period()

        # ==========================================================
        # CONTRÔLE : PÉRIODE DÉJÀ CHARGÉE
        # ==========================================================

        self.logger.subsection(
            "LOAD CONTROL"
        )

        self._check_already_loaded(context)

        # ==========================================================
        # EXÉCUTION DU PIPELINE
        # ==========================================================

        self.logger.separator(
            "PIPELINE EXECUTION"
        )

        try:

            self._execute_steps(context)

            # Toutes les étapes ont réussi
            context.status = "SUCCESS"
            context.message = "OK"
            context.error_step = ""

        # ==========================================================
        # DONNÉES ABSENTES
        # ==========================================================

        except DataNotAvailableError as e:

            context.status = "NO_DATA"
            context.error_step = getattr(
                context,
                "current_step",
                "PipelineRunner"
            )
            context.message = str(e)

            pipeline_error = e

            self.logger.warning(
                f"No data available | "
                f"step={context.error_step} | "
                f"message={context.message}"
            )

        # ==========================================================
        # ERREUR PIPELINE
        # ==========================================================

        except Exception as e:

            context.status = "ERROR"
            context.error_step = getattr(
                context,
                "current_step",
                "PipelineRunner"
            )
            context.message = str(e)

            pipeline_error = e

            self.logger.error(
                f"Pipeline error | "
                f"step={context.error_step} | "
                f"message={context.message}"
            )

        # ==========================================================
        # FINALISATION
        # ==========================================================

        finally:

            context.end_time = datetime.now()

            context.duration_seconds = (
                    context.end_time - context.start_time
            ).total_seconds()

            # ------------------------------------------------------
            # AUDIT
            # ------------------------------------------------------

            self.logger.subsection(
                "AUDIT"
            )

            try:

                audit_table = self.catalog_manager.audit_load()

                self.audit_manager.delete_period(
                    audit_table,
                    self.periode
                )

                self.audit_manager.insert_audit(context)

                row_count_table = (
                    self.catalog_manager.audit_row_count()
                )

                self.audit_manager.delete_period(
                    row_count_table,
                    self.periode
                )

                self.audit_manager.insert_row_counts(context)

                self.logger.success(
                    "Audit completed"
                )

            except Exception as audit_error:

                self.logger.exception(
                    f"AuditManager failure: {audit_error}"
                )

                if context.status == "SUCCESS":
                    context.status = "ERROR"
                    context.error_step = "AuditManager"
                    context.message = str(audit_error)

                if pipeline_error is None:
                    pipeline_error = audit_error

            # ------------------------------------------------------
            # PIPELINE SUMMARY
            # ------------------------------------------------------

            self.logger.separator(
                "PIPELINE START"
            )
            self.logger.metric(
                "Run ID",
                context.run_id
            )

            self.logger.metric(
                "Environment",
                context.env
            )

            self.logger.metric(
                "Taxi Type",
                context.taxi_type
            )

            self.logger.metric(
                "Period",
                context.periode
            )

            self.logger.metric(
                "Status",
                context.status
            )

            self.logger.metric(
                "Duration",
                f"{context.duration_seconds:.2f}s"
            )

            if context.row_count:

                self.logger.subsection(
                    "ROW COUNTS"
                )

                for table_name, count in context.row_count.items():

                    self.logger.metric(
                        table_name,
                        f"{count:,}".replace(",", " ")
                    )

            self.logger.separator(
                f"PIPELINE FINALIZED - STATUS = {context.status}"
            )

            # ------------------------------------------------------
            # FINALISATION DU LOG
            # ------------------------------------------------------
            self.logger.finalize(
                success=context.status == "SUCCESS"
            )
            self.logger.separator(
                "PIPELINE SUMMARY"
            )
            self.logger.metric(
                "Run ID",
                context.run_id
            )

        if pipeline_error is not None:
            raise pipeline_error

        return context

    def _determine_period(self):
        """Détermination de la période."""

        if self.periode is None:

            self.periode = self.audit_manager.get_next_period(
                table_name="silver_nyc_taxi",
                taxi_type=self.taxi_type
            )

            self.logger.info(
                f"Period automatically determined : "
                f"{self.periode}"
            )

        else:

            self.logger.info(
                f"Period explicitly provided : "
                f"{self.periode}"
            )

    def _build_context(self):
        """Construction du contexte."""

        context = PipelineContext(
            env=self.env,
            taxi_type=self.taxi_type
        )

        context.spark = self.spark
        context.logger = self.logger
        context.config = self.config[context.env]

        context.env = self.env
        context.taxi_type = self.taxi_type
        context.periode = int(self.periode)

        context.run_id = int(datetime.now().timestamp())
        context.start_time = datetime.now()
        context.table_name = "silver_nyc_taxi"

        self.logger.subsection(
            "PIPELINE CONTEXT"
        )

        self.logger.metric(
            "Environment",
            context.env
        )

        self.logger.metric(
            "Taxi Type",
            context.taxi_type
        )

        self.logger.metric(
            "Period",
            context.periode
        )

        self.logger.metric(
            "Catalog",
            context.config["catalog_name"]
        )

        self.logger.metric(
            "Table",
            context.table_name
        )


        self.logger.metric(
            "SQL Schema Path",
            context.config["path_sql_schema"]
        )

        return context

    def _check_already_loaded(self, context):
        """Contrôle ALREADY_LOADED."""

        if self.audit_manager.is_period_loaded(context):

            context.status = "ALREADY_LOADED"

            context.message = (
                f"Period {context.periode} already loaded"
            )

            self.logger.info(
                f"Period {context.periode} already loaded"
            )

            return True

        self.logger.success(
            f"Period {context.periode} is not loaded"
        )

        return False

    def _execute_steps(self, context):
        """Exécution des étapes."""

        if not self.steps:

            raise RuntimeError(
                "PipelineRunner: aucune étape configurée."
            )

        total_steps = len(self.steps)

        for index, step in enumerate(self.steps, start=1):

            context.current_step = (
                step.__class__.__name__
            )

            start = datetime.now()

            self.logger.separator(
                f"STEP {index}/{total_steps} : "
                f"{context.current_step}"
            )

            step.run(context)

            duration = (
                    datetime.now() - start
            ).total_seconds()

            self.logger.success(
                f"{context.current_step} completed "
                f"in {duration:.2f}s"
            )


def main():
    # ==========================================================
    # ARGUMENTS
    # ==========================================================

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        choices=["local", "docker", "databricks"],
        default="local"
    )

    parser.add_argument(
        "--periode",
        type=int,
        default=None
    )

    parser.add_argument(
        "--taxi_type",
        type=str,
        default="yellow"
    )

    args = parser.parse_args()

    env = args.env
    periode = args.periode
    taxi_type = args.taxi_type

    # ==========================================================
    # LOGGER
    # ==========================================================

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type
    )

    # ==========================================================
    # SPARK
    # ==========================================================

    spark_manager = SparkManager(
        app_name="nyc_taxi_pipeline",
        env=env,
        logger=logger
    )

    spark = spark_manager.get_spark()

    # ==========================================================
    # METASTORE
    # ==========================================================

    repair = MetastoreRepair(
        spark=spark,
        env=env,
        logger=logger
    )

    repair.repair()

    # ==========================================================
    # LOGS DE LANCEMENT
    # ==========================================================

    logger.separator(
        "NYC TAXI PIPELINE"
    )

    logger.metric(
        "Environment",
        env
    )

    logger.metric(
        "Taxi Type",
        taxi_type
    )

    logger.metric(
        "Period",
        periode if periode is not None else "AUTO"
    )

    logger.metric(
        "Command",
        " ".join(sys.argv)
    )

    # ==========================================================
    # PIPELINE
    # ==========================================================

    runner = PipelineRunner(
        spark=spark,
        env=env,
        taxi_type=taxi_type,
        periode=periode,
        logger=logger,
        steps=[
            ReferenceDataLoader(
                spark=spark,
                env=env,
                logger=logger
            ),
            UberBronze(
                spark=spark,
                logger=logger
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

    context = runner.run()

    # ==========================================================
    # STATUT FINAL
    # ==========================================================

    if context.status not in {"SUCCESS", "ALREADY_LOADED"}:

        logger.error(
            f"PIPELINE FAILED | "
            f"status={context.status} | "
            f"periode={context.periode} | "
            f"error_step={context.error_step} | "
            f"message={context.message}"
        )

        return 1

    logger.success(
        f"PIPELINE COMPLETED | "
        f"status={context.status} | "
        f"periode={context.periode}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
