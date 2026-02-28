import json
import uuid
from pathlib import Path
from typing import List, Tuple, Dict

from playwright.sync_api import sync_playwright

from pyphase6.models import Subject, VocabItem, VocabList


class AuthError(Exception):
    pass


class APIConnectionError(Exception):
    pass


class Phase6Client:
    BASE_URL = "https://lernen.phase-6.de"
    SESSION_FILE = "~/.config/pyphase6/session.json"

    def __init__(self):
        self.session_file = Path(self.SESSION_FILE).expanduser()

    def login(self, username: str, password: str) -> None:
        """
        Uses Playwright to automate the login flow on the web app and extract cookies.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                page.goto(f"{self.BASE_URL}/v2/#/login", wait_until="networkidle")

                page.fill(
                    'input[type="email"], input[type="e-mail"], input[name="username"]', username
                )
                page.fill('input[type="password"]', password)
                page.get_by_role("button", name="Login").click()

                # Wait for any navigation to complete, giving it 5s to process the login
                page.wait_for_timeout(5000)

                self.session_file.parent.mkdir(parents=True, exist_ok=True)
                context.storage_state(path=self.session_file)

            except Exception as e:
                raise AuthError(f"Login failed: {e}")
            finally:
                browser.close()

    def _get_api_headers(self) -> Tuple[Dict[str, str], str]:
        if not self.session_file.exists():
            raise AuthError("Not logged in. Please run 'pyphase6 login' first.")

        with open(self.session_file) as f:
            session_data = json.load(f)

        local_storage = None
        for origin in session_data.get("origins", []):
            if origin["origin"] == self.BASE_URL:
                local_storage = origin["localStorage"]
                break

        if not local_storage:
            raise AuthError("Invalid session state. Please run 'pyphase6 login' again.")

        user_state_str = next(
            (item["value"] for item in local_storage if item["name"] == "persist:user"), None
        )
        if not user_state_str:
            raise AuthError(
                "Invalid session state (no user data). Please run 'pyphase6 login' again."
            )

        user_state = json.loads(user_state_str)
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
        return headers, owner_id

    def get_subjects(self) -> List[Subject]:
        headers, _ = self._get_api_headers()

        with sync_playwright() as p:
            ctx = p.request.new_context(base_url=self.BASE_URL, extra_http_headers=headers)
            resp = ctx.post("/server.integration/subjectsCombined", data={})

            if not resp.ok:
                raise APIConnectionError(f"API returned non-200 code: {resp.status} {resp.text()}")

            data = resp.json()
            if data.get("httpCode") != 200:
                raise APIConnectionError(f"API returned non-200 code in JSON: {data}")

        subjects_data = data.get("replyContent", {}).get("subjects", [])
        subjects = []
        for s in subjects_data:
            if "subjectId" in s and "subjectContent" in s:
                subjects.append(Subject(**s))
        return subjects

    def get_vocabulary(self, subject_id: str, offset: int = 0, limit: int = 1000) -> VocabList:
        headers, _ = self._get_api_headers()

        with sync_playwright() as p:
            ctx = p.request.new_context(base_url=self.BASE_URL, extra_http_headers=headers)
            resp = ctx.post("/server.integration/cardList", data={"subjectId": subject_id})

            if not resp.ok:
                raise APIConnectionError(f"API returned non-200 code: {resp.status} {resp.text()}")

            data = resp.json()
            if data.get("httpCode") != 200:
                raise APIConnectionError(f"API returned non-200 code in JSON: {data}")

        cards_data = data.get("replyContent", {}).get("cards", [])
        items = [VocabItem(**c) for c in cards_data]
        return VocabList(items=items)

    def add_vocabulary(self, subject_id: str, question: str, answer: str) -> str:
        headers, owner_id = self._get_api_headers()

        with sync_playwright() as p:
            ctx = p.request.new_context(base_url=self.BASE_URL, extra_http_headers=headers)
            new_card_id = str(uuid.uuid4())

            payload = {
                "addSessionId": "",
                "addedByUserId": None,
                "addedUserName": None,
                "answer": answer,
                "answerExample": None,
                "answerTranscription": None,
                "modificationDate": None,
                "order": None,
                "ownerId": owner_id,
                "question": question,
                "questionAnswerId": None,
                "questionExample": None,
                "questionTranscription": None,
                "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
                "swappable": True,
                "unitIdToOwner": {"id": f"0000-{subject_id}", "ownerId": owner_id},
            }

            resp = ctx.post(f"/server.integration/{owner_id}/cards/{new_card_id}", data=payload)

            if not resp.ok:
                raise APIConnectionError(f"Failed to add card: {resp.status} {resp.text()}")

            data = resp.json()
            if data.get("httpCode") != 200:
                raise APIConnectionError(f"API returned non-200 code in JSON: {data}")

            return new_card_id

    def update_vocabulary(self, subject_id: str, card_id: str, question: str, answer: str) -> bool:
        headers, owner_id = self._get_api_headers()

        with sync_playwright() as p:
            ctx = p.request.new_context(base_url=self.BASE_URL, extra_http_headers=headers)

            payload = {
                "answer": answer,
                "answerExample": None,
                "answerTranscription": None,
                "modificationDate": None,
                "order": None,
                "ownerId": owner_id,
                "question": question,
                "questionAnswerId": None,
                "questionExample": None,
                "questionTranscription": None,
                "subjectIdToOwner": {"id": subject_id, "ownerId": owner_id},
                "swappable": True,
                "unitIdToOwner": {"id": f"0000-{subject_id}", "ownerId": owner_id},
            }

            resp = ctx.put(f"/server.integration/{owner_id}/cards/{card_id}", data=payload)

            if not resp.ok:
                raise APIConnectionError(f"Failed to update card: {resp.status} {resp.text()}")

            data = resp.json()
            if data.get("httpCode") != 200:
                raise APIConnectionError(f"API returned non-200 code in JSON: {data}")

            return True

    def delete_vocabulary(self, card_id: str) -> bool:
        headers, owner_id = self._get_api_headers()

        with sync_playwright() as p:
            ctx = p.request.new_context(base_url=self.BASE_URL, extra_http_headers=headers)

            resp = ctx.delete(f"/server.integration/{owner_id}/cards/{card_id}")

            if not resp.ok:
                raise APIConnectionError(f"Failed to delete card: {resp.status} {resp.text()}")

            data = resp.json()
            if data.get("httpCode") != 200:
                raise APIConnectionError(f"API returned non-200 code in JSON: {data}")

            return True
