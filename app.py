from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found! Please set it in .env or Render environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Load portfolio.json
with open("portfolio.json", "r", encoding="utf-8") as f:
    portfolio_data = json.load(f)

model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Chatbot API only
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    prompt = f"""
    You are Sandip Gupta answering questions on your portfolio website.

    Portfolio Data:
    {json.dumps(portfolio_data, indent=2)}

    Question: {user_message}
    Answer politely and concisely, only using the portfolio data provided.
    """

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"⚠️ Error: {str(e)}"

    return jsonify({"reply": answer})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
