* [ ] data ingénierie, 
* [ ] Databricks,  
* [ ] Pyspark
* [ ] Airflow.

### Thèmes abordés
* [ ] Partition = paquet de données, c'est un morceau du DataFrame
* [ ] Partitions → déterminent généralement les Tasks
* [ ] Task = travail à effectuer sur le paquet (sur la partition) pour une étape donnée
* [ ] Une Task est une unité de travail exécutée par Spark sur une partition, pour un stage donné
* [ ] Core = ressource CPU qui exécute le travail, c'est lui qui a la capacité d'exécution
* [ ] Un core représente une capacité de calcul disponible pour exécuter une tâche
* [ ] Cores → déterminent le nombre de Tasks exécutables simultanément
* [ ] Executor = processus de Spark qui possède les cores et la mémoire et qui tourne sur une machine
* [ ] L'Executor est le processus qui possède des cores et de la mémoire
* [ ] Worker Node = la machine. 
* [ ] Worker Node = machine physique ou virtuelle du cluster qui fournit les ressources de calcul. 
* [ ] Les Executors sont des processus Spark lancés sur les Worker Nodes et utilisent leurs Cores et leur mémoire pour exécuter les Tasks
* [ ] DAG : le graphe du travail, Le DAG (Directed Acyclic Graph) représente les dépendances entre les opérations
* [ ] Le Driver construit ce DAG, puis Spark l'utilise pour organiser l'exécution en stages et tasks
* [ ] Le Driver est le processus principal de ton application Spark : exécute ton programme PySpark ; construit le DAG ; construit et optimise le plan d'exécution ; demande des ressources au Cluster Manager ; distribue les tâches aux Executors ; coordonne l'exécution ; récupère les résultats.
* [ ] Cluster Manager : le gestionnaire de ressources, Le Cluster Manager attribue les ressources nécessaires à Spark. Il permet au Driver d'obtenir des ressources pour lancer les Executors
* [ ] Executors : ceux qui travaillent, Les Executors sont les processus qui exécutent réellement les tâches Spark sur la machine
* [ ] ff
* [ ] ff
* [ ] ff
* [ ] ff
* sérialisation
* 
* [ ] Un shuffle correspond à une redistribution des données entre les partitions, généralement nécessaire lorsqu'une opération nécessite de regrouper ou de réorganiser les données selon une clé
* [ ] Shuffle = échange de données entre partitions necessaire pour des opérations de réorganisation des données
* [ ] Spark découpe ton traitement en plusieurs stages lorsque certaines opérations nécessitent une redistribution des données (shuffle)
* [ ] Shuffle → peut créer une frontière entre Stages
* [ ] Stage 0 -> Shuffle -> Stage 1
* [ ] Un Stage est une étape du calcul Spark.
* [ ] Un Stage est composé de Tasks, et le nombre de Tasks dépend du nombre de partitions traitées par ce Stage
* [ ] Un Stage est une étape d'exécution composée de plusieurs Tasks. 
* [ ] Les Tasks travaillent sur les partitions. 
* [ ] Spark regroupe dans un même Stage les opérations qui peuvent s'enchaîner sans redistribution des données. Une opération nécessitant généralement un shuffle crée une frontière entre deux stages
* [ ] Lorsqu'une opération nécessite un shuffle, Spark crée généralement une frontière entre deux stages : le premier produit les données redistribuées, et le suivant les consomme pour poursuivre le calcul.

