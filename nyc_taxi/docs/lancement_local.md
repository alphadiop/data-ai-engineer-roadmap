cd D:\data-ai-engineer-roadmap\nyc_taxi
tree /F src

set PYTHONPATH=D:\data-ai-engineer-roadmap
echo %PYTHONPATH%

python -c "import nyc_taxi.src.jobs.pipeline_runner_jobs_bundles; print('OK')"

python nyc_taxi\src\jobs\pipeline_runner_jobs_bundles.py --periode 202605 --taxi_type yellow
python -m nyc_taxi\src\jobs\pipeline_runner_jobs_bundles.py --periode 202605 --taxi_type yellow
python -m nyc_taxi.src.jobs.pipeline_runner_jobs_bundle.py --periode 202605 --taxi_type yellow


conda deactivate
conda env config vars set PYTHONPATH=D:\data-ai-engineer-roadmap
conda deactivate
conda activate spark_local