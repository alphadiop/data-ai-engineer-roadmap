## Databricks Assets Bundles (DAB)
###### Bundle est simplement une façon de décrire un projet Databricks comme du code
###### afin de pouvoir le déployer automatiquement sur différents environnements
##### Objectif principal de Bundles : intégrer Databricks dans un processus CI/CD
---

### Asset Bundle permet de 
- [ ] décrire ton application Databricks (code + jobs + clusters + paramètres + permissions) dans des fichiers YAML, 
- [ ] puis de la déployer automatiquement.


### Tu exécutes manuellement :
- [ ] ouvrir Databricks
- [ ] attacher un cluster
- [ ] lancer notebook
- [ ] vérifier les résultats
- [ ] Cela marche pour apprendre, mais ce n'est pas industrialisé.


### Avec Asset Bundles
- [ ] On ajoute une couche de déploiement




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
* Ces commandes permettent de valider, déployer et exécuter le projet directement depuis la CLI.


### architecture conseillée
```text
nyc_taxi
│
├── src
│   ├── bronze
│   ├── silver
│   ├── gold
│   ├── audit
│   ├── common
│   └── jobs
│
├── schema
│
├── tests
│
├── resources
│   └── jobs.yml
│
└── databricks.yml
```

---
### Puis créer un Job Databricks :
```text
CreateCatalog
      ↓
CreateTables
      ↓
UberBronze
      ↓
UberSilver
      ↓
UberGold
      ↓
MaintenanceJob
```

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

```text
 Bronze
   ↓
 Silver
   ↓
 Gold
   ↓
 Audit
```


pourra devenir un Job Databricks : 

```text
CreateCatalog
      ↓
CreateTables
      ↓
UberBronze
      ↓
UberSilver
      ↓
UberGold
      ↓
MaintenanceJob
```
* avec exécution planifiée tous les jours.






