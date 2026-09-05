
from nyc_taxi.src.utils.load_json import load_json

import os
from pathlib import Path


class PathManager:

    def __init__(self, context):

        self.context = context

        self.env = context.env
        self.taxi_type = context.taxi_type

        self.logger = context.logger
        self.config = context.config

        self.project_root = self._get_project_root()
        self.schema_root = self._get_schema_root()

        if self.logger:
            self.logger.info(
                f"PathManager initialized | env={self.env}"
            )

            self.logger.info(
                f"project_root={self.project_root}"
            )

            self.logger.info(
                f"schema_root={self.schema_root}"
            )

        self.schema_root = self._resolve_path(
            self.config["path_sql_schema"]
        )

        if self.logger:
            self.logger.info(
                f"Environment : {self.env}"
            )

            self.logger.info(
                f"Path.cwd(): {Path.cwd()}"
            )

            self.logger.info(
                f"Path manager initialized at {self.schema_root}"
            )

    def _get_project_root(self):

        if self.env == "databricks":
            return Path(
                "/Workspace/Users/alphadiop@gmail.com/"
                "Learning workspace/nyc_taxi"
            )

        if "project_root" in self.config:
            return self._resolve_path(
                self.config["project_root"]
            )

        return Path.cwd()

    def _get_schema_root(self):

        return self.project_root / "schema"

    def _resolve_path(self, path):

        path = str(path)

        # ------------------------------------------------------------
        # Databricks
        # ------------------------------------------------------------

        if self.env == "databricks":
            return Path(path)

        # ------------------------------------------------------------
        # WSL
        # ------------------------------------------------------------

        if self._is_wsl():
            return Path(
                self._windows_to_wsl(path)
            )

        # ------------------------------------------------------------
        # Windows / local
        # ------------------------------------------------------------

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

            remaining = (
                path[3:]
                .replace("\\", "/")
            )

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

    def get_schema_json(
            self,
            path_sql_schema,
            taxi_type,
            table_name: str
    ) -> dict:

        path = os.path.join(
            str(path_sql_schema),
            taxi_type,
            f"{table_name}.json"
        )

        return load_json(
            str(path)
        )





# class PathManager:
#
#     def __init__(self, context):
#
#         self.context = context
#
#         # ============================================================
#         # CONTEXT
#         # ============================================================
#
#         self.env = context.env
#         self.taxi_type = context.taxi_type
#
#         self.logger = context.logger
#         self.config = context.config
#
#         # ============================================================
#         # SCHEMA PATH
#         # ============================================================
#
#         self.schema_root = self._resolve_path(
#             self.config["path_sql_schema"]
#         )
#
#         # ============================================================
#         # LOGGING
#         # ============================================================
#
#         if self.logger:
#
#             self.logger.info(
#                 f"PathManager initialized | env={self.env}"
#             )
#
#             self.logger.info(
#                 f"taxi_type={self.taxi_type}"
#             )
#
#             self.logger.info(
#                 f"Path.cwd(): {Path.cwd()}"
#             )
#
#             self.logger.info(
#                 f"schema_root={self.schema_root}"
#             )
#
#     # ================================================================
#     # RESOLVE PATH
#     # ================================================================
#
#     def _resolve_path(self, path):
#
#         path = str(path)
#
#         # ------------------------------------------------------------
#         # Databricks
#         # ------------------------------------------------------------
#
#         if self.env == "databricks":
#             return Path(path)
#
#         # ------------------------------------------------------------
#         # WSL
#         # ------------------------------------------------------------
#
#         if self._is_wsl():
#             return Path(
#                 self._windows_to_wsl(path)
#             )
#
#         # ------------------------------------------------------------
#         # Windows / Local
#         # ------------------------------------------------------------
#
#         return Path(path)
#
#     # ================================================================
#     # DETECT WSL
#     # ================================================================
#
#     @staticmethod
#     def _is_wsl():
#
#         return (
#                 os.name == "posix"
#                 and Path("/proc/version").exists()
#                 and "microsoft" in Path(
#             "/proc/version"
#         ).read_text().lower()
#         )
#
#     # ================================================================
#     # WINDOWS -> WSL
#     # ================================================================
#
#     @staticmethod
#     def _windows_to_wsl(path):
#
#         path = str(path)
#
#         if len(path) >= 3 and path[1:3] == ":/":
#
#             drive = path[0].lower()
#
#             remaining = (
#                 path[3:]
#                 .replace("\\", "/")
#             )
#
#             return f"/mnt/{drive}/{remaining}"
#
#         return path
#
#     # ================================================================
#     # SCHEMA PATH
#     # ================================================================
#
#     def schema_path(
#             self,
#             taxi_type,
#             table_name
#     ):
#
#         path = (
#                 self.schema_root
#                 / taxi_type
#                 / f"{table_name}.json"
#         )
#
#         if self.logger:
#             self.logger.info(
#                 f"Schema path : {path}"
#             )
#
#         return path
#
#     # ================================================================
#     # LOAD SCHEMA JSON
#     # ================================================================
#
#     def get_schema_json(
#             self,
#             taxi_type,
#             table_name: str
#     ) -> dict:
#
#         path = self.schema_path(
#             taxi_type=taxi_type,
#             table_name=table_name
#         )
#
#         if self.logger:
#             self.logger.info(
#                 f"Loading schema : {path}"
#             )
#
#         return load_json(
#             str(path)
#         )
#
#



