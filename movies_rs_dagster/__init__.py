from dagster import Definitions, define_asset_job, AssetSelection

from .assets import (
    core_assets, recommender_assets
)

all_assets = [*core_assets, *recommender_assets]

mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}
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
    selection=['movies', 'users', 'scores', 'training_data'],
    config=job_data_config
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        define_asset_job("full_process", config=job_all_config),
        define_asset_job(
            "only_training",
            # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ],
    # resources={'mlflow': mlflow_tracking},
    # schedules=[core_assets_schedule],
    # sensors=all_sensors,
)

