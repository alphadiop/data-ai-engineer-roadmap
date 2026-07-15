import logging


class PipelineLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        file = logging.FileHandler(
            "pipeline.log",
            mode="a",
            encoding="utf-8"
        )

        file.setFormatter(formatter)
        self.logger.addHandler(console)
        self.logger.addHandler(file)


    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)


    def flush(self):
        pass