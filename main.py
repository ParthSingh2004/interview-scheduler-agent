from fastapi import FastAPI, BackgroundTasks
from models import IncomingEmail
from services.llm_service import detect_intent
from services.email_service import send_scheduling_link
from services.calendly_service import generate_single_use_link

app = FastAPI(title="Interview Scheduler Webhook")

@app.post("/webhook")
async def handle_incoming_email(email: IncomingEmail, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_email, email)
    return {"status": "received", "message": "Processing in background"}

from services.email_service import send_scheduling_link, send_reschedule_link

def process_email(email: IncomingEmail):
    print(f" [INBOX] New email from: {email.sender}")
    
    ai_decision = detect_intent(email.body)
    intent = ai_decision.get("intent")
    extracted_date = ai_decision.get("date")
    
    print(f" [AI AGENT] Decision -> Intent: {intent} | Date: {extracted_date}")
    
    if intent in ["SCHEDULE", "RESCHEDULE"]:
        print(" [CALENDLY] Generating single-use token...")
        unique_link = generate_single_use_link()
        
        if unique_link:
            if extracted_date:
                unique_link = f"{unique_link}?date={extracted_date}"
                
            if intent == "SCHEDULE":
                send_scheduling_link(email.sender, unique_link)
            elif intent == "RESCHEDULE":
                send_reschedule_link(email.sender, unique_link)
                
            print(" [SUCCESS] Email dispatched!")
        else:
            print(" [ERROR] Failed to generate link.")
    else:
        print("⏭ [IGNORED] Intent is OTHER.")