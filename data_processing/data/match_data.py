import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Define your Google Sheets API scope
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
]

# Set up the credentials and client
current_dir = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(current_dir, 'creds.json')


current_dir = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(current_dir, 'creds.json')
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
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

def get_match_outcomes():
    shots_sheet = client.open_by_key('1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU').worksheet('Shots')
    points_sheet = client.open_by_key('1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU').worksheet('Points')
    
    # Convert sheets to DataFrame
    shots_df = sheet_to_df(shots_sheet)
    points_df = sheet_to_df(points_sheet)

    filtered_shots_df = shots_df[(shots_df['Player'] == 'Player') & (shots_df['Shot'].isin([1, 3, 5]))]

    # Initialize an empty list to hold the corrected outcomes
    corrected_outcomes = []

    # Iterate over the filtered shots, taking into account the correct point mapping
    for _, shot_row in filtered_shots_df.iterrows():
        game_number = shot_row['Game']
        shot_number = shot_row['Shot']
        shot_type = shot_row['Type']
        
        # Determine the index for point outcome based on shot number
        if shot_number == 1:
            point_outcome = points_df[(points_df['Game'] == game_number) & (points_df['Set'] == shot_row['Set'])].iloc[0]
        elif shot_number == 3:
            point_outcome = points_df[(points_df['Game'] == game_number) & (points_df['Set'] == shot_row['Set'])].iloc[1]
        elif shot_number == 5:
            point_outcome = points_df[(points_df['Game'] == game_number) & (points_df['Set'] == shot_row['Set'])].iloc[2]
        
        # Determine win or loss based on point_winner
        outcome = 'Won' if point_outcome['Point Winner'] == 'host' else 'Lost'
        
        # Append the outcome along with relevant shot details to the corrected_outcomes list
        corrected_outcomes.append({
            'Player': 'Player',
            'Shot_Number': shot_number,
            'Type': shot_type,
            'Game': game_number,
            'Outcome': outcome
        })

        

    # Convert the corrected_outcomes list to a DataFrame
    corrected_outcomes_df = pd.DataFrame(corrected_outcomes)
    corrected_outcomes_df['Shot_Number'] = corrected_outcomes_df['Shot_Number'].astype('Int64')
    corrected_outcomes_df['Game'] = corrected_outcomes_df['Game'].astype('Int64')

    # Convert 'Player', 'Type', and 'Outcome' columns to categorical data types
    corrected_outcomes_df['Player'] = corrected_outcomes_df['Player'].astype('category')
    corrected_outcomes_df['Type'] = corrected_outcomes_df['Type'].astype('category')
    corrected_outcomes_df['Outcome'] = corrected_outcomes_df['Outcome'].astype('category')

    print(corrected_outcomes_df.dtypes)
    print(corrected_outcomes_df.isnull().sum())
    print(corrected_outcomes_df[['Shot_Number', 'Game']].head(10))
    return corrected_outcomes_df

# Example usage:
# outcomes_df = get_match_outcomes()
# print(outcomes_df.head())
