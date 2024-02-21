"""Functions to download datasets from webpage NYC TLC"""
# =================
# ==== IMPORTS ====
# =================

# Essential
import gc
import os
from tqdm import tqdm

# Internet
from urllib.error import HTTPError

# Data science
import pandas as pd


# ===================
# ==== FUNCTIONS ====
# ===================

def download_dataset_yymm(link: str, year_month: str) -> pd.DataFrame:
    """Download parquet dataset with the link and specific month

    Args:
        link: Link to the website containing the dataset
        year_month: Specific month of the data to download. Written as yyyy-mm
    Returns:
        df: DataFrame of the NYC taxis
    """
    path = f'{link}{year_month}.parquet'
    try:
        df = pd.read_parquet(path=path, engine="fastparquet")
    except HTTPError as err:
        if err.code == 403:
            print(f'Dataset {year_month} not found')
            df = pd.DataFrame()
    return df


def check_available(path_data: str, year_month: str) -> bool:
    """Check if the file is available

    Args:
        path_data: Path to the datafiles
        year_month: date to check
    """
    if os.path.isfile(os.path.join(path_data, f"nyc_taxi_{year_month}.pkl")):
        return True
    else:
        return False


def download_all_data(link: str, path_data: str, yyyy_start: int, yyyy_end: int, mm_start: int, mm_end: int) -> pd.DataFrame:
    """Download all data between two dataset if not saved in the folder and saved them.

    Args:
        link: Webpage path to the NYC Taxi datasets
        path_data: Path where to store datasets
        yyyy_start: Starting year
        yyyy_end: Ending year
        mm_start: Starting month
        mm_end: Ending month
    Returns:
        df: DataFrame merged of datasets between two datasets
    """
    # Create list of months
    if yyyy_start == yyyy_end:
        list_months = [
            str(yyyy_start) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start) + '-' + str(month) for month in range(mm_start, mm_end+1)
        ]
    else:
        n_year_diff = yyyy_end - yyyy_start
        for i in range(n_year_diff):
            list_months = [
                str(yyyy_start+i) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start+i) + '-' + str(month) for month in range(mm_start, 13)
            ]
        list_months += [
            str(yyyy_start) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start) + '-' + str(month) for month in range(mm_start, mm_end+1)
        ]
    df = pd.DataFrame()
    # Download dataset of each month
    for year_month in list_months:
        path_file = os.path.join(path_data, f"nyc_taxi_{year_month}.parquet")
        if os.path.isfile(path=path_file):
            df_temp = pd.read_parquet(path_file, engine="fastparquet")
        else:
            df_temp = download_dataset_yymm(link=link, year_month=year_month)
            df_temp.to_parquet(path_file, engine="fastparquet")
        df = pd.concat([df, df_temp])
        del df_temp
        gc.collect()
    return df


def merge_overall_dataset(link: str, yyyy_start: int, yyyy_end: int, mm_start: int, mm_end: int) -> pd.DataFrame:
    """
    """
    # Create list of months
    if yyyy_start == yyyy_end:
        list_months = [
            str(yyyy_start) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start) + '-' + str(month) for month in range(mm_start, mm_end+1)
        ]
    else:
        n_year_diff = yyyy_end - yyyy_start
        for i in range(n_year_diff):
            list_months = [
                str(yyyy_start+i) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start+i) + '-' + str(month) for month in range(mm_start, 13)
            ]
        list_months += [
            str(yyyy_start) + '-0' + str(month) if len(str(month)) == 1 else str(yyyy_start) + '-' + str(month) for month in range(mm_start, mm_end+1)
        ]
    # download dataset of each month and merge
    df = pd.DataFrame()
    for year_month in tqdm(list_months):
        df_tmp = download_dataset_yymm(link=link, year_month=year_month)
        df = pd.concat([df, df_tmp])
        del df_tmp
        gc.collect()
    df.reset_index(drop=True, inplace=True)
    return df
