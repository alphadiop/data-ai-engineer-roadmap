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


