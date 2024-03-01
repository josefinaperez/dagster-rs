from dagster import Definitions, define_asset_job, ScheduleDefinition, FilesystemIOManager, AssetSelection
from dagster_dbt import DbtCliResource
from dagster_airbyte import AirbyteResource


from .assets import (
    dbt_assets, airbyte_assets, recommender_assets
)


mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
            'mlflow_tracking_uri': 'http://localhost:8002'
        }            
    },
}


dbt_resources = DbtCliResource(project_dir="/Users/josefinaperez/Desktop/MLOPS/TP/mlops-ecosystem/db_postgres",
                               profiles_dir="/Users/josefinaperez/.dbt/")

all_assets = [*airbyte_assets, *dbt_assets, *recommender_assets]


training_config = {
    'keras_dot_product_model': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_data_config = {
    'resources': {
        **mlflow_resources
    }
}

job_training_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}

job_all_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}

get_data_job = define_asset_job(
    name='get_data',
    selection=['recommender_system_raw/movies',
               'recommender_system_raw/users',
               'recommender_system_raw/scores',
               'dbt_assets/movies',
               'dbt_assets/users',
               'dbt_assets/scores',
               'dbt_assets/scores_movies_users']
)

get_data_schedule = ScheduleDefinition(
    job=get_data_job,
    cron_schedule="0 * * * *",  # every hour
)

full_process_job = define_asset_job(
    name='full_process',
    selection=AssetSelection.all(),
    config=job_all_config
)


io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

airbyte_resource = AirbyteResource(
    host="localhost",
    port="8000",
    username="airbyte",
    password="password",
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        full_process_job
    ],
    resources={
        "io_manager": io_manager,
        "dbt": dbt_resources,
    },
    schedules=[get_data_schedule],
    # sensors=all_sensors,
)
