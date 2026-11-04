# Récapitulatif — Orchestration du projet NYC Taxi avec Docker et Airflow

**Date :** 28 octobre 2026
**Objectif :** exécuter le pipeline NYC Taxi avec Airflow dans Docker, en utilisant Python, Spark et Delta Lake.

## 1. Objectif du projet

Le projet NYC Taxi permet de construire un pipeline de données organisé selon l'architecture Medallion :

- **Bronze** : ingestion des fichiers sources Parquet.
- **Silver** : nettoyage, typage, contrôles qualité et rejet des lignes invalides.
- **Gold** : production de tables et d'indicateurs analytiques.

Airflow sert à orchestrer et surveiller l'exécution du pipeline. Les transformations métier sont réalisées par le code Python et Spark.

## 2. Architecture générale

```text
PC Windows
D:\data-ai-engineer-roadmap\nyc_taxi
│
├── airflow/
│   ├── dags/
│   │   └── nyc_taxi_airflow.py
│   ├── logs/
│   ├── plugins/
│   └── compose.yaml
│
├── config/
│   └── variable_environnement.yaml
├── data/
│   ├── bronze/
│   └── reference/
├── schema/
└── src/
    ├── jobs/
    ├── bronze/
    ├── silver/
    ├── gold/
    └── spark/
```

Docker Compose démarre les services nécessaires à Airflow. Le code source du projet est rendu accessible depuis les conteneurs grâce aux montages Docker.

### Principaux composants

| Composant | Rôle |
|---|---|
| Docker Desktop | Permet d'exécuter les conteneurs Docker sous Windows. |
| Docker Compose | Configure et démarre les différents services. |
| Airflow Scheduler | Organise l'exécution des tâches. |
| Airflow DAG Processor | Analyse les fichiers DAG pour découvrir les workflows. |
| Airflow API Server | Expose l'interface et l'API d'Airflow. |
| PostgreSQL | Stocke les métadonnées d'Airflow. |
| Python | Exécute le code du pipeline. |
| Spark | Traite les données distribuées ou locales. |
| Delta Lake | Permet de stocker les tables au format Delta. |
| Derby | Sert de métastore local pour Spark dans la configuration actuelle. |

Spark n'est pas nécessairement un conteneur indépendant dans cette architecture : il est démarré par le code Python dans l'environnement qui exécute la tâche Airflow.

## 3. Comprendre Docker, les conteneurs et les montages

### 3.1 Docker

Docker permet d'exécuter une application dans un environnement isolé, avec ses dépendances et sa configuration.

Dans notre projet, l'environnement Docker possède notamment ses propres versions de Python, Airflow, Java et des bibliothèques Spark.

### 3.2 Conteneur

Un conteneur est une instance en cours d'exécution d'une image Docker.

Il possède son propre système de fichiers et utilise des chemins Linux, par exemple :

```text
/opt/airflow
/opt/airflow/dags
/opt/airflow/nyc_taxi
```

Ces chemins ne sont pas directement les chemins Windows de mon PC.

### 3.3 Montage Docker (*bind mount*)

Un montage relie un dossier de Windows à un emplacement dans un conteneur.

Exemple dans Docker Compose :

```yaml
volumes:
  - ..:/opt/airflow/nyc_taxi
```

Le fichier Compose étant situé dans le dossier `airflow`, `..` désigne le dossier parent `nyc_taxi`.

La correspondance est donc :

| Windows | Conteneur |
|---|---|
| `D:\data-ai-engineer-roadmap\nyc_taxi` | `/opt/airflow/nyc_taxi` |
| `D:\data-ai-engineer-roadmap\nyc_taxi\src` | `/opt/airflow/nyc_taxi/src` |
| `D:\data-ai-engineer-roadmap\nyc_taxi\config` | `/opt/airflow/nyc_taxi/config` |
| `D:\data-ai-engineer-roadmap\nyc_taxi\schema` | `/opt/airflow/nyc_taxi/schema` |

Le code source n'a donc pas besoin d'être copié manuellement dans le conteneur : il est accessible à travers le montage.

**Attention :** le montage ne traduit pas automatiquement les chemins écrits dans le code ou dans les fichiers YAML. Les chemins doivent être adaptés à l'environnement dans lequel le programme s'exécute.

## 4. Les montages configurés dans Docker Compose

Les principaux montages examinés sont :

| Source | Destination dans le conteneur | Utilité |
|---|---|---|
| `./dags` | `/opt/airflow/dags` | Fichiers DAG d'Airflow. |
| `./logs` | `/opt/airflow/logs` | Journaux des exécutions Airflow. |
| `./plugins` | `/opt/airflow/plugins` | Plugins éventuels. |
| `../config` | `/opt/airflow/config` | Configuration du projet accessible à cet emplacement. |
| `..` | `/opt/airflow/nyc_taxi` | Code source, schémas et données du projet. |
| `../data` | `/opt/data` | Données exposées séparément, notamment le référentiel géographique. |

