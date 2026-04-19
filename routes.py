"""Flask routes for webhook and cron endpoints."""
from flask import Blueprint, request
from handlers import handle_start, handle_upcoming
from users import load_users
from telegram_service import send_message
from birthday_logic import get_tomorrow_birthdays

routes = Blueprint('routes', __name__)

@routes.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming Telegram messages."""
    data = request.json

    if "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text == "/start":
        handle_start(chat_id)
    elif text == "/upcoming":
        handle_upcoming(chat_id)

    return "ok"

@routes.route("/send-birthday-alert", methods=["GET"])
def send_alert():
    """Cron endpoint to send birthday alerts for tomorrow's birthdays."""
    users = load_users()
    matches = get_tomorrow_birthdays()

    if not matches:
        return "No birthdays"

    msg = "🎉 Tomorrow's Birthdays:\n\n"
    for p in matches:
        msg += f"- {p['Name']} ({p['Phone']})\n"

    for u in users:
        send_message(u, msg)

    return "Sent"
