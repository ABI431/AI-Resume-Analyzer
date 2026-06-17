from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return {
        "message": "AI Resume Analyzer Running"
    }

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    target_role = request.form.get("target_role", "")
    job_description = request.form.get("job_description", "")

    analysis = analyze_resume(
        text,
        target_role,
        job_description
    )

    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True)