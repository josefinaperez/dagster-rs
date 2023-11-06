from dagster import Definitions, define_asset_job

from .assets import (
    core_assets, recommender_assets
)

all_assets = [*core_assets, *recommender_assets]

job_configs = {
    'resources': {
        'mlflow': {
            'config': {
                'experiment_name': 'recommender_system',
            }            
        },
    },
    'ops': {
        'movies': {
            'config': {
                'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
                }
        },
        'keras_dot_product_model': {'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }}
    }
}


defs = Definitions(
    assets=all_assets,
    jobs=[define_asset_job("train_full_model", config=job_configs)],
    # resources={'mlflow': mlflow_tracking},
    # schedules=[core_assets_schedule],
    # sensors=all_sensors,
)



# import os



# from .assets import (
#     activity_analytics_assets,
#     core_assets,
#     hacker_news_dbt_assets,
#     recommender_assets,
# )
# from .jobs import (
#     activity_analytics_assets_sensor,
#     core_assets_schedule,
#     recommender_assets_sensor,
# )
# from .resources import RESOURCES_LOCAL, RESOURCES_PROD, RESOURCES_STAGING
# from .sensors import make_slack_on_failure_sensor

# all_assets = [
#     *core_assets,
#     *recommender_assets,
#     hacker_news_dbt_assets,
#     *activity_analytics_assets,
# ]

# resources_by_deployment_name = {
#     "prod": RESOURCES_PROD,
#     "staging": RESOURCES_STAGING,
#     "local": RESOURCES_LOCAL,
# }

# deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")

# all_sensors = [activity_analytics_assets_sensor, recommender_assets_sensor]
# if deployment_name in ["prod", "staging"]:
#     all_sensors.append(make_slack_on_failure_sensor(base_url="my_webserver_url"))

# defs = Definitions(
#     assets=all_assets,
#     resources=resources_by_deployment_name[deployment_name],
#     schedules=[core_assets_schedule],
#     sensors=all_sensors,
# )
