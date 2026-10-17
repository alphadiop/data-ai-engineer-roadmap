from src.pilotage.sql_server_reader import SqlServerReader
from src.spark.spark_manager import SparkManager
from nyc_taxi.src.logger.logger import PipelineLogger


if __name__ == "__main__":
    env = "local"
    periode = 202411
    taxi_type = 'yellow'

    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type,
    )
    spark_manager = SparkManager(
        env=env,
        app_name="sql_server_test",
        logger=logger,
    )
    spark = spark_manager.get_spark()

    print("=== JDBC CONFIG ===")
    print(spark.sparkContext.getConf().get("spark.jars"))
    print("===================")

    # 'DIOP\\SQLEXPRESS' DIOP\\SQLEXPRESS
    reader = SqlServerReader(
        spark=spark,
        server="DIOP\SQLEXPRESS",
        database="AdventureWorks2022",
        user="alphadiop",
        password="Ibrahima1",
    )

    df = reader.read_table(
        schema="dbo",
        table_name="trip_date_key",
    )

    df.printSchema()
    df.show(10)