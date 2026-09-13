### Compétences sur la recherche
* [ ] grep -R "load_config(" nyc_taxi/src
* [ ] grep -Rn "load_config(" nyc_taxi/src
* [ ] grep -Rn "SparkSession" nyc_taxi/src
* [ ] grep -Rn "saveAsTable" nyc_taxi/src
* [ ] python -c "from nyc_taxi.src.utils.config.load_config import load_config print(load_config('variable_environnement','local'))"
* grep -R -n "def repair_local_metastore" /mnt/d/data-ai-engineer-roadmap/nyc_taxi/src


* http://localhost:8080

* python -c "from nyc_taxi.src.utils.config.load_config import load_config print(load_config('variable_environnement','docker'))"
---
* grep = recherche de texte dans des fichiers.
* -R signifie Recursive

* Exemple : grep "SparkSession" spark_manager.py
* cherche le mot SparkSession dans spark_manager.py

* D:\data-ai-engineer-roadmap\nyc_taxi\src
* grep -R "load_config(" nyc_taxi/src
* wsl puis cd D:\data-ai-engineer-roadmap

* Cherche le texte "load_config(" dans tous les fichiers à l'intérieur du dossier nyc_taxi/src et de ses sous-dossiers.

`````text
nyc_taxi/src
│
├── audit
├── bronze
├── common
├── gold
├── jobs
├── logger
├── silver
├── utils
└── ...
`````


* docker compose exec airflow-apiserver bash
* grep -n "def normalize_path" /opt/airflow/nyc_taxi/src/utils/config/normalize_path.py

* [ ] parents[0] → /opt/airflow/nyc_taxi/src/utils/config
* [ ] parents[1] → /opt/airflow/nyc_taxi/src/utils
* [ ] parents[2] → /opt/airflow/nyc_taxi/src
* [ ] parents[3] → /opt/airflow/nyc_taxi
* [ ] parents[4] → /opt/airflow


python -c "
from nyc_taxi.src.common.catalog_manager import CatalogManager

c = CatalogManager(
    spark=None,
    logger=None,
    env='docker'
)

print('ENV       =', c.env)
print('AUDIT     =', c.audit_load())
print('SILVER    =', c.silver_nyc_taxi())
print('GOLD      =', c.gold_fact_trips())
"

| Fonction            | local                    | docker                   | databricks                        |
| ------------------- | ------------------------ | ------------------------ | --------------------------------- |
| Spark master        | `local[2]`               | `local[2]`               | actif Databricks                  |
| Catalogue           | `spark_catalog`          | `spark_catalog`          | Unity Catalog                     |
| `audit_load()`      | `audit.audit_load`       | `audit.audit_load`       | `nyc_taxi.audit.audit_load`       |
| `silver_nyc_taxi()` | `silver.silver_nyc_taxi` | `silver.silver_nyc_taxi` | `nyc_taxi.silver.silver_nyc_taxi` |
| `gold_fact_trips()` | `gold.gold_fact_trips`   | `gold.gold_fact_trips`   | `nyc_taxi.gold.gold_fact_trips`   |



* lancement : python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles --env docker --periode 202501 --taxi_type yellow


* attention : 
* environnement : wsl
* dans cd /mnt/d/data-ai-engineer-roadmap/airflow
* docker compose down
* docker compose up -d
* ls -lah /opt/data/ref/