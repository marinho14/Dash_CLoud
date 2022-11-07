import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("exoesquelet-eafit-sheet-bcb340f88950.json", scope)
client = gspread.authorize(credentials)

#sheet = client.create("NewDatabase")
#sheet.share('andresfelipebarretojimenez@gmail.com', perm_type='user', role='writer')
#sheet.share('marinosebastian5@gmail.com', perm_type='user', role='writer')


# Open the spreadsheet
sheet = client.open("NewDatabase").sheet1

# export df to a sheet
#sheet.update('A1', [[1, 2], [3, 4]])
sheet.update('A3', [[5, 6], [7, 8]])

values_list = sheet.row_values(1)
#values_list = sheet.col_values(1)

print(values_list)