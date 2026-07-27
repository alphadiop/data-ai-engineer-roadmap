import os
import sys

from abc import ABC, abstractmethod
from uuid import uuid4
from nyc_taxi.src.common.logger import PipelineLogger

import time

class PipelineStep(ABC):

    def __init__(self, spark, logger):

        self.spark = spark
        self.logger = logger
        self.run_id = str(uuid4())

    @abstractmethod
    def run(self):
        pass

    def execute(self):
        start = time.time()

        try:
            self.logger.info(f"{self.__class__.__name__} START")

            self.run()

            self.logger.info(f"{self.__class__.__name__} SUCCESS")

        except Exception as e:
            self.logger.error(f"{self.__class__.__name__} FAILED : {e}")
            raise

        finally:
            elapsed = time.time() - start
            self.logger.info(f"{self.__class__.__name__} FINISHED in {elapsed:.2f} seconds")

if __name__ == "__main__":
    pass






