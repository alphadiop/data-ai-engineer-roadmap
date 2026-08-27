cd D:\data-ai-engineer-roadmap\nyc_taxi
tree /F src

set PYTHONPATH=D:\data-ai-engineer-roadmap
echo %PYTHONPATH%

python -c "import nyc_taxi.src.jobs.pipeline_runner_jobs_bundles; print('OK')"

python nyc_taxi\src\jobs\pipeline_runner_jobs_bundles.py --periode 202605 --taxi_type yellow
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles --periode 202605 --taxi_type yellow --env local

conda deactivate
conda env config vars set PYTHONPATH=D:\data-ai-engineer-roadmap
conda deactivate
conda activate spark_local

set PYSPARK_PYTHON=python

Amélioration future pour ton projet
reset_local_environment.py → nettoyage complet
create_local_tables.py → création des tables Delta vides avec tes JSON schemas
run_pipeline_local.ps1 → exécution standard du pipeline


import sys

spark = (
SparkSession.builder
.appName("nyc_taxi")
.config(
"spark.pyspark.python",
sys.executable
)
.getOrCreate()
)

python nyc_taxi\src\jobs\pipeline_runner_jobs_bundles.py --periode 202605 --taxi_type yellow --env local


catalog_manager.show_catalogs().show()
catalog_manager.show_schemas("nyc_taxi").show()
catalog_manager.show_tables("nyc_taxi", "bronze").show()
catalog_manager.show_tables("nyc_taxi", "silver").show()
catalog_manager.show_tables("nyc_taxi", "gold").show()
catalog_manager.show_tables("nyc_taxi", "ref").show()
catalog_manager.show_tables("nyc_taxi", "audit").show()



print("=== DATAFRAME ===")
df_audit.printSchema()

print("=== TABLE ===")
self.spark.table(audit_table).printSchema()

