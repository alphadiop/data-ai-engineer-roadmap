## Databricks Assets Bundles (DAB)
###### Bundle est simplement une façon de décrire un projet Databricks comme du code
###### afin de pouvoir le déployer automatiquement sur différents environnements
##### Objectif principal de Bundles : intégrer Databricks dans un processus CI/CD
---

### Asset Bundle permet de 
- [ ] décrire ton application Databricks (code + jobs + clusters + paramètres + permissions) dans des fichiers YAML, 
- [ ] puis de la déployer automatiquement.


### Tu exécutes manuellement (Sans Asset Bundles):
- [ ] ouvrir Databricks
- [ ] attacher un cluster
- [ ] lancer notebook
- [ ] vérifier les résultats
- [ ] Cela marche pour apprendre, mais ce n'est pas industrialisé.


### Avec Asset Bundles
- [ ] On ajoute une couche de déploiement


### Fichiers YAML
- [ ] databricks.yml : C'est la carte d'identité du projet
- [ ] resources/nyc_pipeline.yml : Définir le Job


### Validation
- [ ] Avant de déployer : databricks bundle validate
- [ ] La CLI vérifie :
  - [ ] YAML correct
  - [ ] chemins corrects
  - [ ] ressources valides


### Déploiement
- [ ] Commande : databricks bundle deploy

### Résultat :
- [ ] Uploading files...
- [ ] Creating job nyc_taxi_pipeline...
- [ ] Creating job cluster...
- [ ] Deployment successful

### Dans Databricks :
- [ ] Workflows
- [ ] nyc_taxi_pipeline
- [ ] apparaît automatiquement


### Exécuter le pipeline : 
- [ ] Au lieu de cliquer : databricks bundle run nyc_taxi_job
- [ ] La CLI lance : Bronze -> Silver -> Gold


### Avec Bundle :
- [ ] Git
- [ ] databricks bundle deploy
- [ ] Job Databricks
- [ ] Pipeline reproductible
---

| Avant                  | Avec Bundle           |
| ---------------------- | --------------------- |
| configuration manuelle | configuration en YAML |
| difficile à reproduire | reproductible         |
| risque d'erreur        | contrôlé par Git      |
| déploiement manuel     | automatisé            |
| difficile en équipe    | collaboratif          |



### Créer le Job
- [ ] parameters:
  - periode
  - taxi_type

### Déployer
- [ ] databricks bundle deploy

### Lancer
- [ ] databricks bundle run nyc_taxi_job
- [ ] databricks bundle run nyc_taxi_job --params periode=202603,taxi_type=yellow
- [ ] nyc_taxi_job = clé YAML du Job dans le bundle


---
### Etapes principales
- [ ] Installer la CLI Databricks
- [ ] Structure du projet
- [ ] Créer le bundle
- [ ] Déclarer le job NYC Taxi
- [ ] Définir les environnements 
- [ ] Validation
- [ ] Déploiement


#### Commandes importantes
- [ ] databricks bundle validate
- [ ] databricks bundle deploy
- [ ] databricks bundle run nyc_taxi_pipeline 
- [ ] Ces commandes permettent de valider, déployer et exécuter le projet directement depuis la CLI.



---
### Puis créer un Job Databricks :
- [ ] CreateCatalog
- [ ] CreateTables
- [ ] UberBronze
- [ ] UberSilver
- [ ] UberGold
- [ ] MaintenanceJob


---
### Les tables
```text
nyc_taxi
│
├── silver
│   └── silver_nyc_taxi
│
├── gold
│   ├── gold_fact_trips
│   ├── gold_dim_date
│   └── gold_kpi_daily
│
└── audit
    ├── audit_load
    └── audit_row_count
```
---


#### Structure actuelle de NYC Taxi
```text
Metastore
│
└── nyc_taxi
    │
    ├── bronze
    │   └── bronze_nyc_taxi
    │
    ├── silver
    │   └── silver_nyc_taxi
    │
    ├── gold
    │   ├── gold_fact_trips
    │   ├── gold_dim_date
    │   ├── gold_kpi_daily
    │   └── gold_dim_location
    │
    ├── audit
    │   ├── audit_load
    │   └── audit_row_count
    │
    └── ref
        └── taxi_zone_lookup
```

---

