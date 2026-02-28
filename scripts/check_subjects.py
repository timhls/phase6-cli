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

        try:
            print("Going to manage page...")
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)

            print("Clicking 'Create cards' link...")
            page.get_by_text("Create cards", exact=True).click()
            page.wait_for_timeout(3000)

            print("Extracting full page text to see if there are subjects/options available:")
            print(page.locator("body").inner_text())

            # Take a screenshot specifically of the top part where the dropdown is
            page.screenshot(path="dropdown_area.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
