from flask import Flask, request
import requests

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789
API_URL = f"https://api.telegram.org/bot{TOKEN}/"
app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(API_URL+"sendMessage", json={"chat_id": chat_id, "text": text})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Welcome!")
        if text == "/admin" and chat_id == ADMIN_ID:
            send_message(chat_id, "Admin Panel Active")

    return "OK"
