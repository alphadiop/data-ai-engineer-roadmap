# Mémo — Airflow + Docker + WSL + Windows

## 1. Contexte général

L'objectif est de mettre en place **Apache Airflow** pour orchestrer mon projet Data Engineering **NYC Taxi**.

Le projet contient déjà une pipeline PySpark organisée selon une architecture :

```text
Données NYC Taxi
       │
       ▼
    BRONZE
       │
       ▼
    SILVER
       │
       ▼
     GOLD
       │
       ▼
 Data Quality
```

Airflow aura pour rôle de **piloter cette pipeline**, et non de réaliser lui-même les transformations de données.

Par exemple :

```text
Airflow
   │
   ├── Task 1 → lancer Bronze
   │
   ├── Task 2 → lancer Silver
   │
   ├── Task 3 → lancer Gold
   │
   └── Task 4 → contrôler la qualité
```

---

# 2. Les quatre technologies

Il est important de distinguer les rôles de **Windows, WSL, Docker et Airflow**.

## Windows

Windows est mon **système d'exploitation principal**.

```text
PC
└── Windows 11
```

C'est sur Windows que fonctionne notamment :

* Docker Desktop
* mon navigateur
* Power BI
* mes outils Windows
* mon environnement de développement général

Mon projet est physiquement situé sur le disque Windows :

```text
D:\data-ai-engineer-roadmap
```

---

# 3. WSL

WSL signifie :

**Windows Subsystem for Linux**

WSL permet d'exécuter un environnement Linux directement depuis Windows.

Dans mon cas :

```text
Windows
   │
   └── WSL
        │
        └── Ubuntu
```

J'utilise Ubuntu pour travailler avec les outils Linux et Data Engineering.

Dans WSL, mon disque `D:` de Windows est accessible sous :

```text
/mnt/d/
```

Donc :

```text
Windows :
D:\data-ai-engineer-roadmap

WSL :
/mnt/d/data-ai-engineer-roadmap
```

C'est le **même emplacement physique**, simplement vu depuis deux environnements différents.

---

# 4. Docker

Docker permet d'exécuter des applications dans des **conteneurs**.

Un conteneur est un environnement isolé contenant notamment :

* l'application
* ses dépendances
* sa configuration
* son environnement d'exécution

Dans notre cas, nous utilisons Docker pour exécuter Airflow.

Architecture simplifiée :

```text
Windows
   │
   └── Docker Desktop
          │
          ├── Container Airflow API Server
          ├── Container Airflow Scheduler
          └── Container PostgreSQL
```

Docker Desktop fournit le moteur Docker sur Windows.

---

# 5. Docker Desktop et WSL

Docker Desktop peut utiliser **WSL 2 comme backend**.

Nous avons vérifié que Docker fonctionnait avec :

```bash
docker ps
```

et avec :

```bash
docker context ls
```

Le contexte Docker utilisé était :

```text
desktop-linux
```

Cela signifie que les commandes Docker exécutées depuis WSL peuvent communiquer avec le moteur Docker fourni par Docker Desktop.

Schéma :

```text
Windows
│
├── Docker Desktop
│       │
│       └── Docker Engine
│
└── WSL Ubuntu
        │
        └── docker / docker compose
                 │
                 ▼
          Docker Engine
                 │
                 ▼
             Containers
```

---

# 6. Pourquoi utiliser Docker pour Airflow ?

Airflow possède plusieurs composants et dépendances.

Une installation classique peut être relativement lourde à configurer.

Avec Docker, on peut démarrer l'environnement avec :

```bash
docker compose up -d
```

Docker crée alors les différents conteneurs nécessaires.

Cela évite notamment d'installer directement Airflow et toutes ses dépendances dans mon environnement Python `spark4_env`.

---

# 7. Airflow

Apache Airflow est un **orchestrateur de workflows**.

Son rôle principal est de :

* planifier des traitements
* exécuter des tâches
* gérer les dépendances
* surveiller les exécutions
* gérer les erreurs et les retries
* fournir une interface graphique

Airflow ne remplace donc pas :

* Spark
* SQL
* Python
* Databricks

Il **orchestre** ces technologies.

---

# 8. Les composants Airflow que nous avons installés

Notre environnement contient principalement :

```text
Airflow
│
├── API Server
│
├── Scheduler
│
└── PostgreSQL
```

## API Server

Le **API Server** fournit l'interface permettant de communiquer avec Airflow.

C'est notamment lui qui permet d'accéder à l'interface Web :

```text
http://localhost:8080
```

Le port Docker est :

```text
8080:8080
```

Donc :

```text
Navigateur Windows
       │
       ▼
localhost:8080
       │
       ▼
Airflow API Server
```

---

# 9. Airflow Scheduler

Le **Scheduler** est le composant qui décide **quand et dans quel ordre les tâches doivent être exécutées**.

Par exemple :

```text
Task Bronze
     │
     ▼
Task Silver
     │
     ▼
Task Gold
     │
     ▼
Data Quality
```

