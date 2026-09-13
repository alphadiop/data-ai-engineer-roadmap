
### Comprendre 
* [ ] Pourquoi on utilise Airflow
* [ ] Son architecture
* [ ] Les DAGs
* [ ] Les Operators
* [ ] La planification
* [ ] La gestion des dépendances
* [ ] Les bonnes pratiques
---

### C'est quoi Airflow ?
* [ ] Apache Airflow est un orchestrateur de workflows
* [ ] Il permet d'automatiser, planifier et superviser des traitements de données
---

#### Exemple de traitement de données
* [ ] Télécharger fichier
* [ ] Charger Bronze
* [ ] Transformer Silver
* [ ] Création de Gold
* [ ] Envoie Email

### Objectif Airflow
* [ ] s'assurer que les tâches s'exécutent dans le bon ordre
* [ ] que les erreurs sont détectées
* [ ] que les relances sont possibles
* [ ] que les traitements sont historisés


### Planification automatique.
* [ ] Le Scheduler déclenche les tâches selon le planning défini
  * Tous les jours : schedule="@daily"
  * Toutes les heures : schedule="@hourly"
  * toutes les 5 mn : schedule="*/5 * * * *"


### Pourquoi on utilise Airflow
* [ ] Airflow lance et supervise les jobs Spark mais ne remplace pas Spark.
* [ ] Airflow = orchestrateur
* [ ] Databricks = moteur d'exécution/plateforme de traitement
---

---

---
### Décrivez l'architecture Airflow."
* [ ] Scheduler -> Executor -> Workers -> Tâches


---
* [ ] Scheduler : Le Scheduler détecte les DAGs à exécuter et décide quand lancer les tâches
* [ ] Executor : L'Executor distribue les tâches et determine où les tâches seront exécutées. 
  * Exemple 
    * SequentialExecutor, 
    * LocalExecutor, 
    * CeleryExecutor, 
    * KubernetesExecutor
* [ ] Workers : Les Workers exécutent les traitements, c'est la machine qui exécute réellement les tâches
* [ ] Les résultats sont enregistrés dans la Metadata Database. 
  * Elle stocke 
    * l'historique des exécutions, 
    * les états des tâches, 
    * les utilisateurs, 
    * les configurations 
* [ ] Le Webserver permet le suivi et l'administration, 
  * c'est une interface graphique qui permet de voir 
    * les DAGs, 
    * relancer une tâche, 
    * consulter les logs



### DAG Run vs Task Instance
* [ ] Un DAG Run est une exécution complète du workflow
* [ ] Une Task Instance est l'exécution d'une tâche dans un DAG Run donné.
* [ ] Un DAG Run représente une exécution complète d'un workflow pour une date donnée, alors qu'une Task Instance représente l'exécution d'une tâche particulière dans ce DAG Run
Task Instance = Cron

### Scheduler vs Executor vs Worker
* [ ] C'est la base de l'architecture Airflow
* [ ] Scheduler décide : Il est 2h du matin, Je dois lancer le DAG.
* [ ] Il ne fait pas le travail, il donne juste les ordres

## Executor
* [ ] L'Executor reçoit l'ordre : **Exécute Bronze** et décide où exécuter la tâche

### Worker
* [ ] Le Worker exécute réellement le code. 
* Le Scheduler planifie les tâches, l'Executor décide où elles seront exécutées et les Workers exécutent effectivement le code



### Catchup et Backfill
* [ ] catchup=False signifie que Airflow ne lance que la date actuelle
* [ ] catchup=True signifie que Airflow rejoue tout le retard à part de start_date
* [ ] Backfill est manuel **airflow dags backfill** pour rejouer seulement ces dates


### XCom : XCom = Cross Communication.
* [ ] Permet à deux tâches d'échanger des informations
* [ ] XCom permet l'échange de petites informations entre tâches, comme des identifiants, des dates ou des chemins de fichiers. 
* [ ] Il n'est pas conçu pour transporter de gros volumes de données.


### Pourquoi utiliser Airflow avec Spark ?
* [ ] Spark traite les données et ne sait pas planifier
    * Lancer Bronze à 2h
    * Attendre la fin
    * Puis lancer Silver
    * Puis envoyer une alerte
