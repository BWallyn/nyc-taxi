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
    """Set the parameters of the page
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
    """Load dataframe saved as pickle file

    Args:
        path_file (str): Path to the dataframe
    Returns:
        (pd.DataFrame): Loaded dataframe
    """
    return pd.read_pickle(path_file)


@st.cache_data
def aggregate_all_locations(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate values of all locations.
    All rows are grouped by the datetime hour and sum the number of trips

    Args:
        df (pd.DataFrame): Input dataFrame
    Returns:
        df_group (pd.DataFrame): Output dataframe
    """
    df_group = df.groupby(by=["pickup_datetime"]).agg({
        'n_trips': 'sum',
        'duration': 'mean'
    })
    df_group = df_group.reset_index(drop=False)
    return df_group


def create_selectbox(tuple_locations: tuple[str], key_name: str) -> str:
    """Create a selectbox for the locations to display

    Args:
        tuple_locations (tuple[str]): List of the available locations
    Returns:
        (str): Selected location
    """
    return st.selectbox(
        "Select location:",
        tuple_locations,
        key=key_name
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


def plot_by_datetime(
    df: pd.DataFrame, feat: str, title: str,
) -> go.Figure:
    """Plot a line representing the feature 'feat' by datetime.

    Args:
        df (pd.DataFrame): Input dataframe
        feat (str): Feature to display on the plot
        location_ex (str): Title of the plot
    Returns:
        fig (go.Figure): Figure as a lineplot
    """
    # Define figure
    fig = go.Figure()
    fig = px.line(
        x=df['pickup_datetime'],
        y=df[feat],
        template='plotly_dark',
        markers=True,
        title=title
    )
    return fig


def create_body(path_data: str) -> None:
    """Create the body of the app

    Args:
        path_data (str): Path to the input dataframe
    """
    st.header("The dataset")

    # ---- Display the number of rides ----
    df = load_data(path_file=path_data)

    # Display the number of rides for all places
    df_all = aggregate_all_locations(df)
    st.write("**Display the number of rides for NYC:**")
    fig = plot_by_datetime(df_all, feat='n_trips', title='Number of rides per hour for NYC')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)

    # Diplay the number of rides for specific place
    st.write("**Display the number of rides for a specific place:**")
    tuple_locations = tuple(set(df['zone'].values))
    location_sel = create_selectbox(tuple_locations=tuple_locations, key_name='n_trip')
    df_sel = select_location(df, location_ex=location_sel)
    fig = plot_by_datetime(df_sel, feat='n_trips', title=f'Number of rides per hour for {location_sel}')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width=1000)

    # ---- Display the time of the rides ----
    st.write("**Display the average duration of the rides by datetime:**")
    fig_duration = plot_by_datetime(df_all, feat='duration', title='Average duration of rides')
    st.plotly_chart(fig_duration, theme="streamlit", use_container_width=True, width=1000)

    # Display the average duration of rides per location
    st.write("**Display the average duration of rides for a specific place:**")
    location_sel_duration = create_selectbox(tuple_locations=tuple_locations, key_name='duration')
    df_sel_duration = select_location(df, location_ex=location_sel_duration)
    fig_sel_duration = plot_by_datetime(df_sel_duration, feat='duration', title=f'Average duration of rides for {location_sel_duration}')
    st.plotly_chart(fig_sel_duration, theme="streamlit", use_container_width=True, width=1000)


def main():
    """
    """
    set_parameters()
    create_heading()
    create_body(
        path_data='data/08_reporting/df_training_group_location_datetime.pkl'
    )


# =============
# ==== RUN ====
# =============

if __name__ == "__main__":
    main()
