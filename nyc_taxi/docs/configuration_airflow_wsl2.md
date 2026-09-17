# NYC Taxi — Environnements, Spark local et Airflow

## 1. Objectif du projet

L'objectif est de construire un pipeline Data Engineering complet autour des données NYC Taxi :

```text
Source
  ↓
Bronze
  ↓
Silver
  ↓
Gold
  ↓
Audit
  ↓
Maintenance
```

Le pipeline est piloté par :

```text
Airflow
   ↓
DAG
   ↓
run_pipeline.py
   ↓
PipelineRunner
   ↓
Bronze → Silver → Gold → Audit → Maintenance
```

---

# 2. Architecture actuelle recommandée

Le choix retenu est de faire fonctionner **Airflow et Spark dans le même environnement Linux/WSL ou Docker**, plutôt que de demander à Airflow sous Linux de lancer directement un environnement Conda Windows.

Architecture cible :

```text
                         WSL2
┌─────────────────────────────────────────────────────┐
│                                                     │
│                  Apache Airflow                     │
│                       │                             │
│                       ▼                             │
│              NYC Taxi DAG                           │
│                       │                             │
│                       ▼                             │
│                run_pipeline.py                      │
│                       │                             │
│                       ▼                             │
│                PipelineRunner                       │
│                       │                             │
│          ┌────────────┼────────────┐                │
│          ▼            ▼            ▼                │
│       Bronze       Silver        Gold               │
│          │            │            │                │
│          └────────────┼────────────┘                │
│                       ▼                             │
│                     Audit                           │
│                       │                             │
│                       ▼                             │
│                  Maintenance                        │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              D:\data-ai-engineer-roadmap
```

Le projet peut cependant rester physiquement sur le disque `D:`.

Depuis WSL :

```text
D:\data-ai-engineer-roadmap
```

correspond à :

```text
/mnt/d/data-ai-engineer-roadmap
```

---

# 3. Environnements

## 3.1 Ancien environnement Windows

Historique :

```text
Windows
│
├── D:\conda_envs\spark_local
│      └── environnement Conda Spark
│
└── D:\data-ai-engineer-roadmap
       └── nyc_taxi
```

Cet environnement a servi à exécuter Spark directement sous Windows.

Il ne faut cependant plus chercher à faire communiquer directement :

```text
Airflow Linux
      ↓
Conda Windows
```

car cela complexifie inutilement l'architecture.

---

# 4. Environnement WSL

L'environnement recommandé pour Spark local est maintenant :

```text
WSL2
│
├── ~/spark4_env
│      ├── Python
│      ├── PySpark
│      └── Delta Lake
│
├── ~/airflow_env
│      └── Apache Airflow
│
└── /mnt/d/data-ai-engineer-roadmap
       └── nyc_taxi
```

Le projet reste donc sur `D:` mais il est exécuté depuis WSL.

---

# 5. Accès au projet depuis WSL

Depuis WSL :

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

Le projet NYC Taxi est alors accessible avec :

```bash
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
```

Vérification :

```bash
pwd
```

Résultat attendu :

```text
/mnt/d/data-ai-engineer-roadmap/nyc_taxi
```

---

# 6. Environnement Python Spark
Activer l'environnement Spark :

```bash
source ~/spark4_env/bin/activate
```

Vérifier :

```bash
which python
python --version
```

Vérifier PySpark :

```bash
python -c "import pyspark; print('PySpark =', pyspark.__version__)"
```

Vérifier Delta :

```bash
python -c "import delta; print('Delta OK')"
```

Vérifier PyYAML :

```bash
python -c "import yaml; print('YAML OK')"
```

Vérification globale :

```bash
python -c "
import sys
import pyspark
import delta
import yaml

print('Python :', sys.version)
print('PySpark:', pyspark.__version__)
print('Delta  :', delta.__version__)
print('PyYAML :', yaml.__version__)
"
```

---

# 7. Tester le projet NYC Taxi

Toujours se placer à la racine du projet :

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

Tester l'import du package :

```bash
python -c "import nyc_taxi; print(nyc_taxi)"
```