* [ ] Airflow orchestre et sait faire cela
* [ ] Spark est le moteur de calcul distribué tandis qu'Airflow orchestre les différentes étapes du pipeline. 
* [ ] Spark et Airflow sont complémentaires.



### Airflow + Databricks
* [ ] Airflow peut piloter Databricks
* [ ] Architecture : Airflow -> API Databricks -> Cluster Databricks -> Notebook Spark
* [ ] Exemple : DatabricksSubmitRunOperator
* [ ] Airflow orchestre les traitements tandis que Databricks exécute les workloads Spark. 
* [ ] Airflow communique avec Databricks via son API.

### Architecture CeleryExecutor et KubernetesExecutor
* [ ] SequentialExecutor : Par défaut : Task A puis Task B puis Task C, Une seule tâche à la fois
* [ ] LocalExecutor : une seule machine, plusieurs tâches en parallèle
* [ ] CeleryExecutor : Plusieurs Workers, Très utilisé en production.
  * Avantages :
    * Scalabilité
    * Tolérance aux pannes
    * Distribution de charge
* [ ] KubernetesExecutor : Chaque tâche crée un Pod Kubernetes
    * Task A
      → Pod A
    * Task B
      → Pod B
    * Task C
      → Pod C
    * A la fin Pod supprimé
      * Avantages :
        * Scalabilité
        * Tolérance aux pannes
        * Distribution de charge
* [ ] CeleryExecutor s'appuie sur un pool de Workers permanents qui consomment les tâches depuis une file de messages. 
* [ ] KubernetesExecutor crée dynamiquement un Pod par tâche et le supprime une fois l'exécution terminée.



### Qu'est-ce qu'un DAG ?
* [ ] DAG = Directed Acyclic Graph : C'est un workflow complet
  * Task : c'est une étape du workflow
    * Exemple :
      * Téléchargement 
      * Bronze 
      * Silver 
      * Gold


### les operators
* [ ] PythonOperator : Exécute une fonction Python, Exemple : PythonOperator(...)
* [ ] BashOperator : Exécute une commande Linux, exemple : BashOperator(bash_command="python script.py")
* [ ] EmailOperator : Envoi d'e-mails
* [ ] SparkSubmitOperator : Lance un job Spark, Exemple : SparkSubmitOperator(application="pipeline.py")
* [ ] DatabricksSubmitRunOperator : Pour Databricks

### Quelle différence entre Airflow, XCom et Cron ?
* [ ] Cron : lance un script
* [ ] XCom : Échanger de petites informations entre tâches
* [ ] Airflow :
  * gère un workflow complet
  * dépendances
  * monitoring
  * retry : Si une tâche échoue, Airflow relance automatiquement default_args = {"retries": 3, "retry_delay": timedelta(minutes=5) }
  * logs
  * alertes

### Comment présenter Airflow dans ton projet NYC Taxi
* [ ] J'utiliserais Airflow pour orchestrer mon pipeline NYC Taxi. 
* [ ] Un DAG mensuel déclencherait successivement 
  * le téléchargement du fichier source, 
  * le chargement Bronze, 
  * les transformations Silver, 
  * la création des tables Gold 
  * et enfin le calcul des KPI. 
* [ ] Airflow permettrait de gérer 
  * les dépendances, 
  * les reprises sur erreur, 
  * le monitoring 
  * et l'historisation des exécutions

### Quels sont les composants principaux d'Airflow ? »
Dans Airflow 3, le DAG Processor parse les fichiers DAG et synchronise leur définition avec la metadata database. 
Le Scheduler décide quelles tâches doivent être exécutées en fonction du calendrier et des dépendances. 
L'API Server expose l'interface et les APIs. 
La metadata database, ici PostgreSQL, stocke l'état et les métadonnées des DAGs, runs et tâches.

Airflow orchestre mon pipeline PySpark NYC Taxi. 
Le DAG déclenche mon run_pipeline.py, qui exécute mon PipelineRunner et mes traitements Bronze, Silver et Gold.

```text
Windows
   │
   └── WSL Ubuntu
          │
          └── Docker
                │
                ├── PostgreSQL
                ├── Airflow API Server
                ├── Airflow Scheduler
                └── Airflow DAG Processor
```

