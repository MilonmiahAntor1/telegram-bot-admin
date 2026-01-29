from flask import Flask, request
import requests

# 🔥 Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# ================== APP ==================
app = Flask(__name__)

# ================== BOT CONFIG ==================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 6999345304   # আপনার Telegram ID
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
# ===============================================

# ================== FIREBASE INIT ==================
cred = credentials.Certificate("/etc/secrets/firebase-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
# ===================================================

# ================== FUNCTIONS ==================
def send_message(chat_id, text):
    requests.post(
        API_URL + "sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )
# ==============================================

# ================== ROUTES ==================
@app.route("/", methods=["GET"])
def home():
    return "Bot is running 24/7"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        user = data["message"]["from"]

        # 🔹 /start command
        if text == "/start":
            send_message(
                chat_id,
                "👋 Welcome!\n\n💰 Taka Income Bot চালু আছে 24/7"
            )

            # 🔥 Save user to Firebase
            db.collection("users").document(str(chat_id)).set({
                "chat_id": chat_id,
                "username": user.get("username"),
                "first_name": user.get("first_name"),
                "balance": 0,
                "joined": True
            })

        # 🔹 /admin command
        elif text == "/admin" and chat_id == ADMIN_ID:
            users = db.collection("users").stream()
            total_users = len(list(users))

            send_message(
                chat_id,
                f"🔐 Admin Panel\n\n👥 Total Users: {total_users}"
            )

    return "OK"

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)