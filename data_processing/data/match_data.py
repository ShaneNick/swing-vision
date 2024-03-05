import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pprint import pprint
scope = [
    'http://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',  # Allows read/write access to Sheets and their properties.
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',  # Allows full access to all files in Drive, including creating and deleting files.
    
]

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)



sheet = client.open_by_key('1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU').sheet1

#https://docs.google.com/spreadsheets/d/1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU/edit?usp=sharing

# After opening the sheet
print("Sheet opened:", sheet.title)

# After reading data (if applicable)
data = sheet.get_all_values()
print("Retrieved data:")
print(*data, sep="\n\t")