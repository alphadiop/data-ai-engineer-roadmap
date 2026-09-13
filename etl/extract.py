from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import os
import urllib
import re

from pyspark.sql.functions import (col, lit)

### Path(self.path_volume) / file_name
class Extract:
    def __init__(self, spark, path_volume:Path | str,  taxi_type: str, periode:int):
        self.spark = spark
        self.path_volume = Path(path_volume)
        self.taxi_type = taxi_type
        self.periode = periode
        self.year = int(self.periode // 100)
        self.month = int(self.periode % 100)

    def __repr__(self):
        return f"Extract(path_volume={self.path_volume})"
    
    def __str__(self):
        return f"Extract(path_volume={self.path_volume})"
    

    def get_file_name(self, taxi_type:str) -> str:
        return str(f"{taxi_type}_tripdata_{self.year}-{self.month:02}.parquet")
    

    def get_path_file(self) -> Path:
        return (
            self.path_volume 
            / self.taxi_type 
            / str(self.year) 
            / self.get_file_name(self.taxi_type)
        )


    def extract(self) -> DataFrame:
        """
            Extract the data from the file and return a Spark DataFrame
            we supposed that path_volume exists otherwise we create it in SQL
            we supposed that file_name exists otherwise we download it from the internet
        """

        file_name = f"{self.taxi_type}_tripdata_{self.year}-{self.month:02d}.parquet"
        path_file = self.path_volume / self.taxi_type / str(self.year) / file_name
        archive_dir = self.path_volume / self.taxi_type / str(self.year) / file_name

        periode = self.get_period(file_name)

        path_file.parent.mkdir(parents=True, exist_ok=True)

        if not path_file.exists():
            url = (f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}")
            
            print(f"Downloading {file_name}")
            urllib.request.urlretrieve(url, str(path_file))

        archived = self.path_volume / self.taxi_type / str(self.year) / file_name

        if not archived.exists():
            path_file.replace(archived)
            path_file = archived
        return (
            self.spark.read.parquet(str(path_file))
            .withColumn("periode", lit(self.get_period(file_name)))
            )

    def get_period(self, file_name: str) -> str:
        match = re.search(r"(\d{4})-(\d{2})", file_name)
        if not match:
            raise ValueError(f"Période introuvable dans {file_name}")
        return f"{match.group(1)}{match.group(2)}"
    

    def sauvegarde(self, df):
        (
            df.write
           .format("delta")
           .mode("append")
           .option("mergeSchema", "true")
           .partitionBy("periode")
           .saveAsTable("bronze_nyc_taxi")
        )


if __name__ == "__main__":
    path_volume = "/Volumes/nyc_taxi/bronze/raw_files"
    taxi_type = "yellow"
    taxi_type = "green"
    #taxi_type = "fhv"
    extractor = Extract(
        spark, 
        path_volume, 
        taxi_type, 
        periode=202411
    )
    print(extractor.get_file_name(taxi_type))
    print(extractor.get_path_file())
    df = extractor.extract()
    
    #extractor.sauvegarde(df, file_name)
    #transformer = Transformation()
    #df_silver = transformer(df)
    display(df.limit(10))