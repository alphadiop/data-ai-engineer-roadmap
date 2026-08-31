
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
* Ton projet NYC Taxi est actuellement sous Windows : D:\data-ai-engineer-roadmap\nyc_taxi
* Environnement Spark : D:\conda_envs\spark_local
* Airflow tourne sous WSL2 : /home/alpha/airflow_env

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


### Ouvrir Power Shell
* [ ] wsl
* [ ] cd ~
* [ ] source ~/airflow_env/bin/activate
---

* airflow dags list
* [ ] D:\data-ai-engineer-roadmap\nyc_taxi : projet actuel
* [ ] projet actuel est accessible depuis WSL comme : /mnt/d/data-ai-engineer-roadmap/nyc_taxi
* [ ] which python
* [ ] which airflow
* [ ] python --version
* [ ] airflow version

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


python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
--env local \
--periode 202507 \
--taxi_type yellow