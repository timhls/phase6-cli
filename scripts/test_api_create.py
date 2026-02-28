import json
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright


def run():
    session_file = Path("~/.config/pyphase6/session.json").expanduser()
    with open(session_file) as f:
        session_data = json.load(f)

    local_storage = next(
        (
            o["localStorage"]
            for o in session_data.get("origins", [])
            if o["origin"] == "https://lernen.phase-6.de"
        ),
        None,
    )
    user_state = json.loads(
        next(item["value"] for item in local_storage if item["name"] == "persist:user")
    )
    user_data = json.loads(user_state["user"])

    jauth_token = user_data["jossoSessionId"]
    email = user_data["email"]
    owner_id = user_data["userDnsId"]
    client_id = str(uuid.uuid4())

    headers = {
        "x-clientid": client_id,
        "x-lbtoken": email,
        "x-jauthtoken": jauth_token,
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
    }

    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url="https://lernen.phase-6.de", extra_http_headers=headers
        )

        subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
        new_card_id = str(uuid.uuid4())

        payload = {
            "addSessionId": "",
            "addedByUserId": None,
            "addedUserName": None,
            "answer": "<p>API Answer Context Test</p>",
            "answerExample": None,
            "answerTranscription": None,
            "modificationDate": None,
            "order": None,
            "ownerId": owner_id,
            "question": "<p>API Question Context Test</p>",
            "questionAnswerId": None,
            "questionExample": None,
            "questionTranscription": None,
            "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
            "swappable": True,
            "unitIdToOwner": {"id": f"0000-{subject_id}", "ownerId": owner_id},
        }

        print(f"Creating card {new_card_id}...")
        resp = request_context.post(
            f"/server.integration/{owner_id}/cards/{new_card_id}", data=payload
        )

        if resp.ok:
            print("Card created successfully!")
            print(resp.json())
        else:
            print(f"Failed to create card: {resp.status} {resp.text()}")


if __name__ == "__main__":
    run()
