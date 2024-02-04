from dagster import Definitions, define_asset_job, AssetSelection, ScheduleDefinition, FilesystemIOManager
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project


from .assets import (
    core_assets, recommender_assets
)



mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}

dbt_resources = DbtCliResource(project_dir="/Users/josefinaperez/Desktop/MLOPS/TP/mlops-ecosystem/db_postgres",
                               profiles_dir="/Users/josefinaperez/.dbt/")

dbt_assets = load_assets_from_dbt_project("/Users/josefinaperez/Desktop/MLOPS/TP/mlops-ecosystem/db_postgres",
                                          "/Users/josefinaperez/.dbt/", key_prefix = ["dbt_assets"])

#all_assets = [*core_assets, *recommender_assets, *dbt_assets]
all_assets = [*core_assets, *dbt_assets]


data_ops_config = {
    'movies': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
            }
    }
}

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
    },
    'ops': {
        **data_ops_config,
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
        **data_ops_config,
        **training_config
    }
}

get_data_job = define_asset_job(
    name='get_data',
    selection=['dbt_assets/movies', 'dbt_assets/users', 'dbt_assets/scores', 'dbt_assets/scores_movies_users'],
    #config=job_data_config
)

get_data_schedule = ScheduleDefinition(
    job=get_data_job,
    cron_schedule="0 * * * *",  # every hour
)

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        #define_asset_job("full_process", config=job_all_config),
        # define_asset_job(
        #     "only_training",
        #     # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
        #     selection=AssetSelection.groups('recommender'),
        #     config=job_training_config
        # )
    ],
    resources={
        # 'mlflow': mlflow_tracking
        "io_manager": io_manager,
        "dbt": dbt_resources
    },
    schedules=[get_data_schedule],
    # sensors=all_sensors,
)
