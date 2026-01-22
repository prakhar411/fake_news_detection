import os
import json
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found. Check your .env file.")

# --------------------------------------------------
# Initialize Gemini client (explicit + safe)
# --------------------------------------------------
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# Gemini fallback extraction
# --------------------------------------------------
def gemini_extract(text: str) -> dict:
    """
    Fallback extractor using Gemini when rule-based / spaCy extraction fails.
    Returns a structured dictionary.
    """

    prompt = f"""
You are an information extraction system for disaster event verification.

Extract structured information from the text below.

TEXT:
{text}

Return ONLY valid JSON in this exact schema:
{{
  "event_type": "string or null",
  "location": "string or null",
  "time": "string or null",
  "confidence": "low | medium | high"
}}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    # --------------------------------------------------
    # Parse Gemini output safely
    # --------------------------------------------------
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Safe fallback if Gemini returns malformed output
        return {
            "event_type": None,
            "location": None,
            "time": None,
            "confidence": "low"
        }
