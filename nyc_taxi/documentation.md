# Databricks – Guide d'apprentissage et Projet NYC Taxi

## 1. Architecture Unity Catalog

### Hiérarchie

#### Framework Databricks
```text
Metastore
│
├── Catalog
│   ├── Schema
│   │   ├── Table
│   │   ├── View
│   │   └── Volume
│   │
│   └── Schema
│
└── Catalog
```

### Définitions

#### Metastore

Le metastore est le conteneur principal qui regroupe :

* Catalogs
* Permissions
* Tables
* Volumes
* External Locations

#### Catalog

Un catalog sert à isoler et organiser les données.

Exemple :

```text
nyc_taxi
sales
finance
hr
```

#### Schema

Un schema est un sous-dossier du catalog.

Il contient :

* Tables
* Views
* Functions
* Volumes

Exemple :

```text
nyc_taxi.bronze
nyc_taxi.silver
nyc_taxi.gold
nyc_taxi.audit
nyc_taxi.ref
```

#### Table

Les tables sont stockées dans les schémas.

Exemple :

```text
nyc_taxi.gold.gold_fact_trips
```

### Three-Level Namespace

```text
{catalog}.{schema}.{table}
```

Exemple :

```text
nyc_taxi.gold.gold_fact_trips
```

---

# 2. Compétences Databricks essentielles

## Unity Catalog

* [ ] Metastore
* [ ] Catalog
* [ ] Schema
* [ ] Table
* [ ] Volume
* [ ] External Location
* [ ] Managed Table
* [ ] External Table
* [ ] Grants
* [ ] Ownership
* [ ] Permissions
* [ ] SQL

---

## Spark

* [ ] Spark DataFrame
* [ ] Read CSV
* [ ] Read Parquet
* [ ] Write Delta
* [ ] Read Delta
* [ ] saveAsTable
* [ ] Filter
* [ ] Select
* [ ] GroupBy
* [ ] OrderBy
* [ ] SQL

---

## Delta Lake

* [ ] Delta Table
* [ ] Time Travel
* [ ] Data Versioning
* [ ] Rollback
* [ ] History
* [ ] DESCRIBE DETAIL
* [ ] OPTIMIZE
* [ ] VACUUM
* [ ] ANALYZE TABLE

---

## Streaming

* [ ] Auto Loader
* [ ] Structured Streaming
* [ ] Kafka
* [ ] readStream
* [ ] writeStream
* [ ] checkpoint
* [ ] watermark
* [ ] trigger
* [ ] foreachBatch

---

## Industrialisation

* [ ] Git
* [ ] Databricks Asset Bundles
* [ ] CI/CD
* [ ] Databricks Workflows
* [ ] Monitoring
* [ ] Logging
* [ ] Audit
* [ ] Tests Unitaires

---

# 3. Architecture du projet NYC Taxi

## Catalog

```text
nyc_taxi
│
├── bronze
├── silver
├── gold
├── audit
└── ref
```

## Schémas

### Bronze

```text
bronze_nyc_taxi
```

### Silver

```text
silver_nyc_taxi
```

### Gold

```text
gold_fact_trips
gold_dim_date
gold_dim_location
gold_kpi_daily
```

### Audit

```text
audit_load
audit_row_count
```

### Ref

```text
taxi_zone_lookup
```

---

# 4. Architecture technique du projet

## CatalogManager

Responsable du metastore.

### Fonctions

* [ ] create_catalog()
* [ ] drop_catalog()
* [ ] create_schema()
* [ ] drop_schema()
* [ ] rename_schema()
* [ ] show_catalogs()
* [ ] show_schemas()
* [ ] show_tables()

---

## DeltaManager

Responsable des tables Delta.

### Administration

* [ ] create_table()
* [ ] drop_table()
* [ ] truncate_table()
* [ ] rename_table()

### Lecture / Écriture

* [ ] read_delta()
* [ ] write_delta()
* [ ] sauvegarde_tables_delta()

### Maintenance

* [ ] optimize_table()
* [ ] optimize_period()
* [ ] vacuum()
* [ ] vacuum_dry_run()

### Historique

* [ ] history()
* [ ] describe_detail()
* [ ] time_travel()
* [ ] restore_version()

