from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
        dag_id="nyc_taxi_pipeline",
        schedule="@monthly",
        catchup=False
):

    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command="""
        python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles
        --env local
        --periode {{ data_interval_start.strftime('%Y%m') }}
        --taxi_type yellow
        """
    )