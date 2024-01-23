"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.1
"""
# =================
# ==== IMPORTS ====
# =================

import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error

import seaborn as sns


# ===================
# ==== FUNCTIONS ====
# ===================

def compute_metrics(y_train: np.array, pred_train: np.array, y_test: np.array, pred_test: np.array) -> dict:
    """
    """
    # Compute metrics
    metrics = {
        "RMSE_train": mean_squared_error(y_true=y_train, y_pred=pred_train, squared=False),
        "rmse_valid": mean_squared_error(y_true=y_test, y_pred=pred_test, squared=False),
    }
    return metrics


def plot_histograms(y_true: np.array, y_pred: np.array) -> None:
    """
    """
    
