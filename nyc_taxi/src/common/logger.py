import logging
import os
from pathlib import Path
from nyc_taxi.src.utils.config.load_config import load_config


class PipelineLogger:

    def __init__(self, name, env="local", level:int=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        self.logger.propagate = False

        config = load_config(
            "variable_environnement",
            self.logger
        )

        self.logger.info(
            f"path_logs : {config[env]['path_logs']}"
        )

        path_log = os.path.join(
            config[env]["path_logs"],
            "pipeline.log"
        )

        self.path_log = self.get_path_logs(path_log)

        self.logger.info(
            f"Log file : {self.path_log}"
        )

        print(f"LOGGER ENV = {env}")
        print(f"LOG_DIR = {config[env]['path_logs']}")

        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        self.handlers = [
            logging.StreamHandler(),
            logging.FileHandler(
                self.path_log ,
                mode="a",
                encoding="utf-8",
            ),
        ]

        for handler in self.handlers:
            handler.setFormatter(formatter)
            handler.setLevel(level)
            self.logger.addHandler(handler)



        #console = logging.StreamHandler()
        #console.setFormatter(formatter)

        #file_handler.setFormatter(formatter)
        #self.logger.addHandler(console)
        #self.logger.addHandler(file_handler )

    def get_path_logs(self, path_log: str) -> Path:
        
        path_log = Path(path_log)

        path_log.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        return path_log


    def remove_handlers(self):
        handlers = self.logger.handlers.copy()
        for handler in handlers:
            handler.flush()
            handler.close()
            self.logger.removeHandler(handler)


    def exception(self, e: Exception):
        self.logger.exception(e)
        self.remove_handlers()


    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)


    def flush(self):
        pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        choices=["local", "databricks"],
        default="local"
    )

    parser.add_argument(
        "--periode",
        type=int,
        required=True
    )

    parser.add_argument(
        "--taxi_type",
        type=str,
        default="yellow"
    )

    args = parser.parse_args()

    env = args.env
    periode = args.periode
    taxi_type = args.taxi_type

    logger = PipelineLogger(
        "uber_pipeline",
        env=env
    )

    logger.info(f"env = {env}")
    logger.info(f"periode = {periode}")
    logger.info(f"taxi_type = {taxi_type}")