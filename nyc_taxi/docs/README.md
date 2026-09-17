# Data Engineer & AI Engineer Learning Roadmap
## Framework Databricks ou environnement Databricks
### Progression


```text
              Pipeline
                  |
                  v
           DeltaManager
                  |
                  v
          CatalogManager
             /       \
        local       Databricks
          |             |
   schema.table   catalog.schema.table
   
   
                   PipelineRunner
                       |
                       |
                PipelineContext
                       |
              env = local / dev
                       |
        -------------------------------
        |                             |
        v                             v
 Spark local                   Databricks
        |                             |
 database/schema               Unity Catalog
        |                             |
 silver.table             catalog.schema.table
 ```


```text
    DeltaManager
    │
    ├── saveAsTable()
    ├── delete_period()
    ├── optimize_table()
    ├── optimize_period()
    ├── vacuum()
    ├── vacuum_dry_run()
    ├── describe_history()
    └── describe_detail()
    |
    v
    CatalogManager.get_table_name()
 ```
## self.logger.info(f"{'='*120}")


## Databricks gère
* [ ] dépendances
* [ ] monitoring
* [ ] qualité
* [ ] orchestration
* [ ] lineage : Montre le flux des données.

## Activités principales à 95%
* [ ] Catalog
* [ ] Schema
* [ ] Tables
* [ ] Permissions

### Fondations
- [ ] Python
- [ ] SQL
- [ ] Spark
- [ ] Unity Catalog : un grand espace de stockage métier
- [ ] Delta Lake : Stockage (persistant) des données sous forme de fichiers Parquet
- [ ] Cluster : Calcul (temporaire)
- [ ] Jobs : servent à automatiser et orchestrer l'exécution de traitements
- [ ] Création manuelle des Jobs dans l'interface Databricks
- [ ] Ordonnancement automatique des Jobs
- [ ] Databricks Asset Bundles
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
- [ ] où déposer le code ;
- [ ] quel job créer ;
- [ ] quel cluster utiliser ;
- [ ] quelles permissions appliquer ;
- [ ] quels paramètres passer.

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
### Unity Catalog
- [ ] Schema
    - [ ] Table
    - [ ] View
    - [ ] Volume
    - [ ] Function

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
---

### Unity Catalog
- [ ] Niveau le plus haut de l'organisation des données dans Unity Catalog.
- [ ] Sert à isoler et organiser les données par domaine métier.
- [ ] Contient des schémas (schemas).
- [ ] Les permissions peuvent être accordées au niveau du catalog.
- [ ] Un catalog appartient à un metastore.
- [ ] Référence sous la forme : catalog.schema.object

### Schema
- [ ] Sous-conteneur d'un Catalog.
- [ ] Contient des tables, vues, volumes et fonctions.
- [ ] Sert à organiser les objets.
- [ ] Permet de gérer des permissions à un niveau intermédiaire.
- [ ] Référence sous la forme : catalog.schema.object


### Permissions
- [ ] Catalog : finance
- [ ] Schema  : reporting
- [ ] Table   : silver_nyc_taxi
- [ ] commande: GRANT USE CATALOG ON CATALOG finance TO finance_team
- [ ] commande: GRANT USE SCHEMA ON SCHEMA finance.reporting TO finance_team
- [ ] commande: GRANT SELECT ON TABLE finance.reporting.ventsilver_nyc_taxies TO finance_team
- [ ] GRANT : Accorder un droit
- [ ] USE CATALOG : Autorisation d'utiliser un catalog
- [ ] ON CATALOG finance : Sur le catalog finance
- [ ] TO finance_team : Au groupe ou utilisateur finance_team
---


---
### Delta Lake 
- [ ] pas de table modifiée partiellement
- [ ] optimistic concurrency control
---


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
- [ ] Chaque workspaces est rattaché à un metastore
- [ ] Un workspaces utilise un metastore pour acceder aux catalog, aux tables, aux schemas...

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


---
### Jobs : Lakeflow Jobs dans Databricks
- [ ] automatiser et orchestrer l'exécution de traitements
- [ ] Un job peut exécuter un notebook, un script Python, une pipeline ou plusieurs tâches liées entre elles dans un workflow


### Vue DAG (workflow)
- [ ] Databricks représente les tâches sous forme de graphe (DAG)
- [ ] Les dépendances sont gérées automatiquement.


### Pourquoi utiliser un Job ? un Job contient
- [ ] des tâches (tasks) : une unité de travail
- [ ] des paramètres : 
- [ ] un planning (schedule)
- [ ] des notifications
- [ ] l'historique des exécutions


