
from pathlib import Path
from nyc_taxi.src.common.delta_manager import DeltaManager
from nyc_taxi.src.utils.sql_schema.build_schema import build_schema
from nyc_taxi.src.utils.sql_schema.get_columns_from_schema import get_columns_from_schema
from nyc_taxi.src.utils.load_json import load_json
from nyc_taxi.src.common.catalog_manager import CatalogManager

class CreateTables:

    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger
        self.project_root = Path.cwd() / "nyc_taxi"


    def run(self, context):
        """ Faire attention à : drop_table=False ou True"""
        tables = [
            ("audit", "audit_load", None),
            ("audit", "audit_row_count", None),
            ("gold", "gold_dim_date", None),
            ("gold", "gold_dim_location", None),
            ("gold", "gold_kpi_daily", None),
            ("gold", "gold_fact_trips", "periode"),
            ("silver", "silver_nyc_taxi", "periode")
        ]

        catalog_manager = CatalogManager(
            spark = self.spark,
            logger=self.logger,
            env=context.env
        )

        delta_manager = DeltaManager(
            spark=self.spark,
            catalog_manager=catalog_manager,
            logger=self.logger
        )

        for schema_name, table_name, partition_by in tables:

            delta_manager.create_table(
                schema_name=schema_name,
                table_name=table_name,
                schema=self.get_schema(
                    context=context,
                    table_name=table_name
                ),
                partition_by=partition_by,
                drop_table=False
            )

    def get_schema(
            self,
            context,
            table_name
    ):
        path_schema = Path(context.config["path_sql_schema"])
        self.logger.info(f"path_schema: {path_schema}")
        schema_json = load_json(path_schema / context.taxi_type / f"{table_name}.json")
        return build_schema(schema_json)


