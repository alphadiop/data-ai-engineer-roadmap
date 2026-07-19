import os
import sys

PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.delta_manager import DeltaManager
from utils.sql_schema.build_schema import build_schema
from utils.sql_schema.get_columns_from_schema import get_columns_from_schema
from utils.load_json import load_json



class CreateTables:

    path_sql_schema = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/src/nyc/schema/"

    def __init__(self, spark, logger):
        self.spark = spark
        self.logger = logger


    def run(self):

        tables = [
            ("audit", "audit_load", None),
            ("audit", "audit_row_count", None),
            ("gold", "gold_dim_date", None),
            ("gold", "gold_dim_location", None),
            ("gold", "gold_kpi_daily", None),
            ("gold", "gold_fact_trips", "periode"),
            ("silver", "silver_nyc_taxi", "periode")
        ]

        delta_manager = DeltaManager(
            spark=self.spark,
            logger=self.logger
        )

        for schema_name, table_name, partition_by in tables:

            delta_manager.create_table(
                schema_name=schema_name,
                table_name=table_name,
                schema=self.get_schema(
                        self.path_sql_schema,
                        "yellow",
                        table_name
                ),
                partition_by=partition_by,
                drop_table=True
            )


    def get_schema(self, path_sql_schema, type_taxi, table_name):
        path = os.path.join(
            path_sql_schema,
            type_taxi,
            f"{table_name}.json"
        )

        schema_json = load_json(path)
        return build_schema(schema_json)


