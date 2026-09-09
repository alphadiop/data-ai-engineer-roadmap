from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
        dag_id="nyc_taxi_pipeline",
        start_date=datetime(2025,1,1),
        schedule="@daily",
        catchup=False
):

    bronze = PythonOperator(
        task_id="bronze",
        python_callable=load_bronze
    )

    silver = PythonOperator(
        task_id="silver",
        python_callable=load_silver
    )

    gold = PythonOperator(
        task_id="gold",
        python_callable=load_gold
    )

    bronze >> silver >> gold