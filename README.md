# Data Engineer & AI Engineer Learning Roadmap
## Framework Databricks ou environnement Databricks
### Progression

## Databricks gère
* [ ] dépendances
* [ ] monitoring
* [ ] qualité
* [ ] orchestration
* [ ] lineage


## Activités principales à 95%
* [ ] Catalog
* [ ] Schema
* [ ] Tables
* [ ] Permissions

### Fondations
- [ ] Python
- [ ] SQL
- [ ] Spark
- [ ] Delta Lake
- [ ] Maintenance
- [ ] Industrialisation

### Data Engineering
- [ ] Ingestion
- [ ] ETL
- [ ] Streaming
- [ ] Auto Loader
- [ ] Jobs
- [ ] orchestration Jobs

### Machine Learning
- [ ] Classification
- [ ] Régression
- [ ] Clustering
- [ ] Evaluation modèles
- [ ] Scikit-learn
- [ ] MLflow

### GenAI
- [ ] Embeddings
- [ ] Vector Search
- [ ] Vector database
- [ ] RAG
- [ ] Prompt engineering
- [ ] Fine-tuning
- [ ] Agents

## Validation
- [ ] Théorie comprise
- [ ] Exercices réalisés
- [ ] Notebook Databricks créé
- [ ] Commit GitHub effectué

## Le Bundle va gérer :
- [ ] Toù déposer le code ;
- [ ] Tquel job créer ;
- [ ] Tquel cluster utiliser ;
- [ ] Tquelles permissions appliquer ;
- [ ] Tquels paramètres passer.

## déploiement des traitements
- [ ] Aller dans Databricks
- [ ] Créer un Job
- [ ] Choisir le notebook Python
- [ ] Choisir le cluster
- [ ] Configurer les paramètres
- [ ] Lancer

## Sans Databricks Asset Bundle
- [ ] créer les Jobs Databricks dans l'interface
- [ ] configurer les tâches
- [ ] configurer les paramètres
- [ ] maintenir les Jobs

## Avec Databricks Asset Bundle
- [ ] Ajouter databricks.yml
- [ ] Le Job est décrit dans ce fichier texte versionné dans Git.
- [ ] Donc stockage de la configuration Databricks


---
## Spark
- [ ] Spark DataFrame
- [ ] Read CSV
- [ ] Read Parquet
- [ ] Write Delta
- [ ] Read Delta
- [ ] saveAsTable
- [ ] Filter
- [ ] Select
- [ ] GroupBy
- [ ] OrderBy
- [ ] SQL

---
## workspaces Databricks : environnement de travail
- [ ] Notebooks
- [ ] Jobs
- [ ] Dashboards
- [ ] Clusters
- [ ] Fichiers du Workspace
- [ ] Permissions utilisateur
- [ ] Repos Git
- [ ] chaque workspaces est rattaché à un metastore
- [ ] un workspaces utilise un metastore pour acceder aux catalog, auxtables, aux schemas...

### Metastore
- [ ] Workspace A
- [ ] Workspace B
- [ ] Workspace C


### Chaque équipe peut avoir son propre workspace
- [ ] Workspace Développement
- [ ] Workspace Recette
- [ ] Workspace Production

## Metastore : stocke les métadonnées des objets de données
- [ ] tous les catalogs
- [ ] les permissions
- [ ] les external locations
- [ ] les storage credentials
- [ ] les tables enregistrées
- [ ] Le metastore ne contient pas les données elles-mêmes, mais leur description et leur emplacement.

### Par analogie : 
- [ ] Workspace = les bureaux
- [ ] Metastore = la bibliothèque centrale
---

## Unity Catalog
- [ ] Metastore
- [ ] Catalogs
- [ ] Schemas
- [ ] Tables
- [ ] Volumes
- [ ] External Location
- [ ] Managed Table
- [ ] External Table
- [ ] Grants
- [ ] Ownership
- [ ] Permissions
- [ ] SQL



## Schema
- [ ] tables
- [ ] vues
- [ ] fonctions
- [ ] volumes
---


---
## Delta Lake
- [ ] ACID transactions
- [ ] Delta Table
- [ ] Time Travel
- [ ] Data Versioning
- [ ] Rollback
- [ ] Historique
- [ ] DESCRIBE DETAIL
- [ ] MERGE INTO
- [ ] OPTIMIZE
- [ ] VACUUM DRY RUN
- [ ] VACUUM
- [ ] ANALYZE TABLE
- [ ] Bundle


---
## Streaming 
- [ ] Auto Loader
- [ ] Structured Streaming
- [ ] Kafka
- [ ] readStream
- [ ] writeStream
- [ ] checkpoint
- [ ] watermark
- [ ] trigger
- [ ] foreachBatch

---
## Industrialisation
- [ ] Git
- [ ] Databricks Asset Bundles
- [ ] CI/CD
- [ ] Databricks Workflows
- [ ] Monitoring
- [ ] Logging
- [ ] Audit
- [ ] Tests Unitaires
- [ ] Déploiement DEV
- [ ] Déploiement PROD

---
## Lakehouse avancé
- [ ] Unity Catalog avancé
- [ ] Permissions
- [ ] Lineage
- [ ] Delta Live Tables
- [ ] Lakeflow


## Projet Uber Taxi

## Paramètres à choisir
- [ ] type_taxi
- [ ] periode

## setup
- [ ] catalog : nyc_taxi
- [ ] schema  : gold
- [ ] table   : gold_fact_trips
- [ ] volumes : stocker les fichiers télechargés

## catalog
- [ ] nyc_taxi
- [ ] sales
- [ ] finance
- [ ] hr

## nyc_taxi (schema)
- [ ] bronze
- [ ] silver
- [ ] gold
- [ ] audit
- [ ] ref
---


## three-level namespace
- [ ] catalog.schema.table
---

#### silver
- [ ] silver_nyc_taxi

#### silver
- [ ] gold_fact_trips
- [ ] gold_dim_date
- [ ] gold_kpi_daily

#### tables audit
- [ ] audit_load
- [ ] audit_row_count


---
### class Python
- [ ] CatalogManager
- [ ] DeltaManager
- [ ] AuditManager
- [ ] SchemaManager
- [ ] UberBronze
- [ ] UberSilver
- [ ] UberGold
- [ ] MaintenanceJob 


## class AuditManager
- [ ] insert_audit()
- [ ] insert_row_count()
- [ ] is_period_loaded()


## class CatalogManager
- [ ] create_catalog()
- [ ] drop_catalog()
- [ ] create_schema()
- [ ] drop_schema()
- [ ] show_catalogs()
- [ ] show_schemas()
- [ ] show_tables()

## class DeltaManager
- [ ] create_table()
- [ ] drop_table()
- [ ] read_delta()
- [ ] write_delta()
- [ ] optimize()
- [ ] vacuum()
- [ ] history()
- [ ] describe_detail()
- [ ] time_travel()
- [ ] sauvegarde_tables_delta()
---

* note :
* distinguer un cas métier attendu d'une vraie erreur technique
* par exemple : sur le projet taxi_nyc : voiloir télécharger une période qui n'existe pas est différent d'une vraie erreur
