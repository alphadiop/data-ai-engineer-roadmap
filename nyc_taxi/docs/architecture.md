# Architecture du Projet NYC Taxi

## Objectif

Le projet NYC Taxi a pour objectif de démontrer la mise en œuvre d'une plateforme Data Engineering moderne permettant :

* l'ingestion de données à grande échelle ;
* la transformation de données avec PySpark ;
* le stockage transactionnel avec Delta Lake ;
* l'orchestration de traitements batch ;
* le déploiement automatisé sur Databricks ;
* la mise à disposition de données prêtes pour l'analyse décisionnelle.

Le projet suit les bonnes pratiques Data Engineering utilisées dans les environnements cloud modernes.

---

# Architecture Générale

````text
            PipelineRunner
                 │
      ┌──────────┼──────────┐
      ↓          ↓          ↓
  Terminal     Airflow   Databricks
                              │
                       GitHub Actions

````
---

```text
                    NYC Taxi Dataset
                             |
                             v
                    +----------------+
                    |     Bronze     |
                    | Raw Parquet    |
                    +----------------+
                             |
                             v
                    +----------------+
                    |     Silver     |
                    | Cleaned Data   |
                    | Business Rules |
                    +----------------+
                             |
                             v
                    +----------------+
                    |      Gold      |
                    | Facts & KPIs   |
                    +----------------+
                             |
                             v
                    +----------------+
                    |   Power BI     |
                    | Analytics      |
                    +----------------+

                             ^
                             |
                    +----------------+
                    | Audit Layer    |
                    | Monitoring     |
                    +----------------+
```

---

# Architecture Médaillon

Le projet applique l'architecture Médaillon recommandée par Databricks.

## Bronze Layer

### Rôle

La couche Bronze conserve les données brutes téléchargées depuis la source officielle NYC Taxi.

### Format

* Parquet

### Emplacement

```text
/Volumes/nyc_taxi/bronze/raw_files/
```

### Exemple

```text
yellow/
└── 2025/
    ├── yellow_tripdata_2025-01.parquet
    ├── yellow_tripdata_2025-02.parquet
    ├── yellow_tripdata_2025-03.parquet
    └── ...
```

### Objectifs

* conserver la donnée source ;
* permettre le rejeu d'un traitement ;
* séparer ingestion et transformation.

---

## Silver Layer

### Rôle

La couche Silver contient les données nettoyées et enrichies.

### Table principale

```text
silver.silver_nyc_taxi
```

### Transformations réalisées

#### Contrôles qualité

* suppression des lignes invalides ;
* contrôle des distances ;
* contrôle des montants ;
* contrôle des dates.

#### Colonnes calculées

```text
trip_duration_minute
tip_percent
average_speed
pickup_hour
pickup_day_of_week
pickup_month
pickup_year
trip_date
```

### Objectifs

* fiabiliser les données ;
* standardiser les formats ;
* préparer les analyses.

---

## Gold Layer

### Rôle

La couche Gold contient les données métier prêtes à être consommées.

---

### Table de faits

```text
gold.gold_fact_trips
```

Contient les trajets enrichis utilisés pour les analyses.

---

### Table de KPI

```text
gold.gold_kpi_daily
```

Contient des indicateurs agrégés par jour.

Exemples :

* nombre de trajets ;
* chiffre d'affaires ;
* distance moyenne ;
* durée moyenne.

---

### Dimensions

#### Dimension Date

```text
ref.dim_date
```

Permet :

* analyses temporelles ;
* hiérarchies Année → Mois → Jour.

#### Dimension Localisation

```text
ref.dim_location
```

Permet :

* analyses géographiques ;
* regroupements par Borough ;
* visualisations cartographiques.

---

# Architecture Delta Lake

Toutes les tables sont stockées au format Delta Lake.

## Fonctionnalités utilisées

### ACID Transactions

Garantit :

* cohérence ;
* isolation ;
* fiabilité des écritures.

### Partitionnement

Partition principale :

```text
periode
```

Exemple :

```text
202501
202502
202503
202504
```

### Overwrite Partiel

Les rechargements sont réalisés uniquement sur la période concernée.

Exemple :

```sql
replace where periode = 202504
```

Cette approche évite de réécrire l'intégralité des tables.

---

# Architecture d'Audit

Le projet implémente une couche d'audit dédiée.

## Table audit_load

```text
audit.audit_load
```

Informations stockées :

* run_id ;
* période ;
* statut ;
* durée ;
* date de début ;
* date de fin ;
* message d'erreur éventuel.

---

## Table audit_row_count

```text
audit.audit_row_count
```

Informations stockées :

* nombre de lignes Bronze ;
* nombre de lignes Silver ;
* nombre de lignes Gold ;
* historique des chargements.

---

# Orchestration

Le pipeline peut être exécuté depuis plusieurs environnements.

## Exécution Locale

```bash
python -m nyc_taxi.src.jobs.run_pipeline \
  --env local \
  --taxi_type yellow \
  --periode 202505
```

---

## Airflow

DAG :

```text
nyc_taxi_airflow
```

Responsabilités :

* lancement du pipeline ;
* planification ;
* monitoring ;
* reprise sur incident.

---

## Databricks Jobs

Déploiement via :

```text
Databricks Asset Bundles
```

Exécution :

```bash
databricks bundle run nyc_taxi_job
```

---

# CI/CD

Le projet est intégré à GitHub Actions.

## Contrôles Automatiques

### Python

* installation des dépendances ;
* validation des imports ;
* exécution des tests unitaires.

### Docker

* validation de la configuration Airflow ;
* construction des images.

### Databricks

* validation du bundle ;
* validation du déploiement.

---




---

# Gestion des Logs

Les logs sont produits à chaque exécution.

## Informations journalisées

* environnement ;
* période ;
* durée d'exécution ;
* nombre de lignes ;
* erreurs éventuelles.

### Exemple

```text
logs/
└── yellow/
    └── 2025/
        └── 202505_20260918_112000.log
```

---

# Consommation des Données

Les tables Gold sont exposées à Power BI.

Exemples de tableaux de bord :

* chiffre d'affaires ;
* évolution mensuelle ;
* top zones ;
* analyse des trajets ;
* indicateurs opérationnels.

---

# Évolutions Futures

Les prochaines évolutions envisagées sont :

* Auto Loader ;
* Structured Streaming ;
* Delta Live Tables ;
* Unity Catalog ;
* MLflow ;
* Data Quality Expectations ;
* Lakeflow Jobs ;
* Assistant GenAI basé sur les données NYC Taxi.
