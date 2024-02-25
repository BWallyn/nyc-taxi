"""
This is a boilerplate pipeline 'model_inference'
generated using Kedro 0.19.1
"""
# =================
# ==== IMPORTS ====
# =================

import pandas as pd

from sklearn.pipeline import Pipeline


# ===================
# ==== FUNCTIONS ====
# ===================

def model_predict(df: pd.DataFrame, model: Pipeline) -> pd.Series:
    """
    """
    pred = model.predict(df)
    pred_df = pd.Series(pred, index=df.index)
    return pred_df

