# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd
import geopandas as gpd

# Plots
import matplotlib.pyplot as plt
import pydeck as pdk

# App
import streamlit as st


# Options
LA_GUARDIA = [40.7900, -73.8700]
JFK = [40.6650, -73.7821]
NEWARK = [40.7090, -74.1805]
ZOOM_LEVEL = 12


# ===================
# ==== FUNCTIONS ====
# ===================

def set_parameters():
    """
    """
    st.set_page_config(
        layout='wide',
        page_title="Maps",
        # page_icon=":map:",
        page_icon="🌍",
    )


def create_heading() -> None:
    """Create the heading of the app page
    """
    st.title("NYC taxi - Maps")
    st.subheader("Display rides locations")


def update_query_params_day() -> None:
    """
    """
    day_selected = st.session_state["pickup_day"]
    st.query_params["pickup_day"] = day_selected


def update_query_params_hour() -> None:
    """
    """
    hour_selected = st.session_state["pickup_hour"]
    st.query_params["pickup_hour"] = hour_selected


def select_slider(feat: str, min_slider: int, max_slider: int, title_slider: str, func) -> int:
    """
    """
    val_selected = st.slider(
        title_slider, min_slider, max_slider, key=feat, on_change=func
    )
    return val_selected


@st.cache_resource
def load_data(path_file: str) -> pd.DataFrame:
    """
    """
    gdf = gpd.read_file(path_file)
    return gdf


def select_day_hour(df: pd.DataFrame, day_sel: int, hour_sel: int) -> pd.DataFrame:
    """
    """
    return df.loc[(df['date_dayofweek'] == day_sel) & (df['date_hour'] == hour_sel)]


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
                    "GeoJsonLayer",
                    data=data,
                    get_position=["Geometry"],
                    # radius=100,
                    # elevation_scale=4,
                    # elevation_range=[0, 1000],
                    # pickable=True,
                    # extruded=True,
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


def create_body(path_data_by_day: str):
    """
    """
    day_selected = select_slider(
        feat='pickup_day', min_slider=0, max_slider=6, title_slider='Select the day of the week', func=update_query_params_day
    )
    hour_selected = select_slider(
        feat='pickup_hour', min_slider=0, max_slider=23, title_slider='Select the hour of the day', func=update_query_params_hour
    )
    # Load data
    df = load_data(path_file=path_data_by_day)
    df_sel = select_day_hour(df=df, day_sel=day_selected, hour_sel=hour_selected)
    # Plot maps of the number of trips per hour
    cols_for_map = ['n_trips', 'geometry']
    # JFK Airport
    st.write("**JFK Airport**")
    map(df_sel[cols_for_map], JFK[0], JFK[1], ZOOM_LEVEL)



def main():
    """
    """
    set_parameters()
    create_heading()
    create_body(path_data_by_day='data/08_reporting/df_training_group_dayofweek_hour_w_geo.geojson')


# =============
# ==== Run ====
# =============

if __name__ == '__main__':
    main()