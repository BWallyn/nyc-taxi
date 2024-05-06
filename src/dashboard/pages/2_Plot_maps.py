# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd
import geopandas as gpd

# Plots
import pydeck as pdk

# App
import streamlit as st


# Options
LA_GUARDIA = [40.7900, -73.8700]
JFK = [40.6650, -73.7821]
NEWARK = [40.7090, -74.1805]
MANHATTAN = [40.7766, -73.9713]
ZOOM_LEVEL = 12

WHITE, ORANGE = (255, 255, 255), (255, 128, 0)


# ===================
# ==== FUNCTIONS ====
# ===================

def set_parameters():
    """Set the parameters of page.
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
    """Update the query parameters for the day selected
    """
    day_selected = st.session_state["pickup_day"]
    st.query_params["pickup_day"] = day_selected


def update_query_params_hour() -> None:
    """Update the query parameters for the hour selected
    """
    hour_selected = st.session_state["pickup_hour"]
    st.query_params["pickup_hour"] = hour_selected


def select_slider(feat: str, min_slider: int, max_slider: int, title_slider: str, func) -> int:
    """Slider to select a value.

    Args:
        feat (str): Feature of the slider
        min_slider (int): Minimum value of the slider
        max_slider (int): Maximum value of the slider
        title_slider (str): Title of the slider
        func: Function to update the slider value
    Return:
        (int): Value selected in the slider
    """
    return st.slider(
        title_slider, min_slider, max_slider, key=feat, on_change=func
    )

def select_selectbox(feat: str, func) -> int:
    """Create a selectbox to select the day to display

    Args:
        feat (str): Feature of the selectbox, key for the params
        func: Function to update the selectbox value and pass to map
    Returns:
        (int): Day selected as an int
    """
    list_days = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    str_day = st.selectbox(label="select_the_day", options=list_days, key=feat, on_change=func)
    if str_day == "Monday":
        return 0
    elif str_day == "Tuesday":
        return 1
    elif str_day == "Wednesay":
        return 2
    elif str_day == "Thursday":
        return 3
    elif str_day == "Friday":
        return 4
    elif str_day == "Saturday":
        return 5
    else:
        return 6


@st.cache_resource
def load_data(path_file: str) -> pd.DataFrame:
    """Load the geopandas dataframe

    Args:
        path_file (str): Path to the geopandas dataframe file
    Returns:
        (gpd.GeoDataFrame): Geopandas dataframe
    """
    return gpd.read_file(path_file)


def select_day_hour(df: pd.DataFrame, day_sel: int, hour_sel: int) -> pd.DataFrame:
    """Filter the dataframe on the day and hour selected

    Args:
        df (pd.DataFrame): Input dataframe
        day_sel (int): Number of the day of the week selected
        hour_sel (int): Hour of the day selected
    Returns:
        (pd.DataFrame): Filtered dataframe
    """
    return df.loc[(df['date_dayofweek'] == day_sel) & (df['date_hour'] == hour_sel)]


def map(data: pd.DataFrame, lat, lon, zoom) -> None:
    """Create the map representing the number of trips of the selected day and hour

    Args:
        data (pd.DataFrame): Input dataframe
        lat (float): Latitude of the center of the map
        lon (float): Longitude of the center of the map
        zoom (int): Zoom of the map
    """
    def pseudocolor(
        val: float, minval: float, maxval: float, startcolor: tuple, stopcolor: tuple
    ):
        """
        Convert value in the range minval...maxval to a color in the range
        startcolor to stopcolor. The colors passed and the the one returned are
        composed of a sequence of N component values.

        Credits to https://stackoverflow.com/a/10907855
        """
        f = float(val-minval) / (maxval-minval)
        return tuple(f*(b-a)+a for (a, b) in zip(startcolor, stopcolor))
    
    # Prepare options plot
    max_rides, min_rides = data['n_trips'].max(), data['n_trips'].min()
    data['fill_color'] = data['n_trips'].apply(lambda x: pseudocolor(x, min_rides, max_rides, WHITE, ORANGE))
    # Plot
    initial_view_state = {
        "latitude": lat,
        "longitude": lon,
        "zoom": zoom,
        "pitch": 50,
    }
    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["Lon", "Lat"],
        get_elevation=['n_trips'],
        auto_highlight=True,
        radius=50,
        elevation_scale=10,
        get_fill_color="fill_color",
        get_line_color=[255, 255, 255],
        pickable=True,
        extruded=True,
        coverage=1,
    )
    tooltip = {"html": "<b>Zone:</b> {zone} <br /> <b>Number of trips: </b> {n_trips}"}
    r = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=initial_view_state,
        layers=[layer],
        tooltip=tooltip
    )
    st.pydeck_chart(r)


@st.cache_data
def mpoint(lat: np.array, lon: np.array) -> tuple:
    """Calculate the midpoint for a given set of data.

    Args:
        lat (np.array): List of latitudes
        lon (np.array): List of longitudes
    Returns:
        (tuple): Average latitude and longitude
    """
    return (np.average(lat), np.average(lon))


def create_body(path_data_by_day: str):
    """
    """
    day_selected = select_selectbox(feat='pickup_day', func=update_query_params_day)
    hour_selected = select_slider(
        feat='pickup_hour', min_slider=0, max_slider=23, title_slider='Select the hour of the day', func=update_query_params_hour
    )
    # Load data
    df = load_data(path_file=path_data_by_day)
    df_sel = select_day_hour(df=df, day_sel=day_selected, hour_sel=hour_selected)
    # Plot maps of the number of trips per hour
    cols_for_map = ['n_trips', 'Lon', 'Lat', 'zone']
    # Plot
    st.write(f"**Number of rides on the specific day {day_selected} and hour {hour_selected} chosen:**")
    map(df_sel[cols_for_map], MANHATTAN[0], MANHATTAN[1], ZOOM_LEVEL)



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