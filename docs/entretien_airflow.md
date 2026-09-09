
### Comprendre 
* [ ] Pourquoi on utilise Airflow
* [ ] Son architecture
* [ ] Les DAGs
* [ ] Les Operators
* [ ] La planification
* [ ] La gestion des dépendances
* [ ] Les bonnes pratiques
---

### C'est quoi Airflow ?
* [ ] Apache Airflow est un orchestrateur de workflows
* [ ] Il permet d'automatiser, planifier et superviser des traitements de données
---

#### Exemple de traitement de données
* [ ] Télécharger fichier
* [ ] Charger Bronze
* [ ] Transformer Silver
* [ ] Création de Gold
* [ ] Envoie Email

### Objectif Airflow
* [ ] s'assurer que les tâches s'exécutent dans le bon ordre
* [ ] que les erreurs sont détectées
* [ ] que les relances sont possibles
* [ ] que les traitements sont historisés


### Planification automatique.
* [ ] Le Scheduler déclenche les tâches selon le planning défini
  * Tous les jours : schedule="@daily"
  * Toutes les heures : schedule="@hourly"
  * toutes les 5 mn : schedule="*/5 * * * *"


### Pourquoi on utilise Airflow
* [ ] Airflow lance et supervise les jobs Spark mais ne remplace pas Spark.
* [ ] Airflow = orchestrateur
* [ ] Databricks = moteur d'exécution/plateforme de traitement
---

---

---
### Décrivez l'architecture Airflow."
* [ ] Scheduler -> Executor -> Workers -> Tâches


---
* [ ] Scheduler : Le Scheduler détecte les DAGs à exécuter et décide quand lancer les tâches
* [ ] Executor : L'Executor distribue les tâches et determine où les tâches seront exécutées. 
  * Exemple 
    * SequentialExecutor, 
    * LocalExecutor, 
    * CeleryExecutor, 
    * KubernetesExecutor
* [ ] Workers : Les Workers exécutent les traitements, c'est la machine qui exécute réellement les tâches
* [ ] Les résultats sont enregistrés dans la Metadata Database. 
  * Elle stocke 
    * l'historique des exécutions, 
    * les états des tâches, 
    * les utilisateurs, 
    * les configurations 
* [ ] Le Webserver permet le suivi et l'administration, 
  * c'est une interface graphique qui permet de voir 
    * les DAGs, 
    * relancer une tâche, 
    * consulter les logs



### DAG Run vs Task Instance
* [ ] Un DAG Run est une exécution complète du workflow
* [ ] Une Task Instance est l'exécution d'une tâche dans un DAG Run donné.
* [ ] Un DAG Run représente une exécution complète d'un workflow pour une date donnée, alors qu'une Task Instance représente l'exécution d'une tâche particulière dans ce DAG Run
Task Instance = Cron

### Scheduler vs Executor vs Worker
* [ ] C'est la base de l'architecture Airflow
* [ ] Scheduler décide : Il est 2h du matin, Je dois lancer le DAG.
* [ ] Il ne fait pas le travail, il donne juste les ordres

## Executor
* [ ] L'Executor reçoit l'ordre : **Exécute Bronze** et décide où exécuter la tâche

### Worker
* [ ] Le Worker exécute réellement le code. 
* Le Scheduler planifie les tâches, l'Executor décide où elles seront exécutées et les Workers exécutent effectivement le code



### Catchup et Backfill
* [ ] catchup=False signifie que Airflow ne lance que la date actuelle
* [ ] catchup=True signifie que Airflow rejoue tout le retard à part de start_date
* [ ] Backfill est manuel **airflow dags backfill** pour rejouer seulement ces dates


### XCom : XCom = Cross Communication.
* [ ] Permet à deux tâches d'échanger des informations
* [ ] XCom permet l'échange de petites informations entre tâches, comme des identifiants, des dates ou des chemins de fichiers. 
* [ ] Il n'est pas conçu pour transporter de gros volumes de données.


### Pourquoi utiliser Airflow avec Spark ?
* [ ] Spark traite les données et ne sait pas planifier
    * Lancer Bronze à 2h
    * Attendre la fin
    * Puis lancer Silver
    * Puis envoyer une alerte
* [ ] Airflow orchestre et sait faire cela
* [ ] Spark est le moteur de calcul distribué tandis qu'Airflow orchestre les différentes étapes du pipeline. 
* [ ] Spark et Airflow sont complémentaires.



### Airflow + Databricks
* [ ] Airflow peut piloter Databricks
* [ ] Architecture : Airflow -> API Databricks -> Cluster Databricks -> Notebook Spark
* [ ] Exemple : DatabricksSubmitRunOperator
* [ ] Airflow orchestre les traitements tandis que Databricks exécute les workloads Spark. 
* [ ] Airflow communique avec Databricks via son API.

### Architecture CeleryExecutor et KubernetesExecutor
* [ ] SequentialExecutor : Par défaut : Task A puis Task B puis Task C, Une seule tâche à la fois
* [ ] LocalExecutor : une seule machine, plusieurs tâches en parallèle
* [ ] CeleryExecutor : Plusieurs Workers, Très utilisé en production.
  * Avantages :
    * Scalabilité
    * Tolérance aux pannes
    * Distribution de charge
* [ ] KubernetesExecutor : Chaque tâche crée un Pod Kubernetes
    * Task A
      → Pod A
    * Task B
      → Pod B
    * Task C
      → Pod C
    * A la fin Pod supprimé
      * Avantages :
        * Scalabilité
        * Tolérance aux pannes
        * Distribution de charge
* [ ] CeleryExecutor s'appuie sur un pool de Workers permanents qui consomment les tâches depuis une file de messages. 
* [ ] KubernetesExecutor crée dynamiquement un Pod par tâche et le supprime une fois l'exécution terminée.



### Qu'est-ce qu'un DAG ?
* [ ] DAG = Directed Acyclic Graph : C'est un workflow complet
  * Task : c'est une étape du workflow
    * Exemple :
      * Téléchargement 
      * Bronze 
      * Silver 
      * Gold


### les operators
* [ ] PythonOperator : Exécute une fonction Python, Exemple : PythonOperator(...)
* [ ] BashOperator : Exécute une commande Linux, exemple : BashOperator(bash_command="python script.py")
* [ ] EmailOperator : Envoi d'e-mails
* [ ] SparkSubmitOperator : Lance un job Spark, Exemple : SparkSubmitOperator(application="pipeline.py")
* [ ] DatabricksSubmitRunOperator : Pour Databricks

### Quelle différence entre Airflow, XCom et Cron ?
* [ ] Cron : lance un script
* [ ] XCom : Échanger de petites informations entre tâches
* [ ] Airflow :
  * gère un workflow complet
  * dépendances
  * monitoring
  * retry : Si une tâche échoue, Airflow relance automatiquement default_args = {"retries": 3, "retry_delay": timedelta(minutes=5) }
  * logs
  * alertes

### Comment présenter Airflow dans ton projet NYC Taxi
* [ ] J'utiliserais Airflow pour orchestrer mon pipeline NYC Taxi. 
* [ ] Un DAG mensuel déclencherait successivement 
  * le téléchargement du fichier source, 
  * le chargement Bronze, 
  * les transformations Silver, 
  * la création des tables Gold 
  * et enfin le calcul des KPI. 
* [ ] Airflow permettrait de gérer 
  * les dépendances, 
  * les reprises sur erreur, 
  * le monitoring 
  * et l'historisation des exécutions