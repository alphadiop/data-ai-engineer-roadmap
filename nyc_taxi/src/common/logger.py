import logging
import os
from pathlib import Path

class PipelineLogger:

    PROJECT_ROOT = "/Workspace/Users/alphadiop@gmail.com/Learning workspace/nyc_taxi/"

    def __init__(self, name, level:int=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        self.logger.propagate = False

        path_log = os.path.join(
            self.PROJECT_ROOT,
            "logs",
            "pipeline.log"
        )

        self.path_log = self.get_path_logs(path_log)

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
    logger = PipelineLogger("test")
    logger.info("test")
    logger.error("test")
    logger.warning("test")