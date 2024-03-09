import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from ..data_access.utils import setup_client, sheet_to_df
client = setup_client()
import pandas as pd
from data_processing.data_access.utils import get_shots_df, get_points_df


def enrich_shots_with_point_outcomes():
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    shots_sheet = client.open_by_key(workbook_key).worksheet('Shots')
    points_sheet = client.open_by_key(workbook_key).worksheet('Points')
    
    # Convert sheets to DataFrame
    shots_df = sheet_to_df(shots_sheet)
    points_df = sheet_to_df(points_sheet)

    # Ensure data types match for merging (especially if 'Game' and 'Set' columns are floats)
    shots_df['Game'] = shots_df['Game'].astype(float)
    shots_df['Set'] = shots_df['Set'].astype(float)
    points_df['Game'] = points_df['Game'].astype(float)
    points_df['Set'] = points_df['Set'].astype(float)

    # Rename 'Point Number' in points_df to 'Point' for a consistent merge
    points_df.rename(columns={'Point Number': 'Point'}, inplace=True)

    # Merge shots_df with points_df to enrich shot data with point outcomes
    enriched_shots_df = pd.merge(shots_df, points_df, on=['Point', 'Game', 'Set'], how='left')

    return enriched_shots_df


def analyze_135_patterns(enriched_shots_df):
    # Filter for shots 1, 3, and 5
    shots_135_df = enriched_shots_df[enriched_shots_df['Shot'].isin([1, 3, 5])]
    
    # Example analysis: Print details of shot sequences leading to point outcomes
    for _, row in shots_135_df.iterrows():
        print(f"Game: {row['Game']}, Point: {row['Point']}, Shot: {row['Shot']}, Type: {row['Type']}, Outcome: {row['Point Winner']}, Detail: {row['Detail']}")

if __name__ == "__main__":
    enriched_shots_df = enrich_shots_with_point_outcomes()
    analyze_135_patterns(enriched_shots_df)
