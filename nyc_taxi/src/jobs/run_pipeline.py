def run_nyc_taxi_pipeline():
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
    env = "docker"
    taxi_type = "yellow"
    periode = 202501

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
        app_name="NYC_Taxi_Airflow",
        logger=logger,
    )

    spark = spark_manager.get_spark()

    # ============================================================
    # Étapes du pipeline
    # ============================================================
    steps = [
        EnvironmentSetup(
            spark=spark,
            env=env,
            logger=logger
        ),

        ReferenceDataLoader(
            spark=spark,
            env=env,
            logger=logger
        ),

        UberBronze(
            spark=spark,
            logger=logger
        ),

        UberSilver(
            spark=spark,
            logger=logger
        ),

        UberGold(
            spark=spark,
            logger=logger
        ),

        DataLoader(
            spark=spark,
            logger=logger
        ),

        MaintenanceJob(
            spark=spark,
            logger=logger
        ),
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

    runner.run()