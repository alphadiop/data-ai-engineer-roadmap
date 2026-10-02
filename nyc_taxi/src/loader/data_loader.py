

from nyc_taxi.src.common.path_manager import PathManager
from nyc_taxi.src.common.schema_manager import SchemaManager
from nyc_taxi.src.common.catalog_manager import CatalogManager
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.utils.load_json import load_json

from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.decorators import log_execution
from pathlib import Path
from pyspark.sql.functions import lit
from pyspark.sql.functions import spark_partition_id

class DataLoader(PipelineStep):
    """
    Valide les schémas,
    calcule les row counts,
    charge les données dans Delta.
    """

    def __init__(self, spark, logger=None):

        super().__init__(spark, self.__class__.__name__)

        self.spark = spark
        self.logger = logger

    @log_execution
    def run(self, context):

        # ==========================================================
        # DELTA MANAGER
        # ==========================================================

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

        # ==========================================================
        # TABLES
        # ==========================================================

        tables = [
            (
                "silver",
                "silver_nyc_taxi",
                context.df_silver
            ),
            (
                "gold",
                "gold_fact_trips",
                context.df_fact_trips
            ),
            (
                "ref",
                "dim_date",
                context.df_dim_date
            ),
            (
                "gold",
                "gold_kpi_daily",
                context.df_kpi_daily
            )
        ]

        # ==========================================================
        # TABLES PARTITIONNÉES PAR PERIODE
        # ==========================================================

        partitioned_tables = {
            "silver_nyc_taxi",
            "gold_fact_trips",
            "gold_kpi_daily"
        }

        # ==========================================================
        # TRAITEMENT
        # ==========================================================

        for schema_name, table_name, df in tables:

            row_count = df.count()

            self.logger.separator(
                f"LOAD : {schema_name}.{table_name}"
            )

            self.logger.metric(
                "Rows before load",
                f"{row_count:,}".replace(",", " ")
            )

            self.logger.metric(
                "Period",
                context.periode
            )

            # ======================================================
            # PERIODE
            # ======================================================

            if table_name in partitioned_tables:

                if "periode" not in df.columns:

                    self.logger.info(
                        f"Adding period column : "
                        f"periode={context.periode}"
                    )

                    df = df.withColumn(
                        "periode",
                        lit(context.periode).cast("int")
                    )

                else:

                    self.logger.info(
                        "Period column already present"
                    )

            # ======================================================
            # VALIDATION SCHEMA
            # ======================================================

            self.logger.subsection(
                f"SCHEMA VALIDATION : {table_name}"
            )

            df = self.validate_schema(
                context=context,
                table_name=table_name,
                df=df
            )

            self.logger.success(
                f"Schema validated : {table_name}"
            )

            # ======================================================
            # ROW COUNT
            # ======================================================

            row_count = df.count()

            context.row_count[table_name] = row_count

            self.logger.metric(
                "Rows to write",
                f"{row_count:,}".replace(",", " ")
            )

            # ======================================================
            # WRITE DELTA
            # ======================================================

            self.logger.subsection(
                f"DELTA WRITE : {schema_name}.{table_name}"
            )

            if table_name in partitioned_tables:

                self.logger.metric(
                    "Write mode",
                    "Overwrite partition"
                )

                self.logger.metric(
                    "Partition",
                    f"periode={context.periode}"
                )

            else:

                self.logger.metric(
                    "Write mode",
                    "Standard"
                )

            self.logger.info(
                f"Writing Delta table : {table_name}"
            )
            delta_manager.sauvegarde_tables_delta(
                df=df,
                schema_name=schema_name,
                table_name=table_name,
                periode=context.periode,
                replace=True
            )

            self.logger.success(
                f"Delta write completed : "
                f"{schema_name}.{table_name}"
            )
            self.logger.success(
                f"{table_name} loaded"
            )

    def validate_schema(
            self,
            context,
            table_name,
            df
    ):

        # ==========================================================
        # SCHEMA
        # ==========================================================

        schema_manager = SchemaManager(
            spark=self.spark,
            logger=self.logger
        )

        path_manager = PathManager(
            context=context
        )

        schema_file = path_manager.schema_path(
            context.taxi_type,
            table_name
        )

        self.logger.info(
            f"Schema file : {schema_file}"
        )

        schema_json = load_json(schema_file)

        # ==========================================================
        # APPLICATION DU SCHEMA
        # ==========================================================

        df = schema_manager.apply_schema(
            df=df,
            schema_json=schema_json
        )

        # ==========================================================
        # VALIDATION DES COLONNES
        # ==========================================================
        self.logger.info(
            f"Schema validation started : {table_name}"
        )
        schema_manager.validate_columns(
            df=df,
            schema_json=schema_json
        )

        self.logger.success(
            f"Schema valid : {table_name}"
        )


        num_partitions = (
            df.select(spark_partition_id())
            .distinct()
            .count()
        )

        self.logger.info(
            f"Nombre de partitions : {num_partitions}"
        )
        return df
