from nyc_taxi.src.common.spark_manager import SparkManager

spark = SparkManager(app_name="audit_check",env="local").get_spark()

# print("\n ==================silver.silver_nyc_taxi======================")
# spark.sql("""
# SELECT *
# FROM audit.audit_load
# ORDER BY end_time DESC
# """).show(20, truncate=False)
#
#
# print("\n ==================silver.silver_nyc_taxi======================")
# spark.sql("""
# SELECT
#     periode,
#     status,
#     count(*) nb
# FROM audit.audit_load
# GROUP BY periode, status
# ORDER BY periode
# """).show(100, False)
#
#
# spark.sql("""
# SELECT
#     min(periode) as min_periode,
#     max(periode) as max_periode,
#     count(*) as nb_rows
# FROM silver.silver_nyc_taxi
# """).show()
#
# print("\n ==================silver.silver_nyc_taxi======================")
# spark.sql("""
# SELECT
#     periode,
#     count(*) as nb_rows
# FROM silver.silver_nyc_taxi
# GROUP BY periode
# ORDER BY periode
# """).show(100, False)
#
# print("\n ==================silver.silver_nyc_taxi======================")
# spark.sql("""
# SELECT
#     periode,
#     COUNT(*) AS nb_rows,
#     COUNT(DISTINCT CONCAT(
#         VendorID,
#         tpep_pickup_datetime,
#         tpep_dropoff_datetime,
#         PULocationID,
#         DOLocationID
#     )) AS nb_distinct
# FROM silver.silver_nyc_taxi
# WHERE periode = 202504
# GROUP BY periode
# """).show(truncate=False)
#
# print("\n ==================silver.silver_nyc_taxi======================")
# spark.sql("""
# SELECT periode, COUNT(*)
# FROM silver.silver_nyc_taxi
# GROUP BY periode
# ORDER BY periode
# """).show(100, False)

print("\n ==================silver.silver_nyc_taxi======================")
df = spark.read.parquet(
    "/mnt/d/data-ai-engineer-roadmap/data/bronze/raw_files/yellow/2025/yellow_tripdata_2025-04.parquet"
)
print(df.count())

print("\n ==================silver.silver_nyc_taxi======================")
spark.sql("""
SELECT COUNT(*) AS nb
FROM silver.silver_nyc_taxi
WHERE periode = 202504
""").show()


print("\n ==================silver.silver_nyc_taxi======================")
spark.sql("""
SELECT
    COUNT(*) AS total,
    COUNT(DISTINCT
        CONCAT_WS(
            '|',
            CAST(VendorID AS STRING),
            CAST(tpep_pickup_datetime AS STRING),
            CAST(tpep_dropoff_datetime AS STRING),
            CAST(PULocationID AS STRING),
            CAST(DOLocationID AS STRING),
            CAST(total_amount AS STRING)
        )
    ) AS distinct_rows
FROM silver.silver_nyc_taxi
WHERE periode = 202504
""").show(truncate=False)