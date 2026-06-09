from abc import ABC, abstractmethod
from uuid import uuid4


class PipelineStep(ABC):

    def __init__(self, spark, logger):

        self.spark = spark
        self.logger = logger
        self.run_id = str(uuid4())

    @abstractmethod
    def run(self):
        pass

    def execute(self):
        try:
            self.logger.info(f"{self.__class__.__name__} START")
            self.run()
            self.logger.info(f"{self.__class__.__name__} SUCCESS")

        except Exception as e:
            self.logger.error(f"{self.__class__.__name__} FAILED : {e}")
            raise