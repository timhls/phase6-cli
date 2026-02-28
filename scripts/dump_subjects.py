import os
import json
from playwright.sync_api import sync_playwright


def run():
    username = os.environ.get("PHASE6_USERNAME")
    password = os.environ.get("PHASE6_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def log_response(response):
            if "subjectsCombined" in response.request.url:
                try:
                    data = response.json()
                    with open("subjects_response.json", "w") as f:
                        json.dump(data, f, indent=2)
                except Exception:
                    pass

        page.on("response", log_response)

        try:
            page.goto("https://lernen.phase-6.de/v2/#/login", wait_until="networkidle")
            page.fill('input[type="e-mail"]', username)
            page.fill('input[type="password"]', password)
            page.get_by_role("button", name="Login").click()
            page.wait_for_url("**/manage**", timeout=20000)
            page.wait_for_timeout(3000)
        except Exception:
            pass
        finally:
            browser.close()


if __name__ == "__main__":
    run()
