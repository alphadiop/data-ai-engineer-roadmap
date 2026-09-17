"""
Reset de l'environnement Spark local.

Supprime :
- les tables Spark locales
- les schemas bronze/silver/gold/audit
- le warehouse Spark

Puis recrée les schemas nécessaires.
"""


from pathlib import Path
import shutil
from pyspark.sql import SparkSession


DATABASES = [
    "bronze",
    "silver",
    "gold",
    "audit"
]


def get_spark():
    return (
        SparkSession.builder
        .appName("reset_local_environment")
        .master("local[*]")
        .getOrCreate()
    )


def drop_databases(spark):
    for database in DATABASES:
        print(
            f"Suppression database : {database}"
        )

        spark.sql(
            f"""
            DROP DATABASE IF EXISTS {database}
            CASCADE
            """
        )


def delete_warehouse():
    warehouse_path = Path(
        "spark-warehouse"
    )
    if warehouse_path.exists():
        print(
            f"Suppression warehouse : {warehouse_path}"
        )
        shutil.rmtree(
            warehouse_path
        )

    else:

        print(
            "Warehouse inexistant"
        )


def create_databases(spark):
    for database in DATABASES:

        print(
            f"Création database : {database}"
        )

        spark.sql(
            f"""
            CREATE DATABASE IF NOT EXISTS {database}
            """
        )

def main():

    print("=" * 80)
    print("RESET ENVIRONNEMENT SPARK LOCAL")
    print("=" * 80)


    spark = get_spark()

    try:
        drop_databases(spark)
        clean_spark_warehouse()
        spark.stop()
        delete_warehouse()
        spark = get_spark()
        create_databases(spark)
        print("=" * 80)
        print("RESET TERMINE")
        print("=" * 80)
    finally:
        spark.stop()





def clean_spark_warehouse():

    warehouse = Path(
        "spark-warehouse"
    )

    if warehouse.exists():

        print(
            f"Suppression : {warehouse}"
        )

        shutil.rmtree(
            warehouse
        )


if __name__ == "__main__":
    main()