* [ ] Catalyst = moteur d'optimisation
* [ ] Plan d'exécution = recette de calcul de Spark
* [ ] Les transformations construisent le plan : je décris ce que je veux faire
* [ ] Les actions déclenchent l'exécution : je demande à Spark de réellement le faire
* [ ] repartition = redistribuer les données (shuffle)
* [ ] coalesce = fusionner des partitions
* [ ] coalesce() limite le shuffle parce qu'il réduit le nombre de partitions en évitant, dans le cas général, une redistribution complète des données.
* [ ] coalesce() -> moins de partitions -> moins de tâches -> moins de parallélisme (C'est pourquoi on l'utilise surtout lorsque l'objectif est réellement de réduire le nombre de partitions, notamment avant une écriture)
* [ ] coalesce() permet principalement de réduire le nombre de partitions en fusionnant des partitions existantes, sans provoquer généralement de shuffle complet
* [ ] coalesce() cherche à faire une fusion des partitions, plutôt qu'une redistribution complète donc le Shuffle est limité mais supprimé
* [ ] repartition(), au contraire, redistribue les données et provoque un shuffle
* [ ] J'utiliserais donc plutôt **coalesce()** pour réduire le nombre de fichiers avant une écriture, et repartition() lorsque j'ai besoin de rééquilibrer ou d'augmenter le parallélisme."
* [ ] Broadcast Join : c'est déplacer la petite table vers les partitions plutôt que Déplacer la grosse table dans le cadre d'une jointure
* [ ] Opérations qui provoquent une redistribution de données : groupBy, join, distinct, orderBy ou repartition
* [ ] "Pour faire cette opération, Spark doit-il déplacer des lignes vers d'autres partitions ?" si oui alors c'est du Shuffle sinon pas de Shuffle

* [ ] le Lazy Evaluation : Transformations -> Construction du DAG -> Optimisation par Catalyst -> Execution Plan -> Action -> Stages -> Tasks -> Executors / Cores
* [ ] Avec le Lazy Evaluation, les transformations ne sont pas exécutées immédiatement. Elles attendent qu'une action soit déclenchée pour que Spark lance réellement le calcul.
* [ ] Architecture Spark
* [ ] Transformations et Actions
* [ ] Optimisation des performances
* [ ] Partitionnement
* [ ] Jointures
* [ ] Spark SQL
* [ ] Gestion mémoire
* [ ] Delta Lake
* [ ] Cas pratiques Data Engineering
* [ ] Data Skew : Une partition contient beaucoup plus de données que les autres
* [ ] spill to disk
* [ ] shuffle
* [ ] Shuffle Network.
* [ ] Réseau = déplacement des données entre Executors.
* [ ] Catalyst Optimizer : Catalyst est le moteur d'optimisation de Spark SQL
* [ ] le travail de Catalyst Optimizer consiste à prendre le code, trouver une meilleure façon puis exécuter le calcul attendu
* [ ] Exécution JVM
* [ ] overhead : travail supplémentaire qui ne produit pas directement le résultat métier 
* [ ] Mais Spark doit créer des Tasks -> sérialiser les données -> transférer les données -> gérer les Executors -> écrire/lire du shuffle
* [ ] Spark est principalement exécuté dans la JVM
* [ ] optimisations de Spark
* [ ] UDF Python
* [ ] fonction native
* [ ] Pandas UDF
* [ ] Apache Arrow
* [ ] JVM = Java Virtual Machine

* [ ] Plan optimisé : Spark construit plusieurs plans
* [ ] Plan logique : Lire -> Filter -> GroupBy
* [ ] Plan logique optimisé : Lire seulement les colonnes utiles -> Appliquer le filtre tôt (Filter) -> GroupBy
* [ ] Plan Physique : FileScan -> Filter -> Exchange -> HashAggregate
* [ ] Spark -> Catalyst Optimizer -> Plan optimisé -> Exécution JVM

* [ ] Spark JVM -> conversion -> Python -> fonction utilisateur -> Python -> JVM
* [ ] c'est l'echange entre Python -> JVM qui est couteux
* 
* PySpark -> JVM -> Catalyst -> Plan logique -> Plan optimisé -> Plan physique -> Stages -> Tasks -> Executors

```` text
Cluster
│
├── Driver Node
│     └── Driver
│
├── Worker Node
│     └── Executor
│          ├── Cores
│          └── Memory
│
├── Worker Node
│     └── Executor
│          ├── Cores
│          └── Memory
│
└── Worker Node
      └── Executor
           ├── Cores
           └── Memory
````


| Élément             | Question à se poser           | Rôle                         |
| ------------------- | ----------------------------- | ---------------------------- |
| **Driver**          | Qui coordonne ?               | 🧠 Cerveau                   |
| **Cluster Manager** | Qui attribue les ressources ? | 🎛️ Ressources               |
| **Executor**        | Qui travaille ?               | 💻 Processus                 |
| **Core**            | Où s'exécute une task ?       | ⚙️ Capacité CPU              |
| **Partition**       | Sur quelles données ?         | 📦 Morceau de données        |
| **Task**            | Quel travail ?                | 🔨 Travail sur une partition |
| **Stage**           | Quel groupe de tasks ?        | 🧩 Étape d'exécution         |
| **DAG**             | Quelles dépendances ?         | 🗺️ Graphe du traitement     |


| Transformation  | Action      |
| --------------- | ----------- |
| `filter()`      | `show()`    |
| `select()`      | `count()`   |
| `withColumn()`  | `collect()` |
| `groupBy()`     | `write()`   |
| `join()`        | `save()`    |
| `repartition()` | `count()`   |



| Notion                     | Question à laquelle elle répond                      |
| -------------------------- | ---------------------------------------------------- |
| **DAG**                    | Quelles opérations et quelles dépendances ?          |
| **Logical Plan**           | Quelle logique de traitement ?                       |
| **Optimized Logical Plan** | Comment optimiser cette logique ?                    |
| **Physical Plan**          | Comment Spark va réellement exécuter le traitement ? |
| **Stage**                  | Comment découper le traitement autour des shuffles ? |
| **Task**                   | Comment traiter une partition concrète ?             |


| Type                  | Où s'exécute le code ? | Performance | Optimisable par Spark ? |
| --------------------- | ---------------------- | ----------- | ---------------------- |
| Fonction native Spark | JVM / Spark            | ⭐⭐⭐⭐⭐       | Oui                    |
| Pandas UDF            | Python + Arrow         | ⭐⭐⭐         | Partiellement          |
| UDF Python classique  | Python                 | ⭐           | Non ou très peu        |



### Simulation d'entretien
* [ ] pouvez-vous vous présenter rapidement ?
* [ ] Question : Qu'est-ce qu'Apache Spark ? Apache Spark est un moteur de calcul distribué permettant de traiter de grands volumes de données sur un cluster de machines. Il est conçu pour le traitement batch, le streaming, le machine learning et l'analyse SQL. Spark distribue les traitements entre plusieurs nœuds afin d'améliorer les performances et la scalabilité
* [ ] Question : Quelle est la différence entre repartition() et coalesce() ?
* [ ] Question : Qu'est-ce qu'un shuffle et pourquoi est-il coûteux ?
* [ ] Question : Dans quel cas utilisez-vous un Broadcast Join ?
* [ ] Question : Pourquoi Spark utilise le Lazy Evaluation ?
* [ ] Question : Comment optimiser une requête Spark lente ? « Je commence par Spark UI pour identifier le Job et le Stage qui sont lents. Je regarde ensuite les Tasks, le volume de Shuffle Read/Write et les éventuels problèmes de data skew. Avec explain(True), j'analyse également le plan physique pour identifier les opérations coûteuses comme les Exchange, les joins ou les agrégations. Ensuite, selon le problème, je réduis les données le plus tôt possible avec les filtres et projections, j'utilise un Broadcast Join pour les petites dimensions, j'ajuste les partitions avec repartition ou coalesce, et j'évite les Python UDF lorsque des fonctions Spark natives existent. »

* [ ] Question : Quels sont les principaux composants de l'architecture Spark ? L'architecture Spark repose sur Driver Program, Cluster Manager, Worker Nodes, Executors, Tasks.
* [ ] Question : Quels sont les principaux composants de l'architecture Spark ?« L'architecture Spark repose principalement sur un Driver, un Cluster Manager et des Executors. Le Driver coordonne l'application, construit le DAG et planifie l'exécution. Le Cluster Manager attribue les ressources. Les Executors exécutent réellement les Tasks. Les données sont divisées en Partitions, et généralement une Task traite une Partition pour un Stage donné. Les Cores des Executors permettent d'exécuter plusieurs Tasks en parallèle
* [ ] Question : Quelle différence entre Spark et PySpark ?
* [ ] Question : Quelle différence entre RDD et DataFrame ?
* [ ] Question : Expliquez le principe du Lazy Evaluation.
* [ ] Question : Quelle différence entre une transformation et une action ?
* [ ] Question : Qu'est-ce qu'un DAG ?
* [ ] Question : Qu'est-ce qu'un shuffle ?
* [ ] Question : Comment identifier un problème de shuffle ?
* [ ] Question : Comment optimiser un job Spark lent ?
* [ ] Question : Qu'est-ce qu'une partition Spark ?
* [ ] Question : Différence entre repartition() et coalesce() ?
* [ ] Question : Qu'est-ce que le Data Skew ?
* [ ] Question : Quels types de jointures connaissez-vous ?
* [ ] Question : Dans quel cas utilisez-vous un Broadcast Join ?
* [ ] Question : Pourquoi une jointure peut-elle devenir très lente ?
* [ ] Question : Qu'est-ce que Catalyst Optimizer ?
* [ ] Question : Comment analyser un plan d'exécution ?
* [ ] Question : Pourquoi éviter les UDF Python ?
* [ ] Question : Quelle différence entre UDF et Pandas UDF ?
* [ ] Question : Pourquoi une UDF Python est-elle plus lente ? car l'échange entre la JVM de spark et le Processus Python est énorme. De plus, Catalyst ne peut pas optimiser efficacement le contenu de la fonction comme il le fait avec les fonctions natives Spark.
* [ ] Question : Pourquoi utilisez-vous Delta Lake ?
* [ ] Question : Différence entre Parquet et Delta ?
* [ ] Question : Qu'est-ce qu'un MERGE ?
* [ ] Question : Décrivez votre projet PySpark.
* [ ] Question : Quelle différence entre Delta Lake et Parquet ?
* [ ] Question : Quels contrôles qualité avez-vous mis en place ?
* [ ] Question : Comment calculer le chiffre d'affaires mensuel ?
* [ ] Question : Pourquoi devrions-nous vous recruter ?
* [ ] Question : Quand utiliser quand même une UDF ? absence de fonctions natives équivalente
* [ ] Question : Quand utiliser repartition ? Lorsque je souhaite redistribuer les données ou augmenter le nombre de partitions afin d'améliorer le parallélisme.
* [ ] Question : Quand utiliser coalesce ? Lorsque je souhaite réduire le nombre de partitions, notamment avant l'écriture, tout en limitant le coût d'un shuffle
* [ ] Question : Comment utilisez-vous Spark UI pour optimiser une application ? »
* [ ] Question : Expliquez votre pipeline NYC Taxi de bout en bout.

# Simulation d'entretien technique Spark / PySpark
## Présentation (2 min)

**Interviewer :** Bonjour Alpha, pouvez-vous vous présenter rapidement ?

**Candidat :**
* [ ] Je suis Data Engineer avec plus de 10 ans d'expérience dans la Data et la BI. 
* [ ] J'ai travaillé sur des projets de traitement de données à grande échelle dans les secteurs de la santé, du transport et de la recherche.
* [ ] Mes compétences principales sont SQL, Python, PySpark, Databricks, Azure, Power BI et les architectures Data Lake.
* [ ] Dernièrement, j'ai développé un pipeline Data Engineering complet basé sur 
* [ ] PySpark et Delta Lake selon une architecture Medallion Bronze, Silver et Gold 
* [ ] pour analyser les données NYC Taxi et alimenter des tableaux de bord Power BI.
---




# Partie 1 : Fondamentaux Spark
## Question 1
**Interviewer : Qu'est-ce qu'Apache Spark ?**

**Candidat :**
* [ ] Apache Spark est un moteur de calcul distribué permettant de traiter de grands volumes de données sur un cluster de machines.
* [ ] Il est conçu pour le traitement batch, le streaming, le machine learning et l'analyse SQL.
* [ ] Spark distribue les traitements entre plusieurs nœuds afin d'améliorer les performances et la scalabilité.

---

### Question 2
**Interviewer : Quels sont les principaux composants de l'architecture Spark ?**

**Candidat :** L'architecture Spark repose sur :
* Driver Program : Le Driver est le cerveau.
* Cluster Manager : Le Cluster Manager attribue les ressources selon l'environnement
* Worker Nodes : C'est là où le travail est réellement effectué
* Executors : Chaque Task est envoyée à un Executor
* Tasks : traitement d'une partition.


### Le Driver 
* [ ] reçoit ton code PySpark
* [ ] construit le DAG qui représente les différentes opérations et leurs dépendances
* [ ] construit le plan d'exécution, Spark va ensuite optimiser et déterminer comment exécuter réellement ces opérations
* [ ] décide comment découper le travail
* [ ] envoie les tâches aux Executors


### Le Cluster Manager : alloue les ressources du cluster selon l'environnement
* [ ] Locale Mode
* [ ] Standalone
* [ ] YARN
* [ ] Kubernetes
* [ ] Databricks
---

### le Cluster Manager décide :
  * combien d'Executors
  * combien de mémoire
  * combien de CPU

### Executors
* [ ] * C'est là où le travail est réellement effectué
* [ ] * Les Executors exécutent les tâches sur les partitions de données.
* [ ] * chaque partition du DataFrame est traitée par une Task qui s'exécute sur un Executor

---
* [ ] * Un core est une ressource CPU
* [ ] * Une Task est une unité de travail Spark
* [ ] * Un core peut exécuter une Task à la fois
* [ ] * Mais un même core va ensuite exécuter beaucoup de Tasks successivement.
---

``` text
CPU
├── Core 1
├── Core 2
├── Core 3
└── Core 4
``` 
* [ ] CPU = puissance de calcul
* [ ] RAM = espace de travail temporaire
* [ ] CPU = processeur qui effectue les calculs
* [ ] Core = unité de calcul du CPU.
* [ ] RAM = mémoire temporaire utilisée pendant les traitements (sert à stocker temporairement les données)
* [ ] Executor = processus Spark qui dispose de cores et de mémoire et exécute les Tasks.
* [ ] Une Task traite généralement une partition et s'exécute sur un core à un instant donné.
---


* [ ] Executor → Core → Task → Partition → Shuffle → Stage



### Dans Spark, la mémoire est notamment utilisée pour :
* [ ] charger des données
* [ ] faire des calculs
* [ ] stocker des résultats intermédiaires
* [ ] effectuer des joins
* [ ] faire des aggregations
* [ ] mettre des DataFrames en cache



---
* Exemple :  4 Executors, 4 cores par Executor et 100 partitions. 
* Combien de Tasks peuvent tourner simultanément ?
* Réponse :
  * 4 * 4 = 16 cores disponibles
  * donc 16 Tasks tournent simultanément, puis Spark traite les autres par vagues jusqu'à terminer les 100
  * 84 Tasks attendent
  * les cores reprennent les Tasks suivantes
---






---
### Exemple :
* supposons qu'on 4 millions de lignes à traiter en parallèle
* Spark découpe le fichier en 4 partitions
  * Executor 1 filtre 1 million : Partition 1
  * Executor 2 filtre 1 million : Partition 2
  * Executor 3 filtre 1 million : Partition 3
  * Executor 4 filtre 1 million : Partition 4
* Chaque partition devient une unité de travail
* Une Task = traitement d'une partition

---
* Pourquoi les partitions sont importantes ?
  * Parcequ'elles determinent le niveau de parallelisme.
  * Plus il y a des partitions équilibrées, plus Spark peut distribuer efficacement la charge sur les Executors


* Le nombre d'Executors est plutôt déterminé par la configuration des ressources du cluster, 
* pas par le nombre de partition

* Le nombre de partitions ne détermine pas le nombre d'Executors. 
* Les partitions déterminent principalement le nombre de Tasks qu'une étape peut générer. 
* Les Executors fournissent les ressources CPU et mémoire pour exécuter ces Tasks en parallèle. 
* Je cherche donc généralement à avoir suffisamment de partitions pour exploiter les cores disponibles,
* sans créer un nombre excessif de petites partitions.

```python
df_clean = (
    df
    .filter(col("trip_distance") > 0)
    .filter(col("total_amount") > 0)
    .filter(col("trip_duration_min") > 0)
)
```

```python
Lire parquet
   ↓
Filtre trip_distance
   ↓
Filtre total_amount
   ↓
Filtre duration
```











---
## Question 3

**Interviewer : Quelle différence entre Spark et PySpark ?**

**Candidat :**

Spark est le moteur de traitement distribué développé en Scala.

PySpark est l'API Python qui permet d'interagir avec ce moteur.

Le traitement est toujours exécuté par Spark ; PySpark ne sert que d'interface.

---

## Question 4

**Interviewer : Quelle différence entre RDD et DataFrame ?**

**Candidat :**

Les RDD sont les structures historiques de Spark.

Les DataFrames sont plus performants car ils bénéficient de Catalyst Optimizer et Tungsten.

Aujourd'hui, pour la majorité des traitements Data Engineering, on privilégie les DataFrames.

---

# Partie 2 : Exécution Spark
## Question 5
**Interviewer : Expliquez le principe du Lazy Evaluation.**
**Candidat :**
Spark ne lance pas immédiatement les traitements.
Les transformations construisent un plan logique.
L'exécution réelle n'intervient qu'au moment d'une action comme :

* show()
* count()
* collect()
* write()

Cela permet à Spark d'optimiser le plan avant exécution.

Spark utilise le Lazy Evaluation pour retarder l'exécution des transformations 
jusqu'à ce qu'une action soit déclenchée. 
Cela permet à Spark de construire le DAG, d'optimiser le plan d'exécution avec Catalyst 
et d'éviter des calculs inutiles. »
---





## Question 6

**Interviewer : Quelle différence entre une transformation et une action ?**

**Candidat :**

Transformations :

* select
* filter
* join
* groupBy

Elles retournent un nouveau DataFrame.

Actions :

* count
* show
* collect
* write

Elles déclenchent l'exécution du DAG.

---

## Question 7

**Interviewer : Qu'est-ce qu'un DAG ?**

**Candidat :**

DAG signifie Directed Acyclic Graph.

Il représente l'ensemble des opérations à effectuer sur les données.

Spark construit ce graphe puis le découpe en stages et tasks exécutés par les executors.

---

# Partie 3 : Optimisation
## Question 8
**Interviewer : Qu'est-ce qu'un shuffle ?**
**Candidat :**
Le shuffle correspond à une redistribution des données entre les partitions.
Il intervient notamment lors :

* des joins : join()
* des groupBy : groupBy()
* des distinct : df.distinct()
* des orderBy : orderBy()
* repartition()

"Dans Spark, lorsqu'une opération nécessite de redistribuer les données entre partitions, 
cela correspond généralement à un shuffle. 
Les opérations comme groupBy, join, distinct, orderBy ou repartition provoquent donc souvent un shuffle. 
En revanche, des transformations locales comme filter ou select n'en provoquent pas. 
Certaines optimisations, comme le Broadcast Join ou coalesce, permettent également d'éviter 
ou de limiter les coûts d'un shuffle complet.


C'est souvent l'opération la plus coûteuse dans Spark car elle implique des échanges réseau.
« Le shuffle est le mécanisme par lequel Spark redistribue les données entre les partitions, 
généralement pour que les lignes ayant une même clé se retrouvent ensemble. 
Il intervient notamment lors des groupBy, join, distinct ou orderBy. 
C'est une opération coûteuse car elle peut nécessiter des échanges réseau, de la mémoire et du disque. 
Je cherche donc à limiter les shuffles inutiles, notamment en filtrant tôt, en sélectionnant uniquement 
les colonnes nécessaires et en utilisant un Broadcast Join lorsqu'une table est suffisamment petite. »
---


### Pourquoi le shuffle est coûteux ?

#### Task
* [ ] écrire des données intermédiaires
* [ ] transférer des données
* [ ] réorganiser les données
* [ ] lire les nouvelles partitions

Le shuffle est coûteux parce qu'il implique une redistribution des données entre partitions. 
Cette redistribution sollicite le CPU pour organiser les données, 
la mémoire pour les données intermédiaires, le réseau pour transférer 
les données entre Executors et éventuellement le disque lorsque la mémoire est insuffisante 
et qu'un spill se produit.





## Question 9
**Interviewer : Comment identifier un problème de shuffle ?**
**Candidat :**

J'utilise :
* Spark UI
* DAG Visualization
* Stage Metrics
* Task Metrics

Je surveille particulièrement :

* le volume de données échangées
* la durée des stages
* les tâches déséquilibrées

---

## Question 10
**Interviewer : Comment optimiser un job Spark lent ?**
**Candidat :**

Ma démarche est :
1. Examiner Spark UI.
2. Identifier les shuffles.
3. Réduire les colonnes inutiles.
4. Filtrer le plus tôt possible.
5. Utiliser des Broadcast Joins.
6. Adapter le partitionnement.
7. Utiliser Parquet ou Delta.
8. Éviter les UDF Python.

---

# Partie 4 : Partitionnement

## Question 11

**Interviewer : Qu'est-ce qu'une partition Spark ?**

**Candidat :**

Une partition représente une unité de traitement distribuée.

Chaque partition est traitée indépendamment par un executor.

Le nombre de partitions influence directement le parallélisme.

---

## Question 12

**Interviewer : Différence entre repartition() et coalesce() ?**

**Candidat :**

repartition()

* augmente ou réduit le nombre de partitions
* provoque un shuffle

coalesce()

* réduit uniquement le nombre de partitions
* limite les mouvements de données

Pour réduire le nombre de fichiers avant écriture, je privilégie souvent coalesce().

---

## Question 13

**Interviewer : Qu'est-ce que le Data Skew ?**

**Candidat :**

Le Data Skew apparaît lorsqu'une partition contient beaucoup plus de données que les autres.

Certaines tâches deviennent alors très longues tandis que les autres terminent rapidement.

Les solutions sont :

* salting
* repartitionnement adapté
* broadcast join
* AQE (Adaptive Query Execution)

---

# Partie 5 : Jointures

## Question 14

**Interviewer : Quels types de jointures connaissez-vous ?**

**Candidat :**

* inner
* left
* right
* full
* left_semi
* left_anti

---

## Question 15
**Interviewer : Dans quel cas utilisez-vous un Broadcast Join ?**

**Candidat :**
Lorsque l'une des tables est suffisamment petite pour tenir en mémoire sur un executor.
Spark envoie alors cette table à tous les executors afin d'éviter un shuffle coûteux.

"Le Broadcast Join évite le shuffle de la grande table. 
Spark envoie la petite table à tous les Executors, 
puis chaque partition de la grande table effectue sa jointure localement. 
On obtient ainsi plusieurs joins locaux exécutés en parallèle."

Exemple dans mon projet :
Fact Trips + Taxi Zone Lookup.

---

## Question 16

**Interviewer : Pourquoi une jointure peut-elle devenir très lente ?**

**Candidat :**

Les causes fréquentes sont :

* gros shuffle
* skew de données
* mauvais partitionnement
* trop de colonnes
* absence de broadcast sur une petite table

---

# Partie 6 : Spark SQL

## Question 17

**Interviewer : Qu'est-ce que Catalyst Optimizer ?**

**Candidat :**

Catalyst est le moteur d'optimisation logique de Spark SQL.

Il :

* réécrit les requêtes
* pousse les filtres
* optimise les projections
* choisit certaines stratégies de jointure

---

## Question 18
**Interviewer : Comment analyser un plan d'exécution ?**
**Candidat :**
J'utilise :

```python
df.explain(True)
```

Je vérifie :

* plan logique
* plan optimisé
* plan physique

Je recherche particulièrement :

* Exchange
* Shuffle
* SortMergeJoin
* BroadcastHashJoin
---

# Partie 7 : PySpark
## Question 19
**Interviewer : Pourquoi éviter les UDF Python ?**

**Candidat :**
Les UDF Python nécessitent des échanges entre JVM et Python.
Cela ralentit fortement les traitements.
Je privilégie toujours les fonctions natives de pyspark.sql.functions.
---

« Les UDF Python peuvent être coûteuses car elles nécessitent des échanges entre 
le moteur Spark exécuté dans la JVM et le processus Python. 
De plus, Catalyst connaît moins bien la logique interne d'une UDF et dispose donc 
de moins de possibilités pour l'optimiser. 
Je privilégie donc les fonctions natives Spark, qui peuvent être optimisées par le moteur. 
Si une logique spécifique n'est pas réalisable avec les fonctions natives, 
je peux envisager une Pandas UDF ou une UDF Python en dernier recours. »

--
Les fonctions natives Spark sont mon premier choix car elles s'exécutent directement 
dans le moteur Spark et bénéficient des optimisations Catalyst. 
Lorsque la logique métier n'est pas couverte par les fonctions natives, 
je peux utiliser une Pandas UDF qui exploite Apache Arrow et traite les données par lots. 
Les UDF Python classiques sont mon dernier recours car elles introduisent un coût important lié 
aux échanges JVM-Python et limitent les optimisations du moteur Spark.



---
## Question 20
**Interviewer : Quelle différence entre UDF Python, Pandas UDF et une fonction native Spark ?**
**Candidat :**

Les Pandas UDF utilisent Apache Arrow.
Elles sont vectorisées et beaucoup plus performantes que les UDF classiques.
Cependant les fonctions natives Spark restent le meilleur choix lorsqu'elles existent.
---



---
# Partie 8 : Delta Lake
## Question 21
**Interviewer : Pourquoi utilisez-vous Delta Lake ?**
**Candidat :**
Delta Lake apporte :
* transactions ACID
* gestion des versions
* merge
* schema evolution
* time travel

Il améliore la fiabilité des Data Lakes.

---

## Question 22
**Interviewer : Différence entre Parquet et Delta ?**
**Candidat :**
Parquet est un format de stockage.
Delta Lake est une couche au-dessus de Parquet qui ajoute la gestion transactionnelle et le versioning.

---

## Question 23

**Interviewer : Qu'est-ce qu'un MERGE ?**

**Candidat :**

Le MERGE permet de faire des UPSERT.

Il combine INSERT, UPDATE et DELETE dans une seule instruction.

Très utile pour les chargements incrémentaux.

---

# Partie 9 : Cas pratique NYC Taxi

## Question 24

**Interviewer : Décrivez votre projet PySpark.**

**Candidat :**

J'ai développé un pipeline Data Engineering complet selon une architecture Medallion.

Bronze :
* ingestion des fichiers taxi

Silver :
* nettoyage
* normalisation
* contrôle qualité

Gold :
* tables de faits
* dimensions
* KPI métier

Les données sont stockées dans Delta Lake puis exploitées dans Power BI.

---

## Question 25

**Interviewer : Quels contrôles qualité avez-vous mis en place ?**

**Candidat :**

J'ai filtré :

* trip_distance > 0
* total_amount > 0
* durée de course > 0

J'ai également contrôlé les types de données et la cohérence temporelle.

---

## Question 26

**Interviewer : Comment calculer le chiffre d'affaires mensuel ?**

**Candidat :**

J'utiliserais :

```python
df.groupBy("periode").agg(sum("total_amount"))
```

Puis chargement dans une table Gold destinée au reporting.

---

# Question finale
**Interviewer : Pourquoi devrions-nous vous recruter ?**
**Candidat :**
Je possède une double compétence Data Engineering et Reporting.
Je maîtrise l'ensemble de la chaîne de valeur :

* ingestion
* transformation
* optimisation Spark
* modélisation
* visualisation Power BI

Je suis également habitué à travailler dans des environnements cloud et à industrialiser les pipelines de données.




Comment utilisez-vous Spark UI pour optimiser une application ? »
« Je commence par l'onglet Jobs pour identifier les actions lentes. 
Ensuite je regarde les Stages et les Tasks afin d'identifier les étapes coûteuses, 
notamment le volume de Shuffle Read/Write et les éventuelles tâches anormalement lentes. 
Je regarde ensuite le plan SQL pour comprendre les opérations comme les Exchange, les joins ou les agrégations. 
Enfin, je vérifie les Executors pour identifier d'éventuels problèmes de CPU, mémoire ou GC.


```` text
Spark UI
│
├── Jobs
│     └── Quelle action est lente ?
│
├── Stages
│     └── Quelle étape est lente ?
│
├── Tasks
│     └── Une partition est-elle beaucoup plus lente ?
│
├── Shuffle
│     └── Combien de données sont redistribuées ?
│
├── SQL
│     └── Quelle opération provoque le coût ?
│
└── Executors
└── CPU / mémoire / GC

```` 



« Je commence par Spark UI pour identifier le Job et le Stage qui sont lents. 
Je regarde ensuite les Tasks, le volume de Shuffle Read/Write et les éventuels problèmes de data skew. 
Avec explain(True), j'analyse également le plan physique pour identifier les opérations coûteuses comme les Exchange, les joins ou les agrégations. 
Ensuite, selon le problème, je réduis les données le plus tôt possible avec les filtres et projections, 
j'utilise un Broadcast Join pour les petites dimensions, j'ajuste les partitions avec repartition ou coalesce, et j'évite les Python UDF lorsque des fonctions Spark natives existent. »




Comment traitez-vous un data skew ? »
« Je commence par le détecter dans Spark UI en comparant la durée et le volume de données des différentes tasks. 
Je vérifie ensuite la distribution de la clé avec un groupBy.
Si le problème vient d'une clé très fréquente, je peux utiliser le salting pour répartir cette clé sur plusieurs partitions. 
Si une des tables est petite, je peux utiliser un Broadcast Join pour éviter le shuffle de la grosse table. 
Je peux également m'appuyer sur Adaptive Query Execution et sa gestion du skew join. »