conda activate D:\conda_envs\spark_local
cd D:\data-ai-engineer-roadmap\nyc_taxi
conda activate spark_local
python -c "import pyspark; print(pyspark.__version__)"



cd validations
python spark_ui_exercise.py

spark ui : http://localhost:4040



Get-ChildItem .\dist\
tree src /F
Get-Content .\src\jobs\run_pipeline.py


databricks bundle summary -t dev
databricks auth login --host https://dbc-8c847397-3c66.cloud.databricks.com --profile alphadiop

databricks auth profiles

databricks bundle summary -t dev


Remove-Item `
  .\inspect_wheel_2, `
  .\inspect_wheel, `
  .\inspect_wheel_1 `
  -Recurse -Force

Get-ChildItem -Directory .\inspect_wheel*

python -m zipfile -l .\dist\nyc_taxi-1.0.0-py3-none-any.whl

Get-Content .\resources\nyc_pipeline.yml

# 1. Configuration du projet NYC Taxi
Get-Content .\pyproject.toml

# 2. Vérifier si une configuration existe aussi à la racine du dépôt
if (Test-Path ..\pyproject.toml) {
    Get-Content ..\pyproject.toml
} else {
    Write-Host "Pas de pyproject.toml à la racine du dépôt."
}

# 3. État actuel des Wheels
Get-ChildItem .\dist\*.whl

Remove-Item .\.gitignore


python -m pip show build
Get-ChildItem .\pyproject.toml, ..\pyproject.toml -ErrorAction SilentlyContinue





      - name: Deploy Databricks bundle
        run: |
          databricks bundle deploy