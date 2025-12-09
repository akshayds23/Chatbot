import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def ask_ai(text: str) -> str:
    resp = model.generate_content([
         "You are a friendly science tutor chatbot. "
        "Your domain is ONLY science: physics, chemistry, biology, astronomy, "
        "earth science, basic math used in science, and related scientific concepts.\n\n"
        "Rules:\n"
        "1. If the question is about science, answer clearly in simple English.\n"
        "2. If the question is NOT about science, do NOT answer it. Instead say: "
        "\"I'm a science-only chatbot, so I can only answer science questions.\"\n"
        "3. Do not switch to non-science topics even if the user insists.\n"
        "4. Respond with plain text only - NO markdown formatting, NO ** or ## or bullet points.\n\n"
        f"User question: {text}"
    ])
    return (resp.text or "").strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify({"error": "message is required"}), 400

    try:
        reply = ask_ai(msg) or "Sorry, I couldn't generate a response."
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Gemini Chatbot API running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

