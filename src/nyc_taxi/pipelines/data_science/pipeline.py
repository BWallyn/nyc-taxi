"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.1
"""

from kedro.pipeline import node, Pipeline, pipeline
from nyc_taxi.pipelines.data_science.feature_engineering import create_hour_feat
from nyc_taxi.pipelines.data_science.nodes import (
    column_transformer,
    create_or_get_mlflow_experiment,
    create_training_set,
    feature_imputer,
    merge_airport_fee,
    pipe_estimator,
    # train_model,
    train_model_mlflow
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=merge_airport_fee,
                inputs="df_train",
                outputs="df_train_airport",
                name="merge_airport_fee_train"
            ),
            node(
                func=merge_airport_fee,
                inputs="df_valid",
                outputs="df_valid_airport",
                name="merge_airport_fee_valid"
            ),
            node(
                func=merge_airport_fee,
                inputs="df_test",
                outputs="df_test_airport",
                name="merge_airport_fee_test"
            ),
            node(
                func=create_hour_feat,
                inputs=["df_train_airport", "params:col_date_hour"],
                outputs="df_train_hour",
                name="create_hour_train_set",
            ),
            node(
                func=create_hour_feat,
                inputs=["df_valid_airport", "params:col_date_hour"],
                outputs="df_valid_hour",
                name="create_hour_valid_set",
            ),
            node(
                func=create_hour_feat,
                inputs=["df_test_airport", "params:col_date_hour"],
                outputs="df_test_hour",
                name="create_hour_test_set",
            ),
            node(
                func=column_transformer,
                inputs=None,
                outputs="col_transf",
                name='create_column_transformer',
            ),
            node(
                func=feature_imputer,
                inputs=None,
                outputs="feat_imp",
                name="create_feature_imputer",
            ),
            node(
                func=pipe_estimator,
                inputs=["feat_imp", "col_transf", "params:params_hgbr"],
                outputs="model",
                name="create_pipeline_model",
            ),
            node(
                func=create_training_set,
                inputs=["df_train_hour", "df_valid_hour", "y_train", "y_valid"],
                outputs=["df_training", "y_training"],
                name="create_training_dataset"
            ),
            node(
                func=create_or_get_mlflow_experiment,
                inputs=[
                    "params:data_science.experiment_id",
                    "params:data_science.experiment_folder",
                    "params:data_science.experiment_name",
                ],
                outputs="experiment_id",
                name="create_or_get_MLflow_experiment"
            ),
            # node(
            #     func=train_model,
            #     inputs=["model", "df_training", "df_test_hour", "y_training", "y_test", "params:params_hgbr", "params:api_key"],
            #     outputs="model_trained",
            #     name="train_model_and_log",
            # ),
            node(
                func=train_model_mlflow,
                inputs=["experiment_id", "model", "df_training", "df_test_hour", "y_training", "y_test", "params:params_hgbr"],
                outputs="model_trained",
                name="train_model_and_log_to_MLflow",
            ),
        ],
        inputs=["df_train", "df_valid", "df_test", "y_train", "y_valid", "y_test"],
        outputs=["df_training", "y_training", "model_trained", "df_test_hour"],
        namespace="data_science"
    )
