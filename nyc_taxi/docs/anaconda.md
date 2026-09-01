### Configurer Airflow
* [ ] conda create -n airflow_env python=3.11 -y
* [ ] conda activate airflow_env
* [ ] pip install "apache-airflow==3.1.8" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.8/constraints-3.11.txt" 
* [ ] Airflow recommande toujours l'utilisation du fichier de contraintes pour éviter les conflits de dépendances 



### Configurer AIRFLOW_HOME
* [ ] mkdir D:\airflow
* [ ] set AIRFLOW_HOME=D:\airflow
* [ ] echo %AIRFLOW_HOME%


### Initialiser Airflow
* [ ] airflow db migrate ou airflow standalone

### Cette commande :
* [ ] crée la base Airflow
* [ ] démarre le scheduler
* [ ] démarre le webserver
* [ ] crée un compte admin automatiquement


### Accéder à l'interface
* [ ] Ouvre : http://localhost:8080



### Créer le répertoire des DAGs
* [ ] D:\airflow\dags
* [ ] Puis dans airflow.cfg : dags_folder = D:\airflow\dags


### Vérifier l'installation
* [ ] airflow dags list


### Structure projet NYC Taxi
* [ ] D:\airflow\dags
    * [ ] nyc_taxi_dag.py

* Le DAG appellera simplement ton runner : 
* python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles --env local --periode 202507 --taxi_type yellow