Le Scheduler respecte les dépendances définies dans le DAG.

---

# 10. PostgreSQL

Nous avons utilisé PostgreSQL comme **base de métadonnées Airflow**.

Il ne s'agit pas de la base contenant les données NYC Taxi.

PostgreSQL contient les informations nécessaires au fonctionnement d'Airflow :

* DAGs
* tâches
* états des tâches
* historiques d'exécution
* utilisateurs/configuration selon le système d'authentification
* métadonnées Airflow

Architecture :

```text
Airflow
   │
   ├── API Server
   │
   ├── Scheduler
   │
   └── PostgreSQL
          │
          └── Métadonnées Airflow
```

Les données NYC Taxi restent dans notre pipeline Data Engineering.

---

# 11. Docker Compose

Nous avons utilisé :

```text
docker-compose.yml
```

Docker Compose permet de **décrire plusieurs conteneurs dans un seul fichier YAML**.

Au lieu de démarrer manuellement :

```text
PostgreSQL
Airflow API Server
Airflow Scheduler
```

on les décrit dans `docker-compose.yml`.

Puis :

```bash
docker compose up -d
```

permet de démarrer l'ensemble.

---

# 12. Structure de notre dossier Airflow

Nous avons créé :

```text
airflow/
│
├── docker-compose.yml
│
├── dags/
│
├── logs/
│
├── plugins/
│
└── config/
```

### dags/

Contiendra les DAGs Airflow.

Exemple futur :

```text
dags/
└── nyc_taxi_pipeline.py
```

### logs/

Contient les logs des exécutions Airflow.

### plugins/

Permet d'ajouter des extensions Airflow.

### config/

Nous l'avons créé notamment lors de nos tests de configuration de l'authentification.

---

# 13. Le fichier docker-compose.yml

Notre Compose définit plusieurs services.

Simplification :

```yaml
services:

  postgres:
    image: postgres:16

  airflow-init:
    image: apache/airflow:3.0.6

  airflow-apiserver:
    image: apache/airflow:3.0.6

  airflow-scheduler:
    image: apache/airflow:3.0.6
```

Chaque service devient un **conteneur Docker**.

---

# 14. Le réseau Docker

Dans le fichier Compose, les conteneurs peuvent communiquer entre eux grâce à leur nom de service.

Par exemple :

```text
postgres
```

est utilisé comme hostname dans :

```text
postgresql+psycopg2://airflow:airflow@postgres/airflow
```

Cela signifie :

```text
utilisateur : airflow
mot de passe : airflow
serveur     : postgres
base        : airflow
```

Attention :

```text
airflow / airflow
```

ici correspondent aux **identifiants PostgreSQL**, pas aux identifiants de connexion à l'interface Web Airflow.

---

# 15. airflow-init

Nous avons un conteneur :

```text
airflow-init
```

Son rôle est notamment d'initialiser la base Airflow.

Nous avons utilisé :

```bash
airflow db migrate
```

Cette commande permet de créer/mettre à jour le schéma de la base de métadonnées Airflow.

Le conteneur `airflow-init` peut ensuite s'arrêter.

C'est normal.

Il sert principalement à l'initialisation.

---

# 16. Le problème des identifiants Airflow

Nous avons rencontré :

```text
401 Unauthorized
Invalid credentials
```

Au départ, nous pensions utiliser :

```bash
airflow users create
```

Mais la commande :

```bash
airflow users
```

n'était pas disponible.

Pourquoi ?

Parce qu'Airflow 3.0.6 utilise par défaut :

```text
SimpleAuthManager
```

et non l'ancien modèle Flask-AppBuilder utilisé dans certains exemples.

---

# 17. SimpleAuthManager

Nous avons vérifié la configuration avec :

```bash
docker compose exec airflow-apiserver \
airflow config get-value core auth_manager
```

Le résultat était :

```text
airflow.api_fastapi.auth.managers.simple.simple_auth_manager.SimpleAuthManager
```

C'est donc le gestionnaire d'authentification utilisé par notre installation.

---

# 18. Configuration finale de l'authentification

Pour notre environnement local d'apprentissage, nous avons choisi :

```yaml
AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS: "true"
```

Cette configuration permet de désactiver l'authentification classique et de considérer les utilisateurs comme administrateurs.

Nous avons vérifié :

```bash
docker compose exec airflow-apiserver \
airflow config get-value core simple_auth_manager_all_admins
```

Résultat :

```text
true
```

Puis nous avons confirmé que l'accès à Airflow fonctionnait.

---

# 19. Pourquoi nous n'utilisons finalement pas `admin:admin`

Nous avions initialement utilisé :

```yaml
AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_USERS: "admin:admin"
```

Il faut comprendre que :

```text
admin:admin
```

signifie :

```text
username : admin
role     : admin
```

Cela ne signifie pas :

```text
username : admin
password : admin
```

Le système SimpleAuthManager gère le mot de passe séparément.

