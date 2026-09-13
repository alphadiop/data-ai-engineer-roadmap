from pathlib import Path
import yaml
import platform
from .normalize_path import normalize_path

def load_config(file_name: str, env: str, logger=None) -> dict:
    project_root = Path(__file__).parents[4]

    if logger:
        logger.info(f"project_root : {project_root}")

    config_file = (
            project_root
            / "config"
            / f"{file_name}.yaml"
    )

    if logger:
        logger.info(f"Loading config from {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:

        config = yaml.safe_load(f)

        if env not in config:
            raise ValueError(
                f"Environnement '{env}' absent de la configuration"
            )

        if platform.system() == "Linux":
            for key, value in config[env].items():

                if isinstance(value, str):
                    config[env][key] = normalize_path(
                        value,
                        env
                    )

                    if logger and key in [
                        "warehouse_dir",
                        "metastore_dir",
                        "bronze_path"
                    ]:
                        logger.info(
                            f"Config Linux | {key} : {config[env][key]}"
                        )

        return config

#
#
# import os
# from pathlib import Path
# import yaml
# import platform
# from .normalize_path import normalize_path
#
# def load_config(file_name: str, env: str, logger=None) -> dict:
#
#     if env == "docker":
#         project_root = Path("/opt")
#     else:
#         project_root = Path(__file__).parents[4]
#
#     if logger:
#         logger.info(f"project_root : {project_root}")
#
#     config_file = (
#             project_root
#             / "config"
#             / f"{file_name}.yaml"
#     )
#
#     if logger:
#         logger.info(f"Loading config from {config_file}")
#
#     with open(config_file, "r", encoding="utf-8") as f:
#
#         config = yaml.safe_load(f)
#
#         if env not in config:
#             raise ValueError(
#                 f"Environnement '{env}' absent de la configuration"
#             )
#
#         if platform.system() == "Linux":
#
#             for key, value in config[env].items():
#
#                 if isinstance(value, str):
#
#                     config[env][key] = normalize_path(
#                         value,
#                         env
#                     )
#
#                     if logger and key in [
#                         "warehouse_dir",
#                         "metastore_dir",
#                         "bronze_path"
#                     ]:
#                         logger.info(
#                             f"Config Linux | {key} : "
#                             f"{config[env][key]}"
#                         )
#
#         return config
#


# def load_config(file_name: str, env:str, logger=None) -> dict:
#     project_root = Path(__file__).parents[4]
#
#     if logger:
#         logger.info(f"project_root : {project_root}")
#
#     config_file = (
#             project_root
#             / "config"
#             / f"{file_name}.yaml"
#     )
#     if logger:
#         logger.info(f"Loading config from {config_file}")
#
#     with open(config_file, "r", encoding="utf-8") as f:
#
#         config = yaml.safe_load(f)
#
#         if platform.system() == "Linux":
#             for env_name in ["local"]:
#                 for key, value in config[env_name].items():
#
#                     if isinstance(value, str):
#                         config[env_name][key] = normalize_path(value, env)
#
#                         if logger and key in ["warehouse_dir", "metastore_dir", "bronze_path"]:
#                             logger.info(
#                                 f"Config Linux | {key} : {config[env_name][key]}"
#                             )
#         return config
#

