from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = []

@app.route('/api/users')
def get_users():
    return jsonify(USERS)

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    msg = request.json.get("text", "")
    return {"status":"sent","message":msg}
