"""
This is a boilerplate pipeline 'prepare_for_dashboard'
generated using Kedro 0.19.3
"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import datetime

# Data science
import pandas as pd
import geopandas as gpd



# ===================
# ==== FUNCTIONS ====
# ===================

def aggregate_specific_date(df: pd.DataFrame, feat_loc_groupby: str, date_select: str) -> pd.DataFrame:
    """Aggregate the different features of the dataset by a location feature, on a specific date.

    Args:
        df: Input dataframe
        feat_loc_groupby: Location feature used for the groupby
        date_select: Date chosen to select rows
    Returns:
        df_group: Dataframe grouped by the the location feature
    """
    df_group = df.loc[df['tpep_pickup_datetime'] == pd.to_datetime(date_select).date()].groupby(feat_loc_groupby)\
        .agg({
            'VendorID': 'count',
            'passenger_count': 'median',
            'trip_distance': 'mean',
            'payment_type': 'most_frequent',
            'fare_amount': 'mean',
            'extra': 'mean',
            'mta_tax': 'median',
            'tip_amount': 'mean',
            'tolls_amount': 'mean',
            'improvement_surcharge': 'median',
            'total_amount': 'mean',
            'congestion_surcharge': 'mean',
            'airport_fee': 'mean',
        })
    return df_group


def aggregate_by_day_hour(df: pd.DataFrame, beg_specific_week: str) -> pd.DataFrame:
    """Aggregate the different features of the dataset by the day of the week, the hour and
    the pickup location id.

    Args:
        df: Input dataframe
        beg_specific_week: Date of the specific week to select to analyze
    Returns:
        df_group: Dataframe grouped by day of week and hour
    """
    # Transform the date of the beginning of the week to date type
    beg_specific_week = pd.to_datetime(beg_specific_week).date()
    # Define the end of this specific week (7 days later)
    end_specific_week = beg_specific_week + datetime.timedelta(days=7)
    # Select the right week in the dataset
    df = df.loc[
        (df['tpep_pickup_datetime'].dt.date >= beg_specific_week)
        & (df['tpep_pickup_datetime'].dt.date < end_specific_week)
    ]
    # Create the day of week and hour features
    df = df.assign(
        date_dayofweek=df['tpep_pickup_datetime'].dt.day_of_week,
        date_hour=df['tpep_pickup_datetime'].dt.hour
    )
    # Compute the data aggregated by the day of the week and the 
    df_group = df.groupby(by=['date_dayofweek', 'PULocationID', 'date_hour'])\
        .agg({
            'VendorID': 'count',
            'DOLocationID': lambda x: x.value_counts().index[0],
            'passenger_count': 'median',
            'trip_distance': 'mean',
            'payment_type': lambda x: x.value_counts().index[0],
            'fare_amount': 'mean',
            'extra': 'mean',
            'mta_tax': 'median',
            'tip_amount': 'mean',
            'tolls_amount': 'mean',
            'improvement_surcharge': 'median',
            'total_amount': 'mean',
            'congestion_surcharge': 'mean',
            'airport_fee': 'mean',
        })
    df_group = df_group.rename(columns={'VendorID': 'n_trips'})
    return df_group


def load_geographical_dataframe(path_geo: str) -> gpd.GeoDataFrame:
    """Load the geographical dataframe

    Args:
        path_geo (str): path to the geographical dataframe
    Returns:
        (gpd.GeoDataFrame): Geographical dataframe
    """
    return gpd.read_file(path_geo)


def add_geographical_info_pickup(df: pd.DataFrame, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Add geographical info from geopandas dataframe

    Args:
        df: Input dataframe
        gdf: Geopandas dataframe with shapes of the location ID
    Returns:
        gdf: Output dataframe with the geographical info
    """
    # Merge geographical info
    gdf = df.merge(gdf, left_on='PULocationID', right_on='LocationID', how='left')
    return gdf
