from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline

run_nyc_taxi_pipeline(
    params={
        "periode": 202501,
        "taxi_type": "yellow",
        "env": "docker",
    }
)

