"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.1
"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import numpy as np
import pandas as pd
import mlflow
from typing import Any

# Machine learning
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from nyc_taxi.pipelines.data_science.feature_engineering import periodic_spline_transformer
from nyc_taxi.pipelines.data_science.log_mlflow import _log_model_mlflow, _log_mlflow_metric, _log_mlflow_parameters
from nyc_taxi.pipelines.data_science.log_model import log_hgbr_model


# ===================
# ==== FUNCTIONS ====
# ===================

def merge_airport_fee(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    mask_ = df["airport_fee"].isna()
    df.loc[mask_, 'airport_fee'] = df.loc[mask_, 'Airport_fee']
    df = df.drop(columns=["Airport_fee"])
    return df


def column_transformer() -> ColumnTransformer:
    """Create a column transformer

    Returns:
        col_transf: Column transformer element from sklearn
    """
    # Column transformer
    col_transf = ColumnTransformer(
        transformers=[
            # ("hour_sin", sin_transformer(24), ["tpep_pickup_datetime_hour"]),
            # ("hour_cos", cos_transformer(24), ["tpep_pickup_datetime_hour"]),
            ("hour_spline", periodic_spline_transformer(24, n_splines=12), ["tpep_pickup_datetime_hour"]),
            ("ordinal_enc", OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan), ["store_and_fwd_flag"]),
            ("ordinal_enc_max", OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan, max_categories=255), ["PULocationID", "DOLocationID"]),
        ], remainder='passthrough', verbose_feature_names_out=False,
    )
    return col_transf


def feature_imputer():
    """Create a feature imputer for the missing values

    Returns:
        feat_imp: Feature imputer element from sklearn
    """
    feat_imp = ColumnTransformer(
        transformers=[
            ("pass_count", SimpleImputer(strategy="median"), ["passenger_count"]),
            ("rate_code", SimpleImputer(strategy="most_frequent"), ["RatecodeID"]),
            ("store_flag", SimpleImputer(strategy="most_frequent"), ["store_and_fwd_flag"]),
            ("cong_surch", SimpleImputer(strategy="median"), ["congestion_surcharge"]),
            ("air_fee", SimpleImputer(strategy="most_frequent"), ["airport_fee"]),
            ("passthrough_cols", "passthrough", [
                "VendorID", "trip_distance", "PULocationID", "DOLocationID",
                "payment_type", "fare_amount", "extra",
                "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount", "tpep_pickup_datetime_hour"
            ])
        ], remainder='drop', verbose_feature_names_out=False
    )
    return feat_imp


def pipe_estimator(feat_imp: ColumnTransformer, col_transf: ColumnTransformer, params_hgbr) -> Pipeline:
    """Create a regressor estimator from sklearn using a pipeline

    Args:
        feat_imp: Feature imputer element
        col_transf: Column transformer element
        params_hgbr: Hyperparameters for the HistGradientBoosting method
    Returns:
        estimator: Estimator element from sklearn
    """
    estimator = Pipeline(
        steps=[
            ('feature_imp', feat_imp),
            ('column_transf', col_transf),
            ('model', HistGradientBoostingRegressor(**params_hgbr)),
        ]
    ).set_output(transform="pandas")
    return estimator


def create_training_set(df_train: pd.DataFrame, df_valid: pd.DataFrame, y_train: pd.Series, y_valid: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    """Create a training set by concatenating the given training and validation dataframes and arrays.

    Args:
        df_train (pd.DataFrame): The training dataframe.
        df_valid (pd.DataFrame): The validation dataframe.
        y_train (pd.Series): The training array.
        y_valid (pd.Series): The validation array.
    Returns:
        tuple[pd.DataFrame, pd.Series]: A tuple containing the concatenated dataframe and array.
    """
    df_training = pd.concat([df_train, df_valid])
    y_training = pd.concat([y_train, y_valid])
    return df_training, y_training



def train_model(
    estimator: Pipeline, df_train: pd.DataFrame, df_valid: pd.DataFrame, y_train: pd.Series, y_valid: pd.Series, params_hgbr: dict,
    api_key: str,
) -> Pipeline:
    """
    """
    # Train the model
    estimator.fit(df_train, y_train)
    # Predict
    pred_train = estimator.predict(df_train)
    pred_valid = estimator.predict(df_valid)
    # Compute metrics
    metrics = {
        "RMSE_train": mean_squared_error(y_true=y_train, y_pred=pred_train, squared=False),
        "RMSE_valid": mean_squared_error(y_true=y_valid, y_pred=pred_valid, squared=False),
    }
    # Log to Comet
    log_hgbr_model(api_key=api_key, params=params_hgbr, metrics=metrics, model=estimator, model_name="HistGradientBoostingRegressor_model")
    return estimator


def train_model_mlflow(
    experiment_id: str,
    estimator: Pipeline, df_train: pd.DataFrame, df_valid: pd.DataFrame,
    y_train: pd.DataFrame, y_valid: pd.DataFrame,
    params_hgbr: dict[str, Any],
) -> Pipeline:
    """Train a model and log to MLflow the info about the estimator:
    - Train a model defined as a scikit-learn pipeline
    - Predict on the train and validation sets
    - Compute metrics on both datasets
    - Log metrics, model parameters and model to MLflow

    Args:
        experiment_id (str): Id of the MLflow experiment
        estimator (Pipeline): Scikit learn pipeline
        df_train (pd.DataFrame): Train dataframe
        df_valid (pd.DataFrame): Validation dataframe
        y_train (pd.DataFrame): Target of the train dataframe
        y_valid (pd.DataFrame): Target of the validation dataframe
        params_hgbr (dict[str, Any]): Parameters of the HistGradientBoosting model
    Returns:
        estimator (Pipeline): Trained estimator
    """
    with mlflow.start_run(experiment_id=experiment_id):
        # Train the model
        estimator.fit(df_train, y_train)
        # Predict
        pred_train = estimator.predict(df_train)
        pred_valid = estimator.predict(df_valid)
        # Compute metrics
        metrics = {
            "RMSE_train": mean_squared_error(y_true=y_train, y_pred=pred_train, squared=False),
            "RMSE_valid": mean_squared_error(y_true=y_valid, y_pred=pred_valid, squared=False),
        }
        # Log to MLflow
        _log_model_mlflow(estimator, df=df_train)
        _log_mlflow_parameters(dict_params=params_hgbr)
        _log_mlflow_metric(metrics)
    # Return model trained
    return estimator
