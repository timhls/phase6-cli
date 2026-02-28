import json
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright

class Phase6API:
    def __init__(self):
        self.session_file = Path("~/.config/pyphase6/session.json").expanduser()
        
    def _get_api_headers(self):
        with open(self.session_file) as f:
            session_data = json.load(f)
            
        local_storage = next((o["localStorage"] for o in session_data.get("origins", []) if o["origin"] == "https://lernen.phase-6.de"), None)
        user_state = json.loads(next(item["value"] for item in local_storage if item["name"] == "persist:user"))
        user_data = json.loads(user_state["user"])
        
        jauth_token = user_data["jossoSessionId"]
        email = user_data["email"]
        owner_id = user_data["userDnsId"]
        client_id = str(uuid.uuid4())
        
        return {
            'x-clientid': client_id,
            'x-lbtoken': email,
            'x-jauthtoken': jauth_token,
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json'
        }, owner_id

    def get_subjects(self):
        headers, _ = self._get_api_headers()
        with sync_playwright() as p:
            ctx = p.request.new_context(base_url="https://lernen.phase-6.de", extra_http_headers=headers)
            # wait, subjectsCombined needs POST with empty body
            resp = ctx.post("/server.integration/subjectsCombined", data={})
            return resp.json()

    def add_card(self, subject_id, question, answer):
        headers, owner_id = self._get_api_headers()
        with sync_playwright() as p:
            ctx = p.request.new_context(base_url="https://lernen.phase-6.de", extra_http_headers=headers)
            new_card_id = str(uuid.uuid4())
            payload = {
                "addSessionId": "",
                "addedByUserId": None,
                "addedUserName": None,
                "answer": f"<p>{answer}</p>",
                "answerExample": None,
                "answerTranscription": None,
                "modificationDate": None,
                "order": None,
                "ownerId": owner_id,
                "question": f"<p>{question}</p>",
                "questionAnswerId": None,
                "questionExample": None,
                "questionTranscription": None,
                "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
                "swappable": True,
                "unitIdToOwner": {"id": f"0000-{subject_id}", "ownerId": owner_id}
            }
            resp = ctx.post(f"/server.integration/{owner_id}/cards/{new_card_id}", data=payload)
            return resp.json(), new_card_id

if __name__ == "__main__":
    api = Phase6API()
    print("Subjects:")
    subs = api.get_subjects()
    print(subs['replyContent']['subjects'][0]['subjectContent']['name'])
    
    print("Adding card...")
    resp, card_id = api.add_card("0b82cb9c-0175-490d-d14f-8c7c400a4c1f", "Refactored Q", "Refactored A")
    print(resp)
