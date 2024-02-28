from dagster_dbt import load_assets_from_dbt_project


dbt_assets = load_assets_from_dbt_project("/Users/josefinaperez/Desktop/MLOPS/TP/mlops-ecosystem/db_postgres",
                                          "/Users/josefinaperez/.dbt/", key_prefix = ["dbt_assets"])

