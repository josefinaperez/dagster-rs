# %%
import mlflow
logged_model = 'runs:/4bb3e68ee901429dab607d33edcc40d5/keras_dot_product_model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
# %%
# Predict on a Pandas DataFrame.
import numpy as np
loaded_model.predict([np.array([1, 2]), np.array([2, 3])])
# %%
