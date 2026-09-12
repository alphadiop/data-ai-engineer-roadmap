from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
from airflow.models.param import Param

with DAG(
        dag_id="nyc_taxi_airflow",
        start_date=datetime(2026, 1, 1),
        schedule=None,
        catchup=False,
        tags=["nyc_taxi", "data_engineering"],

        params={
            "periode": Param(202501,type="integer",title="Période"),
            "taxi_type": Param("yellow",type="string",enum=["yellow", "green"],title="Type de taxi"),
            "env": Param("docker",type="string",enum=["docker"],title="Environnement"),
        }

) as dag:

    run_pipeline = PythonOperator(
        task_id="run_nyc_taxi_pipeline",
        python_callable=run_nyc_taxi_pipeline,
    )



