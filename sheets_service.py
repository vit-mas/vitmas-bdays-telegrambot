"""Google Sheets service operations."""
from config import client, SHEET_ID

def get_sheet():
    """Get the main birthday sheet."""
    return client.open_by_key(SHEET_ID).sheet1

def get_user_sheet():
    """Get the users worksheet."""
    return client.open_by_key(SHEET_ID).worksheet("Users")

def get_all_birthdays():
    """Fetch all birthday records from the sheet."""
    return get_sheet().get_all_records()

def add_user(chat_id):
    """Add a new user to the users sheet."""
    user_sheet = get_user_sheet()
    user_sheet.append_row([chat_id])

def get_all_users():
    """Fetch all registered user IDs."""
    user_sheet = get_user_sheet()
    data = user_sheet.get_all_records()
    return [int(u["ChatID"]) for u in data]
