from dagster import asset, Output, String, AssetIn, FreshnessPolicy
from dagster_mlflow import mlflow_tracking

# %%
import pandas as pd

# %%
movies_categories_columns = [
    'unknown', 'Action', 'Adventure', 'Animation',
    "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
    'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# %%
# @dbt_asset
# def movies(context):
#     result = dbt_cli_run(context, selector="movies")
#     return result

@asset(
    freshness_policy=FreshnessPolicy(maximum_lag_minutes=5),
    # group_name='csv_data',
    code_version="2",
    config_schema={
        'uri': String
    },
)
def movies(context) -> Output[pd.DataFrame]:
  
    uri = context.op_config["uri"]
    result = pd.read_csv(uri)
    return Output(
        result,
        metadata={
            #"Total rows": len(result),
            #**result[movies_categories_columns].sum().to_dict(),
            #"preview": MetadataValue.md(result.head().to_markdown()),
        },
    )


# @asset(
#     # group_name='csv_data',
#     # io_manager_key="parquet_io_manager",
#     # partitions_def=hourly_partitions,
#     # key_prefix=["s3", "core"],
#     # config_schema={
#     #     'uri': String
#     # }
# )
# def users() -> Output[pd.DataFrame]:
#     uri = 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv'
#     result = pd.read_csv(uri)
#     return Output(
#         result,
#         metadata={
#             "Total rows": len(result),
#             **result.groupby('Occupation').count()['id'].to_dict()
#         },
#     )


# @asset(
#     resource_defs={'mlflow': mlflow_tracking}
#     # io_manager_key="parquet_io_manager",
#     # partitions_def=hourly_partitions,
#     # key_prefix=["s3", "core"],
#     # config_schema={
#     #     'uri': String
#     # }
# )
# def scores(context) -> Output[pd.DataFrame]:
#     mlflow = context.resources.mlflow
#     uri = 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv'
#     result = pd.read_csv(uri)
#     metrics = {
#         "Total rows": len(result),
#         #"scores_mean": result['rating'].mean(),
#         #"scores_std": result['rating'].std(),
#         "unique_movies": len(result['movie_id'].unique()),
#         "unique_users": len(result['user_id'].unique())
#     }
#     mlflow.log_metrics(metrics)

#     return Output(
#         result,
#         metadata=metrics,
#     )

# @asset(ins={
#     "scores": AssetIn(
#         # key_prefix=["snowflake", "core"],
#         # metadata={"columns": ["id"]}
#     ),
#     "movies": AssetIn(
#         # key_prefix=["snowflake", "core"],
#         # metadata={"columns": ["id"]}
#     ),
#     "users": AssetIn(
#         # key_prefix=["snowflake", "core"],
#         # metadata={"columns": ["id", "user_id", "parent"]}
#     ),
# })
# def training_data(users: pd.DataFrame, movies: pd.DataFrame, scores: pd.DataFrame) -> Output[pd.DataFrame]:
#     scores_users = pd.merge(scores, users, left_on='user_id', right_on='id')
#     all_joined = pd.merge(scores_users, movies, left_on='movie_id', right_on='id')

#     return Output(
#         all_joined,
#         metadata={
#             "Total rows": len(all_joined),
#         },
#     )
