"""
This is a boilerplate pipeline 'prepare_for_dashboard'
generated using Kedro 0.19.3
"""

from kedro.pipeline import node, Pipeline, pipeline
from .nodes import (
    load_geographical_dataframe,
    convert_crs,
    get_representative_points,
    get_lon_lat,
    add_geographical_info_pickup,
    add_target_col,
    aggregate_by_location_hour,
    add_location_name,
    aggregate_by_location_dayofweek_hour,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_geographical_dataframe,
                inputs="params:path_shape_locations",
                outputs="gdf_shape_locations",
                name="Load_geo_dataframe"
            ),
            node(
                func=convert_crs,
                inputs="gdf_shape_locations",
                outputs="gdf_crs_changed",
                name="Change_crs_to_4326",
            ),
            node(
                func=get_representative_points,
                inputs="gdf_crs_changed",
                outputs="gdf_w_point",
                name="Add_representative_points_polygon"
            ),
            node(
                func=get_lon_lat,
                inputs="gdf_w_point",
                outputs="gdf_w_lon_lat",
                name="Add_longitude_and_latitude"
            ),
            node(
                func=add_target_col,
                inputs=["df_training", "y_training"],
                outputs="df_training_w_duration",
                name="Add_duration_to_dataset"
            ),
            node(
                func=aggregate_by_location_hour,
                inputs="df_training_w_duration",
                outputs="df_training_group_location_date",
                name="Aggregate_by_location_datetime"
            ),
            node(
                func=add_location_name,
                inputs=['df_training_group_location_date', 'gdf_w_lon_lat'],
                outputs='df_training_location_date_w_zone',
                name="Add_geographical_info"
            ),
            node(
                func=aggregate_by_location_dayofweek_hour,
                inputs="df_training_w_duration",
                outputs="df_training_location_day_hour",
                name="Aggregate_by_location_day_hour",
            ),
            node(
                func=add_geographical_info_pickup,
                inputs=['df_training_location_day_hour', 'gdf_w_lon_lat'],
                outputs='gdf_training_location_date_w_geo',
                name="Add_zone_name"
            )
        ],
        inputs=["df_training", "y_training"],
        outputs=["df_training_location_date_w_zone", "gdf_training_location_date_w_geo"],
        namespace="prepare_data_for_dashboard"
    )
