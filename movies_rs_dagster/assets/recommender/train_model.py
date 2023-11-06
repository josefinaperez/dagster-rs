from dagster import asset, AssetIn, Int, Float
import pandas as pd
from dagster_mlflow import mlflow_tracking

@asset(
    ins={
        "training_data": AssetIn(
        # key_prefix=["snowflake", "core"],
        # metadata={"columns": ["id"]}
        ),
    }
)
def preprocess_data(training_data: pd.DataFrame):
    u_unique = training_data.user_id.unique()
    user2Idx = {o:i+1 for i,o in enumerate(u_unique)}

    m_unique = training_data.movie_id.unique()
    movie2Idx = {o:i+1 for i,o in enumerate(m_unique)}
    training_data['encoded_user_id'] = training_data.user_id.apply(lambda x: user2Idx[x])
    training_data['encoded_movie_id'] = training_data.movie_id.apply(lambda x: movie2Idx[x])
    return training_data, user2Idx, movie2Idx


@asset(
    resource_defs={'mlflow': mlflow_tracking},
    ins={
        "preprocess_data": AssetIn(
        # key_prefix=["snowflake", "core"],
        # metadata={"columns": ["id"]}
        ),
    },
    config_schema={
        'batch_size': Int,
        'epochs': Int,
        'learning_rate': Float,
        'embeddings_dim': Int
    }
)
def keras_dot_product_model(context, preprocess_data):
    from .model_helper import get_model
    from keras.optimizers import Adam
    mlflow = context.resources.mlflow
    mlflow.log_params(context.op_config)

    training_data, user2Idx, movie2Idx = preprocess_data
    
    batch_size = context.op_config["batch_size"]
    epochs = context.op_config["epochs"]
    learning_rate = context.op_config["learning_rate"]
    embeddings_dim = context.op_config["embeddings_dim"]

    model = get_model(len(movie2Idx), len(user2Idx), embeddings_dim)

    model.compile(Adam(learning_rate=learning_rate), 'mean_squared_error')
    
    context.log.info(f'batch_size: {batch_size} - epochs: {epochs}')
    history = model.fit(
        [
            training_data.encoded_user_id,
            training_data.encoded_movie_id
        ], 
        training_data.rating, 
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating), 
        epochs=epochs, 
        verbose=1
    )
    for i, l in enumerate(history.history['loss']):
        mlflow.log_metric('mse', l, i)
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(1)
    axs.plot(history.history['loss'], label='mse')
    plt.legend()
    mlflow.log_figure(fig, 'plots/loss.png')
    return model

@asset(
    resource_defs={'mlflow': mlflow_tracking},
    ins={
        "keras_dot_product_model": AssetIn(),
    },
)
def log_model(context, keras_dot_product_model):
    import numpy as np
    mlflow = context.resources.mlflow
    
    mlflow.tensorflow.log_model(
        keras_dot_product_model,
        "keras_dot_product_model",
        registered_model_name='keras_dot_product_model',
        input_example=[np.array([1, 2]), np.array([2, 3])],
    )
    