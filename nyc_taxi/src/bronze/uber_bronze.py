import os
import sys

from datetime import datetime
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

    def __init__(self, spark,logger:PipelineLogger):
        super().__init__(spark,self.__class__.__name__)
        self.spark = spark
        self.logger = logger



    # def __repr__(self):
    #     return f"UberBronze(path_volume={self.path_volume})"
    #
    # def __str__(self):
    #     return f"UberBronze(path_volume={self.path_volume})"

    def avoid_future_period(self, periode:int):
        current_period = int(datetime.now().strftime("%Y%m"))
        if periode >= current_period:
            raise DataNotAvailableError(
                f"La période {periode} n'est pas encore publiée"
            )



    @log_execution
    def get_file_name(self, taxi_type:str, year:int, month:int) -> str:
        file = f"{taxi_type}_tripdata_{year}-{month:02}.parquet"
        if self.logger:
            self.logger.info(f"File name: {file}")
        return file

    @log_execution
    def get_path_file(self, path_volume, taxi_type, year, month) -> Path:
        return (
            path_volume
            / taxi_type
            / str(year)
            / self.get_file_name(taxi_type, year, month)
        )

    @log_execution
    def run(self, context) -> DataFrame:
        """
            Extract the data from the file and return a Spark DataFrame
            we supposed that path_volume exists otherwise we create it in SQL
            we supposed that file_name exists otherwise we download it from the internet
        """
        self.avoid_future_period(context.periode)

        config = load_config('variable_environnement', self.logger)

        path_volume = config[context.env]["bronze_path"]

        self.logger.info(f"Bronze path : {path_volume}")

        context.path_volume = Path(path_volume)
        context.year = int(context.periode) // 100
        context.month = int(context.periode) % 100

        file_name = self.get_file_name(
            taxi_type = context.taxi_type,
            year=context.year,
            month = context.month
        )
        path_file = self.get_path_file(
            path_volume = context.path_volume,
            taxi_type =context.taxi_type,
            year = context.year,
            month= context.month
        )

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
                            f"{context.taxi_type} {context.periode}"
                        )
                raise

            except URLError as e:
                self.logger.error(
                    f"Error downloading {file_name} : {e}"
                )
                raise

        #archived = self.path_volume / self.taxi_type / str(self.year) / file_name

        archived = path_file

        if not archived.exists():
            path_file.replace(archived)
            path_file = archived

        df = self.spark.read.parquet(str(path_file))

        df_bronze = df.withColumn("periode", lit(context.periode))

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