# if TYPE_CHECKING:
#     from nyc_taxi.src.common.logger import PipelineLogger
#
# class PathManager:
#
#     def __init__(self, context):
#         self.context = context
#
#
#         self.env = context.env
#         self.taxi_type = context.taxi_type
#
#         self.logger = context.logger
#         self.config = context.config
#
#         self.project_root = self._get_project_root()
#         self.schema_root = self._get_schema_root()
#
#         self.logger.info(
#             f"PathManager initialized | env={self.env}"
#         )
#         self.logger.info(
#             f"project_root={self.project_root}"
#         )
#         self.logger.info(
#             f"schema_root={self.schema_root}"
#         )
#
#         self.schema_root  = self._resolve_path(
#             config["path_sql_schema"]
#         )
#
#         if self.logger:
#             self.logger.info(
#                 f"Environment : {self.env}"
#             )
#             self.logger.info(
#                 f"Path.cwd(): {Path.cwd()}"
#             )
#
#         if self.logger:
#             self.logger.info(
#                 f"Path manager initialized at {self.schema_root}"
#             )
#
#     def _resolve_path(self, path):
#         path = str(path)
#
#         # Databricks
#         if self.env == "databricks":
#             return Path(path)
#
#         # WSL
#         if self._is_wsl():
#             return Path(self._windows_to_wsl(path))
#
#         # Windows / local
#         return Path(path)
#
#     @staticmethod
#     def _is_wsl():
#         return (
#                 os.name == "posix"
#                 and "microsoft" in Path(
#             "/proc/version"
#         ).read_text().lower()
#         )
#
#
#     @staticmethod
#     def _windows_to_wsl(path):
#         if len(path) >= 3 and path[1:3] == ":/":
#             drive = path[0].lower()
#             remaining = path[3:].replace("\\","/")
#             return f"/mnt/{drive}/{remaining}"
#         return path
#
#
#     def schema_path(
#             self,
#             taxi_type,
#             table_name
#     ):
#         return (
#                 self.schema_root
#                 / taxi_type
#                 / f"{table_name}.json"
#         )
#
#
#     def get_schema_json(self, path_sql_schema, taxi_type, table_name: str) -> dict:
#         path = os.path.join(
#             path_sql_schema,
#             taxi_type,
#             f"{table_name}.json"
#         )
#         return load_json(str(path))