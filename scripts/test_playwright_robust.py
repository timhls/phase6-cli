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
            # Test getting subjects
            print("Fetching subjects...")
            with page.expect_response("**/subjectsCombined") as response_info:
                page.goto("https://lernen.phase-6.de/v2/#/manage", wait_until="networkidle")

            resp = response_info.value
            data = resp.json()
            print(f"Got subjects data: {data.get('httpCode')}")

            # Test getting vocab
            subject_id = "615cc841-91fa-458d-a1d0-ea4ccaeb2c3e"
            print(f"Clicking subject {subject_id}...")
            with page.expect_response("**/cardList") as vocab_info:
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
