import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Google Sheets API scope
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
]

# Set up the credentials and client
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
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    shots_sheet = client.open_by_key(workbook_key).worksheet('Shots')
    points_sheet = client.open_by_key(workbook_key).worksheet('Points')
    
    # Convert sheets to DataFrame
    shots_df = sheet_to_df(shots_sheet)
    points_df = sheet_to_df(points_sheet)
    
     # Initialize a list to store the analysis results
    analysis_results = []

    # Iterate over each shot made by the player
    for _, shot in shots_df.iterrows():
        # Proceed only if the shot was made by the player
        if shot['Player'] == 'Player':
            # Find the corresponding point outcome
            point_outcome = points_df[
                (points_df['Point Number'] == shot['Point']) &
                (points_df['Game'] == shot['Game']) &
                (points_df['Set'] == shot['Set'])
            ]
            # Determine if the player won or lost the point and capture the score
            if not point_outcome.empty:
                result = 'Won' if point_outcome.iloc[0]['Point Winner'] == 'host' else 'Lost'
                host_score = point_outcome.iloc[0]['Host Game Score']
                guest_score = point_outcome.iloc[0]['Guest Game Score']
                score = f"{host_score} - {guest_score}"

                analysis_results.append({
                    'Player': shot['Player'],
                    'Shot': shot['Shot'],
                    'Shot Type': shot['Type'],
                    'Point': shot['Point'],
                    'Game': shot['Game'],
                    'Set': shot['Set'],
                    'Result': result,
                    'H - G': score  
                })

    # Convert analysis_results list to a DataFrame before returning
    analysis_results_df = pd.DataFrame(analysis_results)
    return analysis_results_df


if __name__ == "__main__":
    outcomes_df = get_match_outcomes()  # Call the function without argument
    print(outcomes_df.head(40))  # Print the first 10 rows of the DataFrame
