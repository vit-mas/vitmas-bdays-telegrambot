from flask import Flask, request
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

USERS_FILE = "users.json"
BIRTHDAYS_FILE = "birthdays.json"


# ------------------ HELPERS ------------------

def load_users():
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def load_birthdays():
    with open(BIRTHDAYS_FILE) as f:
        return json.load(f)

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})


# ------------------ COMMANDS ------------------

def handle_start(chat_id):
    users = load_users()

    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

    send_message(chat_id, "✅ You will now receive birthday alerts!")

def handle_stop(chat_id):
    users = load_users()
    users = [u for u in users if u != chat_id]
    save_users(users)

    send_message(chat_id, "❌ You will no longer receive alerts.")

def handle_upcoming(chat_id):
    birthdays = load_birthdays()

    today = datetime.now()

    upcoming = []
    for b in birthdays:
        dob = datetime.strptime(b["dob"], "%Y-%m-%d")
        next_bday = dob.replace(year=today.year)

        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)

        upcoming.append((next_bday, b))

    upcoming.sort()

    msg = "🎂 Upcoming Birthdays:\n\n"
    for i in range(min(3, len(upcoming))):
        date, person = upcoming[i]
        msg += f"{i+1}. {person['name']} - {date.strftime('%b %d')}\n"

    send_message(chat_id, msg)


# ------------------ WEBHOOK ------------------

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        handle_start(chat_id)
    elif text == "/stop":
        handle_stop(chat_id)
    elif text == "/upcoming":
        handle_upcoming(chat_id)

    return "ok"


# ------------------ CRON ENDPOINT ------------------

@app.route("/send-birthday-alert", methods=["GET"])
def send_birthday_alert():
    users = load_users()
    birthdays = load_birthdays()

    tomorrow = datetime.now() + timedelta(days=1)

    matches = []
    for b in birthdays:
        dob = datetime.strptime(b["dob"], "%Y-%m-%d")

        if dob.day == tomorrow.day and dob.month == tomorrow.month:
            matches.append(b)

    if not matches:
        return "No birthdays"

    msg = "🎉 Tomorrow's Birthdays:\n\n"
    for p in matches:
        msg += f"- {p['name']} ({p['phone']})\n"

    for user in users:
        send_message(user, msg)

    return "Sent"


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)