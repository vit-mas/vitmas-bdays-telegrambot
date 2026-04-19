"""Command handlers for Telegram bot."""
from users import save_user
from telegram_service import send_message
from birthday_logic import get_upcoming_birthdays

def handle_start(chat_id):
    """Handle /start command - subscribe user."""
    save_user(chat_id)
    send_message(chat_id, "✅ Subscribed to birthday alerts!")

def handle_upcoming(chat_id):
    """Handle /upcoming command - show next 3 birthdays."""
    upcoming = get_upcoming_birthdays()

    msg = "🎂 Upcoming Birthdays:\n\n"
    for i, (date, p) in enumerate(upcoming):
        msg += f"{i+1}. {p['Name']} - {date.strftime('%b %d')}\n"

    send_message(chat_id, msg)
