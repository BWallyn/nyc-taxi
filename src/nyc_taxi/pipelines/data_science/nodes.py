"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.1
"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import numpy as np

# Machine learning
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from feature_engineering import cos_transformer, sin_transformer, periodic_spline_transformer


# ===================
# ==== FUNCTIONS ====
# ===================


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
            ("ordinal_enc_max", OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan, max_categories=255), ["PULocationID", "DOLocationID"])
            # ("passthrough_cols", "passthrough", [
            #     "VendorID", "passenger_count", "trip_distance", "RatecodeID", "PULocationID", "DOLocationID", "payment_type", "fare_amount", "extra",
            #     "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount", "congestion_surcharge", "airport_fee",
            # ])
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


def pipe_estimator(feat_imp: ColumnTransformer, col_transf: ColumnTransformer, **kwargs):
    """Create a regressor estimator from sklearn using a pipeline

    Args:
        feat_imp: Feature imputer element
        col_transf: Column transformer element
        **kwargs: Hyperparameters for the HistGradientBoosting method
    Returns:
        estimator: Estimator element from sklearn
    """
    estimator = Pipeline(
        steps=[
            ('feature_imp', feat_imp),
            ('column_transf', col_transf),
            ('model', HistGradientBoostingRegressor(**kwargs)),
        ]
    ).set_output(transform="pandas")
    return estimator
