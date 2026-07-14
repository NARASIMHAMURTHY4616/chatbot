from flask import Flask, render_template, request, jsonify
from config import Config
from database import MongoDB
from gemini import GeminiChat

Config.validate()

app = Flask(__name__)
db = MongoDB()
gemini = GeminiChat()

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/chats")
def chats():
    return jsonify(db.get_all_chats())

@app.post("/api/chat/new")
def new_chat():
    return jsonify(db.create_chat())

@app.get("/api/chat/<chat_id>")
def get_chat(chat_id):
    chat = db.get_chat(chat_id)
    if not chat:
        return jsonify({"error":"Chat not found"}),404
    return jsonify(chat)

@app.post("/api/chat/<chat_id>/message")
def send_message(chat_id):
    data=request.get_json(silent=True) or {}
    message=(data.get("message") or "").strip()
    if not message:
        return jsonify({"error":"Message required"}),400
    chat=db.get_chat(chat_id)
    if not chat:
        return jsonify({"error":"Chat not found"}),404
    db.add_message(chat_id,"user",message)
    chat=db.get_chat(chat_id)
    reply=gemini.generate_response(chat["messages"])
    db.add_message(chat_id,"assistant",reply)
    return jsonify({"reply":reply})

@app.delete("/api/chat/<chat_id>")
def delete_chat(chat_id):
    if db.delete_chat(chat_id):
        return jsonify({"success":True})
    return jsonify({"error":"Chat not found"}),404

if __name__=="__main__":
    app.run(debug=True)
