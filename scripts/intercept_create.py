import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state=Path("~/.config/pyphase6/session.json").expanduser()
        )
        page = context.new_page()

        def handle_request(request):
            if request.method in ["POST", "PUT", "PATCH"] and "card" in request.url.lower():
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

            print("Dumping inputs...")
            for i, input_el in enumerate(page.locator("textarea, input").all()):
                print(f"Input {i}: placeholder={input_el.get_attribute('placeholder')}, type={input_el.get_attribute('type')}")
            
            # Let's try filling out the first two textareas/inputs
            textareas = page.locator("textarea").all()
            if len(textareas) >= 2:
                print("Filling textareas...")
                textareas[0].fill("TestQuestion")
                textareas[1].fill("TestAnswer")
                page.wait_for_timeout(1000)
                
                print("Clicking SAVE AND NEXT...")
                page.get_by_text("SAVE AND NEXT", exact=False).click()
                page.wait_for_timeout(5000)
            else:
                inputs = page.locator("input[type='text']").all()
                if len(inputs) >= 2:
                    print("Filling inputs...")
                    inputs[0].fill("TestQuestion")
                    inputs[1].fill("TestAnswer")
                    page.wait_for_timeout(1000)
                    
                    print("Clicking SAVE AND NEXT...")
                    page.get_by_text("SAVE AND NEXT", exact=False).click()
                    page.wait_for_timeout(5000)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
