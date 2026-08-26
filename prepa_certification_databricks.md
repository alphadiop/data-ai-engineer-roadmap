
```
nyc_taxi                         ← Catalog
│
├── bronze                        ← Schema (données brutes)
│    └── bronze_nyc_taxi           ← Table Delta brute
│
├── silver                        ← Schema (données nettoyées)
│    └── silver_nyc_taxi           ← Table Delta nettoyée/enrichie
│
├── gold                          ← Schema (données analytiques)
│    ├── gold_dim_date            ← Dimension temps
│    ├── gold_dim_location        ← Dimension localisation
│    ├── gold_fact_trips          ← Table de faits des courses
│    └── gold_kpi_daily           ← Indicateurs journaliers
│
├── ref                           ← Schema (données de référence)
│    └── taxi_zone_lookup         ← Référentiel des zones NYC Taxi
│
├── audit                         ← Schema (suivi technique)
│    └── audit_load               ← Historique des chargements
│
└── information_schema            ← Métadonnées Unity Catalog
     ├── tables                   ← Liste des tables
     ├── columns                  ← Colonnes et types
     ├── schemata                 ← Liste des schemas
     ├── views                    ← Liste des vues
     ├── routines                 ← Fonctions SQL
     └── privileges               ← Droits d'accès

```

* Which reference structure do you use to reference a data asset within code?
* We use the three-level namespace: catalog.schema.object to reference data assets in code.

* Where do data assets such as tables, models, and volumes live?
* Data assets live inside a Unity Catalog metastore, organized into catalogs, schemas, and objects.


* What happens when you change the language of a cell away from the default for the notebook?
* When you change the language of a cell, Databricks uses a magic command to execute that cell in the selected language while keeping the notebook's default language unchanged.

* You granted a user SELECT on a table, but they still cannot query it. What are they likely missing?
* They are likely missing USE CATALOG and/or USE SCHEMA privileges. In Unity Catalog, users need permission to access the parent objects before they can access the table.

* The default language of your notebook is Python. How do you get plain SQL from Assistant instead of PySpark SQL?
* Include the language you want in your prompt

* In Free Edition, what happens when you run a notebook cell without attaching compute?
* A serverless compute session is automatically started and attached to the notebook


* You do not remember the exact name of a table. How can you still find it with the search bar?
* Use partial keywords in the search bar. Databricks search supports partial matches, so you do not need the exact table name.


* What does the Popular list in the Your resources section of the Home page show?
* The Popular list shows assets that are frequently visited or used by other users in the workspace.

* Why is it useful to run SELECT current_catalog(), current_schema(); in a notebook?
* To know whether you need to fully qualify table names or can rely on the defaults
