from fastapi import FastAPI
from models import IncomingEmail
from services.llm_service import detect_intent
from services.calendly_service import generate_single_use_link

app = FastAPI(title="Interview Scheduler Webhook")


@app.post("/webhook")
async def handle_incoming_email(email: IncomingEmail):
    print(f"📥 [INBOX] New email from: {email.sender}")
    
    # Step 1: AI intent detection
    ai_decision = detect_intent(email.body)
    intent = ai_decision.get("intent")
    extracted_date = ai_decision.get("date")
    
    print(f"🧠 [AI AGENT] Decision -> Intent: {intent} | Date: {extracted_date}")
    
    # Step 2: Only act on relevant intents
    if intent in ["SCHEDULE", "RESCHEDULE"]:
        print("🔗 [CALENDLY] Generating single-use token...")
        
        unique_link = generate_single_use_link()
        
        if unique_link:
            # Append extracted date if present
            if extracted_date:
                unique_link = f"{unique_link}?date={extracted_date}"
            
            print("✅ [SUCCESS] Link generated and returned to Zapier")
            
            return {
                "status": "success",
                "intent": intent,
                "email": email.sender,
                "calendly_link": unique_link
            }
        else:
            print("❌ [ERROR] Failed to generate link.")
            return {
                "status": "error",
                "message": "Failed to generate Calendly link"
            }

    # Step 3: Ignore irrelevant emails
    print("⏭️ [IGNORED] Intent is OTHER.")
    return {
        "status": "ignored",
        "intent": intent
    }
