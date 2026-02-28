from pathlib import Path
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state=Path("~/.config/pyphase6/session.json").expanduser(),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        def handle_request(request):
            if request.method in ["POST", "PUT", "PATCH"] and (
                "card" in request.url.lower() or "vocab" in request.url.lower()
            ):
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

            # Let's take a closer look at the dropdowns
            print("Clicking the first dropdown...")
            dropdowns = page.get_by_text("Please select...", exact=True).all()
            for d in dropdowns:
                d.click()
                page.wait_for_timeout(1000)
                # Click the first li or div item that appears
                options = page.locator(
                    "li[role='option'], div[role='option'], div.Select-option"
                ).all()
                if options:
                    print(f"Found {len(options)} options, clicking the first one.")
                    options[0].click()
                else:
                    # just press enter
                    page.keyboard.press("ArrowDown")
                    page.keyboard.press("Enter")
                page.wait_for_timeout(1000)

            inputs = page.locator("textarea").all()
            if not inputs:
                inputs = page.locator("input[type='text']").all()

            if len(inputs) >= 2:
                print("Filling inputs...")
                inputs[0].fill("TestQuestion")
                inputs[1].fill("TestAnswer")
                page.wait_for_timeout(1000)

                print("Clicking SAVE AND NEXT...")
                btn = page.get_by_text("SAVE AND NEXT", exact=False)
                if btn.is_enabled():
                    btn.click()
                    print("Clicked!")
                    page.wait_for_timeout(5000)
                else:
                    print("Button still disabled!")
                    page.screenshot(path="create_cards_3.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
