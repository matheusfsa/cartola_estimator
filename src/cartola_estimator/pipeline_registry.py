"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from cartola_estimator.pipelines import data_ingestion as ingestion
from cartola_estimator.pipelines import preprocessing as pp
from cartola_estimator.pipelines import data_science as ds


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    ingestion_pipeline = ingestion.create_pipeline()
    pp_pipeline = pp.create_pipeline()
    ds_pipeline = ds.create_pipeline()
    return {
        "ingestion": ingestion_pipeline,
        "pp": pp_pipeline,
        "ds": ds_pipeline,
        "__default__": ingestion_pipeline + pp_pipeline + ds_pipeline,
    }
