"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import load_cartola_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_cartola_data,
                inputs={
                    "years": "params:years",
                },
                outputs="cartola_raw_data",
                name="load_cartola_data",
            )
        ]
    )
