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
            if request.method == "POST" and "cards" in request.url.lower():
                print(f"REQUEST TO: {request.url}")
                print(f"HEADERS: {request.headers}")
                print(f"POST DATA: {request.post_data}")

        page.on("request", handle_request)

        try:
            page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")
            page.wait_for_timeout(3000)

            page.get_by_text("Create cards", exact=True).click()
            page.wait_for_timeout(3000)

            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            page.mouse.click(10, 10)
            page.wait_for_timeout(1000)

            editors = page.locator(".ql-editor").all()
            if len(editors) >= 2:
                editors[0].click()
                page.keyboard.type("My Header Test Question")
                page.wait_for_timeout(500)

                editors[1].click()
                page.keyboard.type("My Header Test Answer")
                page.wait_for_timeout(1000)

                btn = page.get_by_text("SAVE AND NEXT", exact=False)
                page.wait_for_timeout(2000)

                if btn.is_enabled():
                    btn.click()
                    page.wait_for_timeout(5000)
        except Exception:
            pass
        finally:
            browser.close()


if __name__ == "__main__":
    run()
