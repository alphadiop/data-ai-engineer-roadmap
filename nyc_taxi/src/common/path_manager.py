
import os
from nyc_taxi.src.utils.load_json import load_json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nyc_taxi.src.common.logger import PipelineLogger

class PathManager:

    def __init__(self, config, env='local', logger:'PipelineLogger'=None):
        self.logger = logger
        self.env = env

        self.schema_root  = self._resolve_path(
            config["path_sql_schema"]
        )

        if self.logger:
            self.logger.info(
                f"Environment : {self.env}"
            )
            self.logger.info(
                f"Path.cwd(): {Path.cwd()}"
            )

        if self.logger:
            self.logger.info(
                f"Path manager initialized at {self.schema_root}"
            )

    def _resolve_path(self, path):
        path = str(path)

        # Databricks
        if self.env == "databricks":
            return Path(path)

        # WSL
        if self._is_wsl():
            return Path(self._windows_to_wsl(path))

        # Windows / local
        return Path(path)

    @staticmethod
    def _is_wsl():
        return (
                os.name == "posix"
                and "microsoft" in Path(
            "/proc/version"
        ).read_text().lower()
        )


    @staticmethod
    def _windows_to_wsl(path):
        if len(path) >= 3 and path[1:3] == ":/":
            drive = path[0].lower()
            remaining = path[3:].replace("\\","/")
            return f"/mnt/{drive}/{remaining}"
        return path


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


    def get_schema_json(self, path_sql_schema, taxi_type, table_name: str) -> dict:
        path = os.path.join(
            path_sql_schema,
            taxi_type,
            f"{table_name}.json"
        )
        return load_json(str(path))