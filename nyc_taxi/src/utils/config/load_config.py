from pathlib import Path
import yaml


def load_config(file_name: str, logger=None) -> dict:
    project_root = Path(__file__).parents[4]
    config_file = (
            project_root
            / "config"
            / f"{file_name}.yaml"
    )
    if logger:
        logger.info(f"Loading config from {config_file}")
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)