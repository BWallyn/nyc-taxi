# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd

# Plots
import matplotlib.pyplot as plt
import pydeck as pdk

# App
import streamlit as st


# ===================
# ==== FUNCTIONS ====
# ===================

def map(data: pd.DataFrame, lat, lon, zoom) -> None:
    """
    """
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


@st.cache_data
def mpoint(lat: np.array, lon: np.array) -> tuple:
    """Calculate the midpoint for a given set of data.

    Args:
        lat: List of latitudes
        lon: List of longitudes
    """
    return (np.average(lat), np.average(lon))