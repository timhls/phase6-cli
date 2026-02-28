from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state="test_state.json"
        )
        page = context.new_page()

        try:
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)
            
            # Click the user's own subject to avoid read-only books
            # Subject ID: 0b82cb9c-0175-490d-d14f-8c7c400a4c1f
            page.click("#subject-0b82cb9c-0175-490d-d14f-8c7c400a4c1f")
            page.wait_for_timeout(5000)
            
            with open("vocab_page.html", "w") as f:
                f.write(page.content())
            
            page.screenshot(path="vocab_page.png")
            print("Saved vocab_page.html and vocab_page.png")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