### Une tâche peut exécuter :
- [ ] un Notebook
- [ ] un script Python
- [ ] une pipeline
- [ ] un autre Job
- [ ] du SQL
- [ ] dbt

### Trigger
- [ ] Le Trigger détermine quand lancer le Job
- [ ] Tous les jours à 01:00
- [ ] Toutes les heures
- [ ] Lancement manuel
---

### comment transmettre les paramètres au script

### Monitoring
- [ ] L'un des gros avantages des Jobs est le suivi des exécutions.
- [ ] Tu peux voir : SUCCESS
- [ ] Tu peux voir : FAILED
- [ ] Tu peux voir : SUCCESS

````text
MERGE INTO customer_target t
USING customer_source s
ON t.customer_id=s.customer_id
WHEN MATCHED THEN UPDATE
WHEN NOT MATCHED THEN INSERT
````

### comment créer un Job ?
- [ ] Jobs & Pipelines
- [ ] Create
- [ ] Job
- [ ] Task type
- [ ] Python Script
- [ ] Chemin :
- [ ] Choisir le compute puis
- [ ] Run now


### Lien avec Job et Databricks Asset Bundles
- [ ] Today : GitHub <-> Databricks
- [ ] Tomorrow : GitHub -> Databricks bundle deploy -> Databricks Job -> pipeline_runner
---



---
## Delta Lake
- [ ] ACID transactions : le transaction log
- [ ] Delta Table : fichiers de données sous forme de Parquet
- [ ] Time Travel : la fonctionnalité qui permet d'accéder à ces versions historiques
- [ ] Data Versioning : la capacité de Delta Lake à créer et conserver des versions
- [ ] Delta Log : Stocke l'historique des versions 
- [ ] Optimistic concurrency control
- [ ] Rollback : annuler une transaction avant son commit
- [ ] Historique : permet de voir toutes les opérations effectuées sur une table Delta 
- [ ] DESCRIBE DETAIL : Voir les métadonnées de la table
- [ ] MERGE INTO : Faire des UPDATE + INSERT en une seule commande
- [ ] OPTIMIZE : Réduire le nombre de fichiers et accélérer les lectures (Réorganise physiquement les données)
- [ ] VACUUM DRY RUN : montrer les fichiers devenus inutiles
- [ ] VACUUM : Supprime les anciens fichiers nécessaires au Time Travel
- [ ] ANALYZE TABLE
- [ ] Bundle :


### Historique
- [ ] Historique : permet de voir toutes les opérations effectuées sur une table Delta 
- [ ] Exemple : "DESCRIBE HISTORY nyc_taxi.silver.silver_nyc_taxi;"
- [ ] Cas d'usage : audit ; Débogage ; Time Travel ; comprendre qui a modifié la table


### DESCRIBE DETAIL
- [ ] Afficher les métadonnées d'une table Delta;
- [ ] Commande : DESCRIBE DETAIL nyc_taxi.silver.silver_nyc_taxi;
- [ ] Cas d'usage : Vérifier le partitionnement ; Connaître la taille de la table ; Vérifier les fonctionnalités Delta activées
---



### MERGE INTO


### OPTIMIZE
- [ ] Réorganiser les fichiers Delta afin d'améliorer les performances de lecture.
- [ ] Avec le temps, les écritures créent beaucoup de petits fichiers
- [ ] Les petits fichiers ralentissent les requêtes.
- [ ] OPTIMIZE fusionne ces fichiers.
- [ ] Commande : OPTIMIZE nyc_taxi.silver.silver_nyc_taxi;
- [ ] cas d'usage : améliorer les performances, réduire le nombre de fichiers; préparer une table fortement utilisée
---

### OPTIMIZE avec filtre
- [ ] Optimiser uniquement une partition :
- [ ] Commande : OPTIMIZE nyc_taxi.silver.silver_nyc_taxi WHERE periode = 202601;

### OPTIMIZE + ZORDER
- [ ] Cela regroupe physiquement les données proches dans les mêmes fichiers.
- [ ] Commande : SELECT * FROM nyc_taxi.silver.silver_nyc_taxi WHERE PULocationID = 132;
- [ ] La requête lira moins de fichiers et sera plus rapide.


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
---

---
## Projet Uber Taxi
- [ ] se connecter aux données publiques de NYC Taxi
- [ ] choisir une période données (année et mois)
- [ ] vérifier que les données ne sont pas présentes en local
- [ ] télécharger les données de la période concernée
- [ ] archiver les données télécharger
- [ ] réaliser les traitements attendus
- [ ] stocker les données Dans Delta Lake
---


## UberGold
- [ ] Construit les DataFrames.

