
### construire une architecture quotidienne de un tera par jour
* Je propose une architecture Lakehouse sur Databricks organisée en trois couches : Bronze, Silver et Gold.
* Les données sources (fichiers Parquet, bases de données, API, etc.) sont d'abord ingérées dans la couche Bronze où elles sont stockées sous leur forme brute afin de conserver l'historique et garantir la traçabilité.
* Dans la couche Silver, j'applique les règles de qualité et de transformation : suppression des doublons, gestion des valeurs nulles, contrôle des types de données, calcul des indicateurs techniques et application des règles métier.
* La couche Gold contient les données prêtes à être consommées par les utilisateurs métiers. J'y construis des tables de faits et des dimensions selon une modélisation en étoile afin d'optimiser les performances analytiques.
* Les données sont stockées au format Delta Lake afin de bénéficier des transactions ACID, du contrôle de schéma, du Time Travel et des opérations MERGE pour les chargements incrémentaux.
* Les traitements sont orchestrés via des workflows Databricks ou Airflow, avec un mécanisme de monitoring, de logging et d'audit permettant de suivre les exécutions et les volumes traités.
* Enfin, la couche Gold est exposée à Power BI pour la création des tableaux de bord et le suivi des indicateurs métier.


### Pourquoi utilisez-vous Delta Lake plutôt que de simples fichiers Parquet ?
Delta Lake est une couche de stockage construite au-dessus des fichiers Parquet. Contrairement à Parquet seul, Delta Lake apporte des transactions ACID qui garantissent la cohérence des données même lorsque plusieurs traitements lisent ou écrivent simultanément.
Delta Lake fournit également le Time Travel qui permet de consulter ou restaurer une version précédente d'une table.
Il permet aussi le Schema Enforcement pour empêcher l'écriture de données non conformes au schéma attendu, ainsi que le Schema Evolution pour faire évoluer le schéma de manière contrôlée.
Enfin, Delta Lake supporte des opérations de type UPDATE, DELETE et MERGE, ce qui facilite les chargements incrémentaux et les stratégies d'upsert dans les pipelines Data Engineering


### Schema Enforcement
Vérifie que les données écrites respectent le schéma de la table Delta.
Empêche l'écriture de colonnes inattendues ou de types incompatibles.
Évite la corruption ou l'incohérence des données.


### Schema Evolution
Permet de faire évoluer le schéma de la table de manière contrôlée.
Accepte notamment l'ajout de nouvelles colonnes lorsqu'on active mergeSchema ou certaines options Delta.
Évite de recréer la table lorsqu'une source évolue.

Le Schema Enforcement garantit que les données écrites dans une table Delta respectent le schéma défini. Si une colonne a un type incompatible ou si le schéma ne correspond pas, l'écriture est rejetée afin de préserver la qualité et la cohérence des données.
Le Schema Evolution permet quant à lui de faire évoluer le schéma de la table, par exemple en ajoutant de nouvelles colonnes provenant de la source. Cela facilite l'adaptation des pipelines aux changements de structure des données sans devoir recréer les tables.



### Tu as une table Delta de 500 millions de lignes qui devient très lente. Quelles actions mets-tu en place pour améliorer les performances ?
Pour une table Delta de plusieurs centaines de millions de lignes, je commencerais par analyser les requêtes et le Spark UI afin d'identifier les goulots d'étranglement. 
Je vérifierais ensuite la stratégie de partitionnement pour permettre le partition pruning. J'utiliserais OPTIMIZE afin de compacter les petits fichiers et éventuellement Z-ORDER sur les colonnes les plus utilisées dans les filtres. 
Je m'assurerais également que les jointures sont optimisées, notamment avec des broadcast joins lorsque cela est pertinent. 
Enfin, j'utiliserais VACUUM pour nettoyer les anciens fichiers et réduire les coûts de stockage.


* Pourquoi ne pas transformer directement les données de Bronze vers Gold et supprimer complètement la couche Silver ?
* La couche Silver joue un rôle essentiel dans l'architecture Lakehouse. Même si l'on pourrait techniquement passer directement de Bronze à Gold, cela rendrait les pipelines plus difficiles à maintenir et à faire évoluer.
* La couche Bronze conserve les données brutes telles qu'elles proviennent de la source afin de garantir la traçabilité et permettre de retraiter les données en cas de besoin.
* La couche Silver centralise les transformations techniques et métier : nettoyage, déduplication, contrôle des types, gestion des valeurs manquantes, validation des référentiels et application des règles métier.
* La couche Gold est ensuite dédiée à la consommation. Elle contient des modèles optimisés pour les besoins analytiques, comme des tables de faits, des dimensions et des KPI destinés à Power BI.
* Cette séparation facilite la maintenance, le debugging, la réutilisation des données et l'évolution des traitements


