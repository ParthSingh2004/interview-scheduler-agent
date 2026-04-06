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
    
    # 1. Check Intent via Gemini
    wants_interview = detect_intent(email.body)
    
    # 2. Act based on Intent
    if wants_interview:
        print("Intent: Schedule. Generating unique link...")
        
        # 3. Get unique link
        unique_link = generate_single_use_link()
        
        if unique_link:
            # 4. Send email
            send_scheduling_link(email.sender, unique_link)
        else:
            print("Failed to generate link. Email not sent.")
    else:
        print("Intent: Other. Ignoring.")