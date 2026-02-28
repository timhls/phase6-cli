import os
from playwright.sync_api import sync_playwright


def run():
    username = os.environ.get("PHASE6_USERNAME")
    password = os.environ.get("PHASE6_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Load state
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state="test_state.json",
        )
        page = context.new_page()

        try:
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)
            print("Current URL before click:", page.url)

            # Click the subject by text
            page.get_by_text("HSK 1", exact=False).first.click()
            page.wait_for_timeout(2000)

            print("Current URL after click:", page.url)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
