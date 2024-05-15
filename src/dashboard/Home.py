# =================
# ==== IMPORTS ====
# =================

# App
import streamlit as st

# Custom functions
# from ..src.dashboard.dash_display import create_heading, create_sidebar, create_body


# ===================
# ==== FUNCTIONS ====
# ===================

def set_parameters():
    """
    """
    st.set_page_config(
        page_title="NYC Taxi",
        page_icon="👋",
    )

def create_heading() -> None:
    """Create the heading of the app
    """
    st.title("NYC taxi")
    st.subheader("Data from TLC")


def create_sidebar() -> None:
    """Create a sidebar for the app
    """
    st.sidebar.header("Sidebar")
    st.sidebar.markdown("This is a sidebar")


def create_body() -> None:
    """
    """
    st.image("https://www.nyc.gov/assets/tlc/images/content/pages/businesses/yellow-cab.png")
    st.markdown(
        """
            The goal of this project is to analyze the data from TLC about NYC yellow taxis.
            The dataset is available here: [TLC data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
        """
    )


def main() -> None:
    """
    """
    set_parameters()
    create_heading()
    create_body()
    # create_sidebar()


# =============
# ==== RUN ====
# =============

if __name__ == '__main__':
    main()