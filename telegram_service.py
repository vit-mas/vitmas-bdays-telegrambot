"""Telegram bot service operations."""
import requests
from config import BASE_URL

def send_message(chat_id, text):
    """Send a message to a user via Telegram."""
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})
