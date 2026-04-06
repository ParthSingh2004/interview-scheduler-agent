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

def process_email(email: IncomingEmail):
    print(f"Processing email from: {email.sender}")
    
    # 1. Get the JSON dictionary from Gemini
    ai_decision = detect_intent(email.body)
    
    # 2. Act based on Intent
    if ai_decision.get("intent") == "SCHEDULE":
        print("Intent: Schedule. Generating unique link...")
        
        unique_link = generate_single_use_link()
        
        if unique_link:
            # 3. Add the date to the link if Gemini found one
            extracted_date = ai_decision.get("date")
            if extracted_date:
                unique_link = f"{unique_link}?date={extracted_date}"
                print(f"Added specific date to link: {extracted_date}")
            
            # 4. Send email
            send_scheduling_link(email.sender, unique_link)
        else:
            print("Failed to generate link.")
    else:
        print("Intent: Other. Ignoring.")