Les chemins à gauche sont relatifs au fichier Compose. Les chemins à droite sont les emplacements dans le conteneur.

Le projet dispose ainsi de deux chemins d'accès à des ressources liées aux données : `/opt/airflow/nyc_taxi/data` et `/opt/data`.

## 5. Configuration des environnements local et Docker

Le fichier `config/variable_environnement.yaml` contient deux sections principales :

- `local` : exécution sur mon environnement Windows.
- `docker` : exécution dans les conteneurs Linux.

Exemples de chemins :

| Paramètre | Local | Docker |
|---|---|---|
| `project_root` | `D:/data-ai-engineer-roadmap/nyc_taxi` | `/opt` |
| `path_sql_schema` | Chemin Windows du projet | `/opt/airflow/nyc_taxi/schema` |
| `path_data` | Chemin Windows du projet | `/opt/airflow/nyc_taxi/data` |
| `bronze_path` | Chemin Windows vers les fichiers Parquet | `/opt/airflow/nyc_taxi/data/bronze/raw_files` |
| `ref_path` | Chemin Windows du référentiel | `/opt/data/reference/taxi_zone_lookup.csv` |
| `warehouse_dir` | Répertoire Spark local | `/opt/airflow/docker-spark-warehouse` |
| `metastore_dir` | Répertoire Derby local | `/opt/airflow/docker-metastore_db` |

Le paramètre `project_root` vaut `/opt` dans la configuration Docker, mais cela ne signifie pas que le code source est situé directement dans ce répertoire. Le code est accessible sous `/opt/airflow/nyc_taxi`.

La fonction `load_config()` charge la section correspondant à l'environnement demandé. La fonction `normalize_path()` convertit certains chemins Windows en chemins WSL/Linux lorsque l'environnement est `local` et que le système détecté est Linux.

Dans l'environnement Docker, les chemins Linux sont utilisés directement.

## 6. Déroulement d'une exécution Airflow

Le DAG utilisé est :

```text
DAG ID : nyc_taxi_airflow
Tâche  : run_nyc_taxi_pipeline
```

Les paramètres utilisés lors du test sont :

```text
periode   = 202504
taxi_type = yellow
env       = docker
```

Le déroulement est le suivant :

1. Je déclenche le DAG depuis PowerShell.
2. Airflow crée une exécution avec les paramètres fournis.
3. La tâche `run_nyc_taxi_pipeline` appelle le module `nyc_taxi.src.jobs.run_pipeline_airflow`.
4. Ce module récupère les paramètres et appelle `run_pipeline()`.
5. Le pipeline initialise notamment `SparkManager`, `PipelineLogger`, `EnvironmentSetup` et les composants de traitement.
6. Spark lit les données et exécute les transformations Bronze, Silver et Gold prévues par le pipeline.
7. Airflow enregistre l'état de la tâche et conserve les journaux d'exécution.

**Distinction importante :**

- Le DAG définit l'orchestration.
- La tâche Airflow appelle le code Python.
- Le pipeline réalise les traitements métier.
- Spark exécute les opérations de traitement des données.
- Le stockage conserve les données et les métadonnées.

## 7. Travail effectué et problèmes résolus

### 7.1 Visibilité du code dans Docker

Au départ, le code du projet n'était pas correctement accessible depuis les conteneurs utilisés.

Nous avons vérifié les montages et recréé les services Airflow concernés.

Les contrôles suivants ont ensuite réussi :

- Découverte du DAG `nyc_taxi_airflow`.
- Découverte de la tâche `run_nyc_taxi_pipeline`.
- Import du module `nyc_taxi.src.jobs.run_pipeline`.
- Chargement de la configuration `env=docker`.
- Vérification de plusieurs chemins Linux utilisés par le pipeline.

### 7.2 Initialisation de Spark

Un test Spark a été exécuté dans le conteneur `airflow-scheduler`.

Résultats :

```text
SPARK VERSION = 3.5.1

+----+
|test|
+----+
|   1|
+----+

DELTA WRITE OK
```

Ce test a confirmé que Spark démarre, exécute une requête SQL et peut écrire un fichier Delta dans le répertoire de test.

### 7.3 Erreur d'initialisation du métastore Derby

Le journal Airflow contenait l'erreur :

```text
Failed to create database '/opt/airflow/docker-metastore_db'
Directory /opt/airflow/docker-metastore_db already exists
```

L'inspection a montré que le répertoire existait, mais était vide :

```text
/opt/airflow/docker-metastore_db
Aucun fichier Derby
```

