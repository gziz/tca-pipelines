from kedro.pipeline import Pipeline, node
from .nodes_upload import upload_reports_node


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=upload_reports_node,
                inputs=[
                    "cancellation_percentages",
                    "median_values",
                    "mean_values",
                    "agencia_distribution",
                    "canal_distribution",
                ],
                outputs=None,
                name="upload_reports_node",
            )
        ]
    )
