
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

spark = (
    SparkSession.builder
    .appName("SparkUI_Exercise_Creances")
    .master("local[2]")
    .config("spark.ui.port", "4040")
    .config("spark.sql.shuffle.partitions", "4")
    .config("spark.sql.autoBroadcastJoinThreshold", "-1")
    .config("spark.sql.adaptive.enabled", "false")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# 1. Simuler 200 000 créances de leasing
creances = (
    spark.range(0, 200_000)
    .withColumnRenamed("id", "id_creance")
    .withColumn(
        "id_client",
        (col("id_creance") % 100).cast("long")
    )
    .withColumn(
        "montant",
        (col("id_creance") % 1000 + 100).cast("double")
    )
)

# 2. Référentiel des 100 clients
clients = (
    spark.range(0, 100)
    .withColumnRenamed("id", "id_client")
    .withColumnRenamed("id_client", "id_client")
    .withColumn("segment", (col("id_client") % 3).cast("string"))
)

# 3. Jointure puis agrégation métier
resultat = (
    creances
    .join(clients, on="id_client", how="inner")
    .groupBy("segment")
    .agg(
        spark_sum("montant").alias("montant_total"),
        spark_sum("id_creance").alias("somme_ids")
    )
)

# 4. Afficher le plan et exécuter réellement la requête
resultat.explain("formatted")
resultat.show()

print("\nApplication terminée. Spark UI reste disponible.")
input("Appuie sur Entrée pour arrêter Spark...")

spark.stop()
