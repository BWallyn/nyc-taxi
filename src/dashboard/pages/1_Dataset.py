# =================
# ==== IMPORTS ====
# =================

# Data science
import pandas as pd

# Plots
import plotly.express as px
import plotly.graph_objects as go

# App
import streamlit as st


# ===================
# ==== FUNCTIONS ====
# ===================

def set_parameters():
    """
    """
    st.set_page_config(
        layout='wide',
        page_title="Dataset",
        page_icon="👋",
    )


def create_heading() -> None:
    """Create the heading of the app
    """
    st.title("NYC taxi - Dataset")
    st.subheader("Analyze the dataset from TLC")


@st.cache_resource
def load_data(path_file: str) -> pd.DataFrame:
    """
    """
    df = pd.read_pickle(path_file)
    return df


@st.cache_data
def load_target(path_file: str) -> pd.Series:
    """
    """
    y_target = pd.read_csv(path_file)
    return y_target


@st.cache_data
def aggregate_all_locations(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate values of all locations.
    All rows are grouped by the datetime hour and sum the number of trips

    Args:
        df (pd.DataFrame): Input dataFrame
    Returns:
        df_group (pd.DataFrame): Output dataframe
    """
    df_group = df.groupby(by=["pickup_datetime"])['n_trips'].sum()
    df_group = df_group.reset_index(drop=False)
    return df_group


def create_selectbox(tuple_locations: tuple[str]) -> str:
    """Create a selectbox for the locations to display

    Args:
        tuple_locations (tuple[str]): List of the available locations
    Returns:
        (str): Selected location
    """
    return st.selectbox(
        "Select location:",
        tuple_locations
    )


@st.cache_data
def select_location(df: pd.DataFrame, location_ex: str) -> pd.DataFrame:
    """Filter the dataframe to select only the location selected by the selectbox

    Args:
        df (pd.DataFrame): Input dataframe
        location_ex (str): Location selected
    Returns:
        (pd.DataFrame): Filtered dataframe
    """
    return df.loc[df["zone"] == location_ex]


def plot_n_rides_per_hour(
    df: pd.DataFrame, location_ex: str,
) -> go.Figure:
    """Plot the number of trips in the time on a specific location

    Args:
        df (pd.DataFrame): Input dataframe
        location_ex (str): Location displayed
    Returns:
        fig (go.Figure): Figure of the number of trips
    """
    # Define figure
    fig = go.Figure()
    title = f'Number of trip per hour for {location_ex}'
    fig = px.line(
        x=df['pickup_datetime'],
        y=df['n_trips'],
        template='plotly_dark',
        markers=True,
        title=title
    )
    return fig


def create_body(path_data: str, path_target: str, path_data_by_day: str) -> None:
    """Create the body of the app
    """
    st.header("The dataset")

    # ---- Display the number of rides ----
    df = load_data(path_file='data/08_reporting/df_training_group_location_datetime.pkl')

    # Display the number of rides for all places
    df_all = aggregate_all_locations(df)
    st.write("**Display the number of rides for NYC:**")
    fig = plot_n_rides_per_hour(df_all, location_ex="NYC")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)

    # Diplay the number of rides for specific place
    st.write("**Display the number of rides for a specific place:**")
    tuple_locations = tuple(set(df['zone'].values))
    location_sel = create_selectbox(tuple_locations=tuple_locations)
    df_sel = select_location(df, location_ex=location_sel)
    fig = plot_n_rides_per_hour(df_sel, location_ex=location_sel)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)


def main():
    """
    """
    set_parameters()
    create_heading()
    create_body(
        path_data='data/05_model_input/df_training.pkl', path_target='data/05_model_input/y_training.csv',
        path_data_by_day='data/08_reporting/df_training_group_dayofweek_hour.pkl'
    )


# =============
# ==== RUN ====
# =============

if __name__ == "__main__":
    main()