#### Étape 1 : Installer la CLI Databricks
- [ ] pip install databricks-cli
- [ ] winget install Databricks.DatabricksCLI
- [ ] databricks version

#### Étape 2 : Structure du projet

```text
nyc_taxi/
│
├── databricks.yml
│
├── resources/
│   ├── jobs.yml
│   └── pipelines.yml
│
├── src/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── audit/
│   ├── common/
│   ├── jobs/
│   └── utils/
│
└── tests/
```
---

#### Étape 3 : Créer le bundle
##### Depuis la racine
- [ ] databricks bundle init
- [ ] Choisir :
    - [ ] Default Python
- [ ] Cela génère : 
    - [ ] databricks.yml 
    - [ ] resources/

#### Étape 4 : Déclarer le job NYC Taxi
##### Exemple resources/jobs.yml

#### Étape 5 : Définir les environnements 
* on ajoute un fichier databricks.yml
* ainsi, avec Bundle, on décrit :
- [ ] les jobs
- [ ] les Pipelines
- [ ] les paramètres
- [ ] les clusters
- [ ] les permissions
- [ ] les environnements DEV / TEST / PROD
* Le bundle devient alors la définition complète du projet

#### Étape 6 : Validation
- [ ] databricks bundle validate

#### Étape 7 : Déploiement
- [ ] databricks bundle deploy
- [ ] databricks bundle run nyc_taxi_pipeline


### Databricks Job
- [ ] créer le point d'entrée Databricks ;
- [ ] le tester dans Databricks ;
- [ ] créer le Databricks Job ;
- [ ] tester le Job ;
- [ ] ensuite seulement, on améliorera le déploiement avec Python Wheel / Databricks Asset Bundles.



### sauvegarde du travail local
* git clean
* git reset --hard
* git add .

### Merge de release vers dev
* git merge release
* git commit -m "merge: align dev with release"
* La branche dev contient maintenant le projet complet.



````text
Git
 ↓
Bundle
 ↓
target dev
 ↓
Job Serverless
 ↓
run_pipeline.py
 ↓
Bronze → Silver → Gold → Audit
````

* databricks bundle deploy -t dev
* cd /mnt/d/data-ai-engineer-roadmap && python -c "from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner; print('IMPORT OK')"

````text
````


````text
````


````text
````
#### Le merge a été envoyé sur GitHub

# Déploiement du pipeline NYC Taxi sur Databricks

## 1. Objectif

L'objectif est de déployer automatiquement le projet NYC Taxi sur Databricks afin d'exécuter le pipeline :

```text
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Audit
```

Le déploiement est réalisé avec **Databricks Asset Bundles (DAB)**.

---

# 2. Architecture du projet

## Projet local

```text
nyc_taxi/
│
├── src/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── audit/
│   ├── jobs/
│   ├── loader/
│   └── common/
│
├── resources/
│   └── nyc_pipeline.yml
│
├── databricks.yml
│
├── setup.py
│
├── pyproject.toml
│
└── dist/
    └── nyc_taxi-1.0.0-py3-none-any.whl
```

---

# 3. Les fichiers YAML

Les fichiers YAML sont le cœur du déploiement.

## databricks.yml

C'est le point d'entrée du Bundle.

Exemple :

```yaml
bundle:
  name: nyc_taxi_pipeline

include:
  - resources/*.yml

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://adb-xxxxxxxxxxxxxxxx.xx.azuredatabricks.net
```

Rôle :

* définit le nom du bundle
* définit le workspace Databricks
* indique quels fichiers YAML doivent être chargés
* définit les environnements (dev, prod, etc.)

---

## resources/nyc_pipeline.yml

Ce fichier décrit le Job Databricks.

Exemple :

```yaml
resources:
  jobs:
    nyc_taxi_job:

      name: nyc_taxi_pipeline

      parameters:

        - name: taxi_type
          default: "yellow"

        - name: periode
          default: "202504"

      tasks:

        - task_key: run_pipeline

          python_wheel_task:

            package_name: nyc_taxi

            entry_point: nyc-taxi-pipeline

            named_parameters:

              env: databricks

              taxi_type: "{{job.parameters.taxi_type}}"

              periode: "{{job.parameters.periode}}"

          environment_key: default

      environments:

        - environment_key: default

          spec:

            environment_version: "2"

            dependencies:

              - ../dist/nyc_taxi-1.0.0-py3-none-any.whl
```

