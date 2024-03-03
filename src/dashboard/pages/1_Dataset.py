# =================
# ==== IMPORTS ====
# =================

# Data science
import numpy as np
import pandas as pd

# Plots
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

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


@st.cache_data
def load_data(path_file: str) -> pd.DataFrame:
    """
    """
    df = pd.read_pickle(path_file)
    return df


def plot_histogram(data_to_plot: np.array, name_group: list[str]) -> None:
    """
    """
    # fig = ff.create_distplot(data_to_plot, name_group)
    # Plot
    # st.plotly_chart(fig, use_container_width=True)
    fig, ax = plt.subplots()
    ax.hist(data_to_plot, bins=100)
    st.pyplot(fig)


def create_body(path_data) -> None:
    """Create the body of the app
    """
    st.header("The dataset")
    # st.markdown()
    df = load_data(path_data)
    st.markdown(
        """
            ### Display the overall dataset
            Display 10 random rows of the NYC taxi dataset.
        """        
    )
    st.dataframe(df.sample(10))
    # Plot the average distance
    plot_histogram(df.loc[df['trip_distance'] < 1e2]['trip_distance'].values, name_group=['Trip distance'])




def main():
    """
    """
    set_parameters()
    create_heading()
    create_body(path_data='data/05_model_input/df_training.pkl')


# =============
# ==== RUN ====
# =============

if __name__ == "__main__":
    main()
