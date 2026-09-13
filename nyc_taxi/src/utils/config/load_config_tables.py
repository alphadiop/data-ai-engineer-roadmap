import yaml
from pathlib import Path

def load_tables_config(file_name:str):
    config_file = (
            Path(__file__).parents[2]
            / "config"
            / f"{file_name}.yaml"
    )

    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)