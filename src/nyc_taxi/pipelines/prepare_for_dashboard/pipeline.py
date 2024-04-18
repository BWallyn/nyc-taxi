"""
This is a boilerplate pipeline 'prepare_for_dashboard'
generated using Kedro 0.19.3
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import (
    aggregate_by_day_hour,
    load_geographical_dataframe,
    add_geographical_info_pickup
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=aggregate_by_day_hour,
            inputs=["df_training", "params:beg_specific_week"],
            outputs="df_training_group_dayofweek_hour",
            name="node_aggregate_dayofweek_hour_training"
        ),
        node(
            func=load_geographical_dataframe,
            inputs="params:path_shape_locations",
            outputs="gdf_shape_locations",
            name="node_load_geo_dataframe"
        ),
        node(
            func=add_geographical_info_pickup,
            inputs=["df_training_group_dayofweek_hour", "gdf_shape_locations"],
            outputs="df_training_with_geo_info",
            name="node_add_geographical_info"
        )
    ])
