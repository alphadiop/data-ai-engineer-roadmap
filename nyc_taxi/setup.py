from setuptools import setup, find_packages

# Packages Python situés dans src/
src_packages = find_packages("src")

# Packages exposés dans le wheel sous nyc_taxi.*
mapped_packages = [
                      "nyc_taxi.src",
                      "nyc_taxi.config",
                  ] + [
                      f"nyc_taxi.src.{package}"
                      for package in src_packages
                  ]

package_dir = {
    "nyc_taxi.src": "src",
    "nyc_taxi.config": "config",
}

for package in src_packages:
    package_dir[
        f"nyc_taxi.src.{package}"
    ] = f"src/{package.replace('.', '/')}"

setup(
    name="nyc_taxi",
    version="1.0.0",

    packages=mapped_packages,

    package_dir=package_dir,

    package_data={
        "nyc_taxi.config": [
            "*.yaml",
        ],
    },

    entry_points={
        "console_scripts": [
            "nyc-taxi-pipeline=nyc_taxi.src.jobs.run_pipeline:main"
        ]
    },
)