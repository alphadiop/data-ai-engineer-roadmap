from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

class PathManager:

    def __init__(self, env, logger:'PipelineLogger'):
        self.env = env
        self.logger = logger

        if env == "local":
            self.root = Path.cwd() / "nyc_taxi"

        elif env == "databricks":
            self.root = Path(
                "/Workspace/Users/alphadiop@gmail.com/"
                "Learning workspace/nyc_taxi"
            )
        if self.logger:
            self.logger.info(
                f"Path manager initialized at {self.root}"
            )


    def schema_path(
            self,
            taxi_type,
            table_name
    ):
        return (
                self.root
                / "schema"
                / taxi_type
                / f"{table_name}.json"
        )