#### Pourquoi Docker ?
* Tu aurais pu installer Airflow directement dans WSL
* Mais tu as choisi Docker parce que cela permet d'avoir un environnement Airflow isolé et reproductible.

```text
WSL
 │
 └── Docker Compose
       │
       ├── conteneur PostgreSQL
       ├── conteneur API Server
       ├── conteneur Scheduler
       └── conteneur DAG Processor
```
Chaque composant tourne dans son propre conteneur.


### Docker Compose
* Ton fichier principal est : Ton fichier principal est :
* c'est lui qui décrit ton infrastructure
* services:
  * postgres:
  * ...
  * airflow-apiserver:
  * ...
  * airflow-scheduler:
  * ...
  * airflow-dag-processor:
  * ...

* quand tu fait : docker compose up -d alors Docker Compose démarre les services
* quand tu fais docker compose ps alors tu vois leur état

### PostgreSQL : la mémoire d'Airflow
* PostgreSQL ne contient pas tes données NYC Taxi.
* Il contient les métadonnées Airflow.
* par exemple :
  * DAGs
  * DAG Runs
  * Task Instances
  * états des tâches
  * utilisateurs
  * connexions
  * variables
  * historique des exécutions
  * etc.
  * Ton Airflow utilise : postgresql+psycopg2://airflow:airflow@postgres/airflow
  * PostgreSQL est la mémoire de fonctionnement d'Airflow.




### le DAG
* airflow/dags/nyc_taxi_airflow.py : C'est le fichier qui décrit le workflow.
* Le DAG ne réalise pas directement ton pipeline Data Engineering. il orchestre tion pieline




### DAG Processor
* Lire les fichiers Python présents dans dags/, les parser et enregistrer les DAGs dans la base Airflow.
* airflow dag-processor -n 1 -v : a produit Creating ORM DAG for nyc_taxi_airflow
* puis airflow dags list a enfin affiché : nyc_taxi_airflow
* Le DAG Processor parse les fichiers DAG et synchronise leur définition avec les métadonnées Airflow.




### Scheduler
* Il regarde les DAGs et décide : Quelles tâches doivent être exécutées maintenant ?
* Il surveille notamment :
  * DAG Runs
  * Task Instances
  * dependencies
  * schedule
  * états des tâches

```text
DAG
 │
 └── run_nyc_taxi_pipeline
          │
          ▼
       Scheduler
          │
          ▼
      exécution
```


### API Server
* Il expose l'interface et les APIs Airflow
* on navigateur communique avec : http://localhost:8080
* L'API Server permet notamment à l'interface de voir :
  * DAGs
  * Runs
  * Tasks
  * Logs
  * Variables
  * Connections

```text
Navigateur
    │
    ▼
API Server
    │
    ▼
PostgreSQL
```


#### L'interface Web
* Quand tu vas sur : localhost:8080
* tu n'exécutes pas directement le fichier : nyc_taxi_airflow.py
* L'interface interroge l'API Server.
* Et PostgreSQL sait : nyc_taxi_airflow grâce au DAG Processor.

```text
Navigateur
    ↓
API Server
    ↓
PostgreSQL
```


### Chemin complet
```text
nyc_taxi_airflow.py
        │
        ▼
   DAG Processor
        │
        ▼
   PostgreSQL
        │
        ▼
    API Server
        │
        ▼
   Interface Web
```

* Puis, lorsqu'on lance le DAG :
```text
Interface Web
      │
      ▼
  API Server
      │
      ▼
 PostgreSQL
      │
      ▼
 Scheduler
      │
      ▼
   Task
      │
      ▼
run_nyc_taxi_pipeline()
      │
      ▼
 PipelineRunner
      │
      ├── Bronze
      ├── Silver
      ├── Gold
      └── Maintenance
```

### Tes volumes Docker
```text
volumes:
  - ./dags:/opt/airflow/dags
  - ./logs:/opt/airflow/logs
  - ./plugins:/opt/airflow/plugins
  - ../config:/opt/airflow/config
  - ../nyc_taxi:/opt/airflow/nyc_taxi
  - ../data:/opt/data
```

* Par exemple :
```text
WSL
airflow/dags/
       │
       │ volume
       ▼
Docker
/opt/airflow/dags/
```