### Streaming

* [ ] read_stream()
* [ ] write_stream()

---

## AuditManager

Responsable du suivi des traitements.

### Fonctions

* [ ] insert_audit()
* [ ] insert_row_count()
* [ ] is_period_loaded()

### Suivi

* [ ] Monitoring
* [ ] Historique des chargements
* [ ] Contrôle des volumes

---

# 5. Pipeline de chargement

## Flux fonctionnel

```text
Téléchargement
      ↓
Bronze
      ↓
Silver
      ↓
Gold
      ↓
Audit
      ↓
SUCCESS
      ↓
Maintenance
```

---

## Ordre de chargement

```text
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Audit
```

---

## Ordre de maintenance

```text
OPTIMIZE
    ↓
VACUUM DRY RUN
    ↓
VACUUM
```

---

## Fréquence

### Quotidien

* [ ] OPTIMIZE

### Hebdomadaire

* [ ] VACUUM

---

# 6. Gestion des données

## Téléchargement

* [ ] Choisir une année
* [ ] Choisir un mois
* [ ] Construire l'URL
* [ ] Construire le chemin dans le Volume
* [ ] Vérifier si le fichier existe
* [ ] Télécharger uniquement si absent

---

## Chargement

* [ ] Lire le fichier avec Spark
* [ ] Ajouter la période (YYYYMM)
* [ ] Contrôler le schéma
* [ ] Appliquer les transformations
* [ ] Vérifier que la période n'est pas déjà chargée
* [ ] Charger les données Delta

---

## Contrôle de qualité

* [ ] Définir les schémas JSON
* [ ] Générer les tables Delta à partir des JSON
* [ ] Contrôler les types
* [ ] Vérifier la cohérence DataFrame / Table Delta

---

# 7. Modèle Bronze / Silver / Gold

## Batch

```text
Parquet
   ↓
Bronze
   ↓
Silver
   ↓
Gold
```

---

## Streaming

```text
Kafka
   ↓
Bronze
   ↓
Silver
   ↓
Gold
```

---

# 8. Roadmap d'apprentissage

## Semaine 1 — Spark

* [ ] DataFrames
* [ ] Read CSV
* [ ] Write Delta
* [ ] Filter
* [ ] Select
* [ ] GroupBy

---

## Semaine 2 — Unity Catalog

* [ ] Metastore
* [ ] Catalogs
* [ ] Schemas
* [ ] Tables
* [ ] Volumes
* [ ] External Location
* [ ] Managed Table
* [ ] External Table
* [ ] Grants
* [ ] Ownership
* [ ] SQL

---

## Semaine 3 — Delta Lake

* [ ] Bronze / Silver / Gold
* [ ] Delta Lake
* [ ] Time Travel
* [ ] Rollback
* [ ] Historique
* [ ] OPTIMIZE
* [ ] VACUUM
* [ ] Tests Unitaires

---

## Semaine 4 — Orchestration

* [ ] Databricks Workflows
* [ ] Jobs
* [ ] Paramètres
* [ ] Monitoring
* [ ] Logging
* [ ] Audit

---

## Semaine 5 — Streaming

* [ ] Auto Loader
* [ ] Structured Streaming
* [ ] Kafka
* [ ] readStream
* [ ] writeStream
* [ ] checkpoint
* [ ] watermark
* [ ] trigger
* [ ] foreachBatch

---

## Semaine 6 — Industrialisation

* [ ] Git
* [ ] Databricks Asset Bundles
* [ ] CI/CD
* [ ] Déploiement DEV
* [ ] Déploiement PROD

---

## Semaine 7 — Lakehouse avancé

* [ ] Unity Catalog avancé
* [ ] Permissions
* [ ] Lineage
* [ ] Delta Live Tables
* [ ] Lakeflow

---

# 9. Priorités pour décrocher une mission Databricks

## Priorité 1

* [ ] Unity Catalog

## Priorité 2

* [ ] Databricks Asset Bundles
* [ ] Git
* [ ] CI/CD

## Priorité 3

* [ ] Structured Streaming

## Priorité 4

* [ ] Lakeflow / Delta Live Tables
