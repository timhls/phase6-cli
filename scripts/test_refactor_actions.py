import uuid
from test_refactor_client import Phase6API
from playwright.sync_api import sync_playwright

class ExtendedAPI(Phase6API):
    def update_card(self, subject_id, card_id, question, answer):
        headers, owner_id = self._get_api_headers()
        with sync_playwright() as p:
            ctx = p.request.new_context(base_url="https://lernen.phase-6.de", extra_http_headers=headers)
            # update needs the original card id
            payload = {
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
            # wait, is the PUT request different from POST?
            resp = ctx.put(f"/server.integration/{owner_id}/cards/{card_id}", data=payload)
            return resp.json()

    def delete_card(self, card_id):
        headers, owner_id = self._get_api_headers()
        with sync_playwright() as p:
            ctx = p.request.new_context(base_url="https://lernen.phase-6.de", extra_http_headers=headers)
            # delete request
            resp = ctx.delete(f"/server.integration/{owner_id}/cards/{card_id}")
            return resp.json()

if __name__ == "__main__":
    api = ExtendedAPI()
    subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
    
    # 1. Add
    print("Adding...")
    resp, card_id = api.add_card(subject_id, "Test Q", "Test A")
    print(resp, card_id)
    
    # 2. Update
    print("Updating...")
    resp = api.update_card(subject_id, card_id, "Test Q Updated", "Test A Updated")
    print(resp)
    
    # 3. Delete
    print("Deleting...")
    resp = api.delete_card(card_id)
    print(resp)
