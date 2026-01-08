from flask import Flask, request
import requests

app = Flask(__name__)

# ====== BOT CONFIG ======
BOT_TOKEN = "8506626670:AAFAybkMR3PoHXbE60wUcoi7uFk0PSwaMjI"
ADMIN_ID = 6999345304
# ========================

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(chat_id, text):
    requests.post(API_URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["GET"])
def home():
    return "Bot is running 24/7"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "👋 Welcome!\n\n💰 Taka Income Bot চালু আছে 24/7"
            )

        elif text == "/admin" and chat_id == ADMIN_ID:
            send_message(chat_id, "🔐 Admin Panel Active")

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)