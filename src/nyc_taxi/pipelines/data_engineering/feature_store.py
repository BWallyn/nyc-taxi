"""Function to connect to feature store on Hopsworks"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import pandas as pd

# Hopsworks
import hopsworks


# ===================
# ==== FUNCTIONS ====
# ===================

def log_to_hopswork():
    """Log to hopsworks

    Args:
    """
    project = hopsworks.login()
    project.close()
    fs = project.get_feature_store()
    return fs


def create_nyc_fs(fs, version: int=1):
    """
    """
    # Get or create the 'nyc_taxi_batch_fg' feature group
    nyc_fg = fs.get_or_create_feature_group(
        name="nyc_taxi_batch_fg",
        version=version,
        description="NYC taxi trips data",
        primary_key=["cc_num"],
        event_time="datetime",
        # expectation_suite=expectation_suite_nyc,
    )
    return nyc_fg


def insert_df_fs(nyc_fg, df_taxi: pd.DataFrame):
    """
    """
    nyc_fg.insert(
        df_taxi,
        write_options={"wait_for_job": True},
    )


def update_feature_description(nyc_fg):
    """Add the features descriptions to the feature store.

    Args:
        nyc_fg: Feature store element
    Returns:
        nyc_fg: Feature store element with description updated
    """
    feature_descriptions = [
        {"name": "id", "description": "Id of the transaction"},
        {"name": "VendorID", "description": "Id of the taxi"},
        {"name": "tpep_pickup_datetime", "description": "Pickup time"},
        {"name": "tpep_dropoff_datetime", "description": "Dropoff time"},
        {"name": "passenger_count", "description": "Number of passengers of the trip"},
        {"name": "trip_distance", "description": "Distance of the taxi trip"},
        {"name": "RatecodeID", "description": "The final rate code in effect at the end of the trip"},
        {"name": "store_and_fwd_flag", "description": "This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka store and forward, because the vehicle did not have a connection to the server"},
        {"name": "PULocationID", "description": "TLC Taxi Zone in which the taximeter was engaged"},
        {"name": "DOLocationID", "description": "TLC Taxi Zone in which the taximeter was disengaged"},
    ]
    for desc in feature_descriptions: 
        nyc_fg.update_feature_description(desc["name"], desc["description"])
    return nyc_fg
