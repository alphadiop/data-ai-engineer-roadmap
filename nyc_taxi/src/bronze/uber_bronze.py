import os
import sys

from urllib.request import urlretrieve
import re
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, lit
)
from urllib.error import HTTPError, URLError
from nyc_taxi.src.utils.config import load_config

from nyc_taxi.src.common.pipeline_step import PipelineStep
from nyc_taxi.src.common.logger import PipelineLogger
from nyc_taxi.src.common.decorators import log_execution 
from nyc_taxi.src.exception.exception_handler import DataNotAvailableError


class UberBronze(PipelineStep):

    """ 
     Télécharger les données Uber et les stocker dans le répertoire Bronze
     Mais avant de le télécharger, nous allons vérifier si le fichier existe dans le répertoire Bronze.
     Si le fichier existe, nous allons le télécharger à partir du répertoire Bronze.
     Sinon, nous allons le télécharger à partir du répertoire Bronze.
    """

    def __init__(self, spark,  taxi_type: str, periode:int, logger:PipelineLogger, env='local'):
        super().__init__(spark,self.__class__.__name__)
        self.spark = spark
        self.taxi_type = taxi_type
        self.periode = periode
        self.logger = logger
        self.env = env
        self.config = load_config('variable_environnement', self.logger)

        path_volume = self.config[self.env]["bronze_path"]

        self.logger.info(f"Bronze path : {path_volume}")

        self.path_volume = Path(path_volume)

        self.year = int(self.periode // 100)
        self.month = int(self.periode % 100)


    def __repr__(self):
        return f"UberBronze(path_volume={self.path_volume})"
    
    def __str__(self):
        return f"UberBronze(path_volume={self.path_volume})"
    
    @log_execution
    def get_file_name(self, taxi_type:str) -> str:

        return str(f"{taxi_type}_tripdata_{self.year}-{self.month:02}.parquet")
    

    def get_path_file(self) -> Path:
        return (
            self.path_volume
            / self.taxi_type 
            / str(self.year) 
            / self.get_file_name(self.taxi_type)
        )

    @log_execution
    def run(self, context) -> DataFrame:
        """
            Extract the data from the file and return a Spark DataFrame
            we supposed that path_volume exists otherwise we create it in SQL
            we supposed that file_name exists otherwise we download it from the internet
        """
        context.env = self.env
        context.path_volume =self.path_volume
        context.taxi_type = self.taxi_type
        context.periode = self.periode

        file_name = self.get_file_name(self.taxi_type)
        path_file = self.get_path_file()

        self.logger.info(f"Extracting {file_name} from {path_file}")

        path_file.parent.mkdir(parents=True, exist_ok=True)

        if not path_file.exists():
            url = (
                f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
            )
            
            self.logger.info(
                f"{'=' * 25} Downloading {file_name} {'=' * 25} "
            )

            try:
                urlretrieve(url, str(path_file))

            except HTTPError as e:

                if e.code in (403, 404):
                    raise DataNotAvailableError(
                            f"Dataset indisponible pour "
                            f"{self.taxi_type} {self.periode}"
                        )
                raise

            except URLError as e:
                self.logger.error(
                    f"Error downloading {file_name} : {e}"
                )
                raise

        #archived = self.path_volume / self.taxi_type / str(self.year) / file_name

        archived = self.get_path_file()

        if not archived.exists():
            path_file.replace(archived)
            path_file = archived

        df = self.spark.read.parquet(str(path_file))

        df_bronze = df.withColumn("periode", lit(self.periode))

        context.df_bronze = df_bronze

        context.row_count["bronze"] = df_bronze.count()
        
        context.periode = self.get_period(file_name)

        context.table_name = "silver_nyc_taxi"

        self.logger.info(
            f"{'=' * 55} Bronze rows : {df_bronze.count()} {'=' * 55} "
        )
        return df_bronze
            

    def get_period(self, file_name: str) -> str:
        match = re.search(r"(\d{4})-(\d{2})", file_name)
        if not match:
            raise ValueError(f"Période introuvable dans {file_name}")
        return f"{match.group(1)}{match.group(2)}"
    


if __name__ == "__main__":
    from nyc_taxi.src.common.spark_manager import SparkManager
    from nyc_taxi.src.utils.config import load_config
    logger = PipelineLogger('Bronze')

    config = load_config('pilotage_tables', logger)
    logger.info(f"Bronze config : {config}")
    logger.info(f"Bronze config : {config['tables']}")
    logger.info(f"Bronze config : {config['tables']['silver_nyc_taxi']}")
    # spark_manager = SparkManager(
    #     app_name="nyc_taxi_pipeline",
    #     logger=logger
    # )
    # path_volume = "/Volumes/nyc_taxi/bronze/raw_files"
    # taxi_type = "yellow"
    # #taxi_type = "green"
    # #taxi_type = "fhv"
    #
    # extractor = UberBronze(
    #     spark = spark_manager.get_spark(),
    #     taxi_type=taxi_type,
    #     periode=202607,
    #     logger=logger
    # )