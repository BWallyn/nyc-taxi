"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from .feature_engineering import create_hour_feat
from .nodes import column_transformer, feature_imputer, pipe_estimator, create_training_set, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_hour_feat,
            inputs=["df_train", "params:col_date_hour"],
            outputs="df_train_hour",
            name="node_create_hour_train",
        ),
        node(
            func=create_hour_feat,
            inputs=["df_valid", "params:col_date_hour"],
            outputs="df_valid_hour",
            name="node_create_hour_valid",
        ),
        node(
            func=create_hour_feat,
            inputs=["df_test", "params:col_date_hour"],
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
    ])
