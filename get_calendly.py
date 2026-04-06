import requests

# 1. PASTE YOUR REAL TOKEN HERE INSIDE THE QUOTES
TOKEN = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzc1NDc3MzMyLCJqdGkiOiI3ZTZlZGFkNC1hM2MxLTQ5NzQtOGM4Yy0yNDI5YmEzMWQ3MTYiLCJ1c2VyX3V1aWQiOiJjOThkZGQ4NC02NmQzLTQwOWYtYWU0My0xNDE4YmU1YjE1ZGIiLCJzY29wZSI6ImF2YWlsYWJpbGl0eTpyZWFkIGF2YWlsYWJpbGl0eTp3cml0ZSBldmVudF90eXBlczpyZWFkIGV2ZW50X3R5cGVzOndyaXRlIGxvY2F0aW9uczpyZWFkIHJvdXRpbmdfZm9ybXM6cmVhZCBzaGFyZXM6d3JpdGUgc2NoZWR1bGVkX2V2ZW50czpyZWFkIHNjaGVkdWxlZF9ldmVudHM6d3JpdGUgc2NoZWR1bGluZ19saW5rczp3cml0ZSBncm91cHM6cmVhZCBvcmdhbml6YXRpb25zOnJlYWQgb3JnYW5pemF0aW9uczp3cml0ZSB1c2VyczpyZWFkIGFjdGl2aXR5X2xvZzpyZWFkIGRhdGFfY29tcGxpYW5jZTp3cml0ZSBvdXRnb2luZ19jb21tdW5pY2F0aW9uczpyZWFkIHdlYmhvb2tzOnJlYWQgd2ViaG9va3M6d3JpdGUifQ.uUeJrehmGEr9AVWOM0Cxdi24pEOp351BbbalKtXCo2mZmTZTli4dmIwXnj4GVYf8-GDAjxx1OXAQX3bjd1hpzA" 

def get_event_uris():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    print("Fetching your user details...")
    user_response = requests.get("https://api.calendly.com/users/me", headers=headers)
    
    if user_response.status_code != 200:
        print(f"Error checking user: {user_response.text}")
        return
        
    user_uri = user_response.json()['resource']['uri']
    
    print("Fetching your event types...\n")
    events_response = requests.get(f"https://api.calendly.com/event_types?user={user_uri}", headers=headers)
    
    events = events_response.json().get('collection', [])
    
    for event in events:
        if event['active']:
            print(f"Event Name: {event['name']}")
            print(f"EVENT_TYPE_URI: {event['uri']}")
            print("-" * 40)

if __name__ == "__main__":
    get_event_uris()