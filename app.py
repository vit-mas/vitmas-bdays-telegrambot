from flask import Flask, request
import requests
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# -------- GOOGLE SHEETS SETUP --------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SHEET_ID = os.environ.get("SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

# -------- USER STORAGE (TEMP IN-MEMORY OR FILE) --------
USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# -------- TELEGRAM --------

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# -------- LOGIC --------

def get_birthdays():
    return sheet.get_all_records()

def get_tomorrow_birthdays():
    data = get_birthdays()
    tomorrow = datetime.now() + timedelta(days=1)
    target = tomorrow.strftime("%d/%m")

    return [p for p in data if p["DOB"] == target]

def get_upcoming():
    data = get_birthdays()
    today = datetime.now()
    upcoming = []

    for p in data:
        day, month = map(int, p["DOB"].split("/"))
        next_bday = datetime(today.year, month, day)

        if next_bday < today:
            next_bday = datetime(today.year + 1, month, day)

        upcoming.append((next_bday, p))

    upcoming.sort()
    return upcoming[:3]

# -------- COMMANDS --------

def handle_start(chat_id):
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

    send_message(chat_id, "✅ Subscribed to birthday alerts!")

def handle_upcoming(chat_id):
    upcoming = get_upcoming()

    msg = "🎂 Upcoming Birthdays:\n\n"
    for i, (date, p) in enumerate(upcoming):
        msg += f"{i+1}. {p['Name']} - {date.strftime('%b %d')}\n"

    send_message(chat_id, msg)

# -------- WEBHOOK --------

@app.route("/webhook", methods=["POST"])
def webhook():
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

# -------- CRON ENDPOINT --------

@app.route("/send-birthday-alert", methods=["GET"])
def send_alert():
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

# -------- RUN --------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)