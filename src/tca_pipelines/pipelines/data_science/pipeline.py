from kedro.pipeline import Pipeline, node
from .nodes_clustering import perform_clustering
from .nodes_generate_statistics import generate_statistics
from .nodes_distribute_data import distribute_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=perform_clustering,
                inputs="preprocessed_data",
                outputs="clustered_data",
                name="perform_clustering_node",
            ),
            node(
                func=generate_statistics,
                inputs="clustered_data",
                outputs=["cancellation_percentages", "median_values", "mean_values"],
                name="generate_statistics_node",
            ),
            node(
                func=distribute_data,
                inputs=["clustered_data", "iar_agencias", "iar_canales"],
                outputs=["agencia_distribution", "canal_distribution"],
                name="distribute_data_node",
            ),
        ]
    )
