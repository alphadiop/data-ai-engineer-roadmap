
docker compose exec airflow-scheduler airflow dags trigger nyc_taxi_airflow --conf '{\"periode\": 202505, \"taxi_type\": \"yellow\", \"env\": \"docker\"}'
docker compose exec airflow-scheduler airflow dags list-runs --dag-id nyc_taxi_airflow

Windows : là où tu développes et où se trouvent les fichiers du projet.
Docker Compose : la configuration qui démarre les services et relie les répertoires.
Conteneurs : les environnements dans lesquels les programmes s'exécutent.
Montages : les liens qui rendent certains fichiers de Windows accessibles dans les conteneurs.
Airflow : le chef d'orchestre qui déclenche et surveille les tâches.
Spark et ton code Python : les moteurs qui réalisent les traitements.
Stockage : l'endroit où les données et les métadonnées sont conservées, avec des règles de persistance différentes selon le type de stockage


Get-ChildItem ..\logs\yellow\2025 -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 3 FullName, LastWriteTime




---
Set-Location "D:\data-ai-engineer-roadmap\nyc_taxi\airflow"

Get-ChildItem -Force

# Afficher les fichiers Docker Compose
Get-ChildItem -File -Filter "*compose*"

# Vérifier les DAGs
Get-ChildItem ".\dags" -Recurse -File -ErrorAction SilentlyContinue


## 1. Lancer Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

docker info
docker context ls

Set-Location "D:\data-ai-engineer-roadmap\nyc_taxi\airflow"
docker compose ps


airflow-apiserver -> Interface et API Airflow
airflow-dag-processor -> Analyse des fichiers DAG
airflow-scheduler -> Planification et déclenchement des tâches
postgres -> Base de métadonnées Airflow

lien : http://localhost:8080/


docker compose exec airflow-scheduler airflow dags list
docker compose logs --tail=60 airflow-dag-processor

Get-Content .\dags\nyc_taxi_airflow.py



# 1. Vérifier le dossier racine du projet
Test-Path ..\src\jobs\run_pipeline_airflow.py
Test-Path ..\src\jobs\run_pipeline.py

# 2. Afficher le chemin absolu du dossier monté par Docker
Resolve-Path ..

# 3. Vérifier le contenu du dossier source
Get-ChildItem ..\src\jobs -File | Select-Object Name, FullName



docker compose up -d --no-deps --force-recreate airflow-apiserver airflow-scheduler airflow-dag-processor
docker compose exec airflow-scheduler python -c "import nyc_taxi.src.jobs.run_pipeline_airflow as m; print(m.__file__)"



docker compose exec airflow-scheduler bash -c "ls -la /opt/airflow/nyc_taxi/data"
docker compose exec airflow-scheduler bash -c "ls -la /opt/airflow/nyc_taxi/data/bronze"
docker compose exec airflow-scheduler bash -c "ls -la /opt/airflow/nyc_taxi/data/bronze/raw_files"
docker compose exec airflow-scheduler bash -c "ls -la /opt/data/reference"
docker compose exec airflow-scheduler bash -c "ls -la /opt/airflow/nyc_taxi/schema"


docker compose exec airflow-scheduler bash -c "id && ls -ld /opt/airflow /opt/airflow/nyc_taxi /opt/airflow/config"
docker compose exec airflow-scheduler bash -c "for d in /opt/airflow/docker-spark-warehouse /opt/airflow/docker-metastore_db /opt/airflow/spark_tmp /opt/airflow/spark_ivy; do if test -w \"`$d\"; then echo \"WRITABLE: `$d\"; else echo \"NOT WRITABLE OR MISSING: `$d\"; fi; done"



docker compose exec airflow-scheduler python -c "from nyc_taxi.src.spark.spark_manager import SparkManager; s=SparkManager(env='docker', app_name='NYC_Taxi_Airflow_Test').get_spark(); print('SPARK VERSION =', s.version); s.sql('SELECT 1 AS test').show(); s.range(1).write.format('delta').mode('overwrite').save('/opt/airflow/spark_tmp/delta_smoke_test'); print('DELTA WRITE OK'); s.stop()"
