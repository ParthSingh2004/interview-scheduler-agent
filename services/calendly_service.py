import os
import requests
from dotenv import load_dotenv

load_dotenv()

CALENDLY_TOKEN = os.getenv("CALENDLY_TOKEN")
EVENT_TYPE_URI = os.getenv("CALENDLY_EVENT_TYPE_URI")

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_single_use_link():
    token = os.getenv("CALENDLY_API_TOKEN")
    event_uri = os.getenv("CALENDLY_EVENT_URI")
    
    # 1. Print to verify the .env is actually loaded
    print(f"--- DEBUG: Using Event URI: {event_uri} ---")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. The payload requesting exactly 1 use
    payload = {
        "max_event_count": 1,
        "owner": event_uri,
        "owner_type": "EventType"
    }
    
    # 3. The STRICT endpoint for generating links (This is usually where the 404 happens)
    api_url = "https://api.calendly.com/scheduling_links"
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 201:
            booking_url = response.json()["resource"]["booking_url"]
            print(f"Success! Link generated: {booking_url}")
            return booking_url
        else:
            print(f"Calendly API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Failed to connect to Calendly: {e}")
        return None