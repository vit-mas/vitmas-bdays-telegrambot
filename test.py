import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

# Open sheet
sheet = client.open_by_key("1xDlYvNxdfHD2MzvRqBnAfa5DXU57ic-bRousCXX6JqE").sheet1

# Fetch data
data = sheet.get_all_records()

print(data)