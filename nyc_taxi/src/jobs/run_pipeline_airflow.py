
def run_nyc_taxi_pipeline(**context):
    """
    Adaptateur entre Airflow et le point d'entrée générique du pipeline.

    Le fichier ne connaîtra plus :
        PipelineRunner
        SparkManager
        PipelineLogger
        EnvironmentSetup
        ReferenceDataLoader
        UberBronze
        UberSilver
        UberGold
        DataLoader
        MaintenanceJob
    """

    from nyc_taxi.src.jobs.run_pipeline import run_pipeline

    params = context["params"]

    periode = params.get("periode")
    taxi_type = params.get("taxi_type")
    env = params.get("env")

    print(f"periode   = {periode}")
    print(f"taxi_type = {taxi_type}")
    print(f"env       = {env}")

    return run_pipeline(
        env=env,
        taxi_type=taxi_type,
        periode=periode,
    )

# if __name__ == "__main__":
#     context = {
#         "params": {
#             "periode": 202503,
#             "taxi_type": "yellow",
#             "env": "docker"
#         }
#     }
#     run_nyc_taxi_pipeline(
#         context=context
#     )

    ## Power Shell
    ## wsl
    ## cd /mnt/d/data-ai-engineer-roadmap
    ## source ~/spark4_env/bin/activate
    ## python run_pipeline_airflow.py