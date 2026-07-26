#### l'orchestration consiste à coordonner et automatiser l'enchaînement des traitements
- [ ] Sans orchestration, tu devrais lancer chaque étape manuellement
    - [ ] 1. Charger les données
    - [ ] 2. Nettoyer les données
    - [ ] 3. Construire les KPI
    - [ ] 4. Envoyer le rapport

### L'orchestrateur :
- [ ] Un orchestrateur gère tout automatiquement
    - [ ] lance Bronze : vérifie que Bronze est terminé ;
    - [ ] lance Silver : vérifie que Silver est terminé ;
    - [ ] lance Gold : envoie une alerte si une étape échoue.

* dépendances : Gold ne démarre jamais avant la fin de Silver

### Exemple d'orchestrateur
- [ ] Databricks Jobs
- [ ] Apache Airflow
- [ ] Azure Data Factory

### Rôle de l'orchestrateur
- [ ] lancer des tâches ;
- [ ] gérer les dépendances ;
- [ ] relancer en cas d'échec ;
- [ ] envoyer des alertes ;
- [ ] planifier des exécutions


### Résumé
- [ ] Spark exécute les calculs.
- [ ] L'orchestration organise l'exécution des traitements
- [ ] Elle gère :
    - [ ] l'ordre des tâches ;
    - [ ] les dépendances ;
    - [ ] les erreurs ;
    - [ ] la planification ;
    - [ ] les paramètres.
    - [ ] Dans Databricks, l'orchestration est généralement réalisée avec les Jobs Databricks, 
    - [ ] tandis que tes notebooks Bronze, Silver et Gold réalisent le travail de transformation des données

### Le DAG signifie Directed Acyclic Graph (graphe orienté sans cycle)
- [ ] C'est la description du workflow que l'orchestrateur doit exécuter
- [ ] Par exemple : Bronze -> Silver -> Gold -> Maintenance est une description d'un workflow donc c'est un DAG
- [ ] le DAG montre l'ordre d'exécution
- [ ] Databricks construit automatiquement un DAG à partir des dépendances que tu définis


* Par analogie : imagine un GPS 
* le DAG est l'intinéraire
* l'orchestrateur est le chauffeur qui suit l'intinéraire



### Pour un environnement professionnel
- [ ] Développeur
- [ ] OAuth
- [ ] Databricks
- [ ] CI/CD (GitHub Actions, Azure DevOps)
- [ ] Service Principal
- [ ] Databricks

### Production
- [ ] GitHub Actions
- [ ] Databricks CLI
- [ ] Bundle Deploy
- [ ] Job Production



