import os
import json
import uuid
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state=os.path.expanduser("~/.config/pyphase6/session.json")
        )
        page = context.new_page()

        try:
            # We just need any page to execute fetch from
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")

            owner_id = "2601821"
            subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
            new_card_id = str(uuid.uuid4())

            # Try without unitIdToOwner
            payload = {
                "addSessionId": "",
                "addedByUserId": None,
                "addedUserName": None,
                "answer": "<p>API Test Answer</p>",
                "answerExample": None,
                "answerTranscription": None,
                "modificationDate": None,
                "order": None,
                "ownerId": owner_id,
                "question": "<p>API Test Question</p>",
                "questionAnswerId": None,
                "questionExample": None,
                "questionTranscription": None,
                "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
                "swappable": True,
                "unitIdToOwner": None
            }

            url = f"https://lernen.phase-6.de/server.integration/{owner_id}/cards/{new_card_id}"
            
            print(f"Sending POST to {url}")
            result = page.evaluate("""([url, data]) => {
                return fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*'
                    },
                    body: JSON.stringify(data)
                }).then(r => r.text()).catch(e => e.toString())
            }""", [url, payload])
            
            print("Response:", json.dumps(result, indent=2))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
