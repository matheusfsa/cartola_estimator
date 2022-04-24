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
from .nodes import split_x_y, join_models, model_selection


def training_template(name):
    return Pipeline(
        [

            node(
                func=split_x_y,
                inputs={
                    "data": "train_data",
                    "label": "params:label",
                    "stats_dict": "params:stats",
                },
                outputs=["X", "y"],
                name=f"split_x_y_{name}",
            ),
            node(
                func=model_selection,
                inputs={
                    "X": "X",
                    "y": "y",
                    "models_dict": "params:models",
                    "fold": "params:fold",
                    "columns_to_drop": "params:columns_to_drop"
                },
                outputs="model",
                name=f"fit_model_{name}",
            )
        ]
    )



def create_pipeline(**kwargs) -> Pipeline:
    session = _active_session.load_context()
    stats = session.catalog.load("params:stats")

    training_pipelines = [
        pipeline(
            pipe=training_template(statistic),
            parameters={"params:label": f"params:stats.{statistic}.id"},
            outputs={
                "X": f"X_{statistic}",
                "y": f"y_{statistic}",
                "model": f"model_{statistic}"
            },
        )
        for statistic in stats
    ]
    training_pipeline = reduce(add, training_pipelines)

    join_pipeline = Pipeline(
        [
            node(
                func=join_models,
                inputs=[
                    "params:stats",
                ]
                + [
                    f"model_{statistic}"
                    for statistic in stats
                ],
                outputs="cartola_estimator",
                name="join_models",
            )
        ]
    )
    return training_pipeline  + join_pipeline
