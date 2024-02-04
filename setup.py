import setuptools
import os
DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.6.3')
DAGSTER_AIRBYTE_VERSION=os.getenv('DAGSTER_AIRBYTE_VERSION', '1.5.6')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.22.3')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.10.0')

setuptools.setup(
    name="movies-rs-dagster",
    packages=setuptools.find_packages(),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        f"dagit=={DAGSTER_VERSION}",
        f"dagster-gcp=={DAGSTER_LIBS_VERSION}",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"dagster-dbt=={DAGSTER_LIBS_VERSION}",
        f"dagster-airbyte=={DAGSTER_LIBS_VERSION}",
        f"mlflow=={MLFLOW_VERSION}",
        f"tensorflow",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "jupyter", "dagster-airbyte",
                            "dagster-dbt"], "tests": ["mypy", "pylint", "pytest"]},
)


