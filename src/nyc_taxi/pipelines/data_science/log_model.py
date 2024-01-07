"""Functions to log models to comet"""
# =================
# ==== IMPORTS ====
# =================

import numpy as np
import pandas as pd

from comet_ml import Experiment
from comet_ml.integration.sklearn import log_model
from sklearn.pipeline import Pipeline


# ===================
# ==== FUNCTIONS ====
# ===================

def log_hgbr_model(api_key: str, params: dict, metrics: dict, model: Pipeline, model_name: str="HistGradientBoostingRegressor_model") -> None:
    """
    """
    experiment = Experiment(
        api_key=api_key,
        project_name="nyc-taxi-trip",
        workspace="bwallyn"
    )
    # Log info
    experiment.log_parameters(params)
    experiment.log_metrics(metrics)
    # Log model
    log_model(experiment, model_name, model)
    experiment.end()