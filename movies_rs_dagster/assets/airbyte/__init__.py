from dagster_airbyte import load_assets_from_airbyte_instance, AirbyteResource, build_airbyte_assets


airbyte_instance = AirbyteResource(
     host="localhost",
     port="8000",
     username="airbyte",
     password="password",
 )

airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance,  key_prefix = ["recommender_system_raw"], connection_to_group_fn=None)

