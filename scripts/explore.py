import os
import json
from playwright.sync_api import sync_playwright

def run():
    username = os.environ.get("PHASE6_USERNAME")
    password = os.environ.get("PHASE6_PASSWORD")

    print("Starting browser exploration...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def log_request(request):
            if "cardList" in request.url:
                print(f"-> {request.method} {request.url}")

        def log_response(response):
            if "cardList" in response.request.url:
                try:
                    data = response.json()
                    print(f"<- {response.status} {response.request.url}")
                    print(json.dumps(data, indent=2))
                except Exception as e:
                    pass

        page.on("request", log_request)
        page.on("response", log_response)

        try:
            page.goto("https://lernen.phase-6.de/v2/#/login", wait_until="networkidle")
            page.fill('input[type="e-mail"]', username)
            page.fill('input[type="password"]', password)
            page.get_by_role("button", name="Login").click()
            page.wait_for_url("**/home**", timeout=15000)
            
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)
            
            locator = page.get_by_text("HSK 1", exact=False).first
            locator.click()
            page.wait_for_timeout(5000)
            
        except Exception as e:
            pass
        finally:
            browser.close()

if __name__ == "__main__":
    run()
