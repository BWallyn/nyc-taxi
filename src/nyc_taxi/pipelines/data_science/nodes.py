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
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer

from .feature_engineering import periodic_spline_transformer


# ===================
# ==== FUNCTIONS ====
# ===================

def sin_transformer(period):
    return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))


def cos_transformer(period):
    return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))


def column_transformer() -> ColumnTransformer:
    """
    """
    # Column transformer
    col_transf = ColumnTransformer(
        transformers=[
            ("hour_sin", sin_transformer(24), ["tpep_pickup_datetime_hour"]),
            ("hour_cos", sin_transformer(24), ["tpep_pickup_datetime_hour"]),
            ("hour_spline", periodic_spline_transformer(24, n_splines=12), ["tpep_pickup_datetime_hour"]),
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
        ], remainder='passthrough', verbose_feature_names_out=False
    )
    return feat_imp
