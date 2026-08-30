from pathlib import Path

from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.delta_manager import DeltaManager

from nyc_taxi.src.utils.config.load_config import load_config
from nyc_taxi.src.utils.load_json import load_json

from nyc_taxi.src.utils.sql_schema.build_schema import build_schema
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.spark_manager import SparkManager


class EnvironmentSetup:
    """
    Initialise complètement l'environnement.

    - création du catalogue
    - création des schémas
    - création des tables Delta
    - réparation du metastore local
    """

    def __init__(
            self,
            spark,
            env="local",
            logger=None
    ):
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

        self.config = load_config(
            "variable_environnement",
            logger
        )

    def run(
            self,
            path_sql_schema,
            taxi_type="yellow"
    ):

        if isinstance(path_sql_schema, str):
            path_sql_schema = Path(path_sql_schema)

        if self.logger:
            self.logger.info("=" * 80)
            self.logger.info("Initialisation environnement")
            self.logger.info("=" * 80)

        if self.env != "local":
            self.create_catalog()
        self.create_schemas()

        self.create_tables(
            path_sql_schema=path_sql_schema,
            taxi_type=taxi_type
        )

        if self.env == "local":
            self.repair_metastore()

        if self.logger:
            self.logger.info("=" * 80)
            self.logger.info("Initialisation terminée")
            self.logger.info("=" * 80)



    def create_catalog(self):

        if self.env == "local":

            if self.logger:
                self.logger.info(
                    "Local mode : catalogue ignoré"
                )

            return

        catalog_name = self.config[self.env]["catalog_name"]

        self.catalog_manager.create_catalog(
            catalog_name=catalog_name
        )


    def create_schemas(self):

        if self.logger:
            self.logger.info(
                "Création des schémas"
            )
        self.catalog_manager.create_environment_schemas()


    def create_tables(
            self,
            path_sql_schema,
            taxi_type
    ):

        tables = [
            ("audit", "audit_load", None),
            ("audit", "audit_row_count", None),

            ("silver", "silver_nyc_taxi", "periode"),

            ("gold", "gold_fact_trips", "periode"),
            ("gold", "gold_kpi_daily", "periode"),
            ("gold", "gold_dim_date", None),

            ("ref", "gold_dim_location", None)
        ]

        for schema_name, table_name, partition_by in tables:

            self.create_table(
                path_sql_schema=path_sql_schema,
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

        if self.logger:
            self.logger.info(
                f"Création table : {schema_name}.{table_name}"
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

        if self.logger:
            self.logger.info(
                f"Schema : {schema_file}"
            )

        schema_json = load_json(
            schema_file
        )

        return build_schema(
            schema_json
        )

    def repair_metastore(self):

        if self.logger:
            self.logger.info(
                "Réparation metastore local"
            )

        self.catalog_manager.repair_local_metastore()

if __name__=='__main__':

    logger = PipelineLogger("Setup")
    spark = SparkManager(
        app_name="Setup",
        env="local",
        logger=logger
    ).get_spark()

    EnvironmentSetup(
        spark=spark,
        env="local",
        logger=logger
    ).run(
        path_sql_schema="D:/data-ai-engineer-roadmap/nyc_taxi/schema",
        taxi_type="yellow"
    )
