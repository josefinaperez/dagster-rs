# Creo estructura de carpetas
```bash
dagster project scaffold --name movies_rs
```
# Instalación de dependencias y creación de paquete
```bash
pip install -e ".[dev]"

```
# Correr dagster en modo development
```bash
dagster dev
```

# Archivos `__init__.py`

En la raiz:

```python 
# Importo assets
from dagster import Definitions, define_asset_job
from .assets import (
    core_assets, recommender_assets
)

all_assets = [*core_assets, *recommender_assets]

# Configuraciones de jobs (Podria ir aparte y la importo)
job_configs = {
    'resources': {
        'mlflow': {
            'config': {
                'experiment_name': 'recommender_system',
            }            
        },
    },
    'ops': {
        'movies': {
            'config': {
                'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
                }
        },
        'keras_dot_product_model': {'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }}
    }
}

# Definiciones
defs = Definitions(
    assets=all_assets,
    jobs=[define_asset_job("train_full_model", config=job_configs)],
    resources={'mlflow': mlflow_tracking},
    schedules=[core_assets_schedule],
    sensors=all_sensors,
)
```

En la carpeta assets:
```python
from dagster import load_assets_from_package_module
from . import core
from . import recommender

core_assets = load_assets_from_package_module(package_module=core, group_name='core')
recommender_assets = load_assets_from_package_module(package_module=recommender, group_name='recommender')
```

Recordar agregar los archivos `__init__.py` en todas las carpetas que quiero que formen parte del paquete