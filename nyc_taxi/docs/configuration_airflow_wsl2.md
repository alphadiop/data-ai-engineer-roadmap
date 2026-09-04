source ~/spark4_env/bin/activate
cd /mnt/d/data-ai-engineer-roadmap

python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
--env local \
--periode 202501 \
--taxi_type yellow

python -c "from nyc_taxi.src.utils.config.load_config import load_config; import logging; c=load_config('variable_environnement', logging.getLogger()); print('WAREHOUSE =', c['local']['warehouse_dir']); print('METASTORE =', c['local']['metastore_dir'])"

ls -la /mnt/d/data-ai-engineer-roadmap/spark-warehouse
find /mnt/d/data-ai-engineer-roadmap/spark-warehouse -name "_delta_log"


## Tu as actuellement deux environnements bien séparés :

#### Environnement Conda Windows
```text
WINDOWS
│
├── D:\conda_envs\spark_local
│      └── ton environnement Spark local
│
└── D:\data-ai-engineer-roadmap
└── nyc_taxi
```

---
```text
Linux / WSL2
│
├── /home/alpha/airflow_env
│      └── Airflow
│
└── /home/alpha/airflow
└── configuration / metadata / logs Airflow
```
---

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
---


---
* Ton projet NYC Taxi est actuellement sous Windows : D:\data-ai-engineer-roadmap\nyc_taxi
* Environnement Spark : D:\conda_envs\spark_local
* Airflow tourne sous WSL2 : /home/alpha/airflow_env
* Environnement Airflow : /home/alpha/airflow_env


---
* accès de mon projet depuis WSL : cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* Airflow qui tourne sous WSL ne peut pas simplement faire : source D:\conda_envs\spark_local\...
* objectif : faire communiquer Airflow WSL → ton pipeline Spark local Windows, sans casser ton environnement actuel.

---


```text
                    WINDOWS
┌──────────────────────────────────────────────┐
│                                              │
│  D:\data-ai-engineer-roadmap\nyc_taxi       │
│                    │                         │
│                    ▼                         │
│        Conda : spark_local                   │
│                    │                         │
│                    ▼                         │
│          Spark + Delta Lake                  │
│                                              │
└──────────────────────▲───────────────────────┘
│
│ déclenchement
│
┌──────────────────────┴───────────────────────┐
│                    WSL2                      │
│                                              │
│  /home/alpha/airflow_env                     │
│              │                               │
│              ▼                               │
│         Apache Airflow                       │
│              │                               │
│              ▼                               │
│       NYC Taxi DAG                            │
│                                              │
└──────────────────────────────────────────────┘
```

* le plus propre pédagogiquement est de faire tourner Airflow et le pipeline Spark dans le même environnement Linux WSL.

```text
WSL2
│
├── airflow_env
│     └── Apache Airflow 3.3.1
│
└── nyc_taxi_env
├── Python
├── PySpark
├── Delta Lake
└── ton projet NYC Taxi
```

```text
Airflow
│
▼
NYC Taxi DAG
│
▼
PipelineRunner
│
├── EnvironmentSetup
├── UberBronze
├── UberSilver
├── UberGold
├── DataLoader
└── MaintenanceJob
```

metastore_db
warehouse
Hive
Delta Catalog



* Mais ton projet peut rester sur D:
* Depuis WSL : /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* correspond à : D:\data-ai-engineer-roadmap\nyc_taxi

* Vérifier si ton projet nyc_taxi peut être exécuté depuis WSL avec Python/PySpark. 
* C'est cette étape qui va déterminer exactement comment Airflow doit lancer ton PipelineRunner.
* L'objectif est de vérifier que WSL peut exécuter ton projet nyc_taxi, puis seulement après on branchera Airflow dessus.

* Depuis WSL : cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* pwd : /mnt/d/data-ai-engineer-roadmap/nyc_taxi

