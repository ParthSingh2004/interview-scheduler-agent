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

def send_scheduling_link(recipient_email: str, dynamic_calendly_link: str):
    """Sends the dynamically generated Calendly link via Gmail SMTP."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "Let's schedule your interview!"

    body = f"""
    Hi there,

    Thanks for reaching out! We would love to chat. 
    Please pick a time that works for you using your unique scheduling link below:
    
    {dynamic_calendly_link}

    This link is for one-time use only.

    Best,
    Parth Singh
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"SMTP Error: {e}")