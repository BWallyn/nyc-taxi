"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import compute_metrics, plot_histograms


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=compute_metrics,
            inputs=['y_training', 'pred_training', 'y_test', 'pred_test'],
            outputs='dict_metrics',
            name='node_metrics',
        ),
        node(
            func=plot_histograms,
            inputs=['y_test', 'pred_test'],
            outputs=None,
            name='node_plot_histograms_test',
        )
    ])