---
### Créer l'environnement du projet sous WSL
* cd ~
* python3 -m venv ~/nyc_taxi_env
* source ~/nyc_taxi_env/bin/activate
* python --version
* which python
* python -m pip install --upgrade pip
* pip install pyspark==3.5.1
* pip install delta-spark==3.2.0

### Tester PySpark
* python -c "from pyspark.sql import SparkSession; print('PySpark OK')"
* python -c "from delta import configure_spark_with_delta_pip; print('Delta OK')"
---

### tester ton projet
* cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* python -c "import nyc_taxi; print(nyc_taxi)"
* cd /mnt/d/data-ai-engineer-roadmap
* python -c "import nyc_taxi; print(nyc_taxi)"
* python -c "from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner; print('PipelineRunner OK')"

### Installe PyYAML dans nyc_taxi_env
* python -m pip install PyYAML
* python -c "import yaml; print('YAML OK')"
* python -c "from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner; print('PipelineRunner OK')"
* Et tu dois lancer tes commandes depuis : cd /mnt/d/data-ai-engineer-roadmap
* pas depuis /mnt/d/data-ai-engineer-roadmap/nyc_taxi

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



```text
Airflow
   ↓
PipelineRunner
   ↓
EnvironmentSetup
   ↓
UberBronze
   ↓
UberSilver
   ↓
UberGold
   ↓
DataLoader
   ↓
MaintenanceJob
   ↓
Audit
```
* il faudra que l'environnement Airflow puisse lancer ton environnement nyc_taxi_env

## Lancement manuelle depuis terminal wsl
* se placer dans : /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* python -c "from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner; print('PipelineRunner OK')"



python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
  --periode 202503 \
  --taxi_type yellow \
  --env local \

python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
--env local \
--periode 202504 \
--taxi_type yellow


python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles --periode 202502 --taxi_type yellow --env local


* une fois le lancement reussi alors on passe au dag
```text
Airflow DAG
│
▼
Task Python/Bash
│
▼
/home/alpha/nyc_taxi_env/bin/python
│
▼
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles
│
├── EnvironmentSetup
├── UberBronze
├── UberSilver
├── UberGold
├── DataLoader
├── MaintenanceJob
└── Audit
```




### Ouvrir Power Shell
* [ ] wsl -l -v
* [ ] wsl
* [ ] cd ~
* [ ] source ~/airflow_env/bin/activate
* [ ] python -m pip show pyspark
* [ ] python -m pip show delta-spark
---

* [ ] airflow dags list
* [ ] D:\data-ai-engineer-roadmap\nyc_taxi : projet actuel
* [ ] projet actuel est accessible depuis WSL comme : /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* [ ] which python
* [ ] which airflow
* [ ] python --version
* [ ] airflow version
* [ ] which java
* [ ] java -version

* [ ] python -c "import pyspark; print(pyspark.__version__)"
* [ ] python -c "import delta; print(delta.__version__)"
* [ ] conda --version
* [ ] conda create -n nyc_taxi_wsl python=3.11 -y
* [ ] conda activate nyc_taxi_wsl
* [ ] python --version
* [ ] java -version

* [ ] dans (nyc_taxi_wsl) :
* [ ] pip install pyspark==3.5.1
* [ ] pip install delta-spark==3.2.0
* [ ] python -c "import pyspark; print(pyspark.__version__)"
* [ ] cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* [ ] nano test_spark.py
* [ ] python test_spark.py

* [ ] nano test_spark_derby.py
* [ ] python test_spark_derby.py

* [ ] find /mnt/d/data-ai-engineer-roadmap -name "derby.log"
* [ ] find /mnt/d/data-ai-engineer-roadmap -type d -name "spark-warehouse"
* [ ] find /mnt/d/data-ai-engineer-roadmap -type d -name "metastore_db"


* [ ] rm -rf /mnt/d/data-ai-engineer-roadmap/metastore_db
* [ ] ls -ld /mnt/d/data-ai-engineer-roadmap/metastore_db