## DataLoader
- [ ] Valide les schémas.
- [ ] Calcule les row counts.
- [ ] Charge Delta.

## MaintenanceJob
- [ ] Optimize.
- [ ] Vacuum.


---
## Environnements
- [ ] Spark local avec Delta
- [ ] Databricks Community Edition
- [ ] Databricks Workspace payant avec Unity Catalog
---

## Paramètres à choisir
- [ ] type_taxi
- [ ] periode

#### Gestion de la configuration selon l'environnement (local, dev Databricks, prod Databricks).


## setup
- [ ] catalog : nyc_taxi
- [ ] schema  : gold
- [ ] table   : gold_fact_trips
- [ ] volumes : stocker les fichiers téléchargés

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
- [ ] PipelineRunner

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

### concept
- [ ] partitionner les tables avec un grand volume


### note :
- [ ] distinguer un cas métier attendu d'une vraie erreur technique
- [ ] par exemple : sur le projet taxi_nyc : vouloir télécharger une période qui n'existe pas est différent d'une vraie erreur
---

---
## les Opérations appliquées sur une table Delta et cela qui crée de nouveaux fichiers Delta
- [ ] MERGE
- [ ] UPDATE
- [ ] DELETE
- [ ] INSERT
---

---
### Notion VACUUM : 
- [ ] Opération de maintenance qui sert à supprimer physiquement les anciens fichiers de données qui ne sont plus utilisée par une table Delta
- [ ] Lorsque l'on fait DELETE FROM Table WHERE trip_distance < 0
- [ ] Delta Lake crée de nouveau fichiers Parquet
- [ ] Les données disparaissent de la table, mais les fichiers restent physiquement présents
- [ ] Delta Lake marque les anciens fichiers comme obsolètes dans le journal Delta
- [ ] Delta conserve pendant 7 jours les anciens fichiers pour permettre le Time Travel
- [ ] Toute nouvelle opération sur la table utilise les fichiers récents
- [ ] les anciens fichiers restent stockés et consomment de l'espace
- [ ] VACUUM parcourt le journal Delta et supprime les fichiers devenus inutiles
---

---
```text
Table Delta

Version 1
├── part-001.parquet
└── part-002.parquet

Version 2
├── part-003.parquet
└── part-004.parquet

Version 3
├── part-005.parquet
└── part-006.parquet
```
---

---
## Après le VACUUM :
- [ ] spark.sql("VACUUM nyc_taxi.bronze.bronze_nyc_taxi")
- [ ] spark.sql("VACUUM nyc_taxi.silver.silver_nyc_taxi")
- [ ] spark.sql("VACUUM nyc_taxi.gold.gold_fact_trips")
---

---
## Voilà ce qui reste après l'opération VACUUM
```text
Version 3
├── part-005.parquet
└── part-006.parquet
```
---


--- 
#### Que signifie ACID ?
- [ ] c'est cette garantie qui fait qu'une table Delta peut être utilisée pour des données critiques 
- [ ] finance, santé, facturation, reporting...
- [ ] niveau de fiabilité proche d'une base de données classique


---
### Proprieté ACID
- [ ] Atomicity : une transaction est indivisible
- [ ] Consistency : une table Delta doit rester cohérente
- [ ] Isolation : une transaction doit se comporter comme si elle était seule.
- [ ] plusieurs utilisateurs peuvent travailler ensemble sans que les données ne soient corrompues
- [ ] Durability : Après une transaction validée, les données doivent survivre aux erreurs eventuelles
---

| Propriété           | Question à laquelle elle répond                                                |
| ------------------- | ------------------------------------------------------------------------------ |
| **A - Atomicity**   | *Que se passe-t-il si une transaction échoue au milieu de l'opération ?*       |
| **C - Consistency** | *La table reste-t-elle dans un état valide avant et après la transaction ?*    |
| **I - Isolation**   | *Que se passe-t-il lorsque plusieurs transactions travaillent en même temps ?* |
| **D - Durability**  | *Que se passe-t-il après un commit si le système tombe en panne ?*             |


