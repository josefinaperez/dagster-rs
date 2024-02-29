from dagster_airbyte import load_assets_from_airbyte_instance, AirbyteResource, build_airbyte_assets

# airbyte_assets = load_assets_from_airbyte_project(
#     project_dir="/Users/josefinaperez/Desktop/MLOPS/TP/mlops-ecosystem/airbyte",
# )

# airbyte_instance = airbyte_resource.configured(
#     {
#         "host": "localhost",
#         "port": "8000",
#         "username":"airbyte",
#         "password":"password",
#     }
# )

airbyte_instance = AirbyteResource(
     host="localhost",
     port="8000",
     username="airbyte",
     password="password",
 )

airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance,  key_prefix = ["recommender_system_raw"], connection_to_group_fn=None)

# airbyte_movies_asset = build_airbyte_assets(
#     connection_id="0d9571b6-27b1-4781-8b12-108127c81402",
#     destination_tables=["movies"],
#     asset_key_prefix=["airbyte_assets"],
# )

# airbyte_scores_asset = build_airbyte_assets(
#     connection_id="34c12d4c-a80f-4f86-b7b5-a90288124c03",
#     destination_tables=["scores"],
#     asset_key_prefix=["airbyte_assets"],
# )


# airbyte_users_asset = build_airbyte_assets(
#     connection_id="f820be7a-16a1-48a0-bdb9-65eb215b5f68",
#     destination_tables=["users"],
#     asset_key_prefix=["airbyte_assets"],
# )

# airbyte_assets = [airbyte_movies_asset, airbyte_scores_asset, airbyte_users_asset]
