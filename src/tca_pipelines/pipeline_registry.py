from kedro.pipeline import Pipeline
from tca_pipelines.pipelines.data_engineering import pipeline as de
from tca_pipelines.pipelines.data_science import pipeline as ds
from tca_pipelines.pipelines.azure import pipeline as azure

def register_pipelines() -> dict[str, Pipeline]:
    de_pipeline = de.create_pipeline()
    ds_pipeline = ds.create_pipeline()
    azure_pipeline = azure.create_pipeline()
    return {
        "__default__": de_pipeline + ds_pipeline + azure_pipeline,
        "de": de_pipeline,
        "ds": ds_pipeline,
        "azure": azure_pipeline,
    }