### Comment charger ces données dans Delta Lake sans créer de doublons ?
* « Je mettrais en place un chargement incrémental basé sur une clé métier comme customer_id. Avant le chargement, je contrôlerais les volumes et la période traitée dans une table d'audit afin de garantir la traçabilité et l'idempotence du pipeline. 
* Pour éviter les doublons et gérer les modifications des clients existants, j'utiliserais un MERGE Delta Lake. Si le customer_id existe déjà, je mets à jour les attributs modifiés ; sinon, j'insère le nouveau client. »
```` text
MERGE INTO silver_customer AS target
USING new_customer AS source
ON target.customer_id = source.customer_id

WHEN MATCHED THEN
UPDATE SET
target.email = source.email,
target.last_update_date = source.last_update_date

WHEN NOT MATCHED THEN
INSERT (
customer_id,
email,
last_update_date
)
VALUES (
source.customer_id,
source.email,
source.last_update_date
);
````



« Ton pipeline traite 10 millions de lignes chaque jour. Si le traitement échoue après avoir écrit 6 millions de lignes, que se passe-t-il lorsque tu relances le pipeline ? Comment garantis-tu que tu ne vas pas avoir 16 millions de lignes ? »
* Delta Lake garantit l'atomicité de chaque transaction grâce aux propriétés ACID. Ainsi, une transaction échouée ne laisse pas une écriture partielle visible dans la table.

* Cependant, ACID ne garantit pas à lui seul l'idempotence du pipeline. 
* Si je relance un pipeline après un succès partiel du workflow, je peux retraiter les mêmes données. 
* Pour garantir l'idempotence, je dois identifier la donnée traitée, par exemple avec une clé métier et une période de traitement, puis utiliser une stratégie comme MERGE, ou remplacer explicitement la partition concernée.
* Je peux également utiliser une table d'audit contenant la période, le statut du traitement et les volumes afin de savoir si une période a déjà été chargée.
* Ainsi, si je relance le traitement de la période 202609, je ne vais pas insérer deux fois les mêmes données. »

* ACID : garantie la cohérence de la transaction
* INDEMPOTENCE : garantie la cohérence du PIPELINE


* « Que se passe-t-il si ton fichier source contient deux lignes avec le même customer_id ? »
* La couche Silver doit effectivement contenir les contrôles de qualité et la déduplication afin d'éviter ce type de situation.
* Cependant, je ne pars jamais du principe que la source est parfaite. Avant le MERGE, je vérifie que la clé métier est unique dans le dataset source.
* Si plusieurs lignes possèdent le même customer_id, je mets en place une règle métier pour sélectionner l'enregistrement de référence, par exemple le plus récent selon last_update_date, à l'aide d'une fonction de fenêtre ROW_NUMBER().
* Ainsi, le dataset utilisé dans le MERGE contient une seule ligne par clé métier, ce qui garantit un comportement déterministe et évite les erreurs de type "multiple matches".
```` text
  SELECT *
      FROM (
          SELECT *,
          ROW_NUMBER() OVER(
          PARTITION BY customer_id
          ORDER BY last_update_date DESC
          ) AS rn
      FROM source
      )
  WHERE rn = 1
```` 
* "je garantis l'unicité de la clé métier avant le MERGE grâce à une règle métier explicite"
---


* Quelle différence entre repartition() et coalesce() dans Spark ?
* repartition() permet de redistribuer les données sur un nouveau nombre de partitions. Cette opération déclenche généralement un shuffle, ce qui la rend plus coûteuse mais permet d'obtenir des partitions plus équilibrées.
* coalesce() est principalement utilisé pour réduire le nombre de partitions. Il tente de fusionner les partitions existantes sans provoquer de shuffle complet, ce qui le rend plus performant lorsque l'on souhaite réduire le nombre de fichiers avant une écriture Delta ou Parquet.

* J'utiliserais repartition() pour corriger un déséquilibre des données ou augmenter le parallélisme, tandis que coalesce() serait privilégié pour optimiser l'écriture finale en limitant le nombre de petits fichiers.
* df = df.coalesce(10)
* df = df.repartition(100)
* df.repartition("customer_id")



* voilà un programme
```` text
df = spark.read.table("sales")
df1 = df.filter("amount > 100")
df2 = df1.groupBy("country").sum("amount")
```` 
* À ce stade, combien de jobs Spark ont été exécutés ?
* À ce stade, aucun job Spark n'a encore été exécuté. 
* Les opérations filter, groupBy et sum sont des transformations et Spark applique le principe de Lazy Evaluation. 
* Il construit simplement un DAG représentant les opérations à effectuer. 
* Le traitement ne sera réellement exécuté que lorsqu'une action comme show(), count() ou write() sera appelée. 
* Lors de cette exécution, l'opération groupBy entraînera un shuffle car les données devront être redistribuées entre les partitions pour regrouper les lignes par pays.


* supposons ce programme Combien de fois Spark va-t-il recalculer le filtre ? Et comment éviter ce recalcul ?
df = spark.read.table("sales")
df_filtered = df.filter("amount > 100")
print(df_filtered.count())
print(df_filtered.count())

