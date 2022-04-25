from fake_dataset.columns import FloatRandomColumn, IntegerRandomColumn, CategoricalRandomColumn
from fake_dataset.generators import DataGenerator
import pytest
import numpy as np
import pandas as pd

@pytest.fixture(scope="module")
def stats_dict():
    return {
        "assistencias": {"id": "A", "pos": ["mei", "ata"]},
        "gols": {"id": "G", "pos": ["mei", "ata"]},
    }

@pytest.fixture(scope="module")
def train_data():
    data_columns = {
        "id": IntegerRandomColumn(values_range=(1, 100)),
        "time_idx": IntegerRandomColumn(values_range=(1, 120)),
        "pos": CategoricalRandomColumn(categories=["gol", "lat", "zag", "mei", "ata"], missing_rate=(0.0, 0.0)),
    }
    for statistic in ["G", "A"]:
        data_columns[f"{statistic}_oponente"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
        data_columns[f"{statistic}_pos"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
        data_columns[f"{statistic}_clube"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
        data_columns[statistic] = FloatRandomColumn(values_range=(0, 5),  missing_rate=(0.0, 0.1))
    data_gen =  DataGenerator(**data_columns)
    return data_gen.sample(100)

@pytest.fixture(scope="module")
def X_train():
    data_columns = {
        "id": IntegerRandomColumn(values_range=(1, 100)),
        "time_idx": IntegerRandomColumn(values_range=(1, 120)),
        "pos": CategoricalRandomColumn(categories=["gol", "lat", "zag", "mei", "ata"], missing_rate=(0.0, 0.0)),
    }
    for statistic in ["G", "A"]:
        data_columns[f"{statistic}_oponente"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
        data_columns[f"{statistic}_pos"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
        data_columns[f"{statistic}_clube"] = FloatRandomColumn(values_range=(0, 5), missing_rate=(0.0, 0.2))
    data_gen =  DataGenerator(**data_columns)
    return data_gen.sample(100)

@pytest.fixture(scope="module")
def y_train():
    return pd.Series(np.random.randn(100))

@pytest.fixture(scope="module")
def columns_to_drop():
    return ["id", "time_idx", "pos"]

@pytest.fixture(scope="module")
def cv():
    return {'class': 'sklearn.model_selection.KFold', 'kwargs': {'n_splits': 2}}

@pytest.fixture(scope="module")
def models_dict():
    models = {'ridge':
                {'model_class': 'sklearn.linear_model.Ridge',
                 'default_args': None,
                 'params_search': {'class': 'sklearn.model_selection.RandomizedSearchCV',
                 'kwargs':
                    {'n_iter': 2},
                 'params':
                 {'estimator__alpha':
                    {'class': 'scipy.stats.loguniform',
                    'kwargs':
                        {'a': 0.05, 'b': 10.0}}}}},
             'lasso':
                {'model_class': 'sklearn.linear_model.Lasso',
                 'default_args': None,
                 'params_search': {'class': 'sklearn.model_selection.RandomizedSearchCV',
                 'kwargs':
                    {'n_iter': 2},
                 'params':
                 {'estimator__alpha':
                    {'class': 'scipy.stats.loguniform',
                    'kwargs':
                        {'a': 0.05, 'b': 10.0}}}}},
            }
    return models
