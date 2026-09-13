from nyc_taxi.src.jobs.run_pipeline import run_pipeline
"""
Le notebook/script Databricks ne fait qu'une chose : appeler notre application Python.
La logique reste dans : 
run_pipeline.py
        ↓
PipelineRunner
        ↓
Bronze → Silver → Gold → Audit
"""
run_pipeline(
    env="databricks",
    taxi_type="yellow",
    periode=202501
)