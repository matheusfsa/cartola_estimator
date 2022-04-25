"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.0
"""
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd

from sklearn.model_selection import BaseCrossValidator, train_test_split
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error

from cartola_estimator.utils import import_class
from .models import CartolaEstimator
from .transformers import DropColumns



def split_x_y(
    data: pd.DataFrame, stats_dict: Dict[str, Any], label: str
) -> Tuple[pd.DataFrame, pd.Series]:
    stats = [stat["id"] for k, stat in stats_dict.items()]
    y = data[label].fillna(0)
    X = data.drop(columns=stats)
    return X, y

def split_train_val(data, test_size):
    train, val = train_test_split(data, test_size=test_size)
    return train, val

def model_selection(
    X: pd.DataFrame,
    y: pd.Series,
    models_dict: Dict[str, Any],
    fold: Dict[str, Any],
    columns_to_drop: List[str]
):
    """This node select the best model"""
    models = []
    for _, model_dict in models_dict.items():
        best_model, best_score = fit_model(X, y, model_dict, fold, columns_to_drop)
        models.append((best_model, best_score))

    models.sort(key=lambda tup: tup[1])
    return models[0][0]

def fit_model(
    X: pd.DataFrame,
    y: pd.Series,
    model_dict: Dict[str, Any],
    fold: Dict[str, Any],
    columns_to_drop: List[str]
) -> pd.DataFrame:
    """This node fit a model"""

    model_class = import_class(model_dict["model_class"])
    default_args = model_dict["default_args"] or {}
    estimator = model_class(**default_args)
    model = _build_pipeline(estimator, columns_to_drop)

    cv = import_class(fold["class"])(**fold["kwargs"])

    search = _build_search(model_dict["params_search"], model, cv)
    search.fit(X, y)
    best_model = search.best_estimator_.fit(X, y)
    return best_model, search.best_score_


def _build_pipeline(estimator, columns_to_drop):
    numeric_pipeline = Pipeline(
        [
            ("inputer", SimpleImputer(strategy="median")),
        ]
    )
    cat_pipeline = Pipeline(
        [
            ("ohe", OneHotEncoder()),
        ]
    )
    ct = ColumnTransformer([
          ('num', numeric_pipeline, make_column_selector(dtype_include=np.number)),
          ('cat', cat_pipeline, make_column_selector(dtype_include=object))])

    steps = [
        ("drop_columns", DropColumns(columns_to_drop)),
        ("ct", ct),
        ("estimator", estimator),
    ]

    return Pipeline(steps)

def _build_search(
    search_dict: Dict[str, Any], model: BaseEstimator, cv: BaseCrossValidator
):
    search_class = import_class(search_dict["class"])
    params = {}
    for p_name, p_value in search_dict["params"].items():
        if isinstance(p_value, dict):
            params[p_name] = import_class(p_value["class"])(**p_value["kwargs"])
        else:
            params[p_name] = p_value
    search = search_class(model, params, cv=cv, **search_dict["kwargs"])
    return search


def join_models(stats_dict: Dict[str, Any], *models):
    stats = [stat["id"] for k, stat in stats_dict.items()]
    estimators = {}
    for stat, model in zip(stats, models):
        estimators[stat] = model
    return CartolaEstimator(**estimators)

def evaluate_cartola_estimator(
    val_data: pd.DataFrame,
    cartola_estimator: CartolaEstimator,
    stats_dict: Dict[str, Any]):
    stats = [stat["id"] for k, stat in stats_dict.items()]
    X = val_data.drop(columns=stats)
    y_stats = val_data[stats]
    y_stats_pred = cartola_estimator.predict(X)
    metrics = {}
    for statistic in stats:
        y_true = y_stats[statistic]
        y_pred = y_stats_pred[statistic]

        y_pred = y_pred[~y_true.isna()]
        y_true = y_true[~y_true.isna()]


        error = mean_squared_error(y_true, y_pred)
        metrics[statistic] = {"step": 1, "value": error}
    return metrics
