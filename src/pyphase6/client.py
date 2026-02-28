from typing import Dict, Any
import httpx
from playwright.sync_api import sync_playwright


class AuthError(Exception):
    pass


class APIConnectionError(Exception):
    pass


class Phase6Client:
    BASE_URL = "https://lernen.phase-6.de"

    def __init__(self):
        self.session_cookies: Dict[str, str] = {}
        self.http_client = httpx.Client(base_url=self.BASE_URL)

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

                # Fill in login form
                page.fill('input[type="email"], input[name="username"]', username)
                page.fill('input[type="password"]', password)
                page.click('button[type="submit"], button:has-text("Login")')

                # Wait for successful login (e.g., waiting for the manage page or a specific API request)
                page.wait_for_url("**/manage**", timeout=15000)

                # Extract cookies
                cookies = context.cookies()
                self.session_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}

                # Update httpx client with these cookies
                self.http_client.cookies.update(self.session_cookies)

            except Exception as e:
                raise AuthError(f"Login failed: {e}")
            finally:
                browser.close()

    def get_vocabulary(self) -> Any:
        # TODO: Implement actual endpoint call
        pass

    def add_vocabulary(self, item: Any) -> Any:
        # TODO: Implement actual endpoint call
        pass

    def update_vocabulary(self, item_id: str, data: Any) -> Any:
        # TODO: Implement actual endpoint call
        pass

    def delete_vocabulary(self, item_id: str) -> Any:
        # TODO: Implement actual endpoint call
        pass
