from flask import Flask, render_template, request, jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": msg}],
        "max_tokens": 60
    }
    r = requests.post(URL, headers=headers, json=data)
    if r.status_code == 200:
        ans = r.json()['choices'][0]['message']['content']
        return jsonify({"reply": ans.strip()})
    return jsonify({"reply": "Sorry, something went wrong."})
if __name__ == "__main__":
    app.run(debug=True)
