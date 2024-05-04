"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from .feature_engineering import create_hour_feat
from .nodes import merge_airport_fee, column_transformer, feature_imputer, pipe_estimator, create_training_set, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=merge_airport_fee,
                inputs="df_train",
                outputs="df_train_airport",
                name="node_merge_airport_fee_train"
            ),
            node(
                func=merge_airport_fee,
                inputs="df_valid",
                outputs="df_valid_airport",
                name="node_merge_airport_fee_valid"
            ),
            node(
                func=merge_airport_fee,
                inputs="df_test",
                outputs="df_test_airport",
                name="node_merge_airport_fee_test"
            ),
            node(
                func=create_hour_feat,
                inputs=["df_train_airport", "params:col_date_hour"],
                outputs="df_train_hour",
                name="node_create_hour_train",
            ),
            node(
                func=create_hour_feat,
                inputs=["df_valid_airport", "params:col_date_hour"],
                outputs="df_valid_hour",
                name="node_create_hour_valid",
            ),
            node(
                func=create_hour_feat,
                inputs=["df_test_airport", "params:col_date_hour"],
                outputs="df_test_hour",
                name="node_create_hour_test",
            ),
            node(
                func=column_transformer,
                inputs=None,
                outputs="col_transf",
                name='node_column_transformer',
            ),
            node(
                func=feature_imputer,
                inputs=None,
                outputs="feat_imp",
                name="node_feature_imputer",
            ),
            node(
                func=pipe_estimator,
                inputs=["feat_imp", "col_transf", "params:params_hgbr"],
                outputs="model",
                name="node_pipeline_model",
            ),
            node(
                func=create_training_set,
                inputs=["df_train_hour", "df_valid_hour", "y_train", "y_valid"],
                outputs=["df_training", "y_training"],
                name="node_create_training"
            ),
            node(
                func=train_model,
                inputs=["model", "df_training", "df_test_hour", "y_training", "y_test", "params:params_hgbr", "params:api_key"],
                outputs="model_trained",
                name="node_train_model_and_log",
            ),
        ],
        inputs=["df_train", "df_valid", "df_test", "y_train", "y_valid", "y_test"],
        outputs=["df_training", "y_training", "model_trained", "df_test_hour"],
        namespace="data_science"
    )
