from dagster import graph
from dagster_gcp import bq_op_for_queries
from dagster_dbt import dbt_run_op
from dagster_airbyte import airbyte_sync_op



def get_fetch_data_graph(QUERY, AIRBYTE_CONNECTION_ID, TABLE_NAME):
    from dagster_data_flow.ops.fetch_data import delete_files_from_folder
    @graph(
        name=f'fetch_{TABLE_NAME}_data'
    )
    def fetch_data_graph():
        sync_entities_machine_learning = airbyte_sync_op.configured(
            {"connection_id": AIRBYTE_CONNECTION_ID}, name=f"MS_{TABLE_NAME}_to_BQ")
        airbyte_result = sync_entities_machine_learning()
        dbt_result = dbt_run_op.alias(f"CAST_{TABLE_NAME}_Tables")(airbyte_result)
        bq_op = bq_op_for_queries(
                [QUERY]
        ).configured({}, name=f"BQ_{TABLE_NAME}_to_GCS")
        delete_files_op = delete_files_from_folder.configured({"QUERY": QUERY}, name=f"DELETE_{TABLE_NAME}_FILES")
        return bq_op(delete_files_op(dbt_result))
    return fetch_data_graph

# from dagster import asset, Output, String, AssetIn, FreshnessPolicy
# from dagster_mlflow import mlflow_tracking

# # %%
# import pandas as pd

# # %%
# movies_categories_columns = [
#     'unknown', 'Action', 'Adventure', 'Animation',
#     "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
#     'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
#     'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']



# @asset(
#     freshness_policy=FreshnessPolicy(maximum_lag_minutes=5),
#     # group_name='csv_data',
#     code_version="2",
#     config_schema={
#         'uri': String
#     },
# )
# def movies(context) -> Output[pd.DataFrame]:
  
#     uri = context.op_config["uri"]
#     result = pd.read_csv(uri)
#     return Output(
#         result,
#         metadata={
#             #"Total rows": len(result),
#             #**result[movies_categories_columns].sum().to_dict(),
#             #"preview": MetadataValue.md(result.head().to_markdown()),
#         },
#     )


# # @asset(
# #     # group_name='csv_data',
# #     # io_manager_key="parquet_io_manager",
# #     # partitions_def=hourly_partitions,
# #     # key_prefix=["s3", "core"],
# #     # config_schema={
# #     #     'uri': String
# #     # }
# # )
# # def users() -> Output[pd.DataFrame]:
# #     uri = 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv'
# #     result = pd.read_csv(uri)
# #     return Output(
# #         result,
# #         metadata={
# #             "Total rows": len(result),
# #             **result.groupby('Occupation').count()['id'].to_dict()
# #         },
# #     )


# # @asset(
# #     resource_defs={'mlflow': mlflow_tracking}
# #     # io_manager_key="parquet_io_manager",
# #     # partitions_def=hourly_partitions,
# #     # key_prefix=["s3", "core"],
# #     # config_schema={
# #     #     'uri': String
# #     # }
# # )
# # def scores(context) -> Output[pd.DataFrame]:
# #     mlflow = context.resources.mlflow
# #     uri = 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv'
# #     result = pd.read_csv(uri)
# #     metrics = {
# #         "Total rows": len(result),
# #         #"scores_mean": result['rating'].mean(),
# #         #"scores_std": result['rating'].std(),
# #         "unique_movies": len(result['movie_id'].unique()),
# #         "unique_users": len(result['user_id'].unique())
# #     }
# #     mlflow.log_metrics(metrics)

# #     return Output(
# #         result,
# #         metadata=metrics,
# #     )

# # @asset(ins={
# #     "scores": AssetIn(
# #         # key_prefix=["snowflake", "core"],
# #         # metadata={"columns": ["id"]}
# #     ),
# #     "movies": AssetIn(
# #         # key_prefix=["snowflake", "core"],
# #         # metadata={"columns": ["id"]}
# #     ),
# #     "users": AssetIn(
# #         # key_prefix=["snowflake", "core"],
# #         # metadata={"columns": ["id", "user_id", "parent"]}
# #     ),
# # })
# # def training_data(users: pd.DataFrame, movies: pd.DataFrame, scores: pd.DataFrame) -> Output[pd.DataFrame]:
# #     scores_users = pd.merge(scores, users, left_on='user_id', right_on='id')
# #     all_joined = pd.merge(scores_users, movies, left_on='movie_id', right_on='id')

# #     return Output(
# #         all_joined,
# #         metadata={
# #             "Total rows": len(all_joined),
# #         },
# #     )
