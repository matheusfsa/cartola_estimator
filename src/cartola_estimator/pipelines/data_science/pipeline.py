"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.0
"""

from functools import reduce
from operator import add
from itertools import product

from kedro.pipeline import Pipeline, node
from kedro.framework.session.session import _active_session
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import split_x_y, fit_model, join_models

def split_template(name):
    return Pipeline(
        [
            node(
                func=split_x_y,
                inputs={
                    "data": "train_data",
                    "label": "params:label",
                    "stats_dict": "params:stats",
                    "id_cols": "params:id_columns"
                },
                outputs=["X", "y"],
                name=f"split_x_y_{name}"

            )
        ]
    )

def fit_template(name):
    return Pipeline(
        [
            node(
                func=fit_model,
                inputs={
                    "X": "X",
                    "y": "y",
                    "model_dict": "params:models",
                    "fold": "params:fold",
                },
                outputs="model",
                name=f"fit_model_{name}"

            )
        ]
    )
def create_pipeline(**kwargs) -> Pipeline:
    session = _active_session.load_context()
    stats = session.catalog.load("params:stats")
    models = session.catalog.load("params:models")

    split_pipelines = [
        pipeline(
            pipe=split_template(statistic),
            parameters={"params:label": f"params:stats.{statistic}.id"},
            outputs={"X": f"X_{statistic}", "y": f"y_{statistic}", }
        )
        for statistic in stats
    ]
    split_pipeline = reduce(add, split_pipelines)

    fit_pipelines = [
        pipeline(
            pipe=fit_template(f"{statistic}_{model}"),
            inputs={
                "X": f"X_{statistic}",
                "y": f"y_{statistic}",
                },
            parameters={"params:models": f"params:models.{model}"},
            outputs={"model": f"model_{statistic}_{model}"}
        )
        for statistic, model in product(stats, models)
    ]
    fit_pipeline = reduce(add, fit_pipelines)

    join_pipeline = Pipeline(
        [
            node(
                func=join_models,
                inputs=["params:stats",] + [f"model_{statistic}_{model}" for statistic, model in product(stats, models)],
                outputs="cartola_estimator",
                name="join_models"
            )
        ]
    )
    return split_pipeline + fit_pipeline + join_pipeline