* Donc ton fichier local : airflow/dags/nyc_taxi_airflow.py
* est visible dans Docker comme : /opt/airflow/dags/nyc_taxi_airflow.py



### PYTHONPATH
* PYTHONPATH: /opt/airflow
* Parce que ton DAG fait : from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
* Python doit donc savoir où chercher : /opt/airflow/nyc_taxi
* Avec : PYTHONPATH=/opt/airflow



### Ton Dockerfile : airflow/Dockerfile
* sert à construire ton image Airflow.
* Il permet notamment d'installer ce dont ton environnement a besoin.
* Conceptuellement :
```text
Dockerfile
     │
     ▼
docker build
     │
     ▼
Airflow Image
     │
     ├── Airflow
     ├── Python
     ├── Providers
     └── dépendances
```
* Puis tes services utilisent cette image :
build:
  context: .
  dockerfile: Dockerfile



### airflow-init
* Son rôle est de préparer la base Airflow.
* Il ne sert pas à exécuter ton DAG quotidiennement.
```text
airflow-init
     │
     ▼
PostgreSQL
     │
     ▼
tables Airflow
```



### Les logs
```text
```


### Tes fichiers importants
* Ton environnement peut être résumé ainsi :
```text
airflow/
│
├── docker-compose.yml       ← infrastructure
├── Dockerfile               ← image Airflow
│
├── dags/
│   └── nyc_taxi_airflow.py  ← orchestration
│
├── logs/                    ← logs Airflow
│
└── plugins/                 ← plugins éventuels
```


### Les commandes essentielles à connaître
* Voir les conteneurs : docker compose ps
* Démarrer : docker compose up -d
* Arrêter : docker compose down
* Logs Scheduler : docker compose logs airflow-scheduler
* Entrer dans le conteneur : docker compose exec airflow-scheduler bash
* Lister les DAGs : docker compose exec airflow-scheduler airflow dags list
* Tester le parsing : docker compose exec airflow-scheduler airflow dag-processor -n 1 -v
* Tester un DAG : docker compose exec airflow-scheduler airflow dags test nyc_taxi_airflow 2026-09-11


```text
                    ┌──────────────────────┐
                    │      Navigateur      │
                    │   Airflow UI :8080   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     API Server       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │   Metadata Database  │
                    └───────┬────────┬─────┘
                            ▲        ▲
                            │        │
                 ┌──────────┘        └──────────┐
                 │                              │
        ┌────────┴─────────┐          ┌─────────┴────────┐
        │  DAG Processor   │          │    Scheduler     │
        │                  │          │                  │
        │ Parse les DAGs   │          │ Planifie les     │
        │                  │          │ tâches            │
        └────────┬─────────┘          └─────────┬────────┘
                 │                              │
                 ▼                              ▼
       dags/nyc_taxi_airflow.py       run_nyc_taxi_pipeline
                                                │
                                                ▼
                                         PipelineRunner
                                                │
                                  ┌─────────────┼─────────────┐
                                  ▼             ▼             ▼
                               Bronze        Silver         Gold
```


| Élément            | Problème                        | État         |
| ------------------ | ------------------------------- | ------------ |
| DAG Processor      | absent du Compose initial       | ✅ corrigé    |
| Détection du DAG   | DAG absent de `serialized_dag`  | ✅ corrigé    |
| Pipeline PySpark   | suspicion initiale              | ✅ fonctionne |
| Spark              | suspicion initiale              | ✅ fonctionne |
| Bronze/Silver/Gold | suspicion initiale              | ✅ fonctionne |
| LocalExecutor      | worker lancé mais bloqué        | 🔧 en cours  |
| Execution API      | URL non configurée correctement | ✅ corrigée   |
| Réseau Docker      | suspicion                       | ✅ fonctionne |



```text
Airflow UI
    │
    ▼
DAG Processor ──────────────┐
    │                       │
    ▼                       │
PostgreSQL ◄──────── Scheduler
                            │
                            ▼
                      LocalExecutor
                            │
                            ▼
                         Worker
                            │
                            ▼
                Execution API
                            │
                            ▼
                airflow-apiserver:8080
                            │
                            ▼
                         ✅ OK
```


```text
```


```text
```

```text
```

```text
```