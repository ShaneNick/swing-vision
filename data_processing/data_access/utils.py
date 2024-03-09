# utils.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

def setup_client():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive',
    ]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(current_dir, 'creds.json')
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Failed to set up Google Sheets client: {e}")
        raise

def sheet_to_df(worksheet):
    try:
        records = worksheet.get_all_records()
        return pd.DataFrame.from_records(records)
    except Exception as e:
        print(f"Error converting sheet to DataFrame: {e}")
        raise

