# Deployment Guide – NYC Taxi

## 1. Objectif

Ce document décrit les différentes méthodes de déploiement et d'exécution du pipeline NYC Taxi.

Le projet peut être exécuté dans plusieurs environnements :

```text
Local
  │
  ├── Python / PySpark
  │
  ▼
Docker / Airflow
  │
  ▼
Databricks
  │
  ▼
GitHub Actions
```

L'objectif est de conserver la même logique métier tout au long du cycle de développement.

---

# 2. Prérequis

## Environnement local

Les principaux composants utilisés sont :

* Python
* PySpark
* Delta Lake
* Java
* Git
* WSL2 sous Windows

Exemple d'environnement :

```text
Python 3.14
PySpark 3.5.1
Delta Lake 3.2.0
Java 17
```

---

# 3. Installation du projet

Cloner le repository :

```bash
git clone <repository-url>
```

Accéder au projet :

```bash
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
```

Créer ou activer l'environnement Python :

```bash
source spark4_env/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Installer le package :

```bash
pip install .
```

---

# 4. Exécution locale

Le pipeline peut être exécuté directement depuis le terminal.

Exemple :

```bash
python -m nyc_taxi.src.jobs.run_pipeline \
  --env local \
  --taxi_type yellow \
  --periode 202505
```

Les paramètres principaux sont :

| Paramètre     | Description               |
| ------------- | ------------------------- |
| `--env`       | Environnement d'exécution |
| `--taxi_type` | Type de taxi              |
| `--periode`   | Période au format YYYYMM  |

Exemple :

```bash
--env local
--taxi_type yellow
--periode 202505
```

---

# 5. Exécution avec Docker et Airflow

Le projet contient un environnement Airflow permettant d'orchestrer le pipeline.

Accéder au répertoire Airflow :

```bash
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi/airflow
```

Démarrer les services :

```bash
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker compose ps
```

L'interface Airflow est accessible localement sur :

```text
http://localhost:8080
```

Le DAG principal est :

```text
nyc_taxi_airflow
```

Le DAG déclenche le pipeline Python avec les paramètres nécessaires.

---

# 6. Architecture Airflow

```text
Airflow
   |
   v
nyc_taxi_airflow
   |
   v
run_nyc_taxi_pipeline
   |
   v
PipelineRunner
   |
   +---- EnvironmentSetup
   |
   +---- ReferenceDataLoader
   |
   +---- Bronze
   |
   +---- Silver
   |
   +---- Gold
   |
   +---- DataLoader
   |
   +---- MaintenanceJob
   |
   +---- Audit
```

Airflow joue principalement le rôle d'orchestrateur.

La logique métier reste dans le package Python.

Cette séparation permet de réutiliser le même pipeline depuis :

* le terminal ;
* Airflow ;
* Databricks ;
* GitHub Actions ;
* les tests automatisés.

---

# 7. Databricks Asset Bundles

Le déploiement Databricks utilise les **Databricks Asset Bundles**.

Le fichier principal est :

```text
databricks.yml
```

Il définit notamment :

* le bundle ;
* les targets ;
* les variables ;
* les jobs Databricks ;
* les paramètres d'exécution.

Exemple de structure :

```text
nyc_taxi/
│
├── databricks.yml
│
├── src/
│   └── jobs/
│       └── pipeline_runner_jobs_bundles.py
│
└── ...
```

---

# 8. Configuration Databricks

Les informations d'authentification ne sont pas stockées dans Git.

Les variables suivantes sont utilisées :

```text
DATABRICKS_HOST
DATABRICKS_CLIENT_ID
DATABRICKS_CLIENT_SECRET
```

Elles doivent être configurées dans l'environnement d'exécution ou dans les secrets GitHub Actions.

---

# 9. Validation du Bundle

Depuis le répertoire :

```bash
cd /mnt/d/data-ai-engineer-roadmap/nyc_taxi
```

Exécuter :

```bash
databricks bundle validate
```

Cette commande permet de vérifier la configuration du bundle avant le déploiement.

---

# 10. Déploiement du Bundle

Déployer le bundle :

```bash
databricks bundle deploy
```

Le déploiement permet de publier les ressources Databricks définies dans :

```text
databricks.yml
```

---

# 11. Exécution du Job Databricks

Le job peut ensuite être lancé avec :

```bash
databricks bundle run nyc_taxi_job
```

Les paramètres peuvent être transmis au pipeline :

```bash
databricks bundle run nyc_taxi_job \
  --params taxi_type=yellow,periode=202505
```

Le job utilise :

```text
src/jobs/pipeline_runner_jobs_bundles.py
```

comme point d'entrée Databricks.

---

# 12. CI/CD avec GitHub Actions

Le projet utilise GitHub Actions pour automatiser les contrôles et le déploiement.

Les workflows sont organisés dans :

```text
.github/workflows/
```

Exemple :

```text
.github/
└── workflows/
    ├── ci.yml
    └── run-databricks.yml
