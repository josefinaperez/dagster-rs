from dagster import asset, Output, String
# %%
import pandas as pd
# result = pd.read_csv('https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv')

# %%
columns = [
    'unknown', 'Action', 'Adventure', 'Animation',
    "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
    'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# %%
uri = 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
@asset(
    # io_manager_key="parquet_io_manager",
    # partitions_def=hourly_partitions,
    # key_prefix=["s3", "core"],
    config_schema={
        'uri': String
    }
)
def movies(context) -> Output[pd.DataFrame]:
    uri = context.op_config["uri"]
    result = pd.read_csv(uri)
    result.isna().sum()
    return Output(
        result,
        metadata={
            "Total rows": len(result),
            **result[columns].sum().to_dict()
        },
    )

