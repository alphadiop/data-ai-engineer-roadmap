from pathlib import Path
import yaml


def load_config(env: str) -> dict:
    project_root = Path(__file__).parents[4]
    config_file = (
            project_root
            / "config"
            / f"{env}.yaml"
    )
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)