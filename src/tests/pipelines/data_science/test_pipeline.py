"""
This is a boilerplate test file for pipeline 'data_science'
generated using Kedro 0.18.0.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
from cartola_estimator.pipelines.data_science.nodes import (split_x_y, model_selection)
from sklearn.pipeline import Pipeline

def test_split_x_y(train_data, stats_dict):
    X, y = split_x_y(train_data, stats_dict, label="G")
    assert "G" not in X.columns
    assert "A" not in X.columns
    assert y.name == "G"
    assert X.columns.isin(train_data.drop(columns=["G", "A"]).columns).all()

def test_model_selection(X_train, y_train, models_dict, cv, columns_to_drop):
    res = model_selection(X_train, y_train, models_dict, cv, columns_to_drop)
    assert isinstance(res, Pipeline)