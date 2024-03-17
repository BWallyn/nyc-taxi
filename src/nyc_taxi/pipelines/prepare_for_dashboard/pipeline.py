"""
This is a boilerplate pipeline 'prepare_for_dashboard'
generated using Kedro 0.19.3
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import aggregate_specific_date, aggregate_by_day_hour


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=aggregate_by_day_hour,
            inputs=["df_training", "params:beg_specific_week"],
            outputs="df_training_group_dayofweek_hour",
            name="node_aggregate_dayofweek_hour_training"
        ),
    ])
