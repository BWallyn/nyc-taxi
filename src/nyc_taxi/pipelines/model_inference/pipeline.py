"""
This is a boilerplate pipeline 'model_inference'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import model_predict


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=model_predict,
            inputs=["df_training", "model_trained"],
            outputs="pred_training",
            name="node_model_predict_training",
        ),
        node(
            func=model_predict,
            inputs=["df_test_hour", "model_trained"],
            outputs="pred_test",
            name="node_model_predict_test",
        ),
    ])
