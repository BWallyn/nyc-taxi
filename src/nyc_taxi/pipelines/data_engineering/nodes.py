"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.1
"""
# =================
# ==== IMPORTS ====
# =================

import pandas as pd

from .download_data import download_all_data


# ===================
# ==== FUNCTIONS ====
# ===================

def download_between_dates(path_tlc: str, date_start: str, date_end: str) -> pd.DataFrame:
    """Download data of NYC taxi trips between two dates

    Args:
        path_tlc: Link to the NYC TLC website
        date_start: Starting month to download data. Format yyyy-mm
        date_end: Ending month to download data. Format yyyy-mm
    Returns:
        df: DataFrame downloaded
    """
    # Get parameters
    yyyy_start = int(date_start[:4])
    mm_start = int(date_start[5:])
    yyyy_end = int(date_end[:4])
    mm_end = int(date_end[5:])
    # Extract data
    df = download_all_data(link=path_tlc, path_data="./data/01_raw", yyyy_start=yyyy_start, yyyy_end=yyyy_end, mm_start=mm_start, mm_end=mm_end)
    return df


def split_train_val_test(df: pd.DataFrame, date_valid_str: str, date_test_str: str, col_date: str="tpep_pickup_datetime") -> list[pd.DataFrame]:
    """Split the dataset into train, validation and test sets.

    Args:
        df: Entire dataframe
    """
    # Options
    date_valid = pd.to_datetime(date_valid_str, errors="raise", format="%Y-%m")
    date_test = pd.to_datetime(date_test_str, errors="raise", format="%Y-%m")
    # Select data
    df_train = df.loc[df[col_date] < date_valid]
    df_valid = df.loc[(df[col_date] >= date_valid) & (df[col_date] < date_test)]
    df_test = df.loc[df[col_date] >= date_test]
    return df_train, df_valid, df_test


def create_duration(df: pd.DataFrame, col_pickup_date: str="tpep_pickup_datetime", col_dropoff_date: str="tpep_dropoff_datetime") -> pd.DataFrame:
    """Add duration time (in s) to the dataset using pickup and dropoff times.

    Args:
        df: DataFrame with pick-up and drop-off times
        col_pickup_date: Name of the pickup datetime column
        col_dropoff_date: Name of the dropoff datetime column
    Returns:
        df: DataFrame with the duration feature
    """
    # Convert datetime
    df[col_pickup_date] = pd.to_datetime(df[col_pickup_date], errors='coerce')
    df[col_dropoff_date] = pd.to_datetime(df[col_dropoff_date], errors='coerce')
    # Compute duration
    df['duration'] = (df[col_dropoff_date] - df[col_pickup_date]).dt.total_seconds()
    return df


def delete_dropoff_date(df: pd.DataFrame) -> pd.DataFrame:
    """Delete the dropoff date feature

    Args:
        df: DataFrame
    Returns:
        df: DataFrame without the dropoff date feat
    """
    df = df.drop(columns=["tpep_dropoff_datetime"])
    return df


def create_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    df = df.reset_index(drop=False).rename(columns={"index": "id"})
    return df