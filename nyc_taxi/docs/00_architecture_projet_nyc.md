# Architecture du projet NYC Taxi

* [ ] Airflow = orchestrateur local
* [ ] Databricks Jobs = orchestrateur cloud
* [ ] PipelineRunner = orchestrateur métier
* [ ] Bronze/Silver/Gold = logique de traitement


```text
                    Airflow
                        │
                        ▼
                 PipelineRunner
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
    Environment    AuditManager   PipelineContext
       Setup
          │
          ▼
      UberBronze
          │
          ▼
      UberSilver
          │
          ▼
       UberGold
          │
          ▼
      DataLoader
          │
          ▼
    MaintenanceJob
          │
          ▼
      Audit tables
```

```text
Windows 11
│
├── D:\data-ai-engineer-roadmap\nyc_taxi
│       └── ton projet actuel
│
└── WSL2
└── Ubuntu
│
├── airflow_env
│     └── Airflow
│
└── spark_local
└── NYC Taxi + PySpark + Delta
```



## Classes principales

### Pipeline et orchestration

* [ ] PipelineRunner
* [ ] PipelineContext
* [ ] PipelineStep
* [ ] DataLoader
* [ ] MaintenanceJob

### Administration plateforme
* [ ] CatalogManager
* [ ] DeltaManager
* [ ] MetadataExplorer
* [ ] EnvironmentSetup
* [ ] PurgeDeltaStorage


### Audit et supervision
* [ ] AuditManager


### Validation et schémas
* [ ] SchemaManager
* [ ] PathManager


### Pipeline métier
* [ ] UberBronze
* [ ] UberSilver
* [ ] UberGold

---

# CatalogManager
Gestion du catalogue Spark, des schémas et du metastore.

### Responsabilités
* Création des catalogues
* Création des schémas
* Gestion des tables
* Gestion du metastore local
* Construction des noms de tables selon l'environnement

### Méthodes
* [ ] create_catalog()
* [ ] drop_catalog()
* [ ] create_schema()
* [ ] drop_schema()
* [ ] create_environment_schemas()
* [ ] get_table_name()
* [ ] repair_local_metastore()
* [ ] show_catalogs()
* [ ] show_schemas()
* [ ] show_tables()

---

# DeltaManager
Gestion des tables Delta Lake.

### Responsabilités
* Création des tables Delta
* Lecture / écriture
* Optimisation
* Maintenance
* Historisation

### Méthodes
* [ ] create_table()
* [ ] drop_table()
* [ ] truncate_table()
* [ ] read_delta()
* [ ] write_delta()
* [ ] sauvegarde_tables_delta()
* [ ] optimize()
* [ ] optimize_period()
* [ ] vacuum()
* [ ] history()
* [ ] describe_detail()
* [ ] time_travel()

---

# MetadataExplorer
Exploration et diagnostic de l'environnement.

### Responsabilités
* Inventaire des catalogues
* Inventaire des schémas
* Inventaire des tables
* Analyse des partitions
* Comptage des lignes
* Contrôle qualité

### Méthodes
* [ ] show_catalogs()
* [ ] show_schemas()
* [ ] show_tables()
* [ ] show_table_details()
* [ ] show_table_schema()
* [ ] show_partitions()
* [ ] get_all_row_counts()
* [ ] show_all_row_counts()
* [ ] get_real_row_counts() ← COUNT(*) réel
---

# AuditManager

Gestion de la traçabilité du pipeline.

### Responsabilités

* Audit des exécutions
* Contrôle des périodes déjà chargées
* Stockage des métriques

### Méthodes

* [ ] insert_audit()
* [ ] insert_row_counts()
* [ ] is_period_loaded()

### Tables gérées

* audit.audit_load
* audit.audit_row_count

---

# SchemaManager

Validation des schémas avant chargement.

### Responsabilités

* Validation des colonnes
* Contrôle des types
* Contrôle des colonnes obligatoires

### Méthodes

* [ ] validate_columns()
* [ ] validate_schema()
* [ ] compare_schema()

---

# UberBronze

Couche Bronze : ingestion des fichiers sources.

### Responsabilités

* Téléchargement des fichiers TLC
* Gestion du cache local
* Contrôle des périodes futures
* Lecture des fichiers Parquet

### Méthodes

* [ ] run()
* [ ] avoid_future_period()
* [ ] get_file_name()
* [ ] get_path_file()
* [ ] get_period()

### Sortie

* context.df_bronze

---

# UberSilver

Couche Silver : nettoyage et enrichissement.

### Responsabilités

* Nettoyage des données
* Contrôle qualité
* Calcul des indicateurs techniques
* Standardisation du schéma

### Méthodes

* [ ] run()

### Sortie

* context.df_silver

---

# UberGold

Couche Gold : modélisation analytique.

### Responsabilités

* Construction des tables analytiques
* Construction des KPI
* Construction des dimensions

### Méthodes

* [ ] run()
* [ ] get_fact_trips()
* [ ] get_dim_date()
* [ ] get_dim_location()
* [ ] get_kpi_daily()
* [ ] drop_tables_uber()
* [ ] purges_tables()

### Sorties

* context.df_fact_trips
* context.df_dim_date
* context.df_kpi_daily

---

# DataLoader
Chargement des DataFrames dans Delta Lake.

### Responsabilités
* Validation des schémas
* Comptage des lignes
* Écriture dans Delta
* Mise à jour des métriques du contexte

### Méthodes

* [ ] run()
* [ ] validate_schema()

---

# MaintenanceJob

Maintenance des tables Delta.

### Responsabilités

* OPTIMIZE
* VACUUM
* Nettoyage périodique

### Méthodes

* [ ] run()

---

# EnvironmentSetup

Initialisation complète d'un environnement.

### Responsabilités

* Création du catalogue
* Création des schémas
* Création des tables
* Réparation du metastore

### Méthodes

* [ ] run()
* [ ] create_catalog()
* [ ] create_schemas()
* [ ] create_tables()
* [ ] create_table()
* [ ] create_table_from_json()
* [ ] repair_metastore()

---

# PurgeDeltaStorage

Réinitialisation complète de l'environnement local.

### Responsabilités

* Suppression des schémas
* Arrêt Spark
* Suppression du warehouse
* Suppression du metastore
* Redémarrage propre

### Méthodes

* [ ] run()
* [ ] drop_schemas()
* [ ] delete_local_storage()
* [ ] truncate_all_tables()
* [ ] purge()

---

# PipelineRunner

Orchestrateur principal du pipeline.

### Responsabilités

* Création du contexte
* Exécution des étapes
* Gestion des erreurs
* Audit
* Supervision

### Méthodes

* [ ] run()

---

# Flux d'exécution

PipelineRunner
→ UberBronze
→ UberSilver
→ UberGold
→ DataLoader
→ MaintenanceJob
→ AuditManager

---

# Tables Delta

### Audit

* audit.audit_load
* audit.audit_row_count

### Silver

* silver.silver_nyc_taxi

### Gold

* gold.gold_fact_trips
* gold.gold_dim_date
* gold.gold_kpi_daily

### Référentiel

* ref.taxi_zone_lookup