Tester `PipelineRunner` :

```bash
python -c "
from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
print('PipelineRunner OK')
"
```

Tester également le point d'entrée utilisé par Airflow :

```bash
python -c "
from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline OK')
"
```

---

# 8. Structure du projet

La structure importante est :

```text
nyc_taxi/
└── src/
    ├── bronze/
    │   └── uber_bronze.py
    │
    ├── silver/
    │   └── uber_silver.py
    │
    ├── gold/
    │   └── uber_gold.py
    │
    ├── loader/
    │   └── data_loader.py
    │
    ├── audit/
    │
    ├── common/
    │
    ├── setup/
    │
    ├── table_reference/
    │
    └── jobs/
        ├── pipeline_runner_jobs_bundles.py
        ├── run_pipeline.py
        └── maintenance_job.py
```

Les responsabilités sont séparées :

```text
nyc_taxi_airflow.py
        │
        │ orchestration Airflow
        ▼
run_pipeline.py
        │
        │ point d'entrée
        ▼
PipelineRunner
        │
        ├── EnvironmentSetup
        ├── ReferenceDataLoader
        ├── UberBronze
        ├── UberSilver
        ├── UberGold
        ├── DataLoader
        └── MaintenanceJob
```

---

# 9. Exécution manuelle du pipeline Spark

Avant de connecter Airflow, le pipeline doit pouvoir fonctionner seul.

Depuis :

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

avec l'environnement activé :

```bash
source ~/spark4_env/bin/activate
```

lancer :

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202504 \
    --taxi_type yellow
```

### Exemple avec une autre période

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202503 \
    --taxi_type yellow
```

Autre exemple :

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202507 \
    --taxi_type yellow
```

La logique est :

```text
--env local
       ↓
Spark local WSL

--periode 202504
       ↓
période de données à traiter

--taxi_type yellow
       ↓
type de taxi
```

---

# 10. Vérification du Warehouse Spark

Le Warehouse local est configuré dans le projet.

Pour vérifier sa configuration :

```bash
python -c "
from nyc_taxi.src.utils.config.load_config import load_config
import logging

c = load_config(
    'variable_environnement',
    logging.getLogger()
)

print('WAREHOUSE =', c['local']['warehouse_dir'])
print('METASTORE =', c['local']['metastore_dir'])
"
```

Vérifier le Warehouse :

```bash
ls -la /mnt/d/data-ai-engineer-roadmap/spark-warehouse
```

Rechercher les tables Delta :

```bash
find /mnt/d/data-ai-engineer-roadmap/spark-warehouse \
    -name "_delta_log"
```

---

# 11. Metastore et Warehouse

En environnement local, Spark utilise notamment :

```text
Metastore
    ↓
metastore_db

Warehouse
    ↓
spark-warehouse
```

Le Warehouse contient les données physiques des tables.

Exemple :

```text
spark-warehouse/
│
├── audit.db/
│   ├── audit_load/
│   └── audit_row_count/
│
├── silver.db/
│   └── silver_nyc_taxi/
│
└── gold.db/
    ├── gold_dim_date/
    ├── gold_dim_location/
    ├── gold_fact_trips/
    └── gold_kpi_daily/