* Spark utilise la Lazy Evaluation. Chaque appel à count() déclenche un job Spark. 
* Sans mécanisme de cache, Spark relit les données sources et réexécute le filtre à chaque action.
* Pour éviter ce recalcul, je peux utiliser cache() ou persist(). 
* Le premier job calcule les données et les stocke en mémoire (ou selon le niveau de persistance choisi), puis les actions suivantes réutilisent ces données sans relancer l'ensemble du pipeline.


* Quelle différence entre cache() et persist() ?
* dans Spark moderne, l'objectif est de stocker les données pour éviter les recalculs.
* cache() et persist() permettent tous les deux d'éviter le recalcul des transformations en stockant le DataFrame après son premier calcul.
* La différence est que cache() utilise un niveau de stockage par défaut et constitue une méthode simplifiée.
* persist() permet de choisir explicitement le niveau de stockage, par exemple uniquement en mémoire, uniquement sur disque ou une combinaison des deux. 
* J'utilise généralement persist() lorsque je veux maîtriser la consommation mémoire ou lorsque le dataset est trop volumineux pour tenir entièrement en mémoire.

* df.persist(StorageLevel.MEMORY_ONLY) ou df.persist(StorageLevel.MEMORY_AND_DISK)


* Comment optimiser cette jointure dans Spark et pourquoi ?
* « Comme dim_location contient seulement 250 lignes, je peux utiliser un broadcast join afin de répliquer cette petite table sur les executors. 
* Chaque executor dispose alors d'une copie de la dimension et peut effectuer la jointure localement avec les partitions de fact_trips. 
* Cela évite un shuffle important de la table de faits de 500 millions de lignes et améliore fortement les performances. 
* Je vérifie néanmoins que la dimension est suffisamment petite pour tenir en mémoire sur les executors. »

```` text
from pyspark.sql.functions import broadcast
result = fact_trips.join(
broadcast(dim_location),
"location_id"
)
````







* « Pourquoi une seule task est-elle beaucoup plus lente que les autres et comment corrigerais-tu le problème ? »
* « Je suspecterais un data skew, car une seule task traite beaucoup plus de données que les autres. 
* Je commencerais par analyser la distribution de la clé utilisée dans le groupBy ou la jointure afin d'identifier une ou plusieurs valeurs très fréquentes. 
* Ensuite, selon le cas, je pourrais utiliser AQE pour gérer automatiquement certains skew joins, ou appliquer une stratégie de salting afin de répartir les données d'une clé très fréquente sur plusieurs partitions. 
* Un simple repartition() ne suffit pas nécessairement si la clé elle-même est fortement déséquilibrée. »




### Qu'est-ce que Databricks ?
* [ ] Databricks est une plateforme Lakehouse permettant d'unifier
  * l'ingestion
  * le traitement
  * le stockage 
  * la gouvernance
  * et l'analyse de données
* [ ] Elle repose principalement sur Apache Spark et Delta Lake
* [ ] Elle permet aux Data Engineer, Data Scientist et Data Analyst de travailler sur la même plateforme

```` text
Databricks
│
├── Workspace
├── Compute
├── Notebooks
├── Jobs
├── SQL Warehouse
├── Delta Lake
└── Unity Catalog
````

un pipeline indempotent : fourni toujours le même état pour les mêmes données

---
##### les Opérations appliquées sur une table Delta et cela qui crée de nouveaux fichiers Delta
- [ ] MERGE
- [ ] UPDATE
- [ ] DELETE
- [ ] INSERT
---


### Unity Catalog
* Unity Catalog fournit
* [ ] une gouvernance centralisée des données et des ressources Databricks
* [ ] il permet de gérer les permissions, le contrôle d'accès, l'audit, le lineage et la decouverte des données à travers les différents workspace


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
- [ ] OPTIMIZE : Réduire le nombre de fichiers et accélérer les lectures
- [ ] VACUUM DRY RUN : montrer les fichiers devenus inutiles
- [ ] VACUUM : Supprime les anciens fichiers nécessaires au Time Travel
- [ ] ANALYZE TABLE
- [ ] Databricks Bundle : Un Databricks Bundle est un moyen de définir et déployer l'infrastructure et les ressources Databricks sous forme de code : Infrastructure as Code / CI-CD / DevOps


--- 
#### Que signifie ACID ?
- [ ] c'est cette notion garantie qui fait qu'une table Delta peut être utilisée pour des données critiques
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
- résoudre des problèmes de qualité


### Qu'est-ce qu'un Databricks Bundle ?
- [ ] Un Databricks Bundle permet de définir les ressources d'un projet Databricks sous forme de code et de les déployer de manière reproductible dans différents environnements, par exemple DEV, TEST et PROD. 
- [ ] Je peux versionner cette configuration avec Git et l'intégrer dans une chaîne CI/CD afin d'automatiser les déploiements