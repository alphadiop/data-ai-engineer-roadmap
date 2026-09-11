from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline

with DAG(
        dag_id="nyc_taxi_airflow",
        start_date=datetime(2026, 1, 1),
        schedule=None,
        catchup=False,
        tags=["nyc_taxi", "data_engineering"],
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_nyc_taxi_pipeline",
        python_callable=run_nyc_taxi_pipeline,
    )

