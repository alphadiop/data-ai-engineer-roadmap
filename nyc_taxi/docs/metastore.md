- [ ] spark-warehouse/ = données physiques + Delta transaction log

- [ ] metastore_db/ = catalogue Hive local
- [ ] qui sait que audit.audit_load existe
- [ ] et où se trouve sa location


### metastore
- [ ] c'est le catalogue des métadonnées de Spark/Hive
- [ ] il ne contient pas les données
- [ ] il contient les informations permettant de trouver les données

- [ ] lorsque tu fait spark.read.table("gold.gold_dim_date")
- [ ] Spark regarde d'abord dans le metastore
- [ ] Database : gold
- [ ] Table : gold_dim_date
- [ ] Format : DELTA
- [ ] Location: D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date
- [ ] Colonnes : ...
- [ ] Partition : periode

- [ ] puis Spark va lire les fichiers Delta présents dans D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date


#### C'est très proche de ce que Databricks fait avec Unity Catalog :
- [ ] Metastore → catalogue des objets
- [ ] Location → stockage physique
- [ ] Delta log → état transactionnel de la table
- [ ] Parquet → données réelles.


#### Le metastore est une base de métadonnées.
- [ ] Il ne contient pas les données elles-mêmes.
- [ ] Il contient des informations comme :
  - [ ] gold.gold_dim_date
  - [ ] D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date
  - [ ] Nom de la table
  - [ ] Colonnes
  - [ ] Types
  - [ ] Partitions
  - [ ] Emplacement physique
  - [ ] Propriétaire
  - [ ] Commentaires
- [ ] Les données réelles restent dans les fichiers Delta/Parquet
- [ ] Le metastore contient uniquement les références


### Pourquoi read.table() a besoin du metastore ?
- [ ] Quand tu fais : spark.read.table("gold.gold_dim_date")
- [ ] Spark demande au metastore : Où se trouve gold.gold_dim_date ?
- [ ] Le metastore répond : D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date
- [ ] Puis Spark lit : _delta_log/part-0000.parquet et charge les données
---


#### comment recréer toutes les entrées du metastore sans perdre une seule ligne de données ?
- [ ] Si le metastore a été perdu mais que le dossier Delta existe encore alors
- [ ] il suffit de réenregistrer la table avec LOCATION
- [ ] Delta récupère automatiquement le schéma depuis le _delta_log


### comment vérifier que les données existent ?
- [ ] path_warehouse = spark.conf.get("spark.sql.warehouse.dir")
- [ ] spark.read.format("delta").load(path_warehouse).show(200, truncate=False)
- [ ] Si cela fonctionne, les données sont intactes
- [ ] Réenregistrer une table


#### Réenregistrer une table
- [ ] Delta va créer l'entrée dans le metastore en pointant vers le dossier existant
- [ ] parcourir le spark_warehouse
- [ ] Trouver le dossier contenant _delta_log
- [ ] déduire le nom du schema (silver, gold, audit)
- [ ] déduire le nom de la table
- [ ] Vérifier si la table existe dans le métastore
- [ ] sinon : réenrégistrer automatiquement la table dans le metastore
- [ ] comme delta stocke son vrai schema dans _delta_log, alors le CREATE TABLE USING DELTA LOCATION ... récupère automatiquement la structure de la table
spark.sql("""  
  CREATE TABLE IF NOT EXISTS gold.gold_dim_date  
  USING DELTA  
  LOCATION 'D:/data-ai-engineer-roadmap/spark-warehouse/gold.db/gold_dim_date'  
  """)  


#### Resumé
- [ ] Delta Lake = stocke les données et les logs (_delta_log).
- [ ] Hive Metastore = stocke les métadonnées des tables.
- [ ] enableHiveSupport() = active ce metastore pour que saveAsTable() et read.table() fonctionnent correctement
---

---
```text
WSL
│
├── Python 3.14.4
├── Java 17
├── PySpark 3.5.1
└── Delta Spark 3.2.0
│
▼
Hive Metastore
│
▼
metastore_db
│
▼
spark-warehouse
│
├── audit/
│    ├── audit_load
│    └── audit_row_count
│
├── silver/
│    └── silver_nyc_taxi
│
├── gold/
│    ├── gold_dim_date
│    ├── gold_fact_trips
│    └── gold_kpi_daily
│
└── ref/
└── gold_dim_location
```


```text
WSL
│
├── Python
│   └── /home/alpha/nyc_taxi_env/bin/python
│
├── metastore Derby
│   └── /mnt/d/data-ai-engineer-roadmap/metastore_db
│
└── Spark warehouse
└── /mnt/d/data-ai-engineer-roadmap/spark-warehouse
```



##### Etape pour reparer une table : synchronisation entre wharesouse et metastore
```text
          Situation exceptionnelle
                   │
                   ▼
       Tables Delta existent sur disque
                   │
                   ▼
       Metastore ne les connaît plus
                   │
                   ▼
      repair_local_metastore()
                   │
                   ▼
       Tables réenregistrées
```


---
```text
       Table trouvée dans warehouse
                  │
                  ▼
       tableExists(full_name) ?
        /                    \
      NON                    OUI
      │                       │
      ▼                       ▼
CREATE TABLE             récupérer LOCATION
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
               correcte               incorrecte
                  │                       │
                  ▼                       ▼
                rien                  réparer
```


---
```text
SparkManager
│
├── warehouse = /mnt/d/.../spark-warehouse
│
├── Hive Metastore local
│
└── repair_local_metastore()
│
├── table absente → CREATE TABLE
│
├── location correcte → rien
│
└── mauvaise location → SET LOCATION
```