* [ ] deactivate
* [ ] rm -rf /home/alpha/nyc_taxi_env
* [ ] ls -ld /home/alpha/nyc_taxi_env
* [ ] which -a python3
* [ ] ls -1 /usr/bin/python3*
* [ ] python3 --version


### Créer un environnement
* [ ] python3 -m venv /home/alpha/nyc_taxi_env
* [ ] source /home/alpha/nyc_taxi_env/bin/activate


### Ouvre PowerShell en administrateur et exécute : 
* [ ] wsl --status
* [ ] wsl -d Ubuntu
* [ ] python3 --version
* [ ] uname -a
* [ ] lsb_release -a
* [ ] sudo apt update
* [ ] python3 -m venv --help
* [ ] python3 -m venv ~/airflow_env
* [ ] source ~/airflow_env/bin/activate
* [ ] airflow version
* [ ] pip --version
* [ ] pip install --upgrade pip
* [ ] pip install apache-airflow --dry-run
* [ ] pip install apache-airflow
* [ ] airflow version
* [ ] mkdir ~/airflow
* [ ] export AIRFLOW_HOME=~/airflow

* [ ] echo 'export AIRFLOW_HOME=~/airflow' >> ~/.bashrc
* [ ] source ~/.bashrc

* [ ] airflow db migrate ou airflow db init


* [ ] airflow standalone
* [ ] airflow version
* [ ] airflow info
* [ ] Ctrl + C


### Démarrage
* [ ] Terminal 1 :
* [ ] wsl
* [ ] airflow scheduler
* [ ] source ~/airflow_env/bin/activate
* [ ] airflow dags list

* [ ] (airflow_env) → ton environnement Python virtuel
* [ ] /mnt/c/WINDOWS/system32 → ton répertoire courant
* [ ] source ~/airflow_env/bin/activate : tu actives le virtualenv sans changer le répertoire courant.
* [ ] cd ~
* [ ] pwd ~


* [ ] Terminal 2 : airflow api-server
* [ ] Terminal 3 : airflow webserver
* [ ] Accès navigateur Depuis Windows : http://localhost:8080

* [ ] which python
* [ ] python --version
* [ ] which pip
* [ ] python -m pip --version
* [ ] python -m pip install --upgrade pip
* [ ] python -m pip install --upgrade pip

### installer PySpark et Delta
* [ ] python -m pip install pyspark==3.5.1 delta-spark==3.2.0
* [ ] python -m pip show pyspark
* [ ] python -m pip show delta-spark

* [ ] java -version
* [ ] echo $JAVA_HOME

nano test_spark_clean.py
python test_spark_clean.py

rm -rf /mnt/d/data-ai-engineer-roadmap/metastore_db
sed -n '1,120p' nyc_taxi/src/utils/load_json.py
python -m pip install PyYAML
python -m pip show PyYAML
find /mnt/d/data-ai-engineer-roadmap -maxdepth 3 -type d -name "metastore_db" -print
find /mnt/d/data-ai-engineer-roadmap -maxdepth 3 -type d -name "spark-warehouse" -print


python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
--env local \
--periode 202507 \
--taxi_type yellow


source ~/spark4_env/bin/activate
cd /mnt/d/data-ai-engineer-roadmap
airflow standalone
http://localhost:8080

cd /mnt/d/data-ai-engineer-roadmap
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
--periode 202504 \
--taxi_type yellow

python -c "
from pathlib import Path
print(Path('/mnt/d/data-ai-engineer-roadmap/data/bronze/raw_files').exists())
"
python3 -m pip index versions pyspark

