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

        page.goto("https://lernen.phase-6.de/v2/#/login", wait_until="networkidle")
        page.fill('input[type="e-mail"]', username)
        page.fill('input[type="password"]', password)
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/home**", timeout=15000)
        
        # We must execute JS in the page context! Let's see the text.
        result = page.evaluate("""
        async () => {
            const resp = await fetch("/server.integration/subjectsCombined", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({filterMode: "LIBRARY"})
            });
            return {
               status: resp.status,
               text: await resp.text()
            };
        }
        """)
        
        print(f"Subjects response from inside page: {str(result)[:300]}...")
        browser.close()

if __name__ == "__main__":
    run()
