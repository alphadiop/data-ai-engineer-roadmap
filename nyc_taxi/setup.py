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