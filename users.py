"""User management operations."""
from sheets_service import get_all_users, add_user as add_user_to_sheet

def load_users():
    """Load all registered user IDs from sheets."""
    return get_all_users()

def save_user(chat_id):
    """Register a new user if not already registered."""
    users = load_users()
    if chat_id not in users:
        add_user_to_sheet(chat_id)

def is_user_registered(chat_id):
    """Check if a user is already registered."""
    return chat_id in load_users()
