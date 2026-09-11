from nyc_taxi.src.utils.config.load_config import load_config
from typing import TYPE_CHECKING
from nyc_taxi.src.logger.logger import PipelineLogger
import platform
if TYPE_CHECKING:
    from nyc_taxi.src.logger.logger import PipelineLogger



if __name__ == "__main__":
    env = 'local'
    periode = 202401
    taxi_type = 'yellow'
    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type
    )

    config = load_config(
        file_name='variable_environnement',
        env=env,
        logger=logger
    )
    print("\n===== CONFIG DOCKER =====")
    logger.info(f"env demandé = {env}")
    logger.info(f"platform = {platform.system()}")
    for key, value in config["docker"].items():
        print(f"{key} = {value}")
