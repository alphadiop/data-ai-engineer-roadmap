from pyspark.sql import DataFrame, SparkSession
from typing import Any
from datetime import datetime
class PipelineContext:

    def __init__(
            self,
            env:str = "local",
            taxi_type: str | None = None,
    )-> None:
        self.error_step: str | None = None
        self.env = env
        self.taxi_type: str | None = taxi_type

        self.spark: SparkSession | None = None
        self.logger: Any | None = None
        self.config: dict[str, Any] | None = None

        self.periode: int | str | None = None
        self.table_name: str | None = None

        self.catalogue: str | None = None
        self.schema: str | None = None

        self.df_bronze: DataFrame | None = None
        self.df_silver: DataFrame | None = None
        self.df_rejete: DataFrame | None = None
        self.df_fact_trips: DataFrame | None = None
        self.df_dim_date: DataFrame | None = None
        self.df_kpi_daily: DataFrame | None = None
        self.dim_location: DataFrame | None = None

        self.nb_rows: int = 0
        self.status: str = "RUNNING"
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.duration_seconds: float|int | None = None
        self.message: str = ""
        self.current_step: str = ""
        self.row_count: dict[str, int] = {}
