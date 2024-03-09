import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from .utils import setup_client

def sheet_to_df(worksheet):
    try:
        records = worksheet.get_all_records()
        return pd.DataFrame.from_records(records)
    except Exception as e:
        print(f"Error converting sheet to DataFrame: {e}")
        raise

def get_shots_df():
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    client = setup_client()
    shots_sheet = client.open_by_key(workbook_key).worksheet('Shots')
    return sheet_to_df(shots_sheet)

def get_points_df():
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    client = setup_client()
    points_sheet = client.open_by_key(workbook_key).worksheet('Points')
    return sheet_to_df(points_sheet)