### Memoire
df -h /
du -sh /mnt/d/data-ai-engineer-roadmap/* 2>/dev/null | sort -h
du -sh /mnt/d/data-ai-engineer-roadmap/spark-warehouse/* 2>/dev/null | sort -h
ls -la /mnt/d/data-ai-engineer-roadmap/spark-warehouse/audit.db/audit_load

du -sh /home/alpha/nyc_taxi_env
du -sh /home/alpha/.ivy2
du -sh /home/alpha/.cache

### Nettoyer les caches sans toucher aux données
python -m pip cache purge

### Puis le cache Ivy de Spark/Delta :
rm -rf ~/.ivy2/cache
rm -rf ~/.ivy2/jars
du -sh ~/.cache
rm -rf ~/.cache/*

python3 -m venv ~/spark4_env
source ~/spark4_env/bin/activate
pip install --upgrade pip
pip install pyspark
python -m pip install --upgrade pip
python -c "import pyspark; import delta; print('PySpark =', pyspark.__version__); print('Delta OK')"

### les anciennes versions Delta
rm -rf spark-warehouse/*/_delta_log


echo "=== DISQUE ==="
df -h /

echo "=== PROJET ==="
du -sh /mnt/d/data-ai-engineer-roadmap/* 2>/dev/null | sort -h

echo "=== WAREHOUSE ==="
du -sh /mnt/d/data-ai-engineer-roadmap/spark-warehouse/* 2>/dev/null | sort -h

echo "=== HOME ==="
du -sh /home/alpha/* 2>/dev/null | sort -h




from delta.tables import DeltaTable

tables = [
"audit.audit_load",
"audit.audit_row_count",
"silver.silver_nyc_taxi",
"gold.gold_dim_date",
"gold.gold_dim_location",
"gold.gold_fact_trips",
"gold.gold_kpi_daily",
"ref.gold_dim_location",
]

for table in tables:
print(f"VACUUM : {table}")
DeltaTable.forName(spark, table).vacuum(168)



cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi/src/common
python spark_manager.py


which python
python --version
which pip
pip list | grep airflow
python -m pip show apache-airflow
python -m pip install apache-airflow
airflow version
python -m airflow version
ls -la /home/alpha/airflow
echo $AIRFLOW_HOME
grep "^dags_folder" /home/alpha/airflow/airflow.cfg
ls -la /mnt/d/data-ai-engineer-roadmap/airflow/dags/
nano /home/alpha/airflow/airflow.cfg
ls -la /mnt/d/data-ai-engineer-roadmap/airflow/dags/
grep "^dags_folder" /home/alpha/airflow/airflow.cfg
dags_folder = /mnt/d/data-ai-engineer-roadmap/airflow/dags
python -m airflow dags list-import-errors
python -m airflow dags list | grep nyc
python -m airflow dags report
cat /mnt/d/data-ai-engineer-roadmap/airflow/dags/nyc_taxi_dag.py
python -m airflow dags report | grep nyc_taxi
sudo lsof -i :8080
ss -ltnp | grep :8080
curl.exe http://localhost:8080
hostname -I

source ~/spark4_env/bin/activate
cat ~/airflow/simple_auth_manager_passwords.json.generated
cat ~/airflow/simple_auth_manager_passwords.json.generated
{"admin": "rbFQkhHXU2rmZUht"}
python -m airflow dags report

Le fichier DAG est trouvé
Le DAG est correctement parsé
Airflow CLI le voit comme actif


✅ Pipeline local stable  
✅ Audit fonctionnel  
✅ get_next_period fonctionnel  
✅ DAG Airflow avec 1 tâche  
✅ Paramétrage Airflow (taxi_type)  
✅ DAG découpé Bronze → Silver → Gold  
✅ Maintenance automatisée  
✅ Dashboard de monitoring (Airflow + tables audit)  

✅ Airflow est installé et fonctionne  
✅ L'interface Web est accessible  
✅ Le DAG est détecté et enregistré  
✅ Le parsing du fichier nyc_taxi_dag.py est correct  
✅ On est prêt à exécuter le pipeline depuis Airflow  


### démarrer Airflow
python -m airflow standalone

Get-ChildItem D:\data-ai-engineer-roadmap\nyc_taxi\schema\yellow
Test-Path "D:\data-ai-engineer-roadmap\metastore_db"


cd /mnt/d/data-ai-engineer-roadmap

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



jps
tasklist | findstr java