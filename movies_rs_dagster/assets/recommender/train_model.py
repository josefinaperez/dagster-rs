from dagster import asset, AssetIn, Int
import pandas as pd
from .model_helper import get_model
from keras.optimizers import Adam

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
    ins={
        "preprocess_data": AssetIn(
        # key_prefix=["snowflake", "core"],
        # metadata={"columns": ["id"]}
        ),
    },
    config_schema={
        'batch_size': Int,
        'epochs': Int,
    }
)
def train(context, preprocess_data):
    training_data, user2Idx, movie2Idx = preprocess_data
    model = get_model(len(movie2Idx), len(user2Idx), 5)
    model.compile(Adam(learning_rate=0.001), 'mean_squared_error')
    batch_size = context.op_config["batch_size"]
    epochs = context.op_config["epochs"]
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
    return model

