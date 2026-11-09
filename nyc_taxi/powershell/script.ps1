Write-Host "`n===== POINT D'ENTREE ====="

Select-String `
    -Path "nyc_taxi/src/jobs/run_pipeline.py" `
    -Pattern "def main"

Write-Host "`n===== RESSOURCES DU PACKAGE ====="

Get-ChildItem "nyc_taxi/src" -Recurse -File |
    Where-Object {
        $_.Extension -in ".sql", ".json", ".yaml", ".yml"
    } |
    Select-Object FullName

Write-Host "`n===== CONFIGURATION ====="

Get-ChildItem "nyc_taxi/config" -File |
    Select-Object Name





python -m pip install --no-deps --target "nyc_taxi/verification_wheel/install_test" "nyc_taxi/verification_wheel/build_output/nyc_taxi-1.0.0-py3-none-any.whl"





 '==='
 @'
from pathlib import Path
from zipfile import ZipFile

wheel_dir = Path("nyc_taxi/verification_wheel/build_output")
wheels = list(wheel_dir.glob("*.whl"))

if not wheels:
    raise FileNotFoundError("Aucun fichier .whl trouvé")

wheel = wheels[0]

print(f"\nWHEEL : {wheel.name}")
print(f"TAILLE : {wheel.stat().st_size:,} octets")

with ZipFile(wheel) as archive:
    files = archive.namelist()

    sql_files = [
        f for f in files
        if f.endswith(".sql")
    ]

    json_files = [
        f for f in files
        if f.endswith(".json")
    ]

    yaml_files = [
        f for f in files
        if f.endswith((".yaml", ".yml"))
    ]

    entry_points = [
        f for f in files
        if f.endswith("entry_points.txt")
    ]

    print(f"\nFICHIERS PYTHON : {sum(f.endswith('.py') for f in files)}")
    print(f"FICHIERS SQL : {len(sql_files)}")
    print(f"FICHIERS JSON : {len(json_files)}")
    print(f"FICHIERS YAML : {len(yaml_files)}")

    print("\n===== FICHIERS SQL =====")
    for f in sql_files:
        print(f)

    print("\n===== FICHIERS JSON =====")
    for f in json_files:
        print(f)

    print("\n===== ENTRY POINTS =====")
    for f in entry_points:
        print(archive.read(f).decode("utf-8"))

    print("\n===== VERIFICATIONS =====")
    print("SQL présent :", len(sql_files) > 0)
    print("JSON présent :", len(json_files) > 0)
    print("YAML présent :", len(yaml_files) > 0)
    print("Entry points présent :", len(entry_points) > 0)
'@ | python -






 '==='
@'
import sys
from pathlib import Path
from importlib.resources import files

install_path = Path(
    "nyc_taxi/verification_wheel/install_test"
).resolve()

sys.path.insert(0, str(install_path))

import nyc_taxi

package = files("nyc_taxi.src.sql_operations")

json_file = package.joinpath(
    "sql_queries", "sql_operations.json"
)

sql_file = package.joinpath(
    "sql_queries", "sql_files", "select_table.sql"
)

print("===== PACKAGE =====")
print("Import :", nyc_taxi.__file__)

print("\n===== RESSOURCES =====")
print("JSON accessible :", json_file.is_file())
print("SQL accessible :", sql_file.is_file())

print("\n===== JSON =====")
print(json_file.read_text(encoding="utf-8")[:500])

print("\n===== SQL =====")
print(sql_file.read_text(encoding="utf-8"))
'@ | python -






$installPath = (Resolve-Path "nyc_taxi/verification_wheel/install_test").Path

Push-Location $env:TEMP

@'
import sys
from pathlib import Path
from importlib.resources import files

install_path = Path(r"INSTALL_PATH_PLACEHOLDER")

sys.path.insert(0, str(install_path))

import nyc_taxi

print("===== ORIGINE DU PACKAGE =====")
print(nyc_taxi.__file__)

package = files("nyc_taxi.src.sql_operations")

json_file = package.joinpath("sql_queries", "sql_operations.json")
sql_file = package.joinpath("sql_queries", "sql_files", "select_table.sql")

print("\n===== RESSOURCES INSTALLEES =====")
print("JSON accessible :", json_file.is_file())
print("SQL accessible :", sql_file.is_file())

print("\n===== CONTENU SQL =====")
print(sql_file.read_text(encoding="utf-8"))
'@.Replace("INSTALL_PATH_PLACEHOLDER", $installPath.Replace("\", "\\")) | python -

Pop-Location







Push-Location "nyc_taxi"

# Supprimer les anciens fichiers de construction
Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue

# Supprimer l'ancien wheel
Remove-Item `
    "verification_wheel/build_output/nyc_taxi-1.0.0-py3-none-any.whl" `
    -ErrorAction SilentlyContinue

