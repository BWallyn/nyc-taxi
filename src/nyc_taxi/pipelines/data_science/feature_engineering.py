"""Functions for feature engineering"""
# =================
# ==== IMPORTS ====
# =================

import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer, SplineTransformer


# ===================
# ==== FUNCTIONS ====
# ===================

def is_weekend(df: pd.DataFrame, col_date: str) -> pd.DataFrame:
    """Create an indicator whether it's a weekend day or not.

    Args:
        df: Dataset
        col_state: Name of the date column
    Returns:
        df: DataFrame with the weekend indicator
    """
    df.loc[:, f"{col_date}_isweekend"] = 0
    df.loc[df[f"{col_date}_weekday"] >= 5, f"{col_date}_isweekend"] = 1
    return df


def create_date_feats(df: pd.DataFrame, col_date: str) -> pd.DataFrame:
    """Create features from date column

    Args:
        df: DataFrame with date column
        col_date: Name of the date column used to create features
    Returns:
        df: DataFrame with date features created
    """
    df[f"{col_date}_year"] = df[col_date].dt.year
    df[f"{col_date}_month"] = df[col_date].dt.month
    df[f"{col_date}_day"] = df[col_date].dt.day
    df[f"{col_date}_weekday"] = df[col_date].dt.weekday
    # Check is weekend
    df = is_weekend(df, col_date)
    return df


def sin_transformer(period):
    return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))


def cos_transformer(period):
    return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))


def create_hour_feat(df: pd.DataFrame, col_datetime: str) -> pd.DataFrame:
    """Create hour feat from datetime column

    Args:
        df: DataFrame
        col_datetime: Name of the datetime column
    """
    df[f"{col_datetime}_hour"] = df[col_datetime].dt.hour
    return df


def periodic_spline_transformer(period: int, n_splines: int=None, degree: int=3) -> SplineTransformer:
    """Create a spline transformer from scikit-learn.

    Args:
    """
    if n_splines is None:
        n_splines = period
    n_knots = n_splines + 1
    return SplineTransformer(
        degree=degree,
        n_knots=n_knots,
        knots=np.linspace(0, period, n_knots).reshape(n_knots, 1),
        extrapolation="periodic",
        include_bias=True,
    )