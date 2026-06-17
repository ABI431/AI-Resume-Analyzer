import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# 1. Added target_role as a parameter
def analyze_resume(resume_text, target_role, job_description=""):

    # 2. Updated the prompt context and expected JSON format
    prompt = f"""
You are an advanced ATS Resume Analyzer.

Target Role:
{target_role}

Job Description:
{job_description}

Analyze the resume and return ONLY valid JSON.

{{
  "resume_score": 0,
  "ats_score": 0,
  "role_fit_score": 0,
  "job_match_score": 0,

  "skills": [],
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "suggestions": [],

  "matched_skills": [],
  "keywords_missing": [],

  "sections_present": [],
  "sections_missing": [],

  "interview_questions": []
}}

Resume:
{resume_text}
"""

    response = model.generate_content(prompt)

    if not response.text:
        return {
            "error": "Empty response from Gemini"
    }

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        return {
        "error": "Failed to parse Gemini response",
        "raw_response": text
    }