```

Une table Delta possède notamment :

```text
table/
├── _delta_log/
└── fichiers de données
```

Le dossier `_delta_log` est donc un indicateur important pour vérifier qu'une table est bien gérée comme une table Delta.

---

# 12. Vérification de l'espace disque

Avant de faire du nettoyage :

```bash
df -h /
```

Taille des principaux dossiers du projet :

```bash
du -sh /mnt/d/data-ai-engineer-roadmap/* 2>/dev/null | sort -h
```

Taille du Warehouse :

```bash
du -sh /mnt/d/data-ai-engineer-roadmap/spark-warehouse/* 2>/dev/null | sort -h
```

Taille du HOME :

```bash
du -sh /home/alpha/* 2>/dev/null | sort -h
```

Taille de l'environnement Python :

```bash
du -sh /home/alpha/spark4_env
```

---

# 13. Nettoyage des caches

Ces commandes concernent uniquement les caches et non les données métier.

Cache pip :

```bash
python -m pip cache purge
```

Cache Ivy utilisé par Spark :

```bash
rm -rf ~/.ivy2/cache
rm -rf ~/.ivy2/jars
```

Cache utilisateur :

```bash
du -sh ~/.cache
```

Un nettoyage complet du cache peut être effectué avec :

```bash
rm -rf ~/.cache/*
```

⚠️ Ne pas confondre les caches avec :

```text
spark-warehouse
metastore_db
data/
```

qui contiennent des éléments nécessaires au projet.

---

# 14. Purge du stockage Delta

Le projet possède également un script de maintenance :

```bash
python -m nyc_taxi.src.admin.run_purge_delta_storage.py
```

Son objectif est de nettoyer l'ancien stockage Delta selon les règles définies dans le projet.

La purge Delta est différente du nettoyage des caches Python/Spark :

```text
Cache pip / Ivy
        ↓
fichiers temporaires

Purge Delta
        ↓
anciens fichiers Delta devenus inutiles
```

---

# 15. VACUUM Delta

Pour une table Delta :

```python
from delta.tables import DeltaTable

tables = [
    "audit.audit_load",
    "audit.audit_row_count",
    "silver.silver_nyc_taxi",
    "gold.gold_dim_date",
    "gold.gold_dim_location",
    "gold.gold_fact_trips",
    "gold.gold_kpi_daily",
]

for table in tables:
    print(f"VACUUM : {table}")
    DeltaTable.forName(spark, table).vacuum(168)
```

Ici :

```text
168 heures = 7 jours
```

Le principe est de supprimer les anciens fichiers Delta qui ne sont plus nécessaires après la période de rétention.

---

# 16. CatalogManager

La gestion des noms de tables est centralisée dans `CatalogManager`.

L'objectif est d'avoir une différence entre local et Databricks :

```text
LOCAL

audit.audit_load
silver.silver_nyc_taxi
gold.gold_fact_trips
```

et Databricks :

```text
DATABRICKS

nyc_taxi.audit.audit_load
nyc_taxi.silver.silver_nyc_taxi
nyc_taxi.gold.gold_fact_trips
```

Architecture :

```text
                    CatalogManager
                         │
             ┌───────────┴───────────┐
             │                       │
           LOCAL                 DATABRICKS
             │                       │
      audit.audit_load       nyc_taxi.audit.audit_load
      silver.xxx             nyc_taxi.silver.xxx
      gold.xxx               nyc_taxi.gold.xxx
             │                       │
             └───────────┬───────────┘
                         │
                    AuditManager
                         │
                  utilise seulement
                  audit_table = ...
```

L'intérêt est d'éviter de disperser les règles de nommage dans tout le projet.

---

# 17. Airflow — ancienne installation native WSL

Une première approche a consisté à installer Airflow directement dans :

```text
/home/alpha/airflow_env
```

avec :

```bash
python3 -m venv ~/airflow_env
source ~/airflow_env/bin/activate
```

Puis :

```bash
pip install apache-airflow
```

Vérification :

```bash
airflow version
```

Airflow utilise alors :

```text
/home/alpha/airflow
```

comme `AIRFLOW_HOME`.

Configuration :

```bash
export AIRFLOW_HOME=~/airflow
```

ou :

```bash
echo 'export AIRFLOW_HOME=~/airflow' >> ~/.bashrc
source ~/.bashrc
```

---

# 18. Airflow natif — commandes principales

Lister les DAG :

```bash
airflow dags list
```

Voir les erreurs d'import :

```bash
python -m airflow dags list-import-errors
```

Voir les informations sur les DAG :

```bash
python -m airflow dags report
```

Lancer Airflow :

```bash
python -m airflow standalone
```

Interface :

```text
http://localhost:8080
```

Cette installation native a permis de comprendre et tester Airflow.

---

# 19. Architecture Airflow actuelle : Docker

L'architecture retenue pour le projet est désormais Docker.

Structure :

```text
Docker Desktop
│
├── PostgreSQL
│      └── metadata database Airflow
│
└── Airflow
       │
       ├── API Server
       │
       └── Scheduler
              │
              ▼
             DAG
              │
              ▼
        NYC Taxi Pipeline
              │
        ┌─────┼─────┐
        ▼     ▼     ▼
      Bronze Silver Gold
```

---

# 20. Démarrage d'Airflow Docker

Depuis WSL :

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow
```

Vérifier Docker Compose :

```bash
docker compose version
```

Vérifier la configuration :

```bash
docker compose config
```

Initialiser Airflow :

```bash
docker compose up airflow-init
```

Démarrer les services :

```bash
docker compose up -d
```

Vérifier :

```bash
docker compose ps
```

Interface :

```text
http://localhost:8080
```

---

# 21. Accéder aux conteneurs Airflow

Entrer dans le conteneur API Server :

```bash
docker compose exec airflow-apiserver bash
```

Entrer dans le Scheduler :

```bash
docker compose exec airflow-scheduler bash
```

Une fois dans le conteneur :

```bash
ls -la /opt/airflow
```

Projet NYC Taxi :

```bash
ls -la /opt/airflow/nyc_taxi
```

Jobs :

```bash
ls -la /opt/airflow/nyc_taxi/src/jobs
```

---

# 22. Volumes Docker

Le projet utilise notamment un montage permettant de rendre le projet accessible à Airflow :

```text
WSL
/mnt/d/data-ai-engineer-roadmap/nyc_taxi
              │
              ▼
Docker
/opt/airflow/nyc_taxi
```

Les données :

```text
WSL
/mnt/d/data-ai-engineer-roadmap/data
              │
              ▼
Docker
/opt/data
```

Architecture :

```text
Windows / WSL
│
├── data-ai-engineer-roadmap/
│   ├── nyc_taxi/
│   └── data/
│
└───────────────┐
                │ volumes Docker
                ▼
          /opt/airflow
          /opt/data
```

---

# 23. Vérifier les volumes Docker

Depuis :

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow
```

Vérifier :

```bash
docker compose config
```

Vérifier notamment les mappings :

```bash
docker compose config | grep -A5 -B5 "/opt/data"
```

Vérifier le contenu du conteneur :

```bash
docker compose exec airflow-apiserver bash
```

Puis :

```bash
ls -la /opt/data
```

Référence :

```bash
find /opt/data -name "taxi_zone_lookup.csv" 2>/dev/null
```

---

# 24. Tester NYC Taxi dans Docker

Dans le conteneur Airflow :

```bash
python -c "import nyc_taxi; print('OK')"
```

Puis :

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env docker \
    --periode 202501 \
    --taxi_type yellow
```

Cela permet de vérifier que le pipeline fonctionne indépendamment d'Airflow mais dans l'environnement Docker.

---

# 25. Architecture Airflow + NYC Taxi

Le DAG ne doit pas contenir toute la logique métier.

La séparation retenue est :

```text
Airflow DAG
     │
     ▼
run_pipeline.py
     │
     ▼
PipelineRunner
     │
     ├── EnvironmentSetup
     ├── ReferenceDataLoader
     ├── UberBronze
     ├── UberSilver
     ├── UberGold
     ├── DataLoader
     └── MaintenanceJob
```

### Responsabilités

`nyc_taxi_airflow.py`

```text
Orchestration Airflow
```

`run_pipeline.py`

```text
Point d'entrée du pipeline
```

`pipeline_runner_jobs_bundles.py`

```text
Moteur d'exécution
```

`maintenance_job.py`

```text
Maintenance Delta
```

Les classes Bronze/Silver/Gold réalisent les transformations métier.

---

# 26. Vérifier l'import du pipeline dans Docker

Commande :

```bash
docker compose exec airflow-scheduler python -c "
from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
print('IMPORT OK')
"
```

Puis :

```bash
docker compose exec airflow-scheduler python -c "
from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline import OK')
"
```

---

# 27. Vérifier le DAG

Lister les DAG :

```bash
docker compose exec airflow-scheduler airflow dags list
```

Vérifier les erreurs d'import :

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

Afficher le DAG :

```bash
docker compose exec airflow-scheduler airflow dags show nyc_taxi_airflow
```

---

# 28. Tester le DAG

Une fois le pipeline manuel validé :

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

Cette commande signifie :

```text
docker compose
      ↓
exécute une commande dans
      ↓
airflow-scheduler
      ↓
airflow dags test
      ↓
DAG = nyc_taxi_airflow
      ↓
date logique = 2026-09-11
```

Le test permet de vérifier toute la chaîne :

```text
Airflow
   ↓
DAG
   ↓
run_pipeline.py
   ↓
PipelineRunner
   ↓
EnvironmentSetup
   ↓
Bronze
   ↓
Silver
   ↓
Gold
   ↓
DataLoader
   ↓
Maintenance
   ↓
Audit
```

---

# 29. Résultat attendu

Lorsque le DAG fonctionne correctement, on doit obtenir notamment :

```text
PIPELINE FINALIZED - STATUS = OK
```

et :

```text
state=success
```

Cela signifie que :

```text
Airflow
   ↓
DAG
   ↓
Pipeline
```

fonctionne correctement.

---

# 30. Vérification de l'Audit

Une fois le pipeline exécuté, il est possible de vérifier les dernières exécutions :

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

Puis :

```bash
/home/alpha/spark4_env/bin/python -c '
from nyc_taxi.src.common.spark_manager import SparkManager

spark = SparkManager(
    app_name="audit_check",
    env="local"
).get_spark()

spark.sql("""
SELECT
    run_id,
    periode,
    table_name,
    taxi_type,
    status,
    start_time,
    end_time,
    duration_seconds,
    error_step,
    message
FROM audit.audit_load
ORDER BY end_time DESC
LIMIT 10
""").show(truncate=False)
'
```

L'audit permet notamment de vérifier :

```text
run_id
periode
table_name
taxi_type
status
start_time
end_time
duration
error_step
message
```

---

# 31. Vérification Java / Spark

Pour vérifier Java :

```bash
which java
java -version
```

Vérifier les processus Java :

```bash
jps
```

Sous Windows, si nécessaire :

```powershell
tasklist | findstr java
```

---

# 32. Commandes Docker de diagnostic

Voir l'utilisation Docker :

```bash
docker system df
```

Voir les images :

```bash
docker images
```

Voir les conteneurs :

```bash
docker compose ps
```

Logs du Scheduler :

```bash
docker compose logs airflow-scheduler --since=5m
```

Logs de l'API Server :

```bash
docker compose logs airflow-apiserver --tail=50
```

---

# 33. Attention aux commandes Docker de nettoyage

Commandes possibles :

```bash
docker container prune -f
docker image prune -a
docker volume prune -f
```

Mais les commandes suivantes sont beaucoup plus agressives :

```bash
docker system prune -a --volumes -f
```

⚠️ Elles peuvent supprimer des images, conteneurs, réseaux et volumes Docker inutilisés.

Ne pas les utiliser comme simple commande de nettoyage quotidien.

---

# 34. Diagnostic général de l'espace disque

Commande recommandée :

```bash
echo "=== DISQUE ==="
df -h /

echo "=== PROJET ==="
du -sh /mnt/d/data-ai-engineer-roadmap/* 2>/dev/null | sort -h

echo "=== WAREHOUSE ==="
du -sh /mnt/d/data-ai-engineer-roadmap/spark-warehouse/* 2>/dev/null | sort -h

echo "=== HOME ==="
du -sh /home/alpha/* 2>/dev/null | sort -h
```

---

# 35. Séquence de travail recommandée

Pour éviter les problèmes, toujours travailler dans cet ordre.

## Étape 1 — Activer Spark

```bash
source ~/spark4_env/bin/activate
```

## Étape 2 — Se placer à la racine

```bash
cd /mnt/d/data-ai-engineer-roadmap
```

## Étape 3 — Tester Python

```bash
python --version
which python
```

## Étape 4 — Tester le projet

```bash
python -c "import nyc_taxi; print('NYC Taxi OK')"
```

## Étape 5 — Tester PipelineRunner

```bash
python -c "
from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
print('PipelineRunner OK')
"
```

## Étape 6 — Exécuter le pipeline manuellement

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202504 \
    --taxi_type yellow
```

## Étape 7 — Vérifier l'Audit

Vérifier que l'exécution est correctement enregistrée.

## Étape 8 — Démarrer Airflow Docker

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow
docker compose up -d
```

## Étape 9 — Vérifier Airflow

```bash
docker compose ps
```

## Étape 10 — Vérifier le DAG

```bash
docker compose exec airflow-scheduler airflow dags list
```

## Étape 11 — Tester le point d'entrée

```bash
docker compose exec airflow-scheduler python -c "
from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
print('run_pipeline OK')
"
```

## Étape 12 — Tester le DAG

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

---

# 36. Architecture finale à retenir

```text
                         WINDOWS
                            │
                            │
                 D:\data-ai-engineer-roadmap
                            │
                            ▼
                          WSL2
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
       spark4_env                    Docker
              │                           │
              │                     ┌─────┴─────┐
              │                     │           │
              │                 Airflow     PostgreSQL
              │                     │
              │                     ▼
              │                    DAG
              │                     │
              │                     ▼
              │             run_pipeline.py
              │                     │
              │                     ▼
              └────────────► PipelineRunner
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                 Bronze          Silver           Gold
                                                    │
                                                    ▼
                                                   Audit
                                                    │
                                                    ▼
                                               Maintenance
```

---

# 37. Commandes essentielles à retenir

### Spark local

```bash
source ~/spark4_env/bin/activate
cd /mnt/d/data-ai-engineer-roadmap
```

### Pipeline

```bash
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
    --env local \
    --periode 202504 \
    --taxi_type yellow
```

### Purge Delta

```bash
python -m nyc_taxi.src.admin.run_purge_delta_storage.py
```

### Airflow Docker

```bash
cd /mnt/d/data-ai-engineer-roadmap/airflow
docker compose up -d
```

### Vérification

```bash
docker compose ps
```

### DAG

```bash
docker compose exec airflow-scheduler airflow dags list
```

### Test DAG

```bash
docker compose exec airflow-scheduler \
    airflow dags test nyc_taxi_airflow 2026-09-11
```

---

# 38. État actuel du projet

Les éléments suivants sont maintenant validés :

* [x] Projet NYC Taxi accessible depuis WSL
* [x] Environnement Spark WSL fonctionnel
* [x] PySpark installé
* [x] Delta Lake installé
* [x] PyYAML installé
* [x] Pipeline local fonctionnel
* [x] Bronze → Silver → Gold fonctionnel
* [x] Audit fonctionnel
* [x] Maintenance Delta
* [x] Airflow installé
* [x] Airflow Docker fonctionnel
* [x] PostgreSQL utilisé pour les métadonnées Airflow
* [x] DAG détecté
* [x] `run_pipeline.py` placé dans `nyc_taxi/src/jobs`
* [x] `PipelineRunner` séparé du DAG
* [x] DAG avec une tâche d'orchestration
* [x] Import `nyc_taxi` fonctionnel dans Docker
* [x] Import `run_pipeline.py` fonctionnel
* [x] DAG Airflow testé avec succès
* [x] Pipeline exécuté depuis Airflow
* [x] Statut final `SUCCESS / OK`

## Architecture logicielle finale

```text
Airflow
   │
   ▼
nyc_taxi_airflow.py
   │
   ▼
run_pipeline.py
   │
   ▼
PipelineRunner
   │
   ├── EnvironmentSetup
   ├── ReferenceDataLoader
   ├── UberBronze
   ├── UberSilver
   ├── UberGold
   ├── DataLoader
   └── MaintenanceJob
   │
   ▼
Audit
```

Cette architecture permet ensuite d'évoluer vers un véritable pipeline de production avec scheduling, retries, monitoring, paramétrage des périodes, gestion des erreurs et éventuellement plusieurs tâches Airflow.
