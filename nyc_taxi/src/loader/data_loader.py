from nyc_taxi.src.common.path_manager import PathManager
from nyc_taxi.src.common.schema_manager import SchemaManager
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.utils.load_json import load_json
import logging
from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.decorators import log_execution
from pathlib import Path

class DataLoader(PipelineStep):
    """
    Valide les schémas,
    calcule les row counts,
    charge les données dans Delta.
    """

    def __init__(self,spark,logger=None):

        super().__init__(spark,self.__class__.__name__)

        self.spark = spark
        self.logger = logger


    @log_execution
    def run(self, context):

        catalog_manager = CatalogManager(
            spark=self.spark,
            env=context.env,
            logger=self.logger
        )

        delta_manager = DeltaManager(
            spark=self.spark,
            catalog_manager=catalog_manager,
            logger=self.logger
        )

        tables = [
            ("silver", "silver_nyc_taxi", context.df_silver),
            ("gold", "gold_fact_trips", context.df_fact_trips),
            ("gold", "gold_dim_date", context.df_dim_date),
            ("gold", "gold_kpi_daily", context.df_kpi_daily)
        ]

        for schema_name, table_name, df in tables:

            # récupérer le DataFrame éventuellement casté
            df = self.validate_schema(
                context=context,
                table_name=table_name,
                df=df
            )
            #df.persist()

            row_count = df.count()

            context.row_count[table_name] = row_count

            self.logger.info(
                f"{table_name} : {row_count} rows"
            )

            # self.logger.info(
            #     f"Partitions : {df.rdd.getNumPartitions()}"
            # )

            self.logger.info(f"START WRITE {table_name}")
            delta_manager.sauvegarde_tables_delta(
                df=df,
                schema_name=schema_name,
                table_name=table_name,
                periode=context.periode,
                replace=True
            )
            self.logger.info(f"END WRITE {table_name}")
            #df.unpersist()


    def validate_schema(
            self,
            context,
            table_name,
            df
    ):
        log_path = Path(context.config["path_logs"])

        self.logger.info(f"=============validate_schema=================")
        self.logger.info(f"path_logs = {log_path}")
        self.logger.info(f"exists = {log_path.exists()}")
        self.logger.info(f"is_dir = {log_path.is_dir()}")
        self.logger.info(f"=============validate_schema=================")

        schema_manager = SchemaManager(
            spark=self.spark,
            logger=self.logger
        )

        path_manager = PathManager(
            config=context.config,
            logger=self.logger
        )

        schema_file = path_manager.schema_path(
            context.taxi_type,
            table_name
        )

        self.logger.info(
            f"Validation schema : {schema_file}"
        )

        schema_json = load_json(schema_file)

        # récupérer le DataFrame retourné par SchemaManager
        df = schema_manager.apply_schema(
            df=df,
            schema_json=schema_json
        )

        schema_manager.validate_columns(
            df=df,
            schema_json=schema_json
        )

        self.logger.info(
            f"Schema valide pour {table_name}"
        )

        return df