Pour notre environnement local, nous avons donc simplifié la configuration avec :

```yaml
AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS: "true"
```

---

# 20. Commandes Docker importantes

### Vérifier les conteneurs

```bash
docker compose ps
```

### Démarrer

```bash
docker compose up -d
```

### Arrêter

```bash
docker compose down
```

### Voir les logs

```bash
docker compose logs airflow-apiserver --tail=50
```

ou :

```bash
docker compose logs airflow-scheduler --tail=50
```

### Entrer dans un conteneur

```bash
docker compose exec airflow-apiserver bash
```

### Exécuter une commande Airflow

```bash
docker compose exec airflow-apiserver airflow ...
```

---

# 21. Vérification de notre installation

Notre architecture actuelle est donc :

```text
                 WINDOWS 11
                     │
          ┌──────────┴──────────┐
          │                     │
       WSL Ubuntu          Docker Desktop
          │                     │
          │              Docker Engine
          │                     │
          └──────────┬──────────┘
                     │
              Docker Compose
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
     PostgreSQL   Airflow     Airflow
                  API Server  Scheduler
                     │
                     ▼
              http://localhost:8080
```

---

# 22. Relation avec mon projet NYC Taxi

L'objectif final est :

```text
                  AIRFLOW
                     │
                     ▼
              DAG NYC TAXI
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       BRONZE     SILVER      GOLD
          │          │          │
          └──────────┼──────────┘
                     ▼
                DATA QUALITY
```

Airflow va donc devenir **l'orchestrateur de mon pipeline PySpark**.

Par exemple :

```text
DAG NYC Taxi
     │
     ▼
[Bronze]
     │
     │ succès
     ▼
[Silver]
     │
     │ succès
     ▼
[Gold]
     │
     │ succès
     ▼
[Data Quality]
```

Si Silver échoue :

```text
Bronze ✅
   ↓
Silver ❌
   ↓
Gold      ← ne démarre pas
```

C'est l'un des intérêts majeurs d'Airflow : **gérer les dépendances entre traitements**.

---

# 23. Différence entre les rôles

À retenir pour un entretien :

| Technologie        | Rôle                                                        |
| ------------------ | ----------------------------------------------------------- |
| Windows            | Système d'exploitation principal                            |
| WSL                | Environnement Linux sous Windows                            |
| Docker             | Isolation et exécution des applications dans des conteneurs |
| Docker Desktop     | Fournit/administrer Docker sur Windows                      |
| Docker Compose     | Orchestration de plusieurs conteneurs                       |
| PostgreSQL         | Base de métadonnées Airflow                                 |
| Airflow            | Orchestration des workflows                                 |
| Airflow Scheduler  | Planifie et déclenche les tâches                            |
| Airflow API Server | Expose l'interface/API Airflow                              |
| PySpark            | Transforme et traite les données                            |
| Delta Lake         | Stockage transactionnel des données                         |
| Power BI           | Visualisation et analyse                                    |

---

# 24. La phrase à retenir pour un entretien

Si on me demande :

**« Pourquoi utilisez-vous WSL, Docker et Airflow ensemble ? »**

Je peux répondre :

> « Windows est mon système d'exploitation principal. J'utilise WSL pour disposer d'un environnement Linux proche de celui que l'on retrouve en production. Docker me permet d'isoler et de déployer facilement les différents composants d'Airflow, notamment l'API Server, le Scheduler et PostgreSQL. Enfin, Airflow sert d'orchestrateur pour planifier et superviser ma pipeline Data Engineering, tandis que PySpark réalise les traitements de données. »

---

# 25. Architecture globale de mon environnement

À terme, mon environnement peut être représenté ainsi :

```text
                       WINDOWS 11
                           │
                ┌──────────┴──────────┐
                │                     │
             WSL Ubuntu         Docker Desktop
                │                     │
                │               Docker Engine
                │                     │
                │              Docker Compose
                │                     │
                │       ┌─────────────┼─────────────┐
                │       │             │             │
                │       ▼             ▼             ▼
                │   PostgreSQL    Airflow API   Scheduler
                │                       │
                │                       ▼
                │                  Airflow UI
                │
                ▼
        Projet Data Engineering
                │
                ▼
             PySpark
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
    Bronze    Silver    Gold
                         │
                         ▼
                      KPIs
                         │
                         ▼
                     Power BI
```

## Conclusion

La logique fondamentale est :

**Windows héberge mon environnement de travail.**

**WSL fournit mon environnement Linux.**

**Docker fournit les conteneurs.**

**Docker Compose décrit et démarre les conteneurs.**

**PostgreSQL stocke les métadonnées d'Airflow.**

**Airflow orchestre les traitements.**

**PySpark traite les données.**

**Power BI exploite les données finales pour la visualisation.**

Le prochain objectif sera donc de connecter **Airflow à ma pipeline NYC Taxi PySpark**, en créant un DAG qui orchestre Bronze → Silver → Gold → Data Quality.
