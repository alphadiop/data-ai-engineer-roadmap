from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
        dag_id="nyc_taxi_pipeline",
        start_date=datetime(2026, 1, 1),
        schedule="@monthly",
        catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command="""
        cd /mnt/d/data-ai-engineer-roadmap

        /home/alpha/spark4_env/bin/python \
        -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundles \
        --env local \
        --taxi_type yellow
        """,
    )