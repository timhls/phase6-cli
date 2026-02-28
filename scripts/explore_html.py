from playwright.sync_api import sync_playwright

def run():
    print("Fetching login page HTML...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto("https://lernen.phase-6.de/v2/#/login", wait_until="networkidle")
            page.wait_for_timeout(3000) # Give it a few seconds to render
            print("Page title:", page.title())
            html = page.content()
            with open("login_page.html", "w") as f:
                f.write(html)
            print("Saved HTML to login_page.html")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
