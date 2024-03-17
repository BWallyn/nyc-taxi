"""
This is a boilerplate pipeline 'prepare_for_dashboard'
generated using Kedro 0.19.3
"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import datetime
import pandas as pd


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
    """Aggregate the different features of the dataset by a location feature, on a specific date.

    Args:
        df: Input dataframe
        beg_specific_week: Date of the specific week to select to analyze
    Returns:
        df_group: Dataframe grouped by day of week and hour
    """
    beg_specific_week = pd.to_datetime(beg_specific_week).date()
    end_specific_week = beg_specific_week + datetime.timedelta(days=7)
    df = df.loc[(df['tpep_pickup_datetime'].dt.date >= beg_specific_week) & (df['tpep_pickup_datetime'].dt.date < end_specific_week)]
    df['date_dayofweek'] = df['tpep_pickup_datetime'].dt.day_of_week
    df['date_hour'] = df['tpep_pickup_datetime'].dt.hour
    df_group = df.groupby(by=['date_dayofweek', 'date_hour'])\
        .agg({
            'VendorID': 'count',
            'PULocationID': pd.Series.mode,
            'DOLocationID': pd.Series.mode,
            'passenger_count': 'median',
            'trip_distance': 'mean',
            'payment_type': pd.Series.mode,
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