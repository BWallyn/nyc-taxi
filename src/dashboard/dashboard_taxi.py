# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd

# App
import streamlit as st

# Custom functions
from src.dashboard.dash_display import create_heading, create_sidebar, create_body


# ===================
# ==== FUNCTIONS ====
# ===================

def main() -> None:
    """
    """
    create_heading()
    create_sidebar()
    create_body()
    