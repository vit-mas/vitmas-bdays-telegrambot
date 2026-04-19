"""Configuration and environment setup."""
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

SHEET_ID = os.environ.get("SHEET_ID")
USERS_FILE = "users.json"

# Google Sheets OAuth setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
