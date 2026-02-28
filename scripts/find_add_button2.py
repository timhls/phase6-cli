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

            subject_id = "0b82cb9c-0175-490d-d14f-8c7c400a4c1f"
            print(f"Clicking subject {subject_id}...")
            page.click(f"#subject-{subject_id}")
            page.wait_for_timeout(3000)

            # take a screenshot
            page.screenshot(path="subject_view.png", full_page=True)

            # try to find the word 'add' or 'create' or '+'
            for btn in page.locator("button").all():
                html = btn.inner_html()
                if "plus" in html.lower() or "add" in html.lower() or "create" in html.lower():
                    print("Found a potential ADD button HTML:", html)
                    # draw a red box around it in another screenshot?
                    btn.evaluate("el => el.style.border = '5px solid red'")

            page.screenshot(path="subject_view_highlighted.png", full_page=True)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