# Reconstruire le wheel
python -m pip wheel . `
    --no-deps `
    --no-build-isolation `
    --wheel-dir "verification_wheel/build_output"

Pop-Location




# Supprimer uniquement l'ancienne installation de test
Remove-Item -Recurse -Force `
    "nyc_taxi/verification_wheel/install_test" `
    -ErrorAction SilentlyContinue

# Réinstaller le nouveau wheel
python -m pip install `
    --no-deps `
    --target "nyc_taxi/verification_wheel/install_test" `
    "nyc_taxi/verification_wheel/build_output/nyc_taxi-1.0.0-py3-none-any.whl"





$installPath = (Resolve-Path "nyc_taxi/verification_wheel/install_test").Path
$env:WHEEL_INSTALL_PATH = $installPath

Push-Location $env:TEMP

@'
import os
import sys
from pathlib import Path
from importlib.resources import files

install_path = Path(os.environ["WHEEL_INSTALL_PATH"])
sys.path.insert(0, str(install_path))

import nyc_taxi

print("===== ORIGINE DU PACKAGE =====")
print(nyc_taxi.__file__)

print("\n===== VERIFICATION DES RESSOURCES =====")
package = files("nyc_taxi.src.sql_operations")

json_file = package.joinpath("sql_queries", "sql_operations.json")
sql_file = package.joinpath("sql_queries", "sql_files", "select_table.sql")

print("JSON accessible :", json_file.is_file())
print("SQL accessible :", sql_file.is_file())

print("\n===== VERIFICATION DU PACKAGE RACINE =====")
print("Package installé :", Path(nyc_taxi.__file__).is_relative_to(install_path))
'@ | python -

Pop-Location
Remove-Item Env:WHEEL_INSTALL_PATH





Write-Host "`n===== REQUIREMENTS.TXT ====="
Get-Content "nyc_taxi/requirements.txt" -ErrorAction SilentlyContinue

Write-Host "`n===== PYPROJECT.TOML ====="
Get-Content "nyc_taxi/pyproject.toml"

Write-Host "`n===== SETUP.PY ====="
Get-Content "nyc_taxi/setup.py"

Write-Host "`n===== FICHIERS DE CONFIGURATION ====="
Get-ChildItem "nyc_taxi" -File |
    Where-Object {
        $_.Name -match "requirements|setup|pyproject|environment"
    } |
    Select-Object Name, FullName




@'
import ast
from pathlib import Path

folders = [
    Path("nyc_taxi/src"),
    Path("nyc_taxi/config"),
]

modules = set()

for folder in folders:
    if not folder.exists():
        continue

    for file in folder.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8-sig"))
        except Exception as error:
            print(f"ERREUR {file}: {error}")
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name.split(".")[0])

            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])

print("===== MODULES IMPORTES =====")
for module in sorted(modules):
    print(module)
'@ | python -






@'
import ast
from pathlib import Path

external_candidates = {
    "dask", "faiss", "numpy", "pandas", "polars",
    "pyspark", "delta", "sentence_transformers",
    "sqlalchemy", "sqlparse", "tabulate", "yaml"
}

folders = [
    Path("nyc_taxi/src"),
    Path("nyc_taxi/config"),
]

for folder in folders:
    if not folder.exists():
        continue

    for file in folder.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8-sig"))
        except Exception:
            continue

        found = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    if module in external_candidates:
                        found.add(module)

            elif isinstance(node, ast.ImportFrom) and node.module:
                module = node.module.split(".")[0]
                if module in external_candidates:
                    found.add(module)

        for module in sorted(found):
            print(f"{module:<25} {file}")
'@ | python -






$files = @(
    "nyc_taxi/src/jobs/run_pipeline.py",
    "nyc_taxi/src/spark/spark_manager.py",
    "nyc_taxi/src/bronze/uber_bronze.py",
    "nyc_taxi/src/silver/uber_silver.py",
    "nyc_taxi/src/gold/uber_gold.py",
    "nyc_taxi/src/common/delta_manager.py",
    "nyc_taxi/src/common/delta_load.py",
    "nyc_taxi/src/common/schema_manager.py",
    "nyc_taxi/src/common/pipeline_context.py",
    "nyc_taxi/src/audit/audit_manager.py",
    "nyc_taxi/src/utils/config/load_config.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "`n===== $file ====="
        Select-String -Path $file -Pattern '^\s*(import |from )'
    }
    else {
        Write-Host "`nFICHIER INTROUVABLE : $file"
    }
}