Rôle :

* crée le Job Databricks
* définit les paramètres du Job
* définit la tâche à exécuter
* définit les dépendances Python

---

# 4. Construction du package Python

Databricks ne déploie pas directement le code source.

Le code est transformé en package Python.

Commande :

```bash
python -m build
```

Résultat :

```text
dist/
└── nyc_taxi-1.0.0-py3-none-any.whl
```

Le fichier `.whl` est l'équivalent d'un package Python installable.

---

# 5. Déploiement du Bundle

Commande :

```bash
databricks bundle deploy -t dev
```

Ce que fait Databricks :

### Étape 1

Upload du wheel :

```text
dist/nyc_taxi-1.0.0-py3-none-any.whl
```

---

### Étape 2

Upload des fichiers YAML :

```text
databricks.yml
resources/nyc_pipeline.yml
```

---

### Étape 3

Création ou mise à jour du Job.

Exemple :

```text
Updated jobs.nyc_taxi_job
```

---

# 6. Exécution du Job

Lancement :

```bash
databricks bundle run nyc_taxi_job -t dev
```

ou directement depuis l'interface Databricks :

```text
Workflows
   ↓
Jobs
   ↓
nyc_taxi_pipeline
   ↓
Run now
```

---

# 7. Passage des paramètres

Les paramètres définis dans le YAML sont injectés dans le code Python.

YAML :

```yaml
periode: "{{job.parameters.periode}}"
```

Code Python :

```python
args.periode
```

Exemple :

```text
Job
    periode = 202504
```

↓

```python
context.periode = 202504
```

↓

```python
Bronze
Silver
Gold
```

---

# 8. Gestion des périodes

Deux modes sont possibles.

## Mode manuel

Le Job reçoit :

```text
202504
```

Le pipeline charge :

```text
202504
```

uniquement.

---

## Mode automatique

Le pipeline consulte :

```text
nyc_taxi.audit.audit_load
```

pour récupérer la dernière période chargée avec succès.

Exemple :

```text
202501 SUCCESS
202502 SUCCESS
202503 SUCCESS
202504 SUCCESS
```

Le pipeline calcule :

```text
202505
```

et charge automatiquement le mois suivant.

Fonction utilisée :

```python
AuditManager.get_next_period()
```

---

# 9. Audit du pipeline

Table :

```text
nyc_taxi.audit.audit_load
```

Contient :

```text
run_id
periode
status
start_time
end_time
duration_seconds
```

Exemple :

```text
202504 SUCCESS
```

Cette table sert à :

* suivre les exécutions
* détecter les erreurs
* calculer la prochaine période

---

# 10. Audit des volumes de données

Table :

```text
nyc_taxi.audit.audit_row_count
```

Contient :

```text
table_name
row_count
periode
```

Exemple :

```text
silver_nyc_taxi 3776318
gold_fact_trips 3776318
```

Cette table permet de vérifier :

* qu'aucune donnée n'a été perdue
* que Silver et Gold sont cohérents

---

# 11. Vérification du chargement

Exemple SQL :

```sql
SELECT
    periode,
    COUNT(*)
FROM nyc_taxi.silver.silver_nyc_taxi
GROUP BY periode
ORDER BY periode;
```

Résultat :

```text
202501 3323486
202502 3421081
202503 3955117
202504 3776318
```

Cela confirme que les données sont bien présentes dans Delta Lake.

---

# 12. Ce qui est maintenant opérationnel

## Ingestion

```text
Volumes Unity Catalog
```

---

## Bronze

```text
Parquet → Bronze
```

---

## Silver

```text
Nettoyage
Validation
Normalisation
```

---

## Gold

```text
Fact Trips
Dim Date
KPI Daily
```

---

## Audit

```text
audit_load
audit_row_count
```

---

## Databricks

```text
Catalog
Schemas
Delta Tables
Volumes
Job
Bundle
```

---

# 13. Prochaine étape

La prochaine étape logique est l'orchestration.

Architecture cible :

```text
Airflow
    ↓
Databricks Job
    ↓
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Audit
```

Le DAG Airflow n'exécutera plus directement le code PySpark.

Il déclenchera simplement le Job Databricks via l'API Databricks.

C'est l'architecture la plus proche d'un environnement Data Engineer de production.

