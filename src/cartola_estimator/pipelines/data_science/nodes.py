"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.0
"""
from typing import Any, Dict, List, Tuple
from numpy import isin
import pandas as pd
from sklearn.model_selection import BaseCrossValidator
from sklearn.base import BaseEstimator
from cartola_estimator.utils import import_class
from .models import CartolaEstimator


def split_x_y(
    data: pd.DataFrame, stats_dict: Dict[str, Any], id_cols: List[str], label: str
) -> Tuple[pd.DataFrame, pd.Series]:
    stats = [stat["id"] for k, stat in stats_dict.items()]
    y = data[label]
    X = data.drop(columns=stats + id_cols)
    return X, y


def fit_model(
    X: pd.DataFrame, y: pd.Series, model_dict: Dict[str, Any], fold: Dict[str, Any]
) -> pd.DataFrame:
    """This node fit a model"""
    X = X.fillna(0)
    y = y.fillna(0)
    model_class = import_class(model_dict["model_class"])
    default_args = model_dict["default_args"] or {}
    model = model_class(**default_args)

    cv = import_class(fold["class"])(**fold["kwargs"])

    search = _build_search(model_dict["params_search"], model, cv)
    search.fit(X, y)
    best_model = search.best_estimator_.fit(X, y)

    return best_model


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
