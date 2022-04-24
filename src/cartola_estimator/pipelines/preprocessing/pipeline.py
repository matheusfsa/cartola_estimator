"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import add_match_info, create_target_data, create_hist_features, split_test


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=add_match_info,
                inputs={"cartola_data": "cartola_raw_data", "cb_data": "cb_data"},
                outputs="cartola_hist_data",
                name="add_match_info",
            ),
            node(
                func=create_target_data,
                inputs={"data": "cartola_hist_data", "stats_dict": "params:stats"},
                outputs="cartola_data",
                name="create_target_data",
            ),
            node(
                func=create_hist_features,
                inputs={
                    "data": "cartola_data",
                    "stats_dict": "params:stats",
                    "window": "params:window",
                    "columns": "params:feature_columns",
                    "id_cols": "params:id_columns",
                },
                outputs="feature_data",
                name="create_hist_features",
            ),
            node(
                func=split_test,
                inputs={
                    "data": "feature_data",
                    "test_size": "params:test_size",
                    "random_seed": "params:random_seed",
                },
                outputs=["train_data", "test_data"],
                name="split_test",
            ),
        ]
    )
