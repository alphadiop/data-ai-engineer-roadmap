
### Lancement du programme
* wsl
* cd /mnt/d/data-ai-engineer-roadmap
* source ~/spark4_env/bin/activate
* from nyc_taxi.src.jobs.run_pipeline import run_nyc_taxi_pipeline
* run_nyc_taxi_pipeline(env="local", taxi_type="yellow",periode=202501)
* python -m nyc_taxi.src.jobs.run_pipeline --env local --periode 202504 --taxi_type yellow
* http://localhost:8080

