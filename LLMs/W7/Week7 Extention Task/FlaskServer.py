from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import io
import os

app = Flask(__name__)

# set up Gemini
api_key = "AIzaSyB2P0_bGLgloGJwyswLPMedv1XUpazrIEI"  # <<< replace with your key or set env var and modify
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


@app.route("/summeriseCSV", methods=["POST"])
def summerise_csv():
    """
    Upload a CSV -> send a trimmed version to LLM -> get back a text summary.
    """
    if "file" not in request.files:
        return jsonify({"error": "No CSV file uploaded. Use form-data with key 'file'."}), 400

    csv_file = request.files["file"]
    try:
        raw = csv_file.read().decode("utf-8", errors="ignore")
        lines = raw.splitlines()
        head_lines = lines[:50]  # limit for prompt size
        csv_preview = "\n".join(head_lines)

        prompt = f"""
You are a data analyst. Summarise the following CSV snippet.
Say what the dataset seems to track, list key columns, and suggest 2-3 follow-up analyses.

CSV:
{csv_preview}
"""
        resp = model.generate_content(prompt)
        summary = resp.text.strip()

        return jsonify({
            "summary": summary,
            "rows_previewed": len(head_lines)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/anysis", methods=["POST"])
def anysis():
    """
    Upload a CSV -> LLM generates a NEW CSV (analysis + chart instructions)
    -> return it as a downloadable CSV file.
    """
    if "file" not in request.files:
        return jsonify({"error": "No CSV file uploaded. Use form-data with key 'file'."}), 400

    csv_file = request.files["file"]
    try:
        raw = csv_file.read().decode("utf-8", errors="ignore")
        lines = raw.splitlines()
        head_lines = lines[:50]
        csv_preview = "\n".join(head_lines)

        prompt = f"""
You are helping a student analyse sales data.

Create a NEW CSV that has TWO sections:

analysis,metric,value,notes
...rows here...

charts,chart_type,x_axis,y_axis,description
...rows here...

Use ONLY columns you can see in the preview. If you can't see dates, don't group by month.
Return ONLY CSV text. Do NOT wrap in markdown.

CSV preview:
{csv_preview}
"""
        resp = model.generate_content(prompt)
        analysis_csv_text = resp.text.strip()

        # return as file
        mem = io.BytesIO()
        mem.write(analysis_csv_text.encode("utf-8"))
        mem.seek(0)

        return send_file(
            mem,
            mimetype="text/csv",
            as_attachment=True,
            download_name="generated_sales_analysis.csv"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
