from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            storage_state="test_state.json",
        )
        page = context.new_page()

        try:
            print("Going to manage page...")
            # We must expect the response *before* navigation starts
            with page.expect_response(
                lambda r: "subjectsCombined" in r.url, timeout=15000
            ) as response_info:
                page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")

            resp = response_info.value
            data = resp.json()
            print(f"Got subjects data, httpCode: {data.get('httpCode')}")

            # Wait for elements to be clickable
            page.wait_for_timeout(2000)

            subject_id = "615cc841-91fa-458d-a1d0-ea4ccaeb2c3e"
            print(f"Clicking subject {subject_id}...")
            with page.expect_response(lambda r: "cardList" in r.url, timeout=15000) as vocab_info:
                page.click(f"#subject-{subject_id}")

            vocab_resp = vocab_info.value
            vocab_data = vocab_resp.json()
            cards = vocab_data.get("replyContent", {}).get("cards", [])
            print(f"Got {len(cards)} vocab cards!")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    run()
