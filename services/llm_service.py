import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Updated to use Gemini 2.5 Flash
model = genai.GenerativeModel('gemini-2.5-flash')

import json

def detect_intent(email_body: str) -> dict:
    """Returns a dictionary with intent and optional date."""
    
    # We tell Gemini today's exact date so it can do the math
    system_prompt = """
    You are an AI assistant. Today's date is April 6, 2026.
    Determine if the sender wants to schedule an interview. 
    If they mention a specific date, extract it in YYYY-MM-DD format.
    
    You MUST reply with ONLY a valid JSON object. Do not include markdown formatting.
    Example 1: {"intent": "SCHEDULE", "date": "2026-04-10"}
    Example 2: {"intent": "SCHEDULE", "date": null}
    Example 3: {"intent": "OTHER", "date": null}
    """
    
    try:
        response = model.generate_content(f"{system_prompt}\n\nEmail:\n{email_body}")
        
        # Clean the output just in case Gemini adds markdown blocks
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(clean_text)
        
        print(f"--- DEBUG: Gemini JSON: {result} ---")
        return result
        
    except Exception as e:
        print(f"Gemini LLM Error: {e}")
        return {"intent": "OTHER", "date": None}