import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Updated to use Gemini 2.5 Flash
model = genai.GenerativeModel('gemini-2.5-flash')

def detect_intent(email_body: str) -> bool:
    """Returns True if the email is asking to schedule an interview."""
    
    # Let's print exactly what Zapier sent to make sure it's not empty
    print(f"\n--- DEBUG: Text Sent to Gemini ---\n{email_body}\n----------------------------------")
    
    system_prompt = """
    You are an AI assistant analyzing email intents. 
    Determine if the sender wants to schedule, propose, or arrange an interview, meeting, or call.
    This includes:
    - Direct questions ("Can we schedule?")
    - Proposals ("Let's have the interview on Monday")
    - Expressing availability ("I am free next week")
    
    If the email is about scheduling or having an interview, reply with ONLY the word: SCHEDULE.
    If it is about anything else, reply with ONLY the word: OTHER.
    """
    
    try:
        response = model.generate_content(
            f"{system_prompt}\n\nEmail:\n{email_body}",
            generation_config=genai.GenerationConfig(
                temperature=0.0
            )
        )
        result = response.text.strip().upper()
        
        # Let's print exactly what Gemini decided
        print(f"--- DEBUG: Gemini Decision: {result} ---\n")
        
        return "SCHEDULE" in result
    except Exception as e:
        print(f"Gemini LLM Error: {e}")
        return False