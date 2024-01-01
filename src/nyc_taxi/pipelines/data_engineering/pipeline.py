"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import download_between_dates, split_train_val_test, create_duration


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=download_between_dates,
            inputs=["params:path_tlc", "params:date_start", "params:date_end"],
            outputs="merged_data",
            name="node_download_data",
        ),
        node(
            func=split_train_val_test,
            inputs=["merged_data", "params:date_valid_str", "params:date_test_str"],
            outputs=["train_split", "valid_split", "test_split"],
            name="node_split_dataset"
        ),
        node(
            func=create_duration,
            inputs=["train_split"],
            outputs="df_train",
            name="node_target_train",
        ),
        node(
            func=create_duration,
            inputs=["valid_split"],
            outputs="df_valid",
            name="node_target_valid",
        ),
        node(
            func=create_duration,
            inputs=["test_split"],
            outputs="df_test",
            name="node_target_test",
        )
    ])
