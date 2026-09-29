from pathlib import Path

from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager


from nyc_taxi.src.utils.load_json import load_json

from nyc_taxi.src.utils.sql_schema.build_schema import build_schema
from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.decorators import log_execution
from nyc_taxi.src.common.pipeline_context import PipelineContext

class EnvironmentSetup(PipelineStep):
    """
    Initialise complètement l'environnement.
    c'est une opération d'initialisation.

    - création du catalogue
    - création des schémas
    - création des tables Delta
    - réparation du metastore local

    attention faut initialiser l'environnement avant de chercher à acceder aux tables

    """

    def __init__(
            self,
            spark,
            env="local",
            logger=None
    ):
        super().__init__(spark,self.__class__.__name__)

        self.spark = spark
        self.env = env
        self.logger = logger

        self.catalog_manager = CatalogManager(
            spark=spark,
            env=env,
            logger=logger
        )

        self.delta_manager = DeltaManager(
            spark=spark,
            catalog_manager=self.catalog_manager,
            logger=logger
        )

    @log_execution
    def run(self,context):

        self.logger.separator(
            "ENVIRONMENT SETUP"
        )

        context.path_sql_schema = Path(
            context.config["path_sql_schema"]
        )

        if self.environment_exists():

            self.logger.success(
                "Environment already initialized"
            )

            if self.env == "local":
                self.repair_metastore()
            return

        self.logger.separator(
            "ENVIRONMENT INITIALIZATION"
        )

        self.create_catalog(
            context.config
        )
        self.create_schemas()

        self.create_tables(
            config=context.config,
            taxi_type=context.taxi_type
        )

        # ----------------------------------------------------------
        # Metastore
        # ----------------------------------------------------------
        if self.env in ("local", "docker"):
            self.repair_metastore()

        self.logger.success(
            "Environment initialization completed"
        )


    def environment_exists(self):
        required_tables = [
            ("audit", "audit_load"),
            ("audit", "audit_row_count"),
            ("silver", "silver_nyc_taxi"),
            ("ref", "dim_date"),
            ("gold", "gold_fact_trips"),
            ("gold", "gold_kpi_daily")
        ]

        for schema_name, table_name in required_tables:
            full_table_name = (
                self.catalog_manager.get_table_name(
                    schema_name=schema_name,
                    table_name=table_name
                )
            )

            self.logger.metric(
                "Check table",
                full_table_name
            )


            if not self.spark.catalog.tableExists(
                    full_table_name
            ):
                self.logger.warning(
                    f"Missing table : {full_table_name}"
                )
                return False
        return True


    def create_catalog(self, config):
        if self.env in ("local", "docker"):
            if self.logger:
                self.logger.info(
                    "Local mode : catalogue ignoré"
                )
            return

        self.catalog_manager.create_catalog(
            catalog_name=config["catalog_name"]
        )


    def create_schemas(self):
        if self.logger:
            self.logger.info(
                "Création des schémas"
            )
        self.catalog_manager.create_environment_schemas()


    def create_tables(self, config, taxi_type):

        tables = [
            ("audit", "audit_load", None),
            ("audit", "audit_row_count", None),

            ("silver", "silver_nyc_taxi", "periode"),
            ("gold", "gold_fact_trips", "periode"),
            ("gold", "gold_kpi_daily", "periode"),

            ("ref", "dim_date", None),
            ("ref", "ref_dim_location", None)
        ]

        for schema_name, table_name, partition_by in tables:

            self.create_table(
                path_sql_schema=config['path_sql_schema'],
                taxi_type=taxi_type,
                schema_name=schema_name,
                table_name=table_name,
                partition_by=partition_by
            )

    def create_table(
            self,
            path_sql_schema,
            taxi_type,
            schema_name,
            table_name,
            partition_by=None
    ):

        schema = self.get_schema(
            path_sql_schema=path_sql_schema,
            taxi_type=taxi_type,
            table_name=table_name
        )

        self.logger.metric(
            "Create table",
            f"{schema_name}.{table_name}"
        )

        self.delta_manager.create_table(
            schema_name=schema_name,
            table_name=table_name,
            schema=schema,
            partition_by=partition_by,
            drop_table=False
        )

    def get_schema(
            self,
            path_sql_schema,
            taxi_type,
            table_name
    ):

        schema_file = (
                Path(path_sql_schema)
                / taxi_type
                / f"{table_name}.json"
        )


        self.logger.metric(
            "Schema file",
            schema_file
        )

        schema_json = load_json(
            schema_file
        )

        return build_schema(
            schema_json
        )

    def repair_metastore(self):
        self.logger.separator(
            "METASTORE REPAIR"
        )
        self.catalog_manager.repair_local_metastore()


if __name__=='__main__':
    env="local"
    taxi_type = "yellow"

    logger = PipelineLogger(
        name="Setup",
        env=env
    )
    spark = SparkManager(
        app_name="Setup",
        env=env,
        logger=logger
    ).get_spark()

    context = PipelineContext(
        env=env,
        taxi_type=taxi_type
    )
    EnvironmentSetup(
        spark=spark,
        env="local",
        logger=logger
    ).run(context)