### Que faire lorsqu'une transaction ne peut pas être menée à son terme ?
- [ ] Rollback : annuler complètement la transaction et revenir à l'état précédent.
- [ ] Dans Delta Lake, le rollback est généralement automatique : si le commit n'aboutit pas, la nouvelle version n'est jamais créée.
- [ ] Le rollback empêche une transaction incomplète ou en erreur de laisser la table dans un état incohérent.
- [ ] Le rollback peut être déclenché par :une erreur Spark ; une panne du cluster ; un problème réseau ; un conflit OCC ; toute erreur survenant avant le commit.
- [ ] Lors d'un rollback, l'ancienne version de la table reste la version active
- [ ] Rollback : Version N -> Échec -> Version N
- [ ] Restore : Version N -> Version N+1 (copie logique d'une ancienne version N-1 ou N-n)


### Time Travel
- [ ] Le Time Travel permet de lire une ancienne version de la table.
- [ ] Exemple : SELECT * FROM silver_nyc_taxi VERSION AS OF 100;
- [ ] Le Time Travel ne modifie pas la table.
- [ ] Le Time Travel n'est pas un rollback.

### RESTORE
- [ ] Le RESTORE permet de revenir à l'état d'une ancienne version de la table.
- [ ] Exemple : RESTORE TABLE nyc_taxi.silver.silver_nyc_taxi TO VERSION AS OF 100;
- [ ] La restauration elle-même est une nouvelle transaction Delta.
- [ ] L'historique n'est pas supprimé.
- [ ] Après un RESTORE, une nouvelle version est créée.
- [ ] Exemple de RESTORE : Version 100 ; Version 101 ; Version 102 ; RESTORE vers 100 --> Version 103
- [ ] Le restore intervient après un ou plusieurs commits réussis.
- [ ] Une ancienne version est utilisée comme référence.
- [ ] Delta crée une nouvelle transaction.
- [ ] Un nouveau numéro de version est généré.
- [ ] L'historique complet est conservé.


### À retenir
- [ ] Rollback = annuler une transaction avant son commit
- [ ] Time Travel = consulter une ancienne version
- [ ] Restore = recréer une ancienne version comme nouvelle version active
- [ ] Restore crée une nouvelle version, alors que Rollback ne crée aucune version
---

### Question : "Comment Delta Lake apporte les transactions ACID ?"
- [ ] Dans Databricks, les ACID transactions sont fournies par Delta Lake
- [ ] Delta Lake ajoute un transaction log (_delta_log) au-dessus des fichiers Parquet. 
- [ ] Chaque opération (INSERT, UPDATE, DELETE, MERGE) crée une nouvelle version atomique de la table. 
- [ ] Le log garantit Atomicity, Consistency, Isolation grâce à l'optimistic concurrency control, et Durability via le stockage persistant. 
- [ ] Cela permet également le Time Travel et l'audit des modifications
- [ ] C'est grâce à la combinaison OCC + Delta Log + stockage cloud persistant que plusieurs jobs Databricks 
- [ ] peuvent écrire sur la même table Delta sans corruption des données.


###### "La transaction est-elle entièrement appliquée ou entièrement annulée ?"
##### A = Atomicity (Atomicité)
- [ ] Une transaction réussit complètement ou échoue complètement.
- [ ] Une transaction est invisible tant qu'elle n'a pas été validée (commit).
- [ ] Les lecteurs ne voient jamais une table partiellement modifiée.
- [ ] Delta Lake utilise le transaction log (_delta_log) pour garantir ce comportement.
- [ ] Une nouvelle version de la table n'existe qu'après l'écriture réussie d'une nouvelle entrée dans le Delta Log.
- [ ] Si une panne survient avant le commit, les modifications sont ignorées et la version précédente reste active.
- [ ] Les fichiers éventuellement écrits avant un échec ne deviennent pas visibles pour les lecteurs.


##### *La table reste-t-elle dans un état valide avant et après la transaction ?*    
##### C = Consistency (Cohérence)
- [ ] Les données passent toujours d'un état valide à un autre état valide.
- [ ] Après le commit, les lecteurs voient soit l'ancienne version, soit la nouvelle version.
- [ ] Il n'existe jamais d'état intermédiaire incohérent.
- [ ] Chaque version de la table correspond à un état cohérent défini par le Delta Log.
- [ ] Toutes les opérations (INSERT, UPDATE, DELETE, MERGE) produisent une nouvelle version cohérente de la table.


#### "Que se passe-t-il lorsque plusieurs transactions travaillent en même temps ?"
##### I = Isolation (Isolation)
- [ ] Plusieurs utilisateurs ou jobs peuvent travailler simultanément sur la même table Delta sans se gêner.
- [ ] Delta Lake utilise un mécanisme appelé Optimistic Concurrency Control (OCC).
- [ ] Chaque transaction lit une version cohérente de la table (par exemple la version 100).
- [ ] Chaque transaction prépare ses modifications indépendamment des autres transactions.
- [ ] Chaque transaction tente ensuite de réaliser son commit.
- [ ] La première transaction qui réussit son commit crée une nouvelle version de la table (par exemple la version 101).
- [ ] Les autres transactions détectent que la table a changé depuis leur lecture initiale.
- [ ] Delta vérifie alors les conflits en comparant les fichiers lus et modifiés par chaque transaction.
- [ ] Une transaction mémorise : la version lue + les fichiers lus  + les fichiers modifiés.
- [ ] Si les fichiers lus ou modifiés ont été impactés par une transaction déjà validée, Delta rejette la transaction avec une erreur de concurrence.
- [ ] Si les fichiers lus n'ont pas été impactés, Delta accepte la transaction et crée une nouvelle version de la table.
- [ ] Les conflits apparaissent généralement lorsque plusieurs transactions tentent de modifier les mêmes données ou les mêmes fichiers Delta.
- [ ] Erreurs typiques : ConcurrentAppendException, ConcurrentDeleteReadException, ConcurrentDeleteDeleteException, ConcurrentModificationException.
- [ ] Ce mécanisme permet à plusieurs jobs Databricks d'écrire simultanément sur une même table Delta sans verrouiller toute la table et sans corrompre les données.


##### *Que se passe-t-il après un commit si le système tombe en panne ?*  
##### D = Durability (Durabilité)
- [ ] Une fois le commit effectué, les données sont persistées de manière durable dans le stockage sous-jacent.
- [ ] Les données survivent à un redémarrage du cluster.
- [ ] Les données survivent à une déconnexion de l'utilisateur.
- [ ] Les données survivent à l'arrêt ou à la suppression d'un notebook.
- [ ] Les données survivent à la recréation d'un cluster Databricks.
- [ ] Le transaction log (_delta_log) et les fichiers de données Delta sont stockés durablement dans le Data Lake.
- [ ] Après validation d'une transaction, les données restent accessibles même si les ressources de calcul disparaissent.
- [ ] La durabilité est assurée par le stockage persistant (Azure Data Lake Storage, Amazon S3 ou Google Cloud Storage selon la plateforme).

#### "Y a-t-il eu un conflit avec une autre transaction ?"
### Optimistic Concurrency Control (OCC)
- [ ] Delta Lake part du principe que : "La plupart du temps, les utilisateurs ne vont pas modifier exactement les mêmes données au même moment."
- [ ] Au lieu de verrouiller toute la table, Delta laisse les transactions travailler librement puis vérifie au moment du commit s'il y a eu conflit.
- [ ] Plusieurs transactions peuvent lire simultanément la même version de la table.
- [ ] La première transaction qui réussit à commiter crée une nouvelle version de la table.
- [ ] Les autres transactions détectent alors que la version de la table a changé depuis leur lecture initiale.
- [ ] Delta vérifie alors si les fichiers lus ou modifiés par ces transactions ont été impactés par la transaction déjà validée.
- [ ] Si les fichiers lus n'ont pas été modifiés par la transaction validée, Delta accepte la transaction et crée une nouvelle version de la table.
- [ ] Si les fichiers lus ou modifiés ont été impactés par la transaction validée, Delta détecte un conflit et rejette la transaction.
- [ ] Les conflits surviennent généralement lorsque plusieurs transactions tentent de modifier les mêmes données ou les mêmes fichiers Delta.
- [ ] Erreurs typiques : ConcurrentAppendException, ConcurrentDeleteReadException, ConcurrentDeleteDeleteException, ConcurrentModificationException.
- [ ] Ce mécanisme permet à plusieurs jobs Databricks d'écrire simultanément sur une même table Delta sans verrouiller toute la table et sans corrompre les données


##### Stockage persistant (Durability)
- [ ] Une fois le commit validé, les données ne disparaissent plus
- [ ] Elles sont stockées dans Azure Data Lake Storage ou AWS S3 ou Google Cloud Storage



---
### Time Travel
- [ ] lire une ancienne version
- [ ] SELECT * FROM silver_nyc_taxi VERSION AS OF 5;
- [ ] SELECT * FROM silver_nyc_taxi@5;
- [ ] SELECT * FROM silver_nyc_taxi TIMESTAMP AS OF '2026-07-01';
- [ ] Mais si les fichiers nécessaires ont été supprimés par VACUUM :
- [ ] alors le Time Travel vers ces anciennes versions ne fonctionnera plus.
---

---
| Concept              | Description                                                                    |
| -------------------- | ------------------------------------------------------------------------------ |
| Delta Lake           | Conserve les anciennes versions des fichiers                                   |
| Time Travel          | Permet de relire une ancienne version                                          |
| VACUUM               | Supprime physiquement les fichiers obsolètes                                   |
| DRY RUN              | Montre ce qui serait supprimé                                                  |
| Rétention par défaut | 7 jours                                                                        |
| Effet secondaire     | Les anciennes versions deviennent inaccessibles après suppression des fichiers |


---
| Concept             | Rôle                                                     |
| ------------------- | -------------------------------------------------------- |
| **Data Versioning** | Conserver plusieurs versions d'une table                 |
| **Time Travel**     | Lire une ancienne version de la table                    |
| **Delta Log**       | Stocke l'historique des versions                         |
| **VACUUM**          | Supprime les anciens fichiers nécessaires au Time Travel |
---


---
#### l'ordre d'exécution de ton job
- [ ] CreateCatalog
- [ ] CreateSchemas
- [ ] CreateTables
- [ ] Bronze ingestion
- [ ] Silver transformation
- [ ] Gold aggregation
- [ ] Maintenance VACUUM
---


---
#### Technique de debogage
- [ ] self.logger.info(f"TABLE = {full_table_name}")
- [ ] print("=== DATAFRAME ===")
- [ ] df.printSchema()

- [ ] print("=== TABLE DELTA ===")
- [ ] self.spark.table(full_table_name).printSchema()



### la gestion de la configuration selon l'environnement (local, dev Databricks, prod Databricks).





### Comment gérez-vous les chargements incrémentaux ?
- [ ] J'utilise principalement une stratégie basée sur un watermark métier, généralement une colonne last_update
- [ ] Je conserve la dernière valeur traitée dans une table d'audit.
- [ ] À chaque exécution, je récupère uniquement les données dont last_update est supérieur au watermark enregistré.
- [ ] Ensuite, j'utilise un MERGE INTO Delta Lake pour gérer les insertions et les mises à jour de manière idempotente.
- [ ] Lorsque la source ne fournit pas de date de modification, j'utilise une clé technique ou une période métier comme dans mon projet NYC Taxi où je traite les données mois par mois

```text
MERGE INTO silver.customer t
USING source_incremental s
ON t.customer_id = s.customer_id

WHEN MATCHED THEN
UPDATE SET *

WHEN NOT MATCHED THEN
INSERT *
```

* Watermark -> Lecture incrémentale -> MERGE INTO -> Table Delta -> Mise à jour du watermark

- [ ] Dans les traitements batch, j'utilise généralement un watermark pour mémoriser la dernière donnée traitée,
- [ ] souvent une colonne **last_update** ou une date métier.
- [ ] Cela permet de réaliser des chargements incrémentaux efficaces.
- [ ] En streaming, le watermark a un autre rôle :
- [ ] il définit la fenêtre pendant laquelle Spark accepte des événements arrivant en retard avant de considérer
- [ ] les agrégations comme définitives.






#### Pourquoi partitionner une table ? Pour éviter de lire inutilement les données.
- [ ] fact_trips
    * periode=202501
    * periode=202502
    * periode=202503
* WHERE periode=202503 ne lira qu'une partition.



---
* Peut-on trop partitionner ? Oui.
* Conséquences :
  * millions de petits fichiers
  * métadonnées volumineuses
  * dégradation des performances



---
* Que choisir entre cache et persist ? Cache :
* df.cache() : stockage mémoire uniquement.

---
* Tu arrives chez un client.

* Chaque nuit :

* 200 millions de lignes
* fichiers CSV
* Power BI le matin

* Comment conçois-tu la solution ?
- [ ] Reponse : ADLS -> Databricks Auto Loader -> Bronze -> Silver -> Gold -> SQL Warehouse -> Power BI
- [ ] Delta Lake
- [ ] Unity Catalog
- [ ] Airflow
- [ ] CI/CD
- [ ] Monitoring
- [ ] Audit



---
### Pourquoi un shuffle est coûteux ?

### Réponse Senior
* Il implique :

- [ ] sérialisation
- [ ] transfert réseau
- [ ] écriture disque temporaire
- [ ] lecture disque



Donc il augmente fortement la latence.
---


---
### Pourquoi Delta Lake est-il indispensable dans Databricks ?

##### Réponse Senior

##### Sans Delta Lake, on stocke simplement des fichiers Parquet.

##### Delta Lake ajoute :
- [ ] les transactions ACID
- [ ] le versionnement
- [ ] le Time Travel
- [ ] les MERGE
- [ ] l'évolution du schéma
- [ ] l'optimisation automatique des fichiers -> OPTIMIZE


MERGE INTO customer_target t
USING customer_source s
ON t.customer_id=s.customer_id
WHEN MATCHED THEN UPDATE
WHEN NOT MATCHED THEN INSERT



---
#### Que se passe-t-il si la source ajoute une colonne demain ?

- [ ] Avec Delta Lake, j'utilise le Schema Evolution. 
- [ ] Si la nouvelle colonne est compatible avec le modèle de données, 
- [ ] Delta peut l'ajouter automatiquement au schéma de la table via mergeSchema ou les fonctionnalités Auto Loader. 
- [ ] Les anciennes lignes conserveront une valeur NULL pour cette nouvelle colonne.



---
### Quelle est la Différence entre Schema Evolution et Schema Enforcement ?

- [ ] Le Schema Evolution permet à une table Delta d'accepter automatiquement des évolutions compatibles du schéma, notamment l'ajout de nouvelles colonnes. 
- [ ] Cela évite de casser les pipelines lorsqu'une source évolue. 
- [ ] J'utilise cette fonctionnalité avec précaution et sous contrôle, car toutes les évolutions de schéma ne doivent pas forcément être acceptées automatiquement en production.
- [ ] Cette dernière phrase est importante : un profil senior ne dit pas seulement "j'active mergeSchema partout", il montre qu'il réfléchit à la gouvernance et à l'impact métier des changements de schéma.



---
### Une requête Databricks devient lente, Comment investigues-tu ?

- [ ] 1. Spark UI

* Regarder :
  * DAG
  * nombre de stages
  * skew
  * shuffle

- [ ] 2. Plan d'exécution : df.explain("formatted")
- [ ] 3. Taille des partitions

* Chercher :
* partitions trop grosses
* partitions trop petites

- [ ] 4. Jointures
* Vérifier :
* broadcast join possible



---
### Quand utiliser un Broadcast Join ?
- [ ] Lorsque l'une des tables est petite.
- [ ] from pyspark.sql.functions import broadcast
- [ ] df.join(broadcast(dim_client),"id")


### Que fait OPTIMIZE ?
- [ ] Fusionne les petits fichiers Delta.



### Que fait ZORDER ?
- [ ] Réorganise physiquement les données.

---
---
### Comment gérer les doublons ?
- [ ] Window.partitionBy("trip_id")
- [ ] row_number()
- [ ] Conserver uniquement : row_number = 1
---
---



### Comment garantis-tu la qualité des données ?
- [ ] Je vérifie que les champs obligatoires ne sont pas nuls, notamment les clés métier, les dates de référence ou les identifiants utilisés dans les jointures
- [ ] Je vérifie que les identifiants métiers censés être uniques ne présentent pas de doublons avant l'intégration dans les couches Silver ou Gold
- [ ] Je valide les types attendus afin d'éviter les erreurs de calcul ou les anomalies lors des agrégations.
- [ ] Je vérifie que les clés étrangères correspondent bien aux référentiels métiers afin d'éviter les incohérences analytique
- [ ] Les règles métier sont généralement les contrôles les plus critiques. Elles permettent de détecter des données techniquement valides mais incohérentes du point de vue du métier
- [ ] nullité
- [ ] unicité : Détecter les doublons
- [ ] Contrôle des types : Vérifier que les données respectent le format attendu
- [ ] Contrôle de référentiel : Vérifier qu'une valeur existe dans une table de référence
- [ ] Contrôle des règles métier : Le métier définit ce qui est acceptable ou non
---

### Comment garantissez-vous la qualité des données ?
- [ ] Je mets en place plusieurs niveaux de contrôles dans la couche Silver :

- [ ] contrôle de nullité sur les champs obligatoires ;
- [ ] contrôle d'unicité sur les clés métier ;
- [ ] validation des types et formats ;
- [ ] vérification de l'intégrité référentielle avec les dimensions ;
- [ ] application des règles métier spécifiques au domaine.

* Les anomalies sont historisées dans des tables d'audit afin d'assurer la traçabilité et le suivi des rejets.
---



#### Databricks avancé
- [ ] Explique Unity Catalog.
- [ ] Reponse : Unity Catalog est la couche de gouvernance de Databricks.
- [ ] Il permet :
  * gestion des droits
  * catalogues
  * audit
  * lineage
  * partage sécurisé

Structure
    Catalog
        └ Schema
            └ Table
---

### Différence entre Hive Metastore et Unity Catalog ?

- [ ] Hive Metastore :
    * ancien modèle
    * gouvernance limitée

- [ ] Unity Catalog :
    * centralisé
    * multi-workspace
    * audit
    * lineage

---


### omment sécuriser des données sensibles ?
- [ ] RBAC = Role-Based Access Control
- [ ] Unity Catalog
- [ ] Dynamic Views
- [ ] Column Masking
- [ ] séparation Bronze/Silver/Gold
* On ne donne pas les droits directement à chaque utilisateur. 
* On donne des droits à des rôles, puis on affecte les utilisateurs à ces rôles

---
---
### Comment sécuriseriez-vous des données sensibles dans Databricks ?
- [ ] Je commencerais par mettre en place Unity Catalog comme couche de gouvernance centralisée. 
- [ ] Ensuite, j'utiliserais du RBAC pour contrôler les accès selon les rôles et le principe du moindre privilège.
- [ ] Pour les données sensibles, je pourrais utiliser du column masking afin de masquer certaines colonnes 
- [ ] et des dynamic views pour adapter les données accessibles selon le profil de l'utilisateur.

- [ ] Enfin, je séparerais les couches Bronze, Silver et Gold et je limiterais l'accès aux données brutes. 
- [ ] Les consommateurs BI accéderaient principalement aux tables Gold, 
- [ ] ce qui permet également de réduire l'exposition des données sensibles.


| Concept                | Question à laquelle il répond              |
| ---------------------- | ------------------------------------------ |
| **RBAC**               | Qui peut faire quoi ?                      |
| **Unity Catalog**      | Où centraliser la gouvernance ?            |
| **Dynamic Views**      | Quelles données montrer à qui ?            |
| **Column Masking**     | Comment masquer une colonne sensible ?     |
| **Bronze/Silver/Gold** | Comment limiter l'exposition des données ? |


---
---



#### Definition
- [ ] Un watermark est la dernière valeur traitée que l'on mémorise afin de savoir où reprendre le traitement suivant.
- [ ] Un Metastore est essentiellement un catalogue qui contient les métadonnées de tes données.
- [ ] ff
- [ ] ff
- [ ] gg
- [ ] ff

### Quelle est la différence entre Hive Metastore et Unity Catalog ?
- [ ] Hive Metastore est le modèle historique de catalogue utilisé avec Spark et Databricks. 
- [ ] Il permet notamment de gérer les métadonnées des tables et certains contrôles d'accès, mais sa gouvernance est plus limitée et davantage liée aux environnements ou workspaces.
- [ ] Unity Catalog fournit une couche de gouvernance centralisée et moderne. 
- [ ] Il permet de gérer les permissions, l'audit et le lineage, et de gouverner les données de manière cohérente à travers plusieurs workspaces.
- [ ] Dans une architecture Databricks moderne, je privilégierais donc Unity Catalog pour centraliser la gouvernance et appliquer le principe du moindre privilège.
- [ ] Hive Metastore = catalogue historique.
- [ ] Unity Catalog = catalogue + gouvernance centralisée + sécurité + audit + lineage.


### qu'est-ce qu'un Metastore ?
* Par exemple, tu as une table : nyc_taxi.gold.gold_fact_trips
* Le Metastore sait notamment :
- [ ] Nom de la table
- [ ] Colonnes
- [ ] Types
- [ ] Emplacement des fichiers
- [ ] Partitions
- [ ] Le Metastore ne contient pas nécessairement les données elles-mêmes
- [ ] Les données peuvent être dans : ADLS S3 GCS
- [ ] Le Metastore contient surtout les informations permettant de retrouver et gérer ces données


### Hive Metastore
* Le Hive Metastore est l'ancien modèle de catalogue utilisé avec Databricks/Spark.
* Hive Metastore offre des capacités de catalogue et de contrôle d'accès, mais sa gouvernance est plus limitée et moins centralisée que celle offerte par Unity Catalog



### Unity Catalog
* Unity Catalog a été conçu pour fournir une gouvernance centralisée des données dans Databricks
* Unity Catalog est la couche centrale de gouvernance de Databricks
* Il permet notamment de gérer :
  - [ ] les permissions ;
  - [ ] les tables ;
  - [ ] les vues ;
  - [ ] les données ;
  - [ ] le lineage ;
  - [ ] l'audit.


### Audit
* Unity Catalog permet de disposer d'informations d'audit sur les accès et activités liées aux données
* Cela est particulièrement important pour les entreprises qui manipulent des données sensibles.


### Lineage
* Lineage = traçabilité des données.
* Le lineage permet de comprendre les relations entre les différents objets de données
* Tu peux alors répondre à une question métier du type : "D'où vient le chiffre d'affaires affiché dans mon dashboard ?"
* C'est extrêmement utile pour :
- [ ] comprendre les dépendances ;
- analyser l'impact d'un changement ;
- auditer les données ;
- résoudre des problèmes de qualité.



---
---
---
---







---
---
---
---



---
---
---
---


---
---
---
---