```

---

# 13. Workflow CI

Le workflow :

```text
ci.yml
```

est déclenché notamment lors des push et pull requests sur :

```text
dev
main
```

Il réalise plusieurs contrôles.

### Python

```bash
python -m pytest -q nyc_taxi/tests
```

Puis :

```bash
python -m compileall -q nyc_taxi/src
```

et :

```bash
python -m compileall -q nyc_taxi/config
```

Les imports principaux sont également vérifiés.

---

# 14. Validation Airflow dans CI

GitHub Actions vérifie également l'environnement Docker/Airflow.

Les principales étapes sont :

```bash
docker compose config
```

puis :

```bash
docker compose build
```

et :

```bash
docker compose run --rm airflow-init
```

Cela permet de détecter rapidement les erreurs de configuration Docker ou Airflow.

---

# 15. Validation Databricks dans CI

Le workflow CI vérifie également le bundle Databricks :

```bash
databricks bundle validate
```

puis :

```bash
databricks bundle deploy
```

Les credentials Databricks sont fournis par les secrets GitHub Actions.

---

# 16. Exécution Databricks depuis GitHub Actions

Le workflow :

```text
.github/workflows/run-databricks.yml
```

permet de lancer manuellement le job Databricks.

Les paramètres sont sélectionnés lors du déclenchement du workflow :

```text
taxi_type
periode
```

Exemple :

```text
taxi_type = yellow
periode   = 202505
```

Le workflow exécute :

```bash
databricks bundle run nyc_taxi_job \
  --params taxi_type=yellow,periode=202505
```

---

# 17. Gestion des environnements

Le pipeline utilise un paramètre d'environnement :

```text
local
docker
databricks
```

Cette abstraction permet de conserver une logique de traitement commune tout en adaptant les ressources techniques à l'environnement.

```text
                PipelineRunner
                      |
          +-----------+-----------+
          |           |           |
        local       docker    databricks
          |           |           |
        Spark       Airflow     Spark
```

---

# 18. Stratégie Git

Le développement est organisé autour de plusieurs branches :

```text
main
 │
 └── version stable
     
dev
 │
 └── développement et intégration
```

Le principe est :

```text
Développement
     |
     v
dev
     |
     v
CI GitHub Actions
     |
     v
Validation
     |
     v
main
```

Les versions importantes peuvent être identifiées avec des tags Git.

Exemple :

```bash
git tag
```

---

# 19. Contrôle avant déploiement

Avant de pousser une modification :

```bash
git status
```

Puis lancer les tests :

```bash
python -m pytest -q nyc_taxi/tests
```

Vérifier la compilation :

```bash
python -m compileall -q nyc_taxi/src
```

Valider le bundle :

```bash
cd nyc_taxi
databricks bundle validate
```

Puis :

```bash
git add -A
git commit -m "description de la modification"
git push origin dev
```

GitHub Actions prend ensuite le relais.

---

# 20. Monitoring du pipeline

Chaque exécution produit des informations permettant de suivre le traitement.

Les principaux éléments surveillés sont :

* `run_id`
* `periode`
* `taxi_type`
* `status`
* durée d'exécution ;
* nombre de lignes ;
* erreurs éventuelles.

Exemple :

```text
AUDIT |
run_id=1789730352 |
periode=202505 |
table=silver_nyc_taxi |
taxi_type=yellow |
status=SUCCESS
```

---

# 21. Audit et traçabilité

Le pipeline écrit les informations d'exécution dans :

```text
nyc_taxi.audit.audit_load
```

Les volumes traités sont enregistrés dans :

```text
nyc_taxi.audit.audit_row_count
```

Cela permet de conserver un historique des traitements.

Exemple :

```text
Bronze
4 591 845 rows

Silver
4 284 519 rows

Gold fact
4 284 519 rows
```

---

# 22. Rechargement d'une période

Le pipeline utilise le partitionnement :

```text
periode
```

Lorsqu'une période est retraitée, l'écriture utilise un overwrite ciblé sur cette partition.

Exemple conceptuel :

```text
periode = 202505
```

Le traitement ne nécessite donc pas de réécrire toutes les périodes déjà présentes.

Cette stratégie permet de limiter les traitements et les coûts de calcul.

---

# 23. Maintenance Delta

Une étape de maintenance est exécutée après le traitement.

Elle prend notamment en charge les opérations de maintenance des tables Delta concernées.

Le nettoyage utilise la politique de rétention configurée dans l'environnement Databricks.

---

# 24. Flux de déploiement complet

```text
Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    +----------------------+
    |                      |
    v                      v
Python Tests          Docker/Airflow
    |                      |
    +----------+-----------+
               |
               v
       Databricks Bundle
               |
               v
       bundle validate
               |
               v
        bundle deploy
               |
               v
        Databricks Job
               |
               v
      PipelineRunner
               |
               v
     Bronze → Silver → Gold
               |
               v
             Audit
               |
               v
          Power BI
```

---

# 25. Résultat attendu

Un déploiement réussi doit permettre d'obtenir :

```text
PIPELINE FINALIZED - STATUS = OK
```

ainsi qu'un enregistrement d'audit :

```text
status = SUCCESS
```

dans :

```text
nyc_taxi.audit.audit_load
```

et les informations de volumétrie correspondantes dans :

```text
nyc_taxi.audit.audit_row_count
```

---

# 26. Bonnes pratiques

Le projet applique les principes suivants :

* séparation du code métier et de l'orchestration ;
* configuration externalisée ;
* secrets hors du repository ;
* tests automatisés ;
* CI/CD ;
* déploiement déclaratif avec Databricks Asset Bundles ;
* traitement incrémental ;
* partitionnement Delta ;
* audit des traitements ;
* contrôle des volumes ;
* logs d'exécution ;
* séparation des environnements.

---

# 27. Évolutions envisagées

Le processus de déploiement pourra évoluer vers :

```text
GitHub
   |
   v
CI
   |
   v
Validation
   |
   v
Dev
   |
   v
Integration
   |
   v
Production
```

avec notamment :

* environnements Databricks `dev` / `prod` ;
* approbation avant production ;
* Unity Catalog ;
* gouvernance des données ;
* tests de qualité automatisés ;
* déploiement de dashboards Power BI ;
* monitoring centralisé.
