### Etapes principales du projet NYC
* [ ] ingestion Bronze
* [ ] transformations Silver
* [ ] modèle Gold
* [ ] Delta Lake
* [ ] audit
* [ ] orchestration Airflow


### Prochaines étapes naturelles
#### Étape 1 : Paramétrer le DAG
* [ ] Faire passer les paramètres Airflow :
* [ ] --taxi_type yellow
* [ ] --periode 202504

#### Étape 2 : Notifications d'échec
* [ ] Configurer un email ou une alerte Teams/Slack lorsque :
* [ ] run_pipeline = FAILED


#### Étape 3 : Découper le DAG
Quand la version actuelle sera stable :
````text
setup_environment
        ↓
bronze
        ↓
silver
        ↓
gold
        ↓
maintenance
````


#### Étape 4 : Déploiement cloud
* [ ] Airflow sur VM Linux ou Azure Data Factory ou Databricks Workflows