$files = @(
    "nyc_taxi/src/jobs/pipeline_runner_jobs_bundles.py",
    "nyc_taxi/src/jobs/maintenance_job.py",
    "nyc_taxi/src/setup/environment_setup.py",
    "nyc_taxi/src/table_reference/load_tab_ref.py",
    "nyc_taxi/src/loader/data_loader.py",
    "nyc_taxi/src/logger/logger.py",
    "nyc_taxi/src/common/logger.py",
    "nyc_taxi/src/common/spark_environment_logger.py",
    "nyc_taxi/src/sql_manager/sql_manager.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "`n===== $file ====="
        Select-String -Path $file -Pattern '^\s*(import |from )'
    }
    else {
        Write-Host "`nFICHIER INTROUVABLE : $file"
    }
}







$files = @(
    "nyc_taxi/src/rag",
    "nyc_taxi/src/sql_operations",
    "nyc_taxi/src/utils/write",
    "nyc_taxi/src/utils/tabulate_dataframe.py"
)

foreach ($path in $files) {
    if (Test-Path $path -PathType Container) {
        Get-ChildItem $path -Recurse -Filter "*.py" |
            ForEach-Object {
                Write-Host "`n===== $($_.FullName) ====="
                Select-String -Path $_.FullName -Pattern '^\s*(import |from )'
            }
    }
    elseif (Test-Path $path -PathType Leaf) {
        Write-Host "`n===== $path ====="
        Select-String -Path $path -Pattern '^\s*(import |from )'
    }
}




@'
from importlib.metadata import version, PackageNotFoundError

packages = [
    "PyYAML",
    "pyspark",
    "delta-spark",
    "sqlparse",
    "SQLAlchemy",
    "pandas",
    "dask",
    "polars",
    "numpy",
    "faiss-cpu",
    "sentence-transformers",
    "tabulate",
    "pytest",
]

print("===== VERSIONS DES DEPENDANCES =====")

for package in packages:
    try:
        print(f"{package:<25} {version(package)}")
    except PackageNotFoundError:
        print(f"{package:<25} NON INSTALLE")
    except Exception as error:
        print(f"{package:<25} ERREUR METADONNEES : {error}")
'@ | python -









# Sauvegarder la configuration actuelle
Copy-Item `
    "nyc_taxi/setup.py" `
    "nyc_taxi/setup.py.bak" `
    -Force

# Remplacer setup.py
@'
from setuptools import setup, find_packages

# Packages Python situés dans src/
src_packages = find_packages("src")

# Packages exposés dans le wheel sous nyc_taxi.*
mapped_packages = [
    "nyc_taxi",
    "nyc_taxi.src",
    "nyc_taxi.config",
] + [
    f"nyc_taxi.src.{package}"
    for package in src_packages
]

package_dir = {
    "nyc_taxi": ".",
    "nyc_taxi.src": "src",
    "nyc_taxi.config": "config",
}

for package in src_packages:
    package_dir[
        f"nyc_taxi.src.{package}"
    ] = f"src/{package.replace('.', '/')}"

# Dépendances obligatoires du pipeline
install_requires = [
    "PyYAML>=6.0",
    "pyspark==3.5.1",
    "delta-spark==3.2.0",
    "sqlparse>=0.5.5",
]

# Dépendances des fonctionnalités complémentaires
extras_require = {
    "sql": [
        "pandas",
        "dask[dataframe]",
        "polars",
        "SQLAlchemy",
        "tabulate",
    ],
    "rag": [
        "numpy",
        "faiss-cpu",
        "sentence-transformers",
    ],
    "dev": [
        "pytest",
    ],
}

setup(
    name="nyc_taxi",
    version="1.0.0",
    packages=mapped_packages,
    package_dir=package_dir,
    package_data={
        "nyc_taxi.config": [
            "*.yaml",
        ],
        "nyc_taxi.src.sql_operations": [
            "sql_queries/*.json",
            "sql_queries/sql_files/*.sql",
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "nyc-taxi-pipeline=nyc_taxi.src.jobs.run_pipeline:main"
        ]
    },
)
'@ | Set-Content -Path "nyc_taxi/setup.py" -Encoding UTF8




# Vérifier que le dossier de destination existe
Test-Path "nyc_taxi/verification_wheel"

# Déplacer la sauvegarde hors du package
Move-Item `
    "nyc_taxi/setup.py.bak" `
    "nyc_taxi/verification_wheel/setup.py.before_dependencies.bak"

# Vérifier le déplacement
Write-Host "`n===== VERIFICATION ====="

Get-Item "nyc_taxi/verification_wheel/setup.py.before_dependencies.bak" |
    Select-Object Name, Length





# Se placer dans le dossier du package
Set-Location "nyc_taxi"

# Supprimer uniquement les anciens artefacts de construction
if (Test-Path "build") {
    Remove-Item "build" -Recurse -Force
}

if (Test-Path "dist") {
    Remove-Item "dist" -Recurse -Force
}

if (Test-Path "nyc_taxi.egg-info") {
    Remove-Item "nyc_taxi.egg-info" -Recurse -Force
}

# Construire le wheel sans réinstaller les dépendances
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist