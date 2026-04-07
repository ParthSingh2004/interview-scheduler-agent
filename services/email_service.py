import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SMTP_EMAIL")
APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

def send_email(to_email: str, subject: str, body: str):
    """Core function to send an email."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"SMTP Error: {e}")

def send_scheduling_link(recipient_email: str, dynamic_calendly_link: str):
    """Sends the initial scheduling link."""
    subject = "Let's schedule your interview!"
    body = f"""Hi there,

Thanks for reaching out! We would love to chat. 
Please pick a time that works for you using your unique scheduling link below:

{dynamic_calendly_link}

This link is for one-time use only.

Best,
Parth Singh
"""
    send_email(recipient_email, subject, body)

def send_reschedule_link(to_email: str, unique_link: str):
    """Sends the reschedule link."""
    subject = "Rescheduling your Interview"
    body = f"""Hello,

No problem at all, I completely understand. Let's find a time that works better for you. 

Please select a new time using this link:
{unique_link}

Best regards,
Parth Singh

--
🤖 This email was drafted by Parth's AI Scheduling Assistant. 
If none of these times work, just reply directly and Parth will take over!
"""
    send_email(to_email, subject, body)