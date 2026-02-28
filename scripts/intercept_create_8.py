import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state=Path("~/.config/pyphase6/session.json").expanduser(),
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        def handle_request(request):
            if request.method in ["POST", "PUT", "PATCH"] and ("card" in request.url.lower() or "vocab" in request.url.lower()):
                print(f"REQUEST TO: {request.url}")
                print(f"METHOD: {request.method}")
                print(f"POST DATA: {request.post_data}")

        page.on("request", handle_request)

        try:
            print("Going to manage page...")
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)

            print("Clicking 'Create cards' link...")
            page.get_by_text("Create cards", exact=True).click()
            page.wait_for_timeout(3000)

            print("Typing into Quill editors (forced click)...")
            editors = page.locator(".ql-editor").all()
            if len(editors) >= 2:
                # Force click to bypass any overlay, then type
                editors[0].click(force=True)
                page.keyboard.type("My Test Question")
                page.wait_for_timeout(500)

                editors[1].click(force=True)
                page.keyboard.type("My Test Answer")
                page.wait_for_timeout(1000)

                page.screenshot(path="create_cards_8_before_save.png")

                print("Clicking SAVE AND NEXT...")
                btn = page.get_by_text("SAVE AND NEXT", exact=False)
                # Wait for the button to be enabled
                page.wait_for_timeout(3000)

                if btn.is_enabled():
                    btn.click()
                    print("Clicked!")
                    page.wait_for_timeout(5000)
                    page.screenshot(path="create_cards_8.png")
                else:
                    print("Button still disabled!")
            else:
                print("Could not find Quill editors")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="create_cards_8_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
