import logging
from pathlib import Path
from typing import Dict


class LOGGER:

    def __init__(
        self,
        parameters: Dict[str, str],
        level: str = "INFO",
        log_file: str = "pipeline.log"
    ):

        self.parameters = parameters

        self.logger = logging.getLogger(
            self.parameters.get("Moteur", "pipeline")
        )

        self.logger.setLevel(self._get_level(level))

        self.logger.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Fichier
        file_handler = logging.FileHandler(
            log_file,
            mode="a",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.logger.propagate = False

    @staticmethod
    def _get_level(level: str):
        return {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }.get(level.upper(), logging.INFO)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)


if __name__=="__main__":
    parameters = {
    "Moteur": "sales_pipeline"
}
    log = LOGGER(
        parameters,
        level="INFO",
        log_file="./log/sales_pipeline.log"
    )

    log.info("Bronze START")
    log.warning("2 lignes rejetées")
    log.error("Impossible de lire le fichier")