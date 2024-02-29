from dagster import load_assets_from_package_module

from . import recommender
from . import dbt
from . import airbyte


recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)

dbt_assets = load_assets_from_package_module(
    package_module=dbt, group_name='dbt'
)

airbyte_assets = load_assets_from_package_module(
    package_module=airbyte, group_name='recommender_system_raw'
)