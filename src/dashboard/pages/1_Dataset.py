# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd

# Plots
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import altair as alt

# App
import streamlit as st


# ===================
# ==== FUNCTIONS ====
# ===================

def set_parameters():
    """
    """
    st.set_page_config(
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


def update_query_params() -> None:
    """
    """
    day_selected = st.session_state["pickup_day"]
    st.query_params(pickup_day=day_selected)


def select_day() -> int:
    """
    """
    day_selected = st.slider(
        "Select day of pickup", 0, 6, key="pickup_day", on_change=update_query_params
    )
    return day_selected


def plot_histogram(data_to_plot: np.array, name_group: list[str], title: str, x_label: str) -> None:
    """
    """
    # fig = ff.create_distplot(data_to_plot, name_group)
    # Plot
    # st.plotly_chart(fig, use_container_width=True)
    fig, ax = plt.subplots()
    ax.hist(data_to_plot, bins=100)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Distribution")
    st.pyplot(fig)


def plot_hist_data(df: pd.DataFrame,) -> None:
    """
    """
    chart = (
        alt.Chart(df)
        .mark_area(opacity=0.3, color='orange')
        .encode(
            x=alt.X("date_hour:Q",),
            y=alt.Y("n_trips:Q", stack=None),
        )
    )
    st.altair_chart(chart, use_container_width=True)


def create_body(path_data: str, path_target: str, path_data_by_day: str) -> None:
    """Create the body of the app
    """
    st.header("The dataset")
    # st.markdown()
    
    # ---- Plot on specific day ----
    st.markdown("""### Analyze on a specific day of week""")
    # Define slider
    day_selected = select_day()
    st.write(f"**Whole New York City on {day_selected} day of week")
    # Load data
    df = load_data(path_file=path_data_by_day).reset_index(drop=False)
    df = df.loc[df['date_dayofweek'] == day_selected]
    # Display some data
    st.dataframe(df)
    # Display the number of rides per hour
    plot_hist_data(df)
    

    # # Plot the distribution of the distance
    # plot_histogram(
    #     df.loc[df['trip_distance'] < 1e2]['trip_distance'].values, name_group=['Trip distance'],
    #     title="Distribution of the trip distances", x_label="Distance"
    # )
    # # Plot the distribution of the target
    # plot_histogram(
    #     y_target.loc[(y_target['duration'] < 1e4) & (y_target['duration'] >= 0)].values, name_group=['Trip duration'],
    #     title="Distribution of the trip durations", x_label="Duration"
    # )


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
