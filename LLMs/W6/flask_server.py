# flask_server.py
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
import re

# --- Configure your Gemini API key ---
# Option A (recommended): set GEMINI_API_KEY as env var and use os.getenv
# Option B (quick): hard-code it here (replace the placeholder)
api_key = "AIzaSyCDc5IQ_tfTNGg_QsC99CBQ5s8sBhhbGvg"  # <<< replace with your key or set env var and modify
genai.configure(api_key=api_key)

app = Flask(__name__)

# Create model once (your environment uses model.generate_content)
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        # Correct method for your version
        response = model.generate_content(question)
        answer = response.text  # This contains the text output
        return jsonify({"answer": answer})
    except Exception as e:
        print("Flask server error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)