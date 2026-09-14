def run_pipeline(
        env,
        taxi_type,
        periode=None
):
    """
    Point d'entrée générique du pipeline NYC Taxi.

    Le pipeline métier ne dépend pas de l'orchestrateur.
    Il peut être appelé depuis :
        - le terminal
        - Airflow
        - Databricks
        - un test Python
        - GitHub Actions
    """
    from nyc_taxi.src.jobs.pipeline_runner_jobs_bundles import PipelineRunner
    from nyc_taxi.src.common.spark_manager import SparkManager
    from nyc_taxi.src.logger.logger import PipelineLogger

    from nyc_taxi.src.setup.environment_setup import EnvironmentSetup
    from nyc_taxi.src.table_reference.load_tab_ref import ReferenceDataLoader
    from nyc_taxi.src.bronze.uber_bronze import UberBronze
    from nyc_taxi.src.silver.uber_silver import UberSilver
    from nyc_taxi.src.gold.uber_gold import UberGold
    from nyc_taxi.src.loader.data_loader import DataLoader
    from nyc_taxi.src.jobs.maintenance_job import MaintenanceJob


    # ============================================================
    # Paramètres du pipeline
    # ============================================================
    print(f"periode   = {periode}")
    print(f"taxi_type = {taxi_type}")
    print(f"env       = {env}")

    # ============================================================
    # Logger
    # ============================================================
    logger = PipelineLogger(
        name="pipeline_runner",
        env=env,
        periode=periode,
        taxi_type=taxi_type,
    )

    # ============================================================
    # Spark
    # ============================================================
    spark_manager = SparkManager(
        env=env,
        app_name="NYC_Taxi_Pipeline",
        logger=logger,
    )

    spark = spark_manager.get_spark()

    # ============================================================
    # Étapes du pipeline
    # ============================================================
    steps = [
        EnvironmentSetup(spark=spark,env=env,logger=logger),
        ReferenceDataLoader(spark=spark,env=env,logger=logger),
        UberBronze(spark=spark,logger=logger),
        UberSilver(spark=spark,logger=logger),
        UberGold(spark=spark,logger=logger),
        DataLoader(spark=spark,logger=logger),
        MaintenanceJob(spark=spark,logger=logger),
    ]

    # ============================================================
    # Pipeline Runner
    # ============================================================
    runner = PipelineRunner(
        spark=spark,
        env=env,
        taxi_type=taxi_type,
        periode=periode,
        logger=logger,
        steps=steps,
    )

    # ============================================================
    # Exécution
    # ============================================================
    return runner.run()


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        choices=["local", "docker", "databricks"],
        default="local"
    )

    parser.add_argument(
        "--taxi_type",
        default="yellow"
    )

    parser.add_argument(
        "--periode",
        type=int,
        default=None
    )

    args = parser.parse_args()

    return run_pipeline(
        env=args.env,
        taxi_type=args.taxi_type,
        periode=args.periode
    )


if __name__ == "__main__":
    main()


    # wsl
    # cd /mnt/d/data-ai-engineer-roadmap
    # source ~/spark4_env/bin/activate
    # python -m nyc_taxi.src.jobs.run_pipeline --env local --taxi_type yellow --periode 202501
    # Le Job est configuré comme : Python script