La cause immédiate était donc un répertoire existant sans base Derby initialisée.

Nous avons supprimé uniquement ce répertoire vide, puis relancé un test Spark.

Résultat :

```text
SPARK VERSION = 3.5.1

+----+
|test|
+----+
|   1|
+----+

METASTORE TEST OK
```

Le test confirme que Spark démarre et que le métastore peut s'initialiser dans cet environnement.

L'avertissement concernant `spark.local.dir` n'a pas empêché le test de réussir.

## 8. Stockage : montages, volumes et répertoires internes

Il faut distinguer trois types de stockage.

| Type | Exemple | Persistance |
|---|---|---|
| Montage de dossier Windows | Projet monté sous `/opt/airflow/nyc_taxi` | Les fichiers restent sur le disque Windows lorsque le conteneur est supprimé. |
| Volume Docker nommé | Volume PostgreSQL de Compose | Les données survivent à la suppression du conteneur, tant que le volume n'est pas supprimé. |
| Répertoire interne au conteneur | `/opt/airflow/docker-metastore_db` | Le contenu peut disparaître lors de la recréation du conteneur. |

Le métastore Derby est actuellement configuré dans un répertoire interne au conteneur qui n'est pas déclaré comme montage dédié dans la configuration examinée.

Il faut donc traiter sa persistance avant de considérer la configuration comme durable.

Il ne faut pas confondre le métastore Spark/Derby avec les métadonnées Airflow stockées dans PostgreSQL : ce sont deux systèmes différents.

## 9. Commandes de diagnostic utiles

Toutes ces commandes sont à exécuter depuis PowerShell, dans le dossier `airflow`.

### Afficher l'état des services

```powershell
docker compose ps
```

### Afficher le contenu du projet depuis le conteneur

```powershell
docker compose exec airflow-scheduler ls -la /opt/airflow/nyc_taxi
```

### Vérifier un fichier Python dans le conteneur

```powershell
docker compose exec airflow-scheduler ls -l /opt/airflow/nyc_taxi/src/jobs/run_pipeline.py
```

### Afficher les montages du scheduler

```powershell
docker inspect (docker compose ps -q airflow-scheduler) --format '{{json .Mounts}}'
```

### Lister les volumes Docker

```powershell
docker volume ls
```

### Lister les DAGs

```powershell
docker compose exec airflow-scheduler airflow dags list --bundle-name dags-folder
```

### Lister les tâches du DAG

```powershell
docker compose exec airflow-scheduler airflow tasks list nyc_taxi_airflow --bundle-name dags-folder
```

### Consulter les derniers journaux Airflow

```powershell
Get-ChildItem .\logs\dag_id=nyc_taxi_airflow -Recurse -Filter *.log |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 3 FullName, LastWriteTime
```

## 10. État d'avancement

### Validé

- [x] Code du projet accessible dans le conteneur Airflow.
- [x] DAG `nyc_taxi_airflow` découvert.
- [x] Tâche `run_nyc_taxi_pipeline` découverte.
- [x] Import des modules Python du pipeline.
- [x] Chargement de la configuration Docker.
- [x] Démarrage de Spark 3.5.1.
- [x] Exécution d'une requête SQL de test.
- [x] Écriture Delta de test.
- [x] Initialisation du métastore Derby après suppression du répertoire vide.

### À faire

- [ ] Confirmer que le DAG complet s'exécute correctement pour avril 2025.
- [ ] Examiner les éventuelles nouvelles erreurs dans les journaux.
- [ ] Vérifier les résultats produits par le pipeline.
- [ ] Vérifier la cohérence des données Bronze, Silver et Gold.
- [ ] Sécuriser la persistance du métastore Derby et des répertoires Spark.
- [ ] Corriger le diagnostic de `SparkEnvironmentLogger` si celui-ci continue à afficher les chemins `local` lorsque `env=docker`.

## 11. Modèle mental à retenir

Pour diagnostiquer un problème Docker, se poser trois questions :

1. **Où se trouve le fichier ?** Sur Windows, dans un volume Docker ou dans le système de fichiers interne d'un conteneur ?
2. **Où le code s'exécute-t-il ?** Dans PowerShell, dans un conteneur Airflow ou dans un autre environnement ?
3. **Où le résultat est-il stocké ?** Dans un dossier monté, un volume Docker ou un répertoire interne au conteneur ?

Ces trois questions permettent de comprendre la plupart des problèmes de chemins, d'accès aux fichiers et de persistance rencontrés dans ce projet.

**Prochaine étape :** vérifier le statut de la nouvelle exécution du DAG `nyc_taxi_airflow` pour `periode=202504`, `taxi_type=yellow` et `env=docker`, puis examiner les résultats ou la prochaine erreur éventuelle.
