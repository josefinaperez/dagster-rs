# %%
# %%
from tensorflow.keras import layers
from tensorflow.keras import Model
# %%
def get_model(n_movies, n_users, n_latent_factors):
    movie_input = layers.Input(shape=[1], name='Item')
    user_input = layers.Input(shape=[1],name='User')
    
    movie_embedding = layers.Embedding(
        n_movies + 1, n_latent_factors, 
        mask_zero=True,
        name='Movie-Embedding'
    )(movie_input)
    movie_vec = layers.Flatten(name='FlattenMovies')(movie_embedding)

    user_embedding = layers.Embedding(
            n_users + 1,
            n_latent_factors,
            mask_zero=True,
            name='User-Embedding'
    )(user_input)
    user_vec = layers.Flatten(name='FlattenUsers')(user_embedding)

    prod = layers.Dot(axes=1, name='DotProduct')([movie_vec, user_vec])
    model = Model([user_input, movie_input], prod)
    return model
# %%

import pandas as pd
scores = pd.read_csv('https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv')
users = pd.read_csv('https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv')
movies = pd.read_csv('https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv')
# %%
scores_users = pd.merge(scores, users, left_on='user_id', right_on='id')
training_data = pd.merge(scores_users, movies, left_on='movie_id', right_on='id')
training_data
# %%

def preprocess_data(training_data):
    u_unique = training_data.user_id.unique()
    user2Idx = {o:i+1 for i,o in enumerate(u_unique)}

    m_unique = training_data.movie_id.unique()
    movie2Idx = {o:i+1 for i,o in enumerate(m_unique)}
    training_data['encoded_user_id'] = training_data.user_id.apply(lambda x: user2Idx[x])
    training_data['encoded_movie_id'] = training_data.movie_id.apply(lambda x: movie2Idx[x])
    return training_data, user2Idx, movie2Idx
# %%
training_data, user2Idx, movie2Idx = preprocess_data(training_data)
# %%
len(movie2Idx)
# %%
training_data.encoded_user_id
# %%
model = get_model(len(movie2Idx), len(user2Idx), 5)
# %%
model.summary()
# %%
from keras.optimizers import Adam

model.compile(Adam(learning_rate=0.001), 'mean_squared_error')
# %%
batch_size = 320
epochs = 10
history = model.fit(
    [
        training_data.encoded_user_id,
        training_data.encoded_movie_id], 
        training_data.rating, 
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating), 
        epochs=epochs, 
        verbose=1
    )
# %%
from matplotlib import pyplot as plt
fig, axs = plt.subplots(1)
axs.plot(history.history['loss'], label='mse')
plt.legend()
# mlflow.log_figure(fig, 'plots/loss.png')
# %%
fig
# %%

import mlflow
logged_model = 'models:/keras_dot_product_model-7'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
# %%
# Predict on a Pandas DataFrame.
import pandas as pd
loaded_model.predict(pd.DataFrame(data))