from pathlib import Path
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state=Path("~/.config/pyphase6/session.json").expanduser(),
        )
        page = context.new_page()

        try:
            print("Going to manage page...")
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)

            subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
            print(f"Clicking subject {subject_id}...")

            # Click the subject
            page.click(f"#subject-{subject_id}")
            page.wait_for_timeout(3000)

            print("--- ALL TEXT ON PAGE ---")
            for text in page.locator("body").inner_text().split("\n"):
                if text.strip():
                    print(text.strip())

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
