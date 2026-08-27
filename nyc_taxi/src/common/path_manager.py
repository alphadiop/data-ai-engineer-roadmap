from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

class PathManager:

    def __init__(self, config, logger:'PipelineLogger'=None):
        self.logger = logger

        self.schema_root  = Path(
            config["path_sql_schema"]
        )

        if self.logger:
            self.logger.info(
                f"Path.cwd(): {Path.cwd()}"
            )

        if self.logger:
            self.logger.info(
                f"Path manager initialized at {self.schema_root}"
            )

    def schema_path(
            self,
            taxi_type,
            table_name
    ):
        return (
                self.schema_root
                / taxi_type
                / f"{table_name}.json"
        )