import json
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright

def run():
    session_file = Path("~/.config/pyphase6/session.json").expanduser()
    
    with open(session_file) as f:
        session_data = json.load(f)
        
    local_storage = None
    for origin in session_data.get("origins", []):
        if origin["origin"] == "https://lernen.phase-6.de":
            local_storage = origin["localStorage"]
            break
            
    if not local_storage:
        print("No local storage found")
        return
        
    user_state_str = next((item["value"] for item in local_storage if item["name"] == "persist:user"), None)
    if not user_state_str:
        print("No persist:user found")
        return
        
    user_state = json.loads(user_state_str)
    user_data = json.loads(user_state["user"])
    
    jauth_token = user_data["jossoSessionId"]
    email = user_data["email"]
    owner_id = user_data["userDnsId"]
    client_id = "a47553e3-7451-4605-9f3f-b42cd4d16d64" # Just a uuid, let's generate one
    client_id = str(uuid.uuid4())
    
    print(f"Token: {jauth_token}")
    print(f"Email: {email}")
    print(f"Owner ID: {owner_id}")
    
    headers = {
        'x-clientid': client_id,
        'x-lbtoken': email,
        'x-jauthtoken': jauth_token,
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json'
    }
    
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url="https://lernen.phase-6.de",
            extra_http_headers=headers
        )
        
        # Test fetching subjects
        print("Fetching subjects via API context...")
        resp = request_context.post(f"/server.integration/subjectsCombined")
        
        if resp.ok:
            data = resp.json()
            print(data)
        else:
            print(f"Failed to fetch subjects: {resp.status} {resp.text()}")

        # Now test creating a card!
        subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
        new_card_id = str(uuid.uuid4())
        
        # We also need a unitIdToOwner... let's just use the same subject_id or None
        payload = {
            "addSessionId": "",
            "addedByUserId": None,
            "addedUserName": None,
            "answer": "<p>API Context Answer</p>",
            "answerExample": None,
            "answerTranscription": None,
            "modificationDate": None,
            "order": None,
            "ownerId": owner_id,
            "question": "<p>API Context Question</p>",
            "questionAnswerId": None,
            "questionExample": None,
            "questionTranscription": None,
            "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
            "swappable": True,
            "unitIdToOwner": None
        }
        
        print(f"Creating card {new_card_id}...")
        resp = request_context.post(f"/server.integration/{owner_id}/cards/{new_card_id}", data=payload)
        
        if resp.ok:
            print("Card created successfully!")
            print(resp.json())
        else:
            print(f"Failed to create card: {resp.status} {resp.text()}")

if __name__ == "__main__":
    run()
