#### Cluster
- [ ] un cluster est l'ensemble des machines (ressources de calcul) qui exécutent ton code Spark 
- [ ] Ce code est sur : notebooks, jobs, pipelines, requêtes SQL, transformations de données
- [ ] le cluster est le moteur d'exécution de ton traitement.


#### Composition d'un Cluster
- [ ] Driver : le chef d'orchestre
- [ ] workers : Chaque worker traite une partie des données c'est eux qui executent les calculs


### Rôle du Driver
- [ ] reçoit ton code Python/SQL
- [ ] construit le plan Spark
- [ ] distribue les tâches
- [ ] collecte les résultats


### Rôle des Workers
- [ ] lisent les fichiers
- [ ] transforment les données
- [ ] exécutent les opérations Spark
- [ ] stockent temporairement les données en mémoire


#### les types de Cluster Databricks
- [ ] All-Purpose Clusters : (cluster interactif) qui reste allumé tant qu'on ne l'arrête pas
- [ ] Job cluster : crée uniquement pour exécuter un job puis supprimé après l'exécution


#### Job cluster : Cluster créé uniquement pour exécuter un job puis supprimé à la fin de l'exécution
- [ ] moins cher : car ne consomme des ressources que pendant l'exécution du job
- [ ] isolé : car chaque exécution dispose de son propre environnement
- [ ] reproductible : a chaque exécution Databricks recrée exactement le même cluster à partir de la définition du job
- [ ] en production on prefere les job clusters, tandis que les All-Purpose Clusters sont surtout utilisés pour le développement, les tests et l'exploration des données

### Exemple de Cluster Job
- [ ] NYC Taxi Pipeline
  - [ ] Job Cluster
  - [ ] Exécution
  - [ ] Suppression du cluster


### Taille d'un cluster : un Cluster possède
- [ ] nombre de workers
- [ ] mémoire RAM
- [ ] nombre de CPU
- [ ] type de machine

### Exemple : Cluster NYC Taxi
- [ ] Driver:
  - [ ] 8 CPU
  - [ ] 32 GB RAM

- [ ] Workers:
  - [ ] 4 machines

- [ ] Chaque worker:
  - [ ] 8 CPU
  - [ ] 32 GB RAM

* Total CPU = 8 + (4 * 8) = 40 CP
* Total RAM : 32 + (32 * 4) = 160 GB

### CPU : la puissance de calcul
- [ ] Le CPU (Central Processing Unit) exécute les instructions
- [ ] Par exemple, lorsque Spark exécute : df.groupBy("payment_type").count()
  - [ ] il lit les données
  - [ ] compare les valeurs
  - [ ] effectue les agrégations
  - [ ] calcule les résultats
- [ ] Plus tu as de CPU (ou de cœurs CPU), plus tu peux traiter de données en parallèle

* Exemple : le traitement de 100 millions de lignes est plus rapide avec 8 CPU à la place de 2 CPU
* car c'est 100 / 8 = 12,5 millions par CPU à la place de 50 millions par CPU

### RAM : la mémoire de travail
- [ ] contient les données pendant leut traitement
- [ ] par exemple : df = spark.read.table("silver_nyc_taxi")
  - [ ] Spark charge une partie des données en mémoire
  - [ ] Si les données tiennent en RAM :
      - [ ] partition 1
      - [ ] partition 2
      - [ ] partition 3
      - [ ] partition 4
  - [ ] le traitement est rapide

  - [ ] Si la RAM est insuffisante
      - [ ] RAM plaine
      - [ ] Spark écrit sur disque --> on parle de spil to disk (Spill vers disque)
      - [ ] le disque étant beacoup plus lent que la RAM, les performances chutent
      - [ ] La RAM est directement connectée au CPU : besoin de CPU en data est rapide
      - [ ] La RAM est conçue pour être consultée en permanence par le CPU
      - [ ] Le disque est beaucoup plus loin : le besoin du CPU en data se fait attendre plus longtemps

* RAM siffusant : la RAM envoie les données au CPU pour le calcul puis résultat 
* RAM insiffusant : Disque -> RAM -> CPU -> Calcul

### SI Spark écrit sur disque alors les étapes pour accèder au disque sont :
- [ ] Lire disque
- [ ] Copier en RAM
- [ ] Calculer
- [ ] Réécrire disque
- [ ] Le cluster devient lent même si les CPU sont puissants
- [ ] Spark utilise la RAM en priorité.
- [ ] Lorsque la RAM est pleine, Spark se rabat sur le disque temporaire (spill), ce qui ralentit fortement le traitement

### Cas typiques : Manque de CPU
- [ ] RAM : 64 Go
- [ ] CPU : 2 cœurs
- [ ] Les données tiennent en mémoire mais les calculs sont lents car manque de CPU


### Cas typiques Manque de RAM
- [ ] RAM : 4 Go
- [ ] CPU : 16 cœurs
- [ ] Les CPU attendent constamment que les données soient relues depuis le disque

* Dans Databricks : Quand tu choisis un type de machine, tu obtiens un certain nombre de CPU et de RAM

| Machine | CPU | RAM   |
| ------- | --- | ----- |
| Small   | 2   | 8 Go  |
| Medium  | 4   | 16 Go |
| Large   | 8   | 32 Go |



| Ressource | Rôle                                                     | Analogie              |
| --------- | -------------------------------------------------------- | --------------------- |
| **CPU**   | Effectue les calculs                                     | Le cerveau            |
| **RAM**   | Stocke temporairement les données en cours de traitement | La mémoire de travail |


### Règle simple
  - [ ] CPU = vitesse de calcul.
  - [ ] RAM = quantité de données pouvant être traitées en mémoire.
  - [ ] plus de CPU → traitements plus rapides
  - [ ] Plus de RAM → moins d'écriture sur disque et meilleure stabilité

  - [ ] Pour un pipeline comme NYC Taxi, 
  - [ ] les opérations de join, groupBy, OPTIMIZE et les agrégations Gold consomment à la fois du CPU et de la RAM, 
  - [ ] mais les gros volumes de données deviennent souvent limités par la RAM avant de l'être par le CPU.



### Cluster fixe vs autoscaling
- [ ] Tu définis workers = 4 alors c'est toujours 4
- [ ] avantage : prévisible
- [ ] inconvéniant : gaspillage possible si toutes les capacités du ressource ne sont utilisés

## cluster autoscaling:
- [ ] Databricks ajuste automatiquement
- [ ] 



## cluster et coût:
- [ ] un cluster consomme des ressources tant qu'il tourne
- [ ] 



| Élément     | Rôle                                        |
| ----------- | ------------------------------------------- |
| Workspace   | endroit où vivent notebooks, fichiers, jobs |
| Cluster     | puissance de calcul                         |
| Notebook    | code                                        |
| Job         | orchestration automatique                   |
| Delta Table | stockage des données                        |
| Catalog     | organisation/sécurité des données           |




