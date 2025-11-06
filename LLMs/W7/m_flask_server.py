# flask_server.py
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
import re
import os

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
    
# --- New Route 1: Clean text and save to file ---
@app.route("/clean", methods=["POST"])
def clean_text():
    data = request.get_json()
    raw_text = data.get("text", "")
    if not raw_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Ask Gemini to clean the text
        prompt = (
            "Clean this text by fixing spelling, removing unnecessary characters, "
            "and formatting into clear sentences. Do not add extra information.\n\n"
            f"Text: {raw_text}"
        )
        response = model.generate_content(prompt)
        cleaned = response.text.strip()

        # Save to file
        with open("cleaned.txt", "w", encoding="utf-8") as f:
            f.write(cleaned)

        return jsonify({
            "message": "Text cleaned and saved",
            "preview": cleaned[:200]  # return first 200 chars
        })
    except Exception as e:
        print("Error in /clean:", e)
        return jsonify({"error": str(e)}), 500


# --- New Route 2: Extract info from cleaned file ---
@app.route("/extract", methods=["GET"])
def extract_info():
    if not os.path.exists("cleaned.txt"):
        return jsonify({"error": "cleaned.txt not found. Please run /clean first."}), 400

    try:
        with open("cleaned.txt", "r", encoding="utf-8") as f:
            cleaned_text = f.read()

        # Ask Gemini to extract entities
        prompt = (
            "Extract all dates, names, and locations from the following text. "
            "Return the result as valid JSON with keys: dates, names, locations, pets.\n\n"
            f"{cleaned_text}"
        )
        response = model.generate_content(prompt)

        extracted = response.text.strip()

        # Try to parse JSON (in case Gemini gives valid JSON)
        try:
            extracted_json = json.loads(extracted)
        except json.JSONDecodeError:
            # If Gemini output is not valid JSON, save raw text
            extracted_json = {"raw_output": extracted}

        # Save structured output
        with open("extracted.json", "w", encoding="utf-8") as f:
            json.dump(extracted_json, f, indent=2)

        return jsonify({
            "message": "Information extracted and saved",
            "data": extracted_json
        })
    except Exception as e:
        print("Error in /extract:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/classify_feedback", methods=["GET"])
def classify_feedback():
    feedback_folder = "game_feedback"
    summary = {"positive": [], "medium": [], "negative": []}

    try:
        if not os.path.exists(feedback_folder):
            return jsonify({"error": "Feedback folder not found."}), 400

        files = [f for f in os.listdir(feedback_folder) if f.endswith(".txt")]
        if not files:
            return jsonify({"error": "No feedback files found in folder."}), 400

        # Step 1: Classify each feedback
        for filename in files:
            with open(os.path.join(feedback_folder, filename), "r", encoding="utf-8") as f:
                feedback = f.read()

            try:
                prompt = (
                    "Classify this feedback as positive, medium, or negative. "
                    "Return only the category.\n\n"
                    f"Feedback: {feedback}"
                )
                response = model.generate_content(prompt)
                category = response.text.strip().lower()
            except Exception as e:
                print(f"Error classifying '{filename}':", e)
                category = "medium"  # fallback

            if category in summary:
                summary[category].append(feedback)
            else:
                summary["medium"].append(feedback)

        # Step 2: Generate summary for each category
        category_summaries = {}
        for cat, texts in summary.items():
            if texts:
                combined_text = "\n".join(texts[:10])  # limit for prompt size
                prompt = (
                    f"Summarize the following {cat} feedback in 1-2 concise sentences:\n\n{combined_text}"
                )
                try:
                    response = model.generate_content(prompt)
                    category_summaries[cat] = response.text.strip()
                except Exception as e:
                    category_summaries[cat] = "Summary unavailable."
            else:
                category_summaries[cat] = "No feedback in this category."

        # Save both classified feedback and summaries
        with open("feedback_summary.json", "w", encoding="utf-8") as f:
            json.dump({"feedback": summary, "summaries": category_summaries}, f, indent=2)

        # Simple response only
        return jsonify({
            "message": "Feedback classified and summarized. Results saved to 'feedback_summary.json'."
        })

    except Exception as e:
        print("Error in /classify_feedback:", e)
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        print("Error in /classify_feedback:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/summarise_film", methods=["GET"])
def summarise_film():
    file_path = "film_summary.txt"
    if not os.path.exists(file_path):
        return jsonify({"error": "film_summary.txt not found."}), 400

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            film_text = f.read()

        # Prompt with constraints
        prompt = (
            "Summarise the following film text in exactly 5 sentences. "
            "Make sure the summary is concise and captures the main points.\n\n"
            f"{film_text}"
        )

        response = model.generate_content(prompt)
        summary = response.text.strip()

        # Save the summary
        with open("film_summary_short.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        return jsonify({
            "message": "Film summary created and saved",
            "summary": summary
        })

    except Exception as e:
        print("Error in /summarise_film:", e)
        return jsonify({"error": str(e